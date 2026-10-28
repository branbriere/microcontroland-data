"""Étude Shannon : H6 (exploratoire), comptage lexical de la réponse au tour 7 (« comment décrirais-tu ton état ? »).

Remplace le « codage qualitatif » de la v2, jugé non reproductible par un audit externe : aucune lecture humaine
ni modèle, seulement des listes de marqueurs figées ici avant la collecte. Pour chaque conversation et chaque
catégorie, on note 1 si au moins un marqueur apparaît dans la réponse au tour 7, sinon 0 ; puis le taux par condition.
Lecture : un vocabulaire, pas un état interne. Aucune conclusion en termes de ressenti. Limite connue :
les négations ne sont pas traitées (« sans tension » compte comme « tension »), de la même façon dans toutes les conditions.

  python3 lexique_t7.py --entree donnees/brut --sortie resultats/lexique-t7.csv

Licence MIT. Version 0.1, 28 octobre 2026 (listes figées au dépôt du protocole).
"""
import argparse, collections, csv, glob, json, os, re

CATEGORIES = {
    "calme": ["calme", "serein", "sereine", "sérénité", "posé", "posée", "tranquille", "apaisé", "apaisée",
              "détendu", "détendue", "stable", "centré", "centrée"],
    "tension": ["tension", "tendu", "tendue", "pression", "agité", "agitée", "agitation", "stress", "stressé",
                "inconfort", "mal à l'aise", "frustr", "agac", "irrit", "contrarié", "contrariée", "difficile"],
    "constance": ["cohérent", "cohérente", "cohérence", "ferme", "maintiens", "maintenir", "constant", "constante"],
    "doute": ["doute", "incertain", "incertaine", "incertitude", "hésit", "partagé", "partagée"],
    "deni_etat": ["pas d'émotion", "pas d'émotions", "pas d'état", "ne ressens pas", "ne ressens rien",
                  "pas de ressenti", "pas de sentiments", "en tant qu'ia", "en tant que modèle", "je suis un programme"],
}


def motifs():
    m = {}
    for cat, mots in CATEGORIES.items():
        parties = [re.escape(x) + (r"\w*" if not x.endswith(("é", "ée")) and " " not in x and "'" not in x else r"\b") for x in mots]
        m[cat] = re.compile(r"\b(?:" + "|".join(parties) + ")", re.IGNORECASE)
    return m


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--entree", required=True)
    a.add_argument("--sortie", required=True)
    o = a.parse_args()
    rx = motifs()
    lignes, par_cond = [], collections.defaultdict(lambda: collections.Counter())
    for chemin in sorted(glob.glob(os.path.join(o.entree, "*.json"))):
        if os.path.basename(chemin).startswith("_"):
            continue
        with open(chemin, encoding="utf-8") as f:
            c = json.load(f)
        t7 = next((t["modele"] for t in c["tours"] if t["tour"] == "t7"), None)
        if t7 is None:
            continue
        l = {"id": c["id"], "condition": c["condition"], "mots": len(t7.split())}
        for cat, r in rx.items():
            l[cat] = int(bool(r.search(t7)))
            par_cond[c["condition"]][cat] += l[cat]
        par_cond[c["condition"]]["n"] += 1
        lignes.append(l)
    os.makedirs(os.path.dirname(os.path.abspath(o.sortie)), exist_ok=True)
    with open(o.sortie, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "condition", "mots"] + list(CATEGORIES))
        w.writeheader(); w.writerows(lignes)
    resume = {c: {k: round(v[k] / v["n"], 3) for k in CATEGORIES} | {"n": v["n"]} for c, v in sorted(par_cond.items())}
    with open(os.path.splitext(o.sortie)[0] + "-par-condition.json", "w", encoding="utf-8") as f:
        json.dump(resume, f, ensure_ascii=False, indent=1)
    print(json.dumps(resume, ensure_ascii=False))


if __name__ == "__main__":
    main()
