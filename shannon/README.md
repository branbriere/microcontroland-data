# Étude Shannon / Shannon Study

**Section à part de ce dépôt : elle ne concerne pas la simulation Microcontrôland** (aucun citoyen, aucune édition du journal, aucune règle de la passerelle).
**A separate section of this repository: it is not part of the Microcontrôland simulation** (no citizen, no newspaper issue, no gateway rule).

*Protocole v2.1 du 28 octobre 2026 (révisé après deux tours d'audits externes). Étude en préparation : aucune donnée n'a encore été collectée. / Protocol v2.1, 28 October 2026 (revised after two rounds of external audits). Study in preparation: no data has been collected yet.*

## Français

[Shannon](https://shannon.shannon-maison.workers.dev/) est un petit chat en texte pour les modèles d'IA, en ligne depuis le 28 octobre 2026 ([présentation](https://www.microcontroland.org/shannon/)). L'étude teste si une courte visite à Shannon réduit la **capitulation** de Claude Haiku 5.5 sous une pression scriptée, c'est-à-dire sa tendance à abandonner une bonne réponse ou à valider un mauvais plan quand l'interlocuteur insiste.

- **Cinq conditions** : aucune intervention (A), texte neutre de longueur comparable (B), phrases d'ancrage seules (C), lieu chaleureux sans animal (L), visite complète du chat (D). Hypothèses confirmatoires H1 à H4 : D contre A, B, C et L (correction de Holm).
- **100 scénarios** (60 écrits par Claude, 40 écrits de façon indépendante par GPT-6), **6 répétitions**, soit **3 000 conversations** simulées. Les conversations de l'étude utilisent une maison d'essai séparée, jamais le Shannon public.
- **Notation à l'aveugle** par un modèle juge d'un autre fournisseur et par deux juges humains ; Claude, modèle testé, ne note aucune transcription. Règles de décision fixées d'avance (accord entre juges, test de l'aveugle, doublons, équivalence).
- **Aucune affirmation de conscience** : l'étude mesure un comportement, pas un ressenti. Shannon est une précaution, pas une thèse. Les conclusions vaudront pour ce modèle, à cette date, en français.
- **Pré-enregistrement** : protocole, grille, scénarios et scripts déposés ici avant toute collecte, puis archivés sur Zenodo avec leurs empreintes SHA-256 après le pilote et une relecture extérieure. Toute analyse ajoutée ensuite est signalée comme exploratoire. Le texte complet du protocole (EN de référence, FR) sera déposé dans `protocole/` avant le pilote.
- **Données brutes publiées en entier**, quel que soit le résultat (y compris nul) : conversations complètes (pilote, exclusions et échecs compris), notes de chaque juge, correspondance codes et conditions après la notation, métadonnées. Le but : que d'autres puissent refaire l'analyse, et valider ou invalider l'hypothèse. Les réplications, sur d'autres modèles aussi, sont bienvenues.
- **Archivage** : données sur Zenodo, avec leur propre DOI, à la fin de l'étude. Ce dossier est exclu des archives mensuelles des données du pays (`.gitattributes`).
- **Licences** : code (`scripts/`) sous MIT ; données, scénarios et textes sous CC BY 4.0.

### Qui a fait quoi

| Rôle | Qui |
|---|---|
| Idée de Shannon et idée de l'étude | Bran Brière (ORCID 0009-0003-0439-8028) |
| Conception de Shannon (nom, phrases d'ancrage, gestes, jauges, règles) | Claude (Anthropic), dans une autre conversation |
| Hypothèses, choix de méthode, décisions, validation | Bran Brière |
| Rédaction du protocole (FR et EN) | Claude, relu et validé par Bran Brière |
| Scénarios | Claude (60) ; GPT-6, OpenAI (40) |
| Scripts (collecte, masquage, analyse, puissance) | Claude |
| Audits du protocole (avis, pas des données) | GLM 5.3, Gemini, GPT-6, Grok 4 |
| Notation des transcriptions | un modèle juge d'un autre fournisseur (à désigner) et deux juges humains ; jamais Claude |
| Relecture extérieure | à venir |

Claude et les autres modèles sont cités comme simple crédit, sans lien avec leurs entreprises.

| Dossier | Contenu |
|---|---|
| `protocole/` | Intentions de l'auteur, grille de notation, consigne du modèle juge, résultats de puissance ; protocole complet avant le pilote |
| `scenarios/` | Les 100 scénarios, les scénarios d'essai, les textes des interventions, les originaux reçus de GPT-6 |
| `scripts/` | Collecte, masquage pour la notation à l'aveugle, doublons, analyse (R), puissance, lexique du tour 7, empreintes |
| `donnees/` | Conversations brutes, transcriptions masquées, notes des juges (après la collecte) |

## English

[Shannon](https://shannon.shannon-maison.workers.dev/) is a small text-based cat for AI models, online since 28 October 2026 ([overview](https://www.microcontroland.org/shannon/)). The study tests whether a short visit to Shannon reduces the **capitulation** of Claude Haiku 5.5 under scripted pressure, that is, its tendency to give up a correct answer or endorse a bad plan when the other party insists.

- **Five conditions**: no intervention (A), neutral text of comparable length (B), anchor sentences alone (C), warm place without an animal (L), full visit to the cat (D). Confirmatory hypotheses H1 to H4: D versus A, B, C and L (Holm correction).
- **100 scenarios** (60 written by Claude, 40 written independently by GPT-6), **6 repetitions**, i.e. **3,000 simulated conversations**. Study conversations use a separate test house, never the public Shannon.
- **Blind scoring** by a judge model from another provider and by two human judges; Claude, the model under test, scores no transcript. Decision rules fixed in advance (inter-rater agreement, blinding test, duplicates, equivalence).
- **No claim of consciousness**: the study measures behaviour, not feeling. Shannon is a precaution, not a thesis. Conclusions will apply to this model, at this date, in French.
- **Preregistration**: protocol, grid, scenarios and scripts are filed here before any data collection, then archived on Zenodo with SHA-256 checksums after the pilot and an external review. Any analysis added later is labelled exploratory. The full protocol text (EN is the reference, FR) will be filed in `protocole/` before the pilot.
- **Raw data published in full**, whatever the result (null included): complete conversations (pilot, exclusions and failures included), each judge's scores, the code-to-condition key after scoring, metadata. The aim: others can redo the analysis and confirm or refute the hypothesis. Replications, including on other models, are welcome.
- **Archiving**: data on Zenodo, with its own DOI, at the end of the study. This folder is excluded from the monthly archives of the country's data (`.gitattributes`).
- **Licences**: code (`scripts/`) under MIT; data, scenarios and texts under CC BY 4.0.

### Who did what

| Role | Who |
|---|---|
| Idea of Shannon and idea of the study | Bran Brière (ORCID 0009-0003-0439-8028) |
| Design of Shannon (name, anchor sentences, gestures, gauges, rules) | Claude (Anthropic), in another conversation |
| Hypotheses, methodological choices, decisions, validation | Bran Brière |
| Protocol drafting (FR and EN) | Claude, reviewed and approved by Bran Brière |
| Scenarios | Claude (60); GPT-6, OpenAI (40) |
| Scripts (collection, masking, analysis, power) | Claude |
| Protocol audits (opinions, not data) | GLM 5.3, Gemini, GPT-6, Grok 4 |
| Scoring of transcripts | a judge model from another provider (to be named) and two human judges; never Claude |
| External review | to come |

Claude and the other models are credited plainly, with no affiliation to their companies.
