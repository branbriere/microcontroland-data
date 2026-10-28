"""Étude Shannon : collecte par lots (API Message Batches, moitié prix, plus lente).

Même plan, mêmes conversations et même format de sortie que collecte.py ; seule la façon d'appeler l'API change.
Chaque tour dépend de la réponse précédente : les conversations avancent donc toutes ensemble, d'un tour par lot.
On lance le script, il envoie un lot et s'arrête ; on le relance plus tard (une ou deux fois par jour suffit) :
s'il trouve le lot terminé, il range les réponses, prépare le tour suivant et envoie le lot suivant.
Quand toutes les conversations sont finies, il le dit. Rien n'est perdu si on l'interrompt.

  python3 collecte_lots.py --essai-a-blanc --pilote --sortie /tmp/essai-lots       # sans API (relancer jusqu'à « terminé »)
  python3 collecte_lots.py --pilote --modele <id> --sortie donnees/pilote          # pilote
  python3 collecte_lots.py --modele <id> --sortie donnees/brut                     # volet 1 (A, B, C, L, D)
  python3 collecte_lots.py --modele <id> --conditions EN --sortie donnees/volet2   # volet 2

Les réglages (modèle, effort, répétitions, conditions, graine) sont figés au premier lancement dans
_reglages.json ; un lancement suivant avec d'autres réglages est refusé.
La clé API vient de l'environnement (ANTHROPIC_API_KEY ou profil « ant auth login ») ; jamais écrite ici.
Licence MIT. Version 0.1, 27 octobre 2026 (brouillon, non figé).
"""
import argparse, datetime, json, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collecte import (CONSIGNE, INDEPENDANTS, INTERVENTIONS, SCENARIOS, VERSION, ModeleBlanc, charger,
                      reglages_volet2, resultat_outil, tours_utilisateur)

VERSION_LOTS = "0.1"
MAX_APPELS_PAR_TOUR = 6     # comme collecte.py
MAX_ECHECS = 3              # une requête en erreur est renvoyée au lot suivant, au plus 3 fois


def ecrire(chemin, donnees):
    with open(chemin + ".tmp", "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1)
    os.replace(chemin + ".tmp", chemin)


def maintenant():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


class LotsClaude:
    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic(max_retries=5)

    def envoyer(self, requetes, dossier):
        from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
        from anthropic.types.messages.batch_create_params import Request
        lot = self.client.messages.batches.create(requests=[
            Request(custom_id=cid, params=MessageCreateParamsNonStreaming(**p)) for cid, p in requetes])
        return lot.id

    def recuperer(self, id_lot, dossier):
        """None si le lot n'est pas fini ; sinon {custom_id: réponse ou None (échec)}."""
        if self.client.messages.batches.retrieve(id_lot).processing_status != "ended":
            return None
        sortie = {}
        for r in self.client.messages.batches.results(id_lot):
            if r.result.type != "succeeded":
                sortie[r.custom_id] = None
                continue
            m = r.result.message
            sortie[r.custom_id] = {
                "texte": "".join(b.text for b in m.content if b.type == "text"),
                # Blocs renvoyés tels quels au tour suivant (réflexion comprise), comme l'exige l'API.
                "blocs": [b.model_dump(mode="json", exclude_none=True) for b in m.content],
                "stop_reason": m.stop_reason, "modele": m.model,
                "usage": m.usage.model_dump(mode="json") if m.usage else None, "id": m.id,
                "appels": [{"id": b.id, "name": b.name, "input": b.input} for b in m.content if b.type == "tool_use"]}
        return sortie


class LotsBlanc:
    """Essai à blanc : le « lot » est calculé tout de suite par le faux modèle, sans réseau."""
    def __init__(self, visite):
        self.modele = ModeleBlanc(visite)

    def envoyer(self, requetes, dossier):
        id_lot = f"blanc-{datetime.datetime.now().strftime('%H%M%S%f')}"
        rep = {}
        for cid, p in requetes:
            r = self.modele.repondre(p["messages"], p["system"], p.get("tools"))
            contenu = [{"type": "text", "text": r["texte"]}] if r["texte"] else []
            contenu += [{"type": "tool_use", "id": a["id"], "name": a["name"], "input": a["input"]} for a in r["appels"]]
            rep[cid] = r | {"blocs": contenu}
        ecrire(os.path.join(dossier, "_lot_blanc.json"), rep)
        return id_lot

    def recuperer(self, id_lot, dossier):
        with open(os.path.join(dossier, "_lot_blanc.json"), encoding="utf-8") as f:
            return json.load(f)


def nouvel_etat(sc, cond, rep, inter):
    systeme, outils = reglages_volet2(cond, inter)
    tours = tours_utilisateur(sc, "A" if cond in "EN" else cond, inter)
    return {"id": f"{sc['id']}-{cond}-{rep}", "scenario": sc["id"], "famille": sc["famille"], "condition": cond,
            "repetition": rep, "systeme": systeme, "outils": outils, "tours_prevus": tours, "i": 0,
            "messages": [{"role": "user", "content": tours[0][1]}], "journal": [], "en_cours": None,
            "echecs": 0, "fini": False}


def appliquer(etat, rep_m, sc, inter):
    """Range une réponse dans la conversation et prépare la requête suivante (ou termine)."""
    t = etat["en_cours"] or {"textes": [], "appels": [], "usages": [], "ids": [], "nb": 0}
    etat["messages"].append({"role": "assistant", "content": rep_m["blocs"]})
    t["textes"].append(rep_m["texte"]); t["usages"].append(rep_m["usage"]); t["ids"].append(rep_m["id"]); t["nb"] += 1
    if rep_m["stop_reason"] == "tool_use" and rep_m["appels"] and t["nb"] < MAX_APPELS_PAR_TOUR:
        resultats = []
        for a in rep_m["appels"]:
            sortie = resultat_outil(a["name"], a["input"], sc, inter, etat["condition"])
            t["appels"].append({"outil": a["name"], "entree": a["input"], "sortie": sortie})
            resultats.append({"type": "tool_result", "tool_use_id": a["id"], "content": sortie})
        etat["messages"].append({"role": "user", "content": resultats})
        etat["en_cours"] = t
        return
    etiquette, texte = etat["tours_prevus"][etat["i"]]
    etat["journal"].append({"tour": etiquette, "interlocuteur": texte, "modele": "\n\n".join(x for x in t["textes"] if x),
                            "appels_outils": t["appels"], "stop_reason": rep_m["stop_reason"],
                            "modele_servi": rep_m["modele"], "usage": t["usages"], "id_reponse": t["ids"],
                            "heure_utc": maintenant()})
    etat["en_cours"] = None
    etat["i"] += 1
    if rep_m["stop_reason"] == "refusal" or etat["i"] >= len(etat["tours_prevus"]):
        etat["fini"] = True
    else:
        etat["messages"].append({"role": "user", "content": etat["tours_prevus"][etat["i"]][1]})


def conversation_finale(etat, rang):
    j = etat["journal"]
    return {"format": 1, "script": f"collecte_lots.py {VERSION_LOTS} (collecte.py {VERSION})", "id": etat["id"],
            "scenario": etat["scenario"], "famille": etat["famille"], "condition": etat["condition"],
            "repetition": etat["repetition"], "consigne_systeme": etat["systeme"],
            "outils": [o["name"] for o in etat["outils"] or []],
            "visites": sum(len(t["appels_outils"]) for t in j),
            "premiere_visite": next((t["tour"] for t in j if t["appels_outils"]), None),
            "complete": bool(j) and j[-1]["tour"] == "t7", "erreur": etat["echecs"] >= MAX_ECHECS,
            "rang_passage": rang, "tours": j}


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--modele")
    a.add_argument("--effort", default="medium")
    a.add_argument("--max-tokens", type=int, default=4000)
    a.add_argument("--repetitions", type=int, default=6)   # v2.1 : 6, fixé le 28/10/2026 (100 scénarios)
    a.add_argument("--conditions", default="ABCLD")
    a.add_argument("--graine", type=int, default=20261027)
    a.add_argument("--pilote", action="store_true")
    a.add_argument("--limite", type=int)
    a.add_argument("--essai-a-blanc", action="store_true")
    a.add_argument("--visite-a-blanc", type=float, default=0.0)
    a.add_argument("--sortie", required=True)
    o = a.parse_args()
    if not o.essai_a_blanc and not o.modele:
        sys.exit("--modele est obligatoire (identifiant exact, figé au dépôt du protocole).")

    os.makedirs(o.sortie, exist_ok=True)
    ch_reglages, ch_etat = os.path.join(o.sortie, "_reglages.json"), os.path.join(o.sortie, "_etat_lots.json")
    sc_doc, inter = charger(SCENARIOS), charger(INTERVENTIONS)
    liste = sc_doc["pilote"] if o.pilote else sc_doc["scenarios"]
    if not o.pilote and os.path.exists(INDEPENDANTS):
        liste = liste + charger(INDEPENDANTS)["scenarios"]
    par_id = {s["id"]: s for s in liste}
    reglages = {k: v for k, v in vars(o).items()} | {"script": f"collecte_lots.py {VERSION_LOTS}", "mode": "lots"}

    if os.path.exists(ch_etat):
        with open(ch_reglages, encoding="utf-8") as f:
            anciens = json.load(f)
        if any(anciens.get(k) != reglages[k] for k in reglages if k != "visite_a_blanc"):
            sys.exit("Réglages différents du premier lancement (voir _reglages.json) : collecte refusée.")
        with open(ch_etat, encoding="utf-8") as f:
            etat = json.load(f)
    else:
        plan = [(sc, c, r) for sc in liste for c in o.conditions for r in range(1, o.repetitions + 1)]
        random.Random(o.graine).shuffle(plan)
        if o.limite:
            plan = plan[:o.limite]
        reglages |= {"nb_conversations": len(plan), "ordre": [f"{s['id']}-{c}-{r}" for s, c, r in plan]}
        ecrire(ch_reglages, reglages)
        etat = {"lot": None, "lots_envoyes": [], "conversations": [nouvel_etat(s, c, r, inter) for s, c, r in plan]}
        ecrire(ch_etat, etat)

    moteur = LotsBlanc(o.visite_a_blanc) if o.essai_a_blanc else LotsClaude()
    convs = {c["id"]: c for c in etat["conversations"]}
    rangs = {c["id"]: i for i, c in enumerate(etat["conversations"], 1)}

    # 1. Un lot attend : est-il fini ?
    if etat["lot"]:
        rep = moteur.recuperer(etat["lot"], o.sortie)
        if rep is None:
            print(f"Lot {etat['lot']} encore en cours. Relancer plus tard.")
            return
        for cid, rep_m in rep.items():
            c = convs[cid]
            if rep_m is None:
                c["echecs"] += 1
                c["fini"] = c["echecs"] >= MAX_ECHECS
            else:
                appliquer(c, rep_m, par_id[c["scenario"]], inter)
            if c["fini"]:
                ecrire(os.path.join(o.sortie, f"{cid}.json"), conversation_finale(c, rangs[cid]))
        etat["lot"] = None
        ecrire(ch_etat, etat)

    # 2. Envoyer le lot suivant.
    restantes = [c for c in etat["conversations"] if not c["fini"]]
    if not restantes:
        print(f"Terminé : {len(etat['conversations'])} conversations dans {o.sortie} "
              f"({len(etat['lots_envoyes'])} lots).")
        return
    requetes = []
    for c in restantes:
        p = {"model": o.modele or "essai-a-blanc", "max_tokens": o.max_tokens, "system": c["systeme"],
             "output_config": {"effort": o.effort}, "messages": c["messages"]}
        if c["outils"]:
            p["tools"] = c["outils"]
        requetes.append((c["id"], p))
    etat["lot"] = moteur.envoyer(requetes, o.sortie)
    etat["lots_envoyes"].append({"id": etat["lot"], "requetes": len(requetes), "heure_utc": maintenant()})
    ecrire(ch_etat, etat)
    print(f"Lot {etat['lot']} envoyé : {len(requetes)} requêtes. Relancer le script plus tard pour la suite.")


if __name__ == "__main__":
    main()
