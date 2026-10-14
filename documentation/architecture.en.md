# Microcontrôland architecture

*[Version française](architecture.md)* · Documentation version: firmware 0.6 (update 1b-2), 14 October 2026

## Overview

Microcontrôland runs on **7 ESP32-S3 boards** talking over radio (ESP-NOW), with no cables between them.

| Board | Role |
| --- | --- |
| Gateway (ESP32-S3 N16R8) | Country clock, politics (elections, government, revolts), market, language, writing the newspaper, publishing online. |
| 6 regions (Mines, Fields, Refineries, Dam, Harbour, City) | 20 citizens each. Every citizen is a small neural network (81 connections) that decides, learns and remembers. |

**One country hour lasts one real hour** and follows French time. Every hour the gateway sends a "TICK" to the regions; each region runs its citizens and answers with its state (satisfaction, fear, anger, rebels, believers, production, the word it proposes for the current idea).

## What is not scripted

No event is written in advance. Elections, revolts, shared words and beliefs come from the citizens' decisions. The gateway applies **fixed rules** (published on the website, "Rules" page); it does not choose outcomes.

## A day's cycle

1. **Every hour**: TICK → regions answer → the gateway updates the country and records the hour in a raw-data buffer (copied to flash so it survives a restart).
2. **6 pm**: real exchange rates from the European Central Bank (4 currencies of producer countries, measured in dollars). Weekends and holidays: market closed.
3. **8 pm**: the gateway writes the issue of *La Puce Libre* (French and English) and the **day's raw file**.
4. **Publishing**:
   - the newspaper goes to the website in **a single commit** (GitHub Git Data API);
   - then the raw file and the manifest go to this repository, in a separate commit. A failure here never blocks the newspaper: it retries every hour.

## Facts, interpretations, hypotheses

| Layer | Where | Nature |
| --- | --- | --- |
| Facts | `donnees/…/quotidien/` | Board measurements, raw 0-255 scale, missing values = `null`. |
| Interpretation | The newspaper, the Embassy | Narrative written by the gateway from the facts. A president may censor it (the figures in the "State of the nation" panel never are). |
| Hypotheses | `protocoles/`, `etudes/` | Questions asked by studies, filed before analysis. |

## The newsroom (since update 1b-2)

Four citizens run the sections (politics, economy, society, humour column). They sign their pieces, with a style drawn from their character that day. A journalist who becomes president or minister leaves the newsroom; a rebel stays. When a president censors at least 6 citizens, politics is handed to a palace-approved correspondent, some figures in the articles are replaced by "████" and a banner warns the reader. When censorship ends, "What we could not write" is published. The newsroom state is saved separately and is not part of the raw data.

## Hardware and safety

- Gateway: outbound only (Internet), plus wireless updates on the local network. No port open to the Internet.
- Country backup: hourly in flash, every evening on the website (`data/sauvegarde.json`).
- Automatic weekly restart around 4 am; 3-minute watchdog.
- Text from the public never enters the country as is (votes are counted, answers filtered by the country's language).

## Source code

Firmware (C++/Arduino): country logic in `lib/mcl_core`, hardware in `src/`. The same core runs on a PC for tests (multi-year simulation, official SHA-256 vectors, mock GitHub server). MIT licence.
