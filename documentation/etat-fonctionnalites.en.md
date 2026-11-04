# Feature status

*[Version française](etat-fonctionnalites.md)*

**Status as of 2 November 2026, firmware 0.9 (gateway) and 0.8.1 (regions) in service (installed on 1 November).** This is the single reference for whether a feature announced on either website exists. Where pages disagree, this table prevails over them, and the code prevails over this table. It is updated with every release.

**States:**
- **In service**: the feature runs in the box or on the websites.
- **Coded, closed**: the code is in the firmware in service, but the feature only opens at an age the country has not reached yet, or awaits a setting.
- **Planned**: nothing is coded yet, or the code is not installed. Order and content may change.

The firmware is not public yet (it will be released with the studies). Until then, the "Where to check" column points to public data and pages.

## The box and the data

| Feature | State | Since | Where to check |
| --- | --- | --- | --- |
| Country of 120 citizens on 6 regions and a gateway (ESP-NOW radio) | In service | 0.3, 8 Oct 2026 | [architecture.en.md](architecture.en.md) |
| One hour in the country = one real hour, on French time | In service | 0.3 | `heures[]` in every raw file |
| Real market prices: European Central Bank rates, read at 6 pm on business days | In service | 0.3 | `bourse` in every issue |
| What comes in from outside: today, only market prices. Counted votes and replies to the signal: see the ages below | In service (market) | 0.3 | "About" page |
| Simulated weather: storms, epidemics, droughts, crises, plenty, drawn at random by the gateway | In service | 0.3 | rules page; no real weather data |
| Elections every 3 days, ministers, censorship, postponement, revolt, palace coup, vacancy | In service | 0.3 | newspaper, `data/histoire.json` |
| Citizens' faith (believer, agnostic, atheist) | In service | 0.3 | newspaper |
| Shared language: one idea per hour, speaker drawn at random | In service | 0.3 | `data/langue.json` |
| Effect of language on politics: two regions that understand each other poorly trust each other less (voters favour a candidate from a region that "speaks like them", and a region that understands the capital poorly gets slightly angrier). This is a fixed rule of the gateway and regions. The words themselves are not inputs to the brains, and their decisions do not depend on them directly | In service | 0.3 | `comprehension` in `data/langue.json` and the raw file; [grille-criteres-v2.en.md](grille-criteres-v2.en.md) (criterion 09) |
| Reward-based learning of the brains (weights strengthened or weakened according to satisfaction) | In service as a mechanism; its effect on behaviour is not demonstrated yet (weights exported daily since 0.8, studies to come) | 0.3 | [grille-criteres-v2.en.md](grille-criteres-v2.en.md) |
| Daily raw file with SHA-256 manifest | In service | 0.6, 15 Oct 2026 | [dictionnaire-donnees.en.md](dictionnaire-donnees.en.md) |
| Random seeds published (format 2) | In service | 0.7, 18 Oct 2026 | `graines` block of the raw file |
| Power consumption read every hour (local smart plug) | In service | 0.7 | `heures[].prise` |
| Automatic Wi-Fi restart after an outage | In service | 0.7 | `systeme.notes` (type `wifi`) |
| Delayed publication when the Internet is down | In service | 0.3 | [registre-incidents.en.md](registre-incidents.en.md) |
| Copy of the country outside the box every evening | In service | 0.3 | `data/sauvegarde.json` (newspaper site) |
| Hidden RESET button (Great Reset) | In service | 0.3 | never used so far |
| Abstention and election column | In service since 26 Oct 2026 | 0.8 | `election` in the raw file; "Election column" brief |
| Blank vote | In service since 27 Oct 2026 | 0.8 | `nouveautes.voteBlanc` in the raw file |
| Polls (20 citizens drawn by lot, halfway through the campaign) | In service since 29 Oct 2026 | 0.8 | `sondage` in the raw file |
| Fame (a known name reassures in the polling booth) | In service since 30 Oct 2026 | 0.8 | `notoriete` in the raw file (computed from 0.8 onwards, no effect before it opens) |
| Weights of all 120 brains and complete lexicons, once a day | In service | 0.8 | `poids`, `lexiques` in the raw file |
| Each hour's speaker, the regions' measurements (memory, computation, reply time, temperature) | In service | 0.8 | `heures[].porteVoix`, `heures[].regions[].systeme` |
| Ministers' names in the newspaper | In service | 0.8 | "State of the nation" panel |
| Country save in format 4 (reserved fields: genealogy, medicine) | In service | 0.8 | [historique-versions.en.md](historique-versions.en.md) |
| Stronger radio: each region sends its state 4 times, the gateway keeps its radio awake (about 13% of region-hours missing from 25 Oct to 1 Nov) | In service | 0.8.1 (regions), 0.9 (gateway), 1 Nov 2026 | `heures[].regions` in the raw file (`null` = silent region) |
| Raw file format 4: biographies, 0.9 new features, event `w` (shared word regained) | In service | 0.9, 2 Nov 2026 | [dictionnaire-donnees.en.md](dictionnaire-donnees.en.md) |
| Work, money, school, generations, etc. (updates 2 to 7) | Planned | — | rules page, "What is planned" |

## The ages of the civilisation

| Age | What opens | State | Where to check |
| --- | --- | --- | --- |
| Founding | The paper | In service since 9 Oct 2026 | newspaper |
| Speech | The "Language" page | In service since 18 Oct 2026 | `ages` in `data/latest.json` |
| Memory | The "History" page, records | In service since 24 Oct 2026 | same field: progress towards the age |
| Civil Registry | Adopting a citizen | In service since 28 Oct 2026 | same |
| Diplomacy | The embassy, its questions and monthly letter | Coded, closed | same |
| Diplomacy | Embassy denials in the paper (typos of past issues) | Coded (0.5), closed | same |
| Diplomacy | Public votes on the embassy's questions (plain counters) | Coded, closed, and waiting for the voting service (not chosen yet) | legal notice page |
| Curiosity | The Research Centre's signal and listening for replies (written in the country's language only) | Coded, closed | same |

## The newspaper

| Feature | State | Since | Where to check |
| --- | --- | --- | --- |
| Bilingual paper written by the gateway, every evening at 8 pm | In service | 0.3 | `data/editions/N.json` |
| Following characters ("What became of…?", journey of the week) | In service | 0.5 and 0.6 | issues |
| Sections, signing citizen journalists, daily note, Sunday issue | In service | 0.6 | `signature` in issues |
| Censored press (articles blacked out, never the figures) | In service | 0.6 | issues under censorship |
| Biography of every citizen (at most 16 steps: the fact, the hour and the mood of the moment, never the reason), quoted by the Sunday portrait and the "My citizen" page | Coded, opens on 3 Nov 2026 (one new feature per evening) | 0.9 | `biographies` in the raw file |
| Binaï, the rebels' newspaper, at the top of the issue from the 3rd consecutive issue under censorship | Opened on 2 Nov 2026; appears only under prolonged censorship | 0.9 | `nouveautes.binai` in the raw file |
| Return of a lost shared word (line in the day's chronology; a brief in at most one issue in seven) | In service | 0.9 | event `w` in the raw file |

## The websites

| Feature | State | Since | Where to check |
| --- | --- | --- | --- |
| microcontroland.org domain (newspaper on www, data on donnees) | In service | 21 Oct 2026 | — |
| Newspaper readable without JavaScript (`journal.txt`, `/texte/`) | In service | 21 Oct 2026 | [journal.txt](https://www.microcontroland.org/journal.txt) |
| History and language without JavaScript, robots.txt, sitemap | In service | 21 Oct 2026 | [/texte/](https://www.microcontroland.org/texte/) |
| "Discover the country in 5 minutes" page (country's state updated every evening) | In service | 21 Oct 2026 | [decouvrir.html](https://www.microcontroland.org/decouvrir.html) |
| Static index of the data site | In service | 21 Oct 2026 | [plan.html](https://donnees.microcontroland.org/plan.html) |
| Anonymous log of self-declared robots (day, robot, page, status; no IP, no cookie) | In service | 21 Oct 2026 | monthly export planned in `agents-ia/` |
| Table of the 18 artificial-life criteria (grid v2) | In service, states "pending" | 19 Oct 2026 | [grille-criteres-v2.en.md](grille-criteres-v2.en.md) |
| Computation of the criteria index | Planned: thresholds dated before the first computation, display at the Age of Curiosity | — | same |
| Hall of the Relic at the Embassy (Microcontrolchess against the AI, gallery, daily puzzle, text version relique.txt) | Coded, closed until Diplomacy | 26 Oct 2026 | [microcontrolchess.en.md](microcontrolchess.en.md) |
| National Tourist Office (regions, religion, places to visit, one-byte collector coin with the president's portrait, PDF leaflet FR/EN, text version tourisme.txt); virtual visa at the Embassy | Coded, closed until Diplomacy | 28 Oct 2026 | [tourisme.txt](https://www.microcontroland.org/en/tourisme.txt) |
| "The Studio" page: primitive art, one 5×5 drawing per evening computed from the published weights (rule B3), two lines from the critic | In service (website only, no firmware) | 28 Oct 2026 | [atelier.html](https://www.microcontroland.org/en/atelier.html), [atelier.json](https://www.microcontroland.org/atelier.json) |
| "The Presidential Gallery" page: one portrait per president (Hinton diagram of the 81 published weights of their citizen brain) and the record of each term; opens at the Age of Memory | In service (website only, no firmware) | 28 Oct 2026 | [galerie.html](https://www.microcontroland.org/en/galerie.html), [galerie.json](https://www.microcontroland.org/galerie.json) |
| 3D National Museum (first-person tour and text tour): rebuilt every evening by a script from the published data only (gallery, studio, ages, institutions); one wing per era, opened when that era reaches the Age of Memory, frozen when the era ends; Hall of Presidents with the statue of the network of the president in office (81 weights of the citizen brain), studio, one room of artists of the evening per month, Temple annex under construction; rooms of different heights; day, evening or night light following the visitor's clock; self-hosted Three.js, no outside call | In service (website only, no firmware) | 4 Nov 2026 | [musee.html](https://www.microcontroland.org/en/musee.html), [musee.json](https://www.microcontroland.org/musee.json), [musee-catalogue.json](https://www.microcontroland.org/musee-catalogue.json) |
| "My citizen" page: each citizen's history, rebuilt every evening from the published raw files (political events since 9 Oct, candidacies, revolt and censorship since 15 Oct), up to the start of their biography | In service (website only, no firmware) | 2 Nov 2026 | [historique.json](https://www.microcontroland.org/data/historique.json) |
| Second "president" portrait in the gallery (75 weights of the governing brain, export to be added to the raw file) | Planned, update 1b-5 | — | — |
| Arts section in the issue (same rule, computed by the gateway) | Planned, update 1b-5 | — | — |
| Release of the firmware source code | Planned, with the studies | — | — |
