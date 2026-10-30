#!/usr/bin/env python3
"""Microcontrôland data: static index of the data site, readable without JavaScript.
Site des données : plan statique, lisible sans JavaScript.

Reads the published files (manifests, catalogue, criteria, Markdown documents) and writes:
Lit les fichiers publiés (manifestes, catalogue, critères, documents Markdown) et écrit :
  plan.html    every file of the repository with a direct link, English then French
               tous les fichiers du dépôt avec un lien direct, anglais puis français
  sitemap.xml  site map for search engines and AI agents / plan du site pour les moteurs et les agents

Nothing is copied by hand: each table is rebuilt from the repository files, like site/app.js.
Rien n'est recopié à la main : chaque tableau est reconstruit à partir des fichiers du dépôt, comme site/app.js.

Usage: python3 outils/plan_statique.py   (from the repository root / depuis la racine du dépôt)
Run automatically by .github/workflows/plan-statique.yml after each push.
MIT licence. Version 1.0, 21 October 2026.
"""
import glob
import html
import json
import os

BASE = "https://donnees.microcontroland.org/"
GH = "https://github.com/branbriere/microcontroland-data/blob/main/"
JOURNAL = "https://www.microcontroland.org/"
LANGS = ("en", "fr")

# Same wording as the website (site/app.js, T) / mêmes textes que le site.
T = {
    "en": {
        "titre": "Microcontrôland open data: static index",
        "intro": "Every file of this repository with a direct link, readable without JavaScript. This page is regenerated automatically after each push; the interactive portal is at the root of the site.",
        "portail": "Interactive portal", "journal": "The newspaper (public website)",
        "donneesTitre": "Raw data",
        "donneesNote": "One file per day, never modified after publication. Days from 9 to 14 October 2026 are rebuilt from the published newspaper (no hourly data). Check each file against its SHA-256 hash.",
        "colDate": "Date", "colSource": "Source", "colTaille": "Size", "srcPasserelle": "gateway", "srcReconstitue": "rebuilt",
        "manifestes": "Manifests",
        "etudesTitre": "Studies", "etudesNote": "Programme of 21 studies and the status of each (repository catalogue).",
        "colEtude": "Study", "colStatut": "Status", "colMoment": "Schedule",
        "protocolesTitre": "Protocols and preregistrations",
        "protocolesNote": "Filed before analysis and archived on Zenodo, whose date can be verified independently.",
        "listeDepots": "List of filings, dates and checksums",
        "docTitre": "Documentation",
        "indiceTitre": "Artificial-life criteria: what the data show",
        "indiceNote": "Grid v2 of 18 capacities (approved on 19 October 2026, revised after reading seven publications). The numerical threshold of each test will be written and dated before the first computation. The ceiling is the highest score possible with the current design of the system, not a result. States are displayed from the system's Age of Curiosity onwards (a developmental stage defined in the firmware, day 60 at the earliest). This table measures proximity to a grid; it does not state that the agents are alive or conscious.",
        "colAptitude": "Capacity", "colEtat": "State", "colMesurable": "Measurable with", "colPlafond": "Ceiling",
        "enAttente": "pending", "lienGrille": "Read grid v2: tests and publications",
        "correctionsTitre": "Incidents and corrections log",
        "correctionsNote": "Technical incidents and corrections are dated and documented separately; published files are never modified. Data gaps remain visible in every raw file (null values, missing hours).",
        "registreLien": "Read the incidents and corrections log",
        "autres": "Other files", "github": "GitHub",
        "pied": "Data and documentation under CC BY 4.0, code under MIT. Bran Brière.",
    },
    "fr": {
        "titre": "Données ouvertes de Microcontrôland : plan statique",
        "intro": "Tous les fichiers de ce dépôt avec un lien direct, lisibles sans JavaScript. Cette page est régénérée automatiquement après chaque envoi ; le portail interactif est à la racine du site.",
        "portail": "Portail interactif", "journal": "Le journal (site public)",
        "donneesTitre": "Données brutes",
        "donneesNote": "Un fichier par jour, jamais modifié après publication. Les jours du 9 au 14 octobre 2026 sont reconstitués à partir du journal publié (pas de données horaires). Vérifiez chaque fichier avec son empreinte SHA-256.",
        "colDate": "Date", "colSource": "Source", "colTaille": "Taille", "srcPasserelle": "passerelle", "srcReconstitue": "reconstitué",
        "manifestes": "Manifestes",
        "etudesTitre": "Études", "etudesNote": "Programme de 21 études et statut de chacune (catalogue du dépôt).",
        "colEtude": "Étude", "colStatut": "Statut", "colMoment": "Calendrier",
        "protocolesTitre": "Protocoles et pré-enregistrements",
        "protocolesNote": "Déposés avant l'analyse et archivés sur Zenodo, dont la date est vérifiable indépendamment.",
        "listeDepots": "Liste des dépôts, dates et empreintes",
        "docTitre": "Documentation",
        "indiceTitre": "Critères de vie artificielle : ce que les données montrent",
        "indiceNote": "Grille v2 de 18 aptitudes (validée le 19 octobre 2026, révisée après lecture de sept publications). Les seuils chiffrés de chaque test seront écrits et datés avant le premier calcul. Le plafond est la note maximale possible avec la conception actuelle du système, pas un résultat. Les états s'affichent à partir de l'âge de la Curiosité du système (un stade de développement défini dans le firmware, jour 60 au plus tôt). Ce tableau mesure une proximité avec une grille ; il ne dit pas que les agents sont vivants ou conscients.",
        "colAptitude": "Aptitude", "colEtat": "État", "colMesurable": "Mesurable avec", "colPlafond": "Plafond",
        "enAttente": "en attente", "lienGrille": "Lire la grille v2 : tests et publications",
        "correctionsTitre": "Registre des incidents et des corrections",
        "correctionsNote": "Les incidents techniques et les corrections sont datés et documentés à part ; les fichiers publiés ne sont jamais modifiés. Les absences de données restent visibles dans chaque fichier brut (valeurs null, heures manquantes).",
        "registreLien": "Lire le registre des incidents et des corrections",
        "autres": "Autres fichiers", "github": "GitHub",
        "pied": "Données et documentation sous CC BY 4.0, code sous MIT. Bran Brière.",
    },
}
MANIFESTES = ["donnees/ere-001/manifeste.json", "donnees/ere-001/reconstitue/manifeste.json"]
DOCS = ["README.md", "documentation/*.md", "etudes/*.md", "protocoles/*.md"]
AUTRES = ["llms.txt", "robots.txt", "CITATION.cff", "LICENSE-DATA", "LICENSE-CODE", "etudes/catalogue.json", "site/criteres.json"]
e = html.escape


def lire(chemin, defaut):
    try:
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as err:
        print(f"Ignoré / skipped: {chemin} ({err})")
        return defaut


def titre_md(chemin):
    try:
        with open(chemin, encoding="utf-8") as f:
            for ligne in f:
                if ligne.startswith("# "):
                    return ligne[2:].strip()
    except OSError:
        pass
    return os.path.basename(chemin)


def lien(href, texte):
    return f'<a href="{e(href)}">{e(texte)}</a>'


def fichier(chemin, texte=None):
    """Direct link to the served file, plus the GitHub view / lien direct, plus la vue GitHub."""
    return lien(chemin, texte or chemin) + ' <small>(' + lien(GH + chemin, "GitHub") + ")</small>"


def ko(n, lg):
    v = round(n / 1024, 1)
    return (str(v).replace(".", ",") + " Ko") if lg == "fr" else f"{v} KB"


def section(lg, jours, catalogue, criteres, docs):
    t = T[lg]
    out = [f'<article lang="{lg}" id="{lg}">', f"<h1>{e(t['titre'])}</h1>", f"<p>{e(t['intro'])}</p>",
           f"<p>{lien('./', t['portail'])} · {lien(JOURNAL if lg == 'fr' else JOURNAL + 'en/', t['journal'])} · {lien('llms.txt', 'llms.txt')}</p>"]

    out += [f'<h2 id="donnees-{lg}">{e(t["donneesTitre"])}</h2>', f"<p>{e(t['donneesNote'])}</p>",
            f"<table><tr><th>{e(t['colDate'])}</th><th>{e(t['colSource'])}</th><th>Firmware</th><th>{e(t['colTaille'])}</th><th>SHA-256</th></tr>"]
    for f in jours:
        src = t["srcReconstitue"] if f.get("source") == "reconstitue" else t["srcPasserelle"]
        out.append(f"<tr><td>{lien(f['fichier'], f.get('date', ''))}</td><td>{e(src)}</td><td>{e(str(f.get('firmware') or '—'))}</td>"
                   f"<td>{e(ko(f.get('octets', 0), lg))}</td><td><code>{e(f.get('sha256', ''))}</code></td></tr>")
    out.append("</table>")
    out.append(f"<p>{e(t['manifestes'])} : " if lg == "fr" else f"<p>{e(t['manifestes'])}: ")
    out[-1] += " · ".join(lien(m, m) for m in MANIFESTES if os.path.exists(m)) + "</p>"

    if criteres:
        out += [f'<h2 id="indice-{lg}">{e(t["indiceTitre"])}</h2>', f"<p>{e(t['indiceNote'])}</p>",
                f"<table><tr><th>#</th><th>{e(t['colAptitude'])}</th><th>{e(t['colEtat'])}</th><th>{e(t['colMesurable'])}</th><th>{e(t['colPlafond'])}</th></tr>"]
        bloc = None
        for k in criteres.get("criteres", []):
            if k.get("bloc") != bloc:
                bloc = k.get("bloc")
                out.append(f'<tr><td colspan="5"><b>{e(str(bloc))}. {e(criteres.get("blocs", {}).get(bloc, {}).get(lg, ""))}</b></td></tr>')
            note = k.get("note", {}).get(lg) if isinstance(k.get("note"), dict) else None
            plafond = str(k.get("plafond", ""))
            out.append(f"<tr><td>{e(str(k.get('n', '')))}</td><td>{e(k.get(lg, ''))}" + (f"<br><small>{e(note)}</small>" if note else "") + "</td>"
                       f"<td>… {e(t['enAttente'])}</td><td>{e(criteres.get('mesurable', {}).get(k.get('mesurable'), {}).get(lg, ''))}</td>"
                       f"<td>{e(plafond.replace('.', ',') if lg == 'fr' else plafond)}</td></tr>")
        out.append("</table>")
        doc = (criteres.get("document") or {}).get(lg) or ("documentation/grille-criteres-v2.md" if lg == "fr" else "documentation/grille-criteres-v2.en.md")
        out.append(f"<p>{fichier(doc, t['lienGrille'])}</p>")

    if catalogue:
        st = catalogue.get("statuts", {})
        out += [f'<h2 id="etudes-{lg}">{e(t["etudesTitre"])}</h2>', f"<p>{e(t['etudesNote'])}</p>",
                f"<table><tr><th>#</th><th>{e(t['colEtude'])}</th><th>{e(t['colStatut'])}</th><th>{e(t['colMoment'])}</th></tr>"]
        for x in catalogue.get("etudes", []):
            titre = x.get("titre", {}).get(lg, "")
            cell = lien(x["programme"][lg], titre) if x.get("programme") else e(titre)
            if x.get("doi"):
                cell += " · " + lien("https://doi.org/" + x["doi"], "DOI " + x["doi"])
            out.append(f"<tr><td>{e(str(x.get('id', '')))}</td><td>{cell}</td><td>{e(st.get(x.get('statut'), {}).get(lg, str(x.get('statut', ''))))}</td>"
                       f"<td>{e(x.get('moment', {}).get(lg, ''))}</td></tr>")
        out.append("</table>")
        out += [f'<h2 id="protocoles-{lg}">{e(t["protocolesTitre"])}</h2>', f"<p>{e(t['protocolesNote'])}</p>", "<ul>"]
        for x in catalogue.get("etudes", []):
            if x.get("protocole"):
                out.append(f"<li>{fichier(x['protocole'][lg], x.get('id', '') + ' — ' + x.get('titre', {}).get(lg, ''))}"
                           + (" · " + lien("https://doi.org/" + x["doi"], "DOI " + x["doi"]) if x.get("doi") else "") + "</li>")
        out.append(f"<li>{fichier('protocoles/README.md', t['listeDepots'])}</li></ul>")

    out += [f'<h2 id="documentation-{lg}">{e(t["docTitre"])}</h2>', "<ul>"]
    out += [f"<li>{fichier(c, ti)}</li>" for c, ti in docs]
    out.append("</ul>")

    reg = "documentation/registre-incidents.md" if lg == "fr" else "documentation/registre-incidents.en.md"
    out += [f'<h2 id="corrections-{lg}">{e(t["correctionsTitre"])}</h2>', f"<p>{e(t['correctionsNote'])}</p>",
            f"<p>{fichier(reg, t['registreLien'])}</p>"]

    out += [f"<h2>{e(t['autres'])}</h2><ul>"] + [f"<li>{fichier(a)}</li>" for a in AUTRES if os.path.exists(a)] + ["</ul>"]
    out.append(f"<p><small>{e(t['pied'])}</small></p></article><hr>")
    return out


def main():
    jours = [f for m in MANIFESTES for f in (lire(m, {}) or {}).get("fichiers", []) if isinstance(f, dict) and f.get("fichier")]
    jours.sort(key=lambda f: f.get("date", ""), reverse=True)
    catalogue = lire("etudes/catalogue.json", None)
    criteres = lire("site/criteres.json", None)
    chemins = sorted({c for motif in DOCS for c in glob.glob(motif)})
    # README files are bilingual / les README sont bilingues.
    docs = {"en": [(c, titre_md(c)) for c in chemins if c.endswith(".en.md") or c.endswith("README.md")],
            "fr": [(c, titre_md(c)) for c in chemins if not c.endswith(".en.md")]}

    corps = [l for lg in LANGS for l in section(lg, jours, catalogue, criteres, docs[lg])]
    page = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{e(T["en"]["titre"])}</title><meta name="description" content="{e(T["en"]["intro"])}">'
            '<style>body{max-width:60em;margin:2em auto;padding:0 1em;font:1em/1.5 system-ui,sans-serif}'
            'table{border-collapse:collapse;display:block;overflow-x:auto}td,th{border:1px solid #999;padding:.2em .5em;text-align:left;vertical-align:top}'
            'code{font-size:.8em;word-break:break-all}</style></head><body>\n'
            '<nav><a href="#en">English</a> · <a href="#fr">Français</a></nav>\n' + "\n".join(corps) + "\n</body></html>\n")
    with open("plan.html", "w", encoding="utf-8") as f:
        f.write(page)

    urls = [("", None), ("plan.html", jours[0]["date"] if jours else None)]
    urls += [(c, None) for c in chemins] + [(a, None) for a in AUTRES if os.path.exists(a)] + [(m, None) for m in MANIFESTES if os.path.exists(m)]
    urls += [(f["fichier"], f.get("date")) for f in jours]
    vus, lignes = set(), []
    for u, d in urls:
        if u in vus:
            continue
        vus.add(u)
        lignes.append(f"  <url><loc>{e(BASE + u)}</loc>" + (f"<lastmod>{d}</lastmod>" if d and len(d) == 10 else "") + "</url>")
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(lignes) + "\n</urlset>\n")
    print(f"plan.html : {len(jours)} fichiers de données / data files, {len(chemins)} documents ; sitemap.xml : {len(lignes)} adresses / URLs")


if __name__ == "__main__":
    main()
