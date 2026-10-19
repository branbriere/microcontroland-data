#!/usr/bin/env python3
"""Construit l'index du moteur de recherche du site (site/recherche.json) à partir des textes du dépôt.
Builds the website search index (site/recherche.json) from the repository's texts.

Usage : python3 outils/index_site.py   (depuis la racine du dépôt / from the repository root)

À relancer après chaque ajout ou modification de documentation, d'étude ou de protocole.
Re-run after any documentation, study or protocol is added or changed.
Les données quotidiennes, le catalogue et les critères sont lus directement par le site : ils n'ont pas besoin d'index.
Daily data, the catalogue and the criteria are read directly by the website: they need no index.
"""
import glob, json, os, re

SOURCES = [('doc', 'documentation/*.md'), ('doc', 'etudes/*.md'), ('protocole', 'protocoles/*.md'), ('doc', 'README.md')]

def texte_brut(md):
    md = re.sub(r'```.*?```', ' ', md, flags=re.S)
    md = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', md)
    md = re.sub(r'[#*_`>|]', ' ', md)
    return re.sub(r'\s+', ' ', md).strip()

def main():
    docs = []
    for type_, motif in SOURCES:
        for chemin in sorted(glob.glob(motif)):
            md = open(chemin, encoding='utf-8').read()
            titre = next((l[2:].strip() for l in md.splitlines() if l.startswith('# ')), os.path.basename(chemin))
            langues = ['en'] if chemin.endswith('.en.md') else ['fr', 'en'] if chemin == 'README.md' or 'README' in chemin else ['fr']
            for lg in langues:
                docs.append({'type': type_, 'lang': lg, 'chemin': chemin, 'titre': titre, 'texte': texte_brut(md)})
    os.makedirs('site', exist_ok=True)
    with open('site/recherche.json', 'w', encoding='utf-8') as f:
        json.dump({'format': 1, 'documents': docs}, f, ensure_ascii=False, separators=(',', ':'))
    print(len(docs), 'documents indexés / indexed')

if __name__ == '__main__':
    main()
