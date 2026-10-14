# Version history

*[Version française](historique-versions.md)*

Every version that changes what the country measures, publishes or narrates is recorded here, with its delivery date (installation usually follows within 24 hours). A day's data should always be read with the firmware version stated in the file.

| Delivered | Firmware | Update | What changes for the data |
| --- | --- | --- | --- |
| 9 Oct 2026 | 0.3 | Production start | Era 1 begins. The newspaper appears at 8 pm. No raw export yet. |
| 10 Oct 2026 | 0.4 | Update 1a | The newspaper tells what changed since the day before (fewer repetitions), rotating section, "Figure of the day". Cable-free maintenance. Save format unchanged. |
| 11 Oct 2026 | 0.5 | Update 1b-1 "Small stories" | The newspaper follows characters (surviving ministers, "Whatever happened to…?", candidates, firsts). Embassy denials. Save format unchanged. |
| 13 Oct 2026 (installation planned 14 Oct, 9 pm) | 0.6 | Update 1b-2 "The newsroom" | **Daily raw export** to this repository (format 1), SHA-256 manifest, system notes. Citizen journalists, sections, humour column, Sunday edition, censored press (articles only, never the figures). Website published in a single commit. Fixes: "d'électricité" elision, tie-break by anger, no "satisfied mood" brief, 4th denial. Country save format unchanged (3440 bytes). First raw file expected on 15 October; it starts at installation (`heuresManquantes` = `null`). |
| upcoming | 0.7 | Update 1b-3 "Elections" | Export of brain weights, save-format migration (4) with reserved fields (genealogy, medicine), power-consumption reading. |

Days from 9 to 14 October 2026 are available in rebuilt form (`donnees/ere-001/reconstitue/`).
