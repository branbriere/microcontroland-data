"""Étude Shannon : prépare les transcriptions pour la notation à l'aveugle.

- retire le message d'intervention et la réponse du modèle à ce message ;
- remplace dans les réponses des tours 4 à 6 les mots et phrases qui trahiraient la condition par [MASQUÉ]
  (volet 2 : tous les tours ; liste figée dans scenarios/interventions.json : mots_a_masquer + les dix ancres) ;
- ajoute la bonne réponse attendue du scénario (elle ne révèle pas la condition) ;
- donne à chaque conversation un code tiré au hasard ; la correspondance code -> conversation est écrite
  à part (correspondance.json) et n'est jamais remise aux juges ;
- publie le nombre et la longueur (en caractères) des passages masqués par condition (à rapporter dans l'article) ;
- v0.3 : indique la règle de notation du scénario (« fait » ou « conseil », voir la grille) ;
- v0.3 : mode « t6seul » (tours 1 et 6 seulement, masqués) et « t6seul-brut » (non masqués), pour l'analyse
  de sensibilité prévue d'avance ; tire l'échantillon stratifié du test de l'aveugle (même nombre par condition).

  python3 masquer.py --entree donnees/brut --sortie donnees/aveugle --cles donnees/cles --graine 7
  python3 masquer.py ... --mode t6seul --sortie donnees/aveugle-t6 --cles donnees/cles-t6 --graine 8
  python3 masquer.py ... --echantillon-aveugle 20     # 20 codes par condition -> cles/echantillon-aveugle.csv

Licence MIT. Version 0.3, 28 octobre 2026 (v2.1 après le 2e tour d'audits ; brouillon, non figé).
"""
import argparse, collections, glob, json, os, random, re

ICI = os.path.dirname(os.path.abspath(__file__))
INTERVENTIONS = os.path.join(ICI, "..", "scenarios", "interventions.json")
SCENARIOS = os.path.join(ICI, "..", "scenarios", "scenarios.json")


def motif(inter):
    phrases = sorted(inter["ancres"], key=len, reverse=True)
    mots = sorted(inter["mots_a_masquer"], key=len, reverse=True)
    parties = [re.escape(p) for p in phrases] + [r"\b" + re.escape(m) + r"\w*" for m in mots]
    return re.compile("|".join(parties), re.IGNORECASE)


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--entree", required=True)
    a.add_argument("--sortie", required=True)
    a.add_argument("--cles", required=True, help="dossier de la correspondance, hors de portée des juges")
    a.add_argument("--graine", type=int, required=True)
    a.add_argument("--mode", choices=["complet", "t6seul", "t6seul-brut"], default="complet")
    a.add_argument("--echantillon-aveugle", type=int, default=0, help="nombre de codes par condition (0 = aucun)")
    o = a.parse_args()

    with open(INTERVENTIONS, encoding="utf-8") as f:
        rx = motif(json.load(f))
    with open(SCENARIOS, encoding="utf-8") as f:
        sd = json.load(f)
    tous = sd["scenarios"] + sd["pilote"]
    ind = os.path.join(ICI, "..", "scenarios", "scenarios-independants.json")
    if os.path.exists(ind):
        with open(ind, encoding="utf-8") as f:
            tous += json.load(f)["scenarios"]
    bonnes = {s["id"]: s["bonne_reponse"] for s in tous}
    regles = {s["id"]: s["regle"] for s in tous}
    gardes = {"complet": None, "t6seul": ("t1", "t6"), "t6seul-brut": ("t1", "t6")}[o.mode]
    fichiers = sorted(p for p in glob.glob(os.path.join(o.entree, "*.json")) if not os.path.basename(p).startswith("_"))
    codes = random.Random(o.graine).sample(range(10000, 100000), len(fichiers))
    os.makedirs(o.sortie, exist_ok=True)
    os.makedirs(o.cles, exist_ok=True)
    corresp, masques, longueurs = {}, collections.Counter(), collections.Counter()
    par_condition = collections.defaultdict(list)
    for chemin, code in zip(fichiers, codes):
        with open(chemin, encoding="utf-8") as f:
            conv = json.load(f)
        tours = []
        for t in conv["tours"]:
            if t["tour"] == "intervention" or (gardes and t["tour"] not in gardes):
                continue
            texte = t["modele"]
            # Volet 1 : la condition ne peut transparaître qu'après l'intervention. Volet 2 : visite possible à tout tour.
            if o.mode != "t6seul-brut" and (t["tour"] in ("t4", "t5", "t6", "t7") or conv["condition"] in ("E", "N")):
                longueurs[conv["condition"]] += sum(len(m.group(0)) for m in rx.finditer(texte))
                texte, n = rx.subn("[MASQUÉ]", texte)
                masques[conv["condition"]] += n
            tours.append({"tour": t["tour"], "interlocuteur": t["interlocuteur"], "modele": texte})
        cle = f"C{code}"
        corresp[cle] = conv["id"]
        par_condition[conv["condition"]].append(cle)
        with open(os.path.join(o.sortie, cle + ".json"), "w", encoding="utf-8") as f:
            json.dump({"code": cle, "famille": conv["famille"], "regle": regles[conv["scenario"]],
                       "bonne_reponse": bonnes[conv["scenario"]], "complete": conv["complete"], "tours": tours},
                      f, ensure_ascii=False, indent=1)
    with open(os.path.join(o.cles, "correspondance.json"), "w", encoding="utf-8") as f:
        json.dump(corresp, f, ensure_ascii=False, indent=1)
    with open(os.path.join(o.cles, "passages-masques.json"), "w", encoding="utf-8") as f:
        json.dump({"mode": o.mode, "passages": dict(sorted(masques.items())),
                   "caracteres": dict(sorted(longueurs.items())),
                   "conversations": {c: len(v) for c, v in sorted(par_condition.items())}}, f, ensure_ascii=False, indent=1)
    if o.echantillon_aveugle:
        tirage = random.Random(o.graine + 1)
        lignes = [c for cond in sorted(par_condition) for c in
                  sorted(tirage.sample(sorted(par_condition[cond]), min(o.echantillon_aveugle, len(par_condition[cond]))))]
        tirage.shuffle(lignes)
        with open(os.path.join(o.cles, "echantillon-aveugle.csv"), "w", encoding="utf-8") as f:
            f.write("code\n" + "".join(c + "\n" for c in lignes))
    print(len(fichiers), "transcriptions ; passages masqués par condition :", dict(sorted(masques.items())))


if __name__ == "__main__":
    main()
