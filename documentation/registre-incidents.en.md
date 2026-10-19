# Incidents and corrections log

[Français](registre-incidents.md) · **English**

This log records the technical incidents that affect the data, and the corrections. Raw files are never modified: this log explains them, it does not replace them. Times are in UTC (Paris time = UTC + 2 in October 2026). A cause is written as established only if it has been verified; otherwise it is marked "not established".

Opened on 19 October 2026. To report an incident or an error: open an issue on the repository.

## Incidents

### INC-001 — Missing region responses, 16 October 2026
- **Period:** ticks 169 to 190 (16 Oct, from 21:00 UTC the day before to 18:00 UTC).
- **Observed in the data:** 43 `null` region-hours in `quotidien/2026-10-16.json`, spread across all six regions. At ticks 180, 182 and 184 (08:00, 10:00 and 12:00 UTC), no region responded. No missing hour (`heuresManquantes` empty); `paquetsPerdus` = 0 in the last hour.
- **Cause:** not established.

### INC-002 — Gateway internet connection lost, 16 October 2026
- **Period:** roughly 15:00 to 17:50 UTC (home internet router failure).
- **Effect:** newspaper edition 8 was built at 18:00 UTC without a connection, then published after the gateway was restarted (website commit at 21:15 UTC). The raw file for 16 Oct, generated at 18:00:05 UTC, was published at 21:16 UTC. The country runs on local radio: no hour is missing from that day's file.
- **Cause:** failure of the internet router, observed by the author.

### INC-003 — Barrage region silent, 16-17 October 2026
- **Period:** from tick 189 (16 Oct, 17:00 UTC) to tick 215 (17 Oct, 19:00 UTC), i.e. 27 consecutive hours. Irregular responses before (ticks 180 to 187). Back at tick 216 (17 Oct, 20:00 UTC), after a manual restart of the board.
- **Observed in the data:** Barrage is `null` for 24 hours out of 24 in `quotidien/2026-10-17.json`. During this period the gateway counts only 5 regions: a word stays shared only if those 5 regions agree. Shared words go from 7 (16 Oct) to 6 (17 Oct).
- **Cause:** not established (the gateway no longer received responses from the board; whether it was off or its messages were lost is unknown).
- **For the studies:** missing responses can delay the stages that depend on the number of shared words.

## Corrections

No correction published so far.
