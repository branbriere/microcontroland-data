# Microcontrôland — données scientifiques / scientific data

**Français** · [English below](#english)

Microcontrôland est un pays fictif simulé par 7 microcontrôleurs ESP32 : 6 régions et 120 citoyens, chacun étant un petit réseau de neurones de 81 connexions. Rien n'est scénarisé : élections, révoltes, langue et croyances naissent des décisions des citoyens. Chaque soir, le pays publie son journal, [La Puce Libre](https://branbriere.github.io/microcontroland/).

Ce dépôt contient les **données brutes** du pays, sa documentation et les études qui s'en servent. Le journal raconte ; ce dépôt enregistre.

## Contenu

| Dossier | Contenu |
| --- | --- |
| `donnees/ere-NNN/quotidien/` | Un fichier par jour, publié par la passerelle chaque soir après le journal. Jamais modifié ensuite. |
| `donnees/ere-NNN/manifeste.json` | Liste des fichiers avec date, version du firmware, taille et empreinte SHA-256. |
| `donnees/ere-001/reconstitue/` | Les jours du 9 au 14 octobre 2026, publiés avant l'export brut, rebâtis à partir du journal. Marqués « reconstitué », avec leur propre manifeste. |
| `outils/` | Le script de reconstitution (licence MIT). |
| `documentation/` | Architecture, dictionnaire des données, historique des versions. |
| `protocoles/` | Protocoles et pré-enregistrements, déposés avant l'analyse et archivés sur Zenodo ([liste et DOI](protocoles/README.md)). |
| `etudes/` | [Programme des études](etudes/programme.md) et catalogue avec le statut de chacune. |

## Règles

- **Faits, interprétations, hypothèses :** les données brutes sont des faits enregistrés par les cartes. Le journal et l'Ambassade en donnent une interprétation narrative. Les études formulent des hypothèses. Les trois ne sont jamais mélangés.
- **Rien n'est réécrit :** une observation publiée n'est jamais modifiée. Une correction est datée et documentée à part.
- **Les absences sont explicites :** paquet perdu, redémarrage ou maintenance sont notés comme tels (`null`), jamais remplacés par zéro.
- **Vérifiable :** chaque fichier peut être contrôlé avec son empreinte SHA-256 du manifeste.
- **Archivé hors de GitHub :** chaque mois, une copie figée du dépôt est déposée sur Zenodo (CERN), où personne ne peut plus la modifier. DOI de toutes les versions (renvoie toujours à la plus récente) : [10.5281/zenodo.23538358](https://doi.org/10.5281/zenodo.23538358) ; première version le 21 octobre 2026 : 10.5281/zenodo.23538359.

## Section à part : Étude Shannon (ne concerne pas Microcontrôland)

Le dossier [`shannon/`](shannon/README.md) contient une expérience **distincte de Microcontrôland**. Shannon est un petit chat en texte, compagnon pour les modèles d'IA ; l'étude teste si une visite au chat réduit la capitulation d'un modèle d'IA sous une pression scriptée (abandonner une bonne réponse quand l'interlocuteur insiste). Ses données brutes seront publiées en entier, pour que chacun puisse vérifier. Elle n'utilise aucune donnée du pays, aucun citoyen, aucune carte ESP32, et le pays ne sait rien d'elle.

- Ses fichiers ne font pas partie des archives mensuelles des données du pays : ils sont exclus des releases Zenodo mensuelles (`.gitattributes`) et seront archivés à part, avec leur propre DOI, à la fin de l'étude.
- Son protocole est déposé avant toute collecte ; l'historique Git sert de pré-enregistrement.
- Comme pour le reste du projet : aucune affirmation de conscience. Elle mesure un comportement, pas un ressenti.

## Licences et citation

- Données et documentation : [CC BY 4.0](LICENSE-DATA) — réutilisation libre en citant la source.
- Code : [MIT](LICENSE-CODE), pour les scripts publiés dans ce dépôt (`outils/` et `shannon/scripts/`). Le programme des cartes (firmware) n'est pas publié pour l'instant.
- Pour citer ce jeu de données : voir [CITATION.cff](CITATION.cff) (bouton « Cite this repository » de GitHub).

Auteur : Bran Brière — ORCID [0009-0003-0439-8028](https://orcid.org/0009-0003-0439-8028)

Signalement d'erreur ou question : ouvrez une *issue*.

---

## English

Microcontrôland is a fictional country simulated by 7 ESP32 microcontrollers: 6 regions and 120 citizens, each a small neural network with 81 connections. Nothing is scripted: elections, revolts, language and beliefs arise from the citizens' decisions. Every evening the country publishes its newspaper, [La Puce Libre](https://branbriere.github.io/microcontroland/).

This repository holds the country's **raw data**, its documentation and the studies that use them. The newspaper tells the story; this repository keeps the record.

## Contents

| Folder | Contents |
| --- | --- |
| `donnees/ere-NNN/quotidien/` | One file per day, published by the gateway every evening after the newspaper. Never modified afterwards. |
| `donnees/ere-NNN/manifeste.json` | List of files with date, firmware version, size and SHA-256 checksum. |
| `donnees/ere-001/reconstitue/` | Days from 9 to 14 October 2026, published before the raw export, rebuilt from the newspaper. Marked "reconstitue" (rebuilt), with their own manifest. |
| `outils/` | The rebuild script (MIT licence). |
| `documentation/` | Architecture, data dictionary, version history. |
| `protocoles/` | Protocols and pre-registrations, filed before analysis and archived on Zenodo ([list and DOIs](protocoles/README.md)). |
| `etudes/` | [Study programme](etudes/programme.en.md) and catalogue with each study's status. |

Folder and field names are in French; the data dictionary gives their meaning in both languages.

## Rules

- **Facts, interpretations, hypotheses:** raw data are facts recorded by the boards. The newspaper and the Embassy give a narrative interpretation. Studies state hypotheses. The three are never mixed.
- **Nothing is rewritten:** a published observation is never modified. A correction is dated and documented separately.
- **Gaps are explicit:** a lost packet, a restart or a maintenance window is recorded as such (`null`), never replaced by zero.
- **Verifiable:** every file can be checked against its SHA-256 checksum in the manifest.
- **Archived outside GitHub:** every month a frozen copy of the repository is deposited on Zenodo (CERN), where nobody can modify it any more. DOI for all versions (always resolves to the latest): [10.5281/zenodo.23538358](https://doi.org/10.5281/zenodo.23538358); first version 21 October 2026: 10.5281/zenodo.23538359.

## Separate section: the Shannon Study (not part of Microcontrôland)

The [`shannon/`](shannon/README.md) folder holds an experiment **separate from Microcontrôland**. Shannon is a small text-based cat, a companion for AI models; the study tests whether a visit to the cat reduces an AI model's capitulation under scripted pressure (giving up a correct answer when the other party insists). Its raw data will be published in full so anyone can check. It uses no data from the country, no citizen, no ESP32 board, and the country knows nothing of it.

- Its files are not part of the monthly archives of the country's data: they are excluded from the monthly Zenodo releases (`.gitattributes`) and will be archived separately, with their own DOI, when the study ends.
- Its protocol is filed before any data collection; the Git history serves as preregistration.
- As in the rest of the project: no claim of consciousness. It measures behaviour, not feeling.

## Licences and citation

- Data and documentation: [CC BY 4.0](LICENSE-DATA) — free reuse with attribution.
- Code: [MIT](LICENSE-CODE), for the scripts published in this repository (`outils/` and `shannon/scripts/`). The boards' program (firmware) is not published for now.
- To cite this dataset: see [CITATION.cff](CITATION.cff) (GitHub's "Cite this repository" button).

Author: Bran Brière — ORCID [0009-0003-0439-8028](https://orcid.org/0009-0003-0439-8028)

To report an error or ask a question: open an *issue*.
