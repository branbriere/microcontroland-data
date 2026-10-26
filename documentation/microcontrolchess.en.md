# Microcontrolchess

*Factual sheet, 26 October 2026. Français : [microcontrolchess.md](microcontrolchess.md).*

## What it is
Microcontrolchess is a mini chess game designed for the project: a board of 5 files by 6 ranks, 9 pieces per side, two offensive squares (b3 and d4). Rules in force: **v1.1**, frozen on 25 October 2026.

- Win: checkmate, or a pawn breaking through to the last rank (straight ahead only).
- Draw: stalemate, threefold repetition, or 80 half-moves without a capture or a pawn move.
- Scout pawn: one step forward, or diagonally forward onto an empty square; captures diagonally forward; no diagonal pawn move on the very first move of the game.
- Offensive square: a piece standing there may capture on any of the 8 neighbouring squares.

Arbiter and AI (negamax alpha-beta search, fixed-seed randomness), MIT licence: [engine.js](https://www.microcontroland.org/relique/engine.js). The newspaper site presents the game in satirical form (the “Hall of the Relic”, at the Embassy, from the Age of Diplomacy); this sheet describes the facts only.

## What it is not
- **It is not study data.** No Microcontrolchess game enters any study of the programme.
- **The current Waïnas do not play it.** Their 9-input brains perceive the country's political life, not a board. The box firmware does not contain the game.
- **Visitors' games train nothing.** The game on the site runs in the browser; games are neither recorded nor sent anywhere.

## Possible later use (nothing is decided)
Microcontrolchess may be used to **assess future neural networks** in the project. It has the qualities of a standardised test for that:
- frozen, versioned rules and a public arbiter that rejects any illegal move;
- a ladder of five opponents (levels 1 to 5, search depth 1 to 5) whose strength gaps are measured (below);
- puzzles with a unique solution checked by exhaustive search (45 so far).

If this use is adopted, it will have a pre-registered protocol (hypotheses, measures, controls, thresholds) **before** any data, like the project's other studies. No date is set.

## Balance measurements (simulator, 24 and 25 October 2026)
Independent games between simulator AIs, a distinct seed for each game, sides alternated. Decisive games are counted per side; two-sided binomial test of “the first player wins one decisive game in two”.

| Rules | Levels | First player wins | Second player wins | p |
| --- | --- | --- | --- | --- |
| v1.0 | 4 vs 4 | 72 | 22 | < 0.0001 |
| **v1.1** | 4 vs 4 | 81 | 63 | 0.16 |
| **v1.1** | 3 vs 3 | 41 | 43 | (balanced) |
| **v1.1** | 2 vs 2 | 78 | 54 | 0.045 |

Gaps between levels under v1.1 (stronger against weaker): level 3 vs 2, 42 wins to 5; level 4 vs 3, 35 to 5. One extra step of calculation clearly pays.

Known limits: a slight first-player advantage remains at level 2; level 5 is not a ceiling (the Fairy-Stockfish 14.0.1 engine beat it 6 games to 0 on 25 October 2026). Correction of 25/10: an early series counted some games twice (same seed for both games of a pair); only the corrected figures appear here.
