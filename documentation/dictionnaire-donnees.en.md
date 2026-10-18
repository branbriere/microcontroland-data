# Data dictionary

*[Version française](dictionnaire-donnees.md)* · Daily file format: **2** (firmware 0.7, from 19 October 2026); format **1** (firmware 0.6) from 15 to 18 October 2026

## General rules

- **One file per day**: `donnees/ere-NNN/quotidien/YYYY-MM-DD.json`, written by the gateway at 8 pm, published right after the newspaper, **never modified afterwards**.
- **Raw scale**: citizen and region mood values range from **0 to 255** (255 = maximum). Country averages are given in **thousandths** (0 to 1000).
- **`null` = missing** (silent region, lost hour, unknown value). Never replaced by 0.
- **Hours**: `tick` is the country-hour number since the start of the era (1, 2, 3…). Use it to compare real and simulated countries by hours lived, not calendar days.
- **Verification**: every file is listed in `donnees/ere-NNN/manifeste.json` with its size in bytes and SHA-256 checksum (`sha256sum file.json`).
- Field names are French; texts are given in French and English (`fr`, `en`).

## File root

| Field | Type | Meaning |
| --- | --- | --- |
| `format` | integer | Format version (1; 2 from firmware 0.7, which adds `graines` and `heures[].prise`). |
| `source` | text | `passerelle` (measured by the gateway); `reconstitue` for days rebuilt afterwards (`reconstitue/` folder). |
| `firmware` | text | Gateway firmware version, e.g. `0.6`. |
| `parametres` | object | `heureDuPaysMs` (length of a country hour in ms), `regions`, `citoyensParRegion` (citizens per region), `connexionsParCerveau` (connections per brain), `idees` (ideas in the lexicon), `seuilMotCommun` (regions that must agree for a word to be shared), `echelle` (255). |
| `ere` | integer | Era number (a "Grand Reset" opens a new era). |
| `date` | text | French date of the issue (YYYY-MM-DD). |
| `jourEre` | integer | Day of the era. |
| `edition` | integer | Number of that evening's newspaper issue. |
| `heuresVecues` | integer | Country hours lived since the start of the era, at issue time. |
| `genereUtc` | text / null | UTC time the file was written (ISO 8601). |
| `heures` | list | One entry per hour recorded since the previous issue (see below). |
| `heuresManquantes` | list / null | `tick` of expected but missing hours (restart, power cut). `null` when the start of the day is unknown (first file after a restart). |
| `evenements` | list | The day's facts as logged by the gateway. |
| `pays` | object | State of the country at issue time. |
| `citoyens` | list of 120 | One object per citizen (`null` if their region never answered). |
| `langue` | object | State of the shared language. |
| `journal` | object | Pointer to the issue (interpretation): `edition`, `fichier` (path on the website). |
| `graines` | object | Random seeds (format 2, see below). Absent from format 1 files. |
| `systeme` | object | `notes`: technical events (see below). |

## `heures[]` (hours)

| Field | Meaning |
| --- | --- |
| `tick` | Country-hour number. |
| `heure` | French clock hour (0-23). |
| `utc` | Real UTC time of the record, or `null` (no Internet time). |
| `regions` | 6 entries in the order Mines, Fields, Refineries, Dam, Harbour, City; `null` if the region did not answer that hour. |
| `idee` | The idea the regions proposed a word for that hour: `id`, `fr`, `en`. `null` if none. |
| `prise` | Format 2: reading of the Shelly smart plug that powers the whole country, taken by the gateway right after the hour's radio round, on the local network. `puissanceW` (instantaneous power, W) and `compteurWh` (the plug's cumulative energy counter, Wh), 3 decimals. Average consumption between two hours = difference of `compteurWh` / duration. `null` if the plug did not answer. The counter restarts from zero if the plug is reset: a decreasing counter signals a reset, not negative consumption. |
| `systeme` | `memoireLibre` (free heap), `psramLibre` (free PSRAM, bytes), `dureeHeureMs` (radio round time), `paquetsPerdus` (packets received but discarded because the gateway's receive queue was full, since the previous hour; this is not the number of silent regions, which is read from `regions`); `null` if not measured. |

### `heures[].regions[]`

| Field | Scale | Meaning |
| --- | --- | --- |
| `cerveaux` | 0-20 | Active citizens (brains). |
| `satisfaction`, `peur` (fear), `colere` (anger) | 0-255 | Region averages. |
| `rebelles` (rebels), `censures` (censored), `croyants` (believers), `athees` (atheists) | 0-20 | Number of citizens. |
| `production`, `objectif` (target) | raw | Region output and its target. |
| `mot` (word) | object / null | Word proposed for the hour's idea: `syllabes` (indices), `ecrit` (written form). |

## `evenements[]` (events)

| Field | Meaning |
| --- | --- |
| `tick`, `heure` | When it happened. |
| `type` | Letter: `e` election · `o` campaign/poll opening · `c` revolt · `k` palace coup · `b` regime change · `p` election postponed · `m` government · `s` censorship · `v` region unreachable · `x` market · `n` nature (storm, epidemic, harvest…) · `f` faith · `W` shared word · `a` new age · `R` record · `l` ambassador's letter · `S` signal sent · `g` signal received · `q` listening · `r` era start. |
| `sous`, `a`, `b`, `c`, `d` | Raw event parameters (citizen ids, regions, values). |
| `texte` | Logbook sentence, `fr` and `en` (never censored). |

## `pays` (country)

| Field | Meaning |
| --- | --- |
| `president` | President's id (1-120), `null` if vacant. |
| `capitale` | President's region (capital), `null` if vacant. |
| `regime` | Démocratie (Democracy), Démocratie fragile (Fragile democracy), Oligarchie, Autocratie, Junte (Junta), Dictature (Dictatorship), Agitation révolutionnaire (Revolutionary unrest). |
| `ministres` | Ministers' ids. |
| `objectifAtteint` (target reached), `ressources` | Thousandths (0-1000). |
| `satisfactionMoyenne`, `peurMoyenne`, `colereMoyenne` | Average satisfaction, fear, anger, in thousandths (0-1000). |
| `rebelles` | Rebels in the regions that answered. |
| `croyantsPct`, `atheesPct` | Believers and atheists, percent. |
| `age` | Civilisation age reached (0 = Founding). |
| `elections`, `revolutions`, `coupsDePalais` (palace coups), `reports` (postponements) | Counters since the start of the era. |
| `bourse` (market) | `statut` (`reels` real, `simules` simulated, `fermee` closed, `echec` failed, `aucune` none) and `variations` (4 values in %, copper, wheat, oil, electricity; `null` without trading). |

## `citoyens[]` (citizens)

| Field | Meaning |
| --- | --- |
| `id` | 1-120 (1-20 Mines, 21-40 Fields… 101-120 City). |
| `region` | Region. |
| `satisfaction`, `colere` (anger), `peur` (fear), `foi` (faith) | 0-255. |
| `etat` (status) | At issue time: `rebelle` (rebel), `censure` (censored), `vote-president` (voted for the president), `ministre`, `president`. |
| `jour` (day) | What happened to them that day: `rebelle`, `censure`, `entre-gouvernement` (joined government), `quitte-gouvernement` (left government), `elu` (elected), `renverse` (toppled), `candidat` (candidate). |

## `langue` (language)

| Field | Meaning |
| --- | --- |
| `motsCommuns` | Number of ideas whose latest count has at least 5 regions agreeing. |
| `idees[]` | For each idea that has appeared: `id`, `fr`, `en`, `motNational` (most shared word), `accord` (regions agreeing, 0-6), `commun` (true if agreement ≥ 5). `motNational` and `accord` are the result of the idea's **latest count** (the last hour in which it was asked and at least 2 regions answered), kept until the next one: they are not the state of the day. |
| `comprehension` | 6 × 6 matrix: understanding between regions, 0-255 (255 on the diagonal). Moving average (step 1/16) updated at each count. |

## `graines` (random seeds, format 2)

The real country's randomness is **not replayable**: at every start-up each board mixes hardware entropy (ESP32 radio noise) into its seed. This block records and dates it; it does not make it replayable. Reproducibility comes from the PC simulator (fixed seeds). Generator: xoshiro128** seeded by splitmix32 (`mcl_rng.h`). Seeds are unsigned 32-bit integers (0 to 4,294,967,295).

| Field | Meaning |
| --- | --- |
| `ere` | Era seed, drawn by the gateway when the era begins (it also sets the names). |
| `passerelle` | Latest known gateway seeds (object below); `null` if unknown. |
| `regions` | 6 objects in the order Mines, Champs, Raffineries, Barrage, Port, Ville: latest seeds announced by each region; `null` if the gateway never received them (region silent since firmware 0.7 was installed, or gateway memory lost). |
| `nouvelles` | **New** seeds received since the previous edition, in order of arrival, with `carte` (`passerelle` or the region's name): a board starting or restarting, a new population (Great Reset), or the first reception after the gateway lost its memory. A repeated announcement is recorded once. |
| `nouvellesNonNotees` | Number of new seeds beyond 24 in a day, counted but not detailed. |

Each seed object: `ere` (era announced by the board; 0 = provisional population of a new board, replaced at the first TICK), `grainePopulation` (regions: seed that created the population of 20 brains; gateway: era seed), `graineHasard` (seed actually given to the generator: when a region restarts, population seed XOR hours lived XOR hardware entropy; when a population is created, the population seed itself), `tick` (country hour when the gateway received it), `tickCarte` (last country hour lived by the board), `utc` (real reception time, `null` if unknown).

## `systeme.notes[]` (system notes)

`tick`, `utc`, `type`, `detail`. Types: `demarrage` (start-up, with the reset cause), `maintenance`, `publication` (a failed upload), `perte` (raw file dropped for lack of space), `version` (firmware 0.7: radio packet from a board running another protocol version, rejected; at most one note per hour), `wifi` (firmware 0.7: connection lost, reconnection attempt by the gateway — the first, then one per hour —, recovery with its duration in minutes, number of attempts and channel). These notes explain gaps in the data; they never fill them.

## Rebuilt files (`donnees/ere-001/reconstitue/`)

Days published before the raw export (9 to 14 October 2026) were rebuilt from the website's issues (`tools/recherche/reconstitue.py`). They carry `"source": "reconstitue"`, `"reconstitue": true`, their origin (website commit) and the method. They contain **only** what the newspaper published: rounded percentages (0-100), mood and rebels per region, market, the day's facts, language. `heures`, `heuresVecues` and `heuresManquantes` are `null`. They have their own manifest and must not be mixed with measured data without saying so.
