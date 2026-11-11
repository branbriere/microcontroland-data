# Data dictionary

*[Version française](dictionnaire-donnees.md)* · Daily file format: **4** (firmware 0.9, from 2 November 2026, subject to the installation on 1 November); format **3** (firmware 0.8) from 26 October to 1 November 2026; format **2** (firmware 0.7) from 19 to 25 October 2026; format **1** (firmware 0.6) from 15 to 18 October 2026

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
| `format` | integer | Format version (1; 2 from firmware 0.7, which adds `graines` and `heures[].prise`; 3 from firmware 0.8, which adds `heures[].porteVoix`, the regions' measurements, `poids`, `lexiques`, `election`, `sondage`, `nouveautes`, `notoriete` and `langue.idees[].depouilleTick`; 4 from firmware 0.9, which adds `biographies` and two new features; 5 from firmware 0.10, which adds `poidsPresident` and `nouveautes.arts`). |
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
| `poids` (weights) | object | Format 3: the 81 weights of each of the 120 brains, frozen at the start of the day (see below). |
| `lexiques` (lexicons) | list of 6 | Format 3: each region's word for all 48 ideas, frozen at the same moment (see below). |
| `election` | object / null | Format 3: detail of the latest vote if it took place that calendar day, otherwise `null` (see below). |
| `sondage` (poll) | object / null | Format 3: poll taken that day, otherwise `null` (see below). |
| `nouveautes` (new rules) | object | Format 3: firmware 0.8 electoral features open at the time of the issue (`abstention`, `voteBlanc` blank vote, `sondages` polls, `notoriete` fame; true or false; format 4: also `binai`, the rebels' newspaper, and `biographies`; format 5: also `arts`, the issue's Arts section). They open one per evening; while a rule is closed, its behaviour does not exist (no abstention is possible before `abstention`). |
| `notoriete` (fame) | list of 120 | Format 3: each citizen's fame (0-255), in id order. Computed every evening by the gateway (roles and the day's events, about 3% forgotten per day); it only influences the vote once `nouveautes.notoriete` is open. |
| `systeme` | object | `notes`: technical events (see below). |

## `heures[]` (hours)

| Field | Meaning |
| --- | --- |
| `tick` | Country-hour number. |
| `heure` | French clock hour (0-23). |
| `utc` | Real UTC time of the record, or `null` (no Internet time). |
| `regions` | 6 entries in the order Mines, Fields, Refineries, Dam, Harbour, City; `null` if the region did not answer that hour. |
| `idee` | The idea the regions proposed a word for that hour: `id`, `fr`, `en`. `null` if none. |
| `porteVoix` (speaker) | Format 3: the hour's lesson. `idee` (id), `oratrice` (region drawn by lot, which the others learn from), `motDiffuse` (`syllabes`, `ecrit`: the word it said) and `accordDiffuse` (regions agreeing with that word, 0-6). `null` if there was no lesson that hour (fewer than 2 regions, no idea). |
| `prise` | Format 2: reading of the Shelly smart plug that powers the whole country, taken by the gateway right after the hour's radio round, on the local network. `puissanceW` (instantaneous power, W) and `compteurWh` (the plug's cumulative energy counter, Wh), 3 decimals. Average consumption between two hours = difference of `compteurWh` / duration. `null` if the plug did not answer. The counter restarts from zero if the plug is reset: a decreasing counter signals a reset, not negative consumption. |
| `systeme` | `memoireLibre` (free heap), `psramLibre` (free PSRAM, bytes), `dureeHeureMs` (radio round time), `paquetsPerdus` (packets received but discarded because the gateway's receive queue was full, since the previous hour; this is not the number of silent regions, which is read from `regions`), `temperatureC` (format 3: the gateway chip's internal sensor, °C, accurate to a few degrees; `null` if unreadable); `null` if not measured. |

### `heures[].regions[]`

| Field | Scale | Meaning |
| --- | --- | --- |
| `cerveaux` | 0-20 | Active citizens (brains). |
| `satisfaction`, `peur` (fear), `colere` (anger) | 0-255 | Region averages. |
| `rebelles` (rebels), `censures` (censored), `croyants` (believers), `athees` (atheists) | 0-20 | Number of citizens. |
| `production`, `objectif` (target) | raw | Region output and its target. |
| `mot` (word) | object / null | Word proposed for the hour's idea: `syllabes` (indices), `ecrit` (written form). |
| `systeme` | object / null | Format 3: measurements from the region's board. `memoireLibre` (free heap, bytes), `calculMs` (time to compute the hour for the 20 brains, ms, rounded), `reponseMs` (delay between the gateway sending the hour and receiving the region's reply: radio + computation + the region's waiting slot, ms; `null` if not measured), `temperatureC` (chip's internal sensor, °C, `null` if unreadable). |

## `evenements[]` (events)

| Field | Meaning |
| --- | --- |
| `tick`, `heure` | When it happened. |
| `type` | Letter: `e` election · `o` campaign/poll opening · `c` revolt · `k` palace coup · `b` regime change · `p` election postponed · `m` government · `s` censorship · `v` region unreachable · `x` market · `n` nature (storm, epidemic, harvest…) · `f` faith · `W` shared word (first time) · `w` shared word regained, `a` = the idea (format 4, firmware 0.9: the idea had a shared word, lost it, and has one again, which may be a different word) · `a` new age · `R` record · `l` ambassador's letter · `S` signal sent · `g` signal received · `q` listening · `r` era start · `u` new feature opened (format 3; `sous`: 0 abstention, 1 blank vote, 2 polls, 3 fame; format 4: 4 Binaï, 5 biographies; format 5: 6 Arts section) · `P` poll (format 3; `a` leading candidate, `b` their share in %, `c` people asked). |
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
| `idees[]` | For each idea that has appeared: `id`, `fr`, `en`, `motNational` (most shared word), `accord` (regions agreeing, 0-6), `commun` (true if agreement ≥ 5). `motNational` and `accord` are the result of the idea's **latest count** (the last hour in which it was asked and at least 2 regions answered), kept until the next one: they are not the state of the day. Format 3: `depouilleTick`, the country hour (`tick`) of that latest count, so the age of the value can be read; `null` if the idea has not been counted since firmware 0.8 was installed. |
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

`tick`, `utc`, `type`, `detail`. Types: `migration` (firmware 0.8: country save converted from format 3 to format 4, once, at installation), `temperature` (firmware 0.8: gateway chip above 70 °C), `demarrage` (start-up, with the reset cause), `maintenance`, `publication` (a failed upload), `perte` (raw file dropped for lack of space), `version` (firmware 0.7: radio packet from a board running another protocol version, rejected; at most one note per hour), `wifi` (firmware 0.7: connection lost, reconnection attempt by the gateway — the first, then one per hour —, recovery with its duration in minutes, number of attempts and channel). `biographies` (firmware 0.9: biography record missing, damaged or behind the country at start-up, restarted from the Archives). These notes explain gaps in the data; they never fill them.

## `poids` and `lexiques` (weights and lexicons, format 3)

At the first hour of each day, every region freezes the weights of its 20 brains and its word for all 48 ideas, then sends them to the gateway in 9 pieces, one per hour, after its reply (lost pieces are sent again in the following hours). Nothing in the life of the country depends on this record.

| Field | Meaning |
| --- | --- |
| `poids.echelle` | Conversion: real weight = value × 5 / 127 (weights are bounded to ± 5 and rounded to a signed byte, -127 to 127). |
| `poids.regions` | 6 entries in region order: `tick` (country hour at which the record was frozen) and `citoyens`, 20 lists of 81 integers in the order of the region's ids; `null` if the region's record is incomplete at the time of the issue (silent region, restarted during the day). Never padded with zeros. |
| `lexiques` | 6 entries: 48 words (`syllabes`, `ecrit`), one per idea in idea-id order, **all 48 without exception** (a region does not know which ideas the country has lived through; `langue.idees` says so); `null` as for `poids`. |

Order of a brain's 81 weights (network of 9 inputs → 6 hidden neurons → 3 outputs): first the hidden layer, neuron by neuron (9 input weights then the bias, i.e. 6 × 10), then the output layer, output by output (6 hidden-neuron weights then the bias, i.e. 3 × 7). Inputs: perceived performance of the president, satisfaction, fear, anger, ego, charisma, ambition, the president's charisma, threat. Outputs: support for the president, wish to stand as a candidate, wish to rebel.

## `poidsPresident` (format 5)

The governing brain (network of 8 inputs → 5 hidden neurons → 5 outputs, 75 weights) of the president in office at the time of the morning record, frozen by their region together with the other weights and sent in the same 9 chunks. This brain is only used during the term, and it learns during the term. `null`: no president that morning, the region's record incomplete, or the region still on 0.8.1. Never filled in with zeros.

| Field | Content |
| --- | --- |
| `id` | The president's identifier at the time of the record (it may have changed before the issue: compare with `pays.president`). |
| `region` | Region that sent the record (0 to 5). |
| `tick` | Country hour at which the record was frozen. |
| `reseau`, `ordre` | "8-5-5"; weight order: hidden layer, neuron by neuron (8 inputs then the bias, 5 × 9), then outputs, output by output (5 hidden neurons then the bias, 5 × 6). |
| `poids` | 75 integers, same scale as `poids` (value × 5 / 127). |

Inputs: actual performance, average anger, average fear, time to the election, ego, size of the government, outside hostility (reserved), resources. Outputs: fairness, repression, wish to postpone, openness of the government, hostility (reserved).

## `election` (format 3)

| Field | Meaning |
| --- | --- |
| `heure` | French time of the count. |
| `inscrits` (registered) | 20 × regions counted. |
| `exprimes`, `abstentions`, `blancs` | Ballots for a candidate, citizens who stayed at home, blank ballots. Voters = `exprimes` + `blancs`. Each candidate's percentage is computed on `exprimes` (valid votes). |
| `abstentionPermise`, `blancPermis` | Rules in force that day. |
| `candidats[]` | `id`, `nom`, `region`, `voix` (votes), `pct`. |
| `regions` | 6 entries: `voix` (one per candidate, in `candidats` order), `abstentions`, `blancs`; `null` if the region was not counted. |
| `sondage` | Present if a poll covered this vote (less than 48 h before, same candidates): each candidate's published share, in %. |

Presidents, ministers and candidates always vote; only ordinary citizens may abstain or vote blank.

## `sondage` (poll, format 3)

Halfway through the campaign, the gateway draws 20 answers by lot, without replacement, from the citizens of the regions answering that hour.

| Field | Meaning |
| --- | --- |
| `tick`, `heure` | Time of the poll. |
| `interroges` | People drawn (20, fewer if few regions answer). |
| `regionsRepondantes` | Size of the population that could be asked (citizens of the regions that answered). |
| `candidats[]` | `id`, `reponses` (in the sample), `pct` (published share, in % of answers for a candidate), `veritePct` (what the whole askable population really thought at that moment, in %). The gap between `pct` and `veritePct` is the sampling error. |
| `abstentions`, `blancs` | Answers in the sample. |

The least self-assured voters may follow the poll published on polling day: its effect is measured by comparing `veritePct` with the result.

## `biographies` (format 4)

Firmware 0.9 (update 1b-4). For each citizen the gateway keeps a record of at most 16 life steps, published on the website ("My citizen" page, from the age of the Civil Registry). The daily file gives the steps **added since the previous issue**.

| Field | Description |
|---|---|
| `depuis` (since) | Date (YYYY-MM-DD) from which every step is recorded. |
| `amorce` (seeded) | `naissance` (birth): record started at the beginning of the era; `archives`: record (re)started during the era from what the Archives knew (firmware installation, record lost or behind the country after a rollback). What happened before `depuis` is not recorded, except the `ARCHIVES` step. |
| `etapesRetirees` (steps removed) | Total number of steps removed from full records since `depuis` (birth and the last 2 steps stay; the least notable goes first). The daily files keep every step ever published. |
| `nouvelles[]` (new) | `id` (citizen) and `etape` (step), an array `[day, hour, type, times, context, satisfaction, anger, fear, a]`. |

In `etape`: `day` = day of the era; `hour` 0-23 (`null` for birth and Archives); `times` = how many times this has happened to this citizen (kept even when a repetition replaces the previous one in the record); `satisfaction`, `anger`, `fear` in % at the time of the step (`null` if unknown).

`type`: 1 born (`a` = region) · 2 Archives (`a` = flags: 1 former president, 2 toppled by a revolution, 4 betrayed, 8 led a coup, 16 sacked, 32 voted out, 64 former minister; `times` = spells in power) · 3 joins the rebellion (after 3 hours in a row) · 4 leaves it (after 24 calm hours) · 5 censored · 6 candidate · 7 elected (`a` = % of the vote, + 256 if re-elected) · 8 toppled (`a` 1 revolution, 2 palace coup) · 9 led a palace coup · 10 voted out · 11 joins the government (`a` = president) · 12 leaves the government (`a` 1 = sacked) · 13 joins the paper (`a` = desk 0-3) · 14 leaves the paper (`a` mod 256: 1 government, 2 palace, 3 rebellion) · 15 record for the longest reign.

`context` (bits): 1 storm in their region · 2 epidemic in their region · 4 censorship in force · 8 polling day · 16 revolution or palace coup that hour · 32 shortage. This is what was happening **at the same time**, as measured by the gateway: never a cause. The paper writes "while", never "because".

## Rebuilt files (`donnees/ere-001/reconstitue/`)

Days published before the raw export (9 to 14 October 2026) were rebuilt from the website's issues (`tools/recherche/reconstitue.py`). They carry `"source": "reconstitue"`, `"reconstitue": true`, their origin (website commit) and the method. They contain **only** what the newspaper published: rounded percentages (0-100), mood and rebels per region, market, the day's facts, language. `heures`, `heuresVecues` and `heuresManquantes` are `null`. They have their own manifest and must not be mixed with measured data without saying so.
