#!/usr/bin/env python3
"""Reconstitue les journées publiées AVANT l'export brut (MAJ 1b-2) à partir de l'historique git du site.
Rebuilds the days published BEFORE the raw export (update 1b-2) from the website's git history.

Usage : python3 reconstitue.py <clone du site / site clone> <dossier du dépôt de données / data repo folder> [ère / era]

Ce que contient un fichier reconstitué / What a rebuilt file contains:
  - seulement ce que le journal a publié ce soir-là (pourcentages arrondis 0-100, pas l'échelle brute 0-255) ;
    only what the newspaper published that evening (rounded 0-100 percentages, not the raw 0-255 scale);
  - aucune donnée heure par heure : "heures" vaut null, jamais une valeur inventée ;
    no hour-by-hour data: "heures" is null, never an invented value;
  - "source": "reconstitue" et "reconstitue": true, dans un dossier séparé du quotidien de la passerelle.
    "source": "reconstitue" and "reconstitue": true, in a folder kept apart from the gateway's daily files.
Les fichiers déjà présents ne sont jamais réécrits. / Existing files are never rewritten.
"""
import hashlib, json, os, subprocess, sys

def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True, check=True).stdout

def at(repo, commit, path):
    try: return json.loads(git(repo, 'show', f'{commit}:{path}'))
    except subprocess.CalledProcessError: return None

def main():
    site, data = sys.argv[1], sys.argv[2]
    era = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    out = os.path.join(data, 'donnees', f'ere-{era:03d}', 'reconstitue')
    os.makedirs(out, exist_ok=True)
    log = git(site, 'log', '--reverse', '--format=%H %cI', '--', 'data/latest.json').decode().split('\n')
    written = []
    for line in filter(None, log):
        commit, when = line.split(' ', 1)
        e = at(site, commit, 'data/latest.json')
        if not e or e.get('ere') != era: continue
        path = os.path.join(out, e['date'] + '.json')
        if os.path.exists(path): continue
        # La langue et les citoyens partent quelques secondes après l'édition : on prend leur état du même soir.
        later = git(site, 'log', '--format=%H %cI', f'{commit}~1..HEAD', '--', 'data/langue.json', 'data/citoyens.json').decode().split('\n')
        same = [l.split(' ')[0] for l in later if l and l.split(' ', 1)[1][:10] == when[:10]]
        ref = same[-1] if same else commit
        lang, civ = at(site, ref, 'data/langue.json'), at(site, ref, 'data/citoyens.json')
        s = e['etat']
        rec = {
            'format': 1, 'source': 'reconstitue', 'reconstitue': True,
            'methode': {'fr': 'Reconstitué après coup à partir de l\'édition publiée sur le site (historique git). Valeurs arrondies telles que publiées ; aucune donnée horaire.',
                        'en': 'Rebuilt afterwards from the edition published on the website (git history). Values rounded as published; no hourly data.'},
            'origine': {'depot': 'branbriere/microcontroland', 'commit': commit, 'publieLe': when},
            'ere': era, 'date': e['date'], 'jourEre': e.get('jourEre'), 'edition': e['day'],
            'heuresVecues': None, 'heures': None, 'heuresManquantes': None,
            'echelle': 'pourcentage 0-100 (arrondi) / percentage 0-100 (rounded)',
            'pays': {'regime': s['regime']['fr'] if isinstance(s.get('regime'), dict) else s.get('regime'),
                     'president': e.get('president') or None, 'capitale': s.get('capitale') or None,
                     'ministres': s.get('ministres'), 'objectif': s.get('objectif'), 'ressources': s.get('ressources'),
                     'satisfaction': s.get('satisfaction'), 'peur': s.get('peur'), 'colere': s.get('colere'),
                     'foi': s.get('foi')},
            'regions': [{'nom': r['nom'], 'humeur': r.get('humeur'), 'rebelles': r.get('rebelles'), 'cerveaux': r.get('cerveaux')} for r in e.get('regions', [])],
            'bourse': e.get('bourse'),
            'evenements': [{'heure': j['heure'], 'texte': j['texte']} for j in e.get('journee', [])],
            'langue': None if not lang else {'motsCommuns': lang.get('partages'), 'idees': lang.get('idees'), 'comprehension': lang.get('comprehension')},
            'citoyens': None if not civ or not civ.get('ouvert') else civ.get('citoyens'),
            'journal': {'edition': e['day'], 'fichier': f'data/editions/{e["day"]}.json'},
        }
        raw = json.dumps(rec, ensure_ascii=False, separators=(',', ':')).encode()
        with open(path, 'wb') as f: f.write(raw)
        written.append({'fichier': f'donnees/ere-{era:03d}/reconstitue/{e["date"]}.json', 'date': e['date'], 'ere': era, 'firmware': None,
                        'octets': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'source': 'reconstitue'})
        print('reconstitué / rebuilt :', e['date'], 'édition', e['day'])
    man = os.path.join(out, 'manifeste.json')
    old = json.load(open(man))['fichiers'] if os.path.exists(man) else []
    with open(man, 'w') as f: json.dump({'format': 1, 'ere': era, 'source': 'reconstitue', 'fichiers': old + written}, f, ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
