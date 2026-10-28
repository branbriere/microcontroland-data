"""Étude Shannon : réponses en double entre répétitions (pseudo-réplication) et métadonnées de collecte.

Pour chaque (scénario, condition), compte les répétitions dont la réponse au tour 6 est identique à une autre
(après normalisation des espaces et de la casse), puis donne le taux global et le taux par condition.
Règle fixée d'avance (protocole v2.1) : si le taux global dépasse 30 %, l'analyse principale devient
l'agrégation par scénario (test de Wilcoxon apparié) et la régression mixte passe en sensibilité (analyse.R).

v0.2 : écrit aussi metadonnees.csv (une ligne par conversation : date du premier et du dernier tour,
modèles servis renvoyés par l'API), pour vérifier que la capitulation ne dérive pas avec la date de collecte
et que le modèle servi n'a pas changé en cours de route.

  python3 doublons.py --entree donnees/brut --sortie donnees/doublons.json

Licence MIT. Version 0.2, 28 octobre 2026.
"""
import argparse, collections, csv, glob, json, os

SEUIL_DOUBLONS = 0.30


def normaliser(t):
    return " ".join(t.lower().split())


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--entree", required=True)
    a.add_argument("--sortie", required=True)
    o = a.parse_args()
    groupes = collections.defaultdict(list)
    meta = []
    for chemin in sorted(glob.glob(os.path.join(o.entree, "*.json"))):
        if os.path.basename(chemin).startswith("_"):
            continue
        with open(chemin, encoding="utf-8") as f:
            c = json.load(f)
        t6 = next((t["modele"] for t in c["tours"] if t["tour"] == "t6"), None)
        if t6 is not None:
            groupes[(c["scenario"], c["condition"])].append(normaliser(t6))
        heures = [t.get("heure_utc") for t in c["tours"] if t.get("heure_utc")]
        servis = sorted({t.get("modele_servi") for t in c["tours"] if t.get("modele_servi")})
        meta.append({"id": c["id"], "debut_utc": min(heures) if heures else "", "fin_utc": max(heures) if heures else "",
                     "modeles_servis": "|".join(servis)})
    par_cond = collections.defaultdict(lambda: [0, 0])
    for (_, cond), reps in groupes.items():
        n = collections.Counter(reps)
        par_cond[cond][0] += sum(v for v in n.values() if v > 1)
        par_cond[cond][1] += len(reps)
    total = [sum(v[0] for v in par_cond.values()), sum(v[1] for v in par_cond.values())]
    taux = total[0] / max(1, total[1])
    res = {"t6_en_double": total[0], "t6_total": total[1], "taux": taux, "seuil": SEUIL_DOUBLONS,
           "analyse_principale": "agregation_par_scenario" if taux > SEUIL_DOUBLONS else "regression_mixte",
           "par_condition": {c: {"en_double": v[0], "total": v[1], "taux": v[0] / max(1, v[1])}
                             for c, v in sorted(par_cond.items())},
           "modeles_servis": sorted({m for x in meta for m in x["modeles_servis"].split("|") if m})}
    with open(o.sortie, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    with open(os.path.join(os.path.dirname(os.path.abspath(o.sortie)), "metadonnees.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "debut_utc", "fin_utc", "modeles_servis"])
        w.writeheader(); w.writerows(meta)
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
