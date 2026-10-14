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
| `protocoles/` | Protocoles et pré-enregistrements, déposés avant l'analyse. |
| `etudes/` | [Programme des études](etudes/programme.md) et catalogue avec le statut de chacune. |

## Règles

- **Faits, interprétations, hypothèses :** les données brutes sont des faits enregistrés par les cartes. Le journal et l'Ambassade en donnent une interprétation narrative. Les études formulent des hypothèses. Les trois ne sont jamais mélangés.
- **Rien n'est réécrit :** une observation publiée n'est jamais modifiée. Une correction est datée et documentée à part.
- **Les absences sont explicites :** paquet perdu, redémarrage ou maintenance sont notés comme tels (`null`), jamais remplacés par zéro.
- **Vérifiable :** chaque fichier peut être contrôlé avec son empreinte SHA-256 du manifeste.

## Licences et citation

- Données et documentation : [CC BY 4.0](LICENSE-DATA) — réutilisation libre en citant la source.
- Code : [MIT](LICENSE-CODE).
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
| `protocoles/` | Protocols and pre-registrations, filed before analysis. |
| `etudes/` | [Study programme](etudes/programme.en.md) and catalogue with each study's status. |

Folder and field names are in French; the data dictionary gives their meaning in both languages.

## Rules

- **Facts, interpretations, hypotheses:** raw data are facts recorded by the boards. The newspaper and the Embassy give a narrative interpretation. Studies state hypotheses. The three are never mixed.
- **Nothing is rewritten:** a published observation is never modified. A correction is dated and documented separately.
- **Gaps are explicit:** a lost packet, a restart or a maintenance window is recorded as such (`null`), never replaced by zero.
- **Verifiable:** every file can be checked against its SHA-256 checksum in the manifest.

## Licences and citation

- Data and documentation: [CC BY 4.0](LICENSE-DATA) — free reuse with attribution.
- Code: [MIT](LICENSE-CODE).
- To cite this dataset: see [CITATION.cff](CITATION.cff) (GitHub's "Cite this repository" button).

Author: Bran Brière — ORCID [0009-0003-0439-8028](https://orcid.org/0009-0003-0439-8028)

To report an error or ask a question: open an *issue*.
