# Artificial-life criteria grid, version 2

*Version 2, approved by the author on 19 October 2026. It replaces version 1 (a draft from the same day). This English version is the reference; the French version (`grille-criteres-v2.md`) is a faithful translation. The numerical threshold of each test will be written down and dated before the first computation; no result has been computed yet.*

## What this grid measures

The grid lists 18 capacities often associated with living systems. For each one, a test on the public data states whether it is **present** (1 point), **partial** (0.5) or **absent** (0). A criterion that cannot be measured yet scores 0 and is shown as "not yet measurable", never as "absent". All 18 criteria carry the same weight. The index is the sum divided by 18.

There is no consensus grid for artificial life. This one is ours: explicit, versioned and open to criticism. A high score would mean "these 18 properties are observed in the data", not "these agents are alive". No grid measures lived experience or consciousness.

## What changed since version 1

Version 2 keeps the same 18 capacities with the same numbers. It tightens the tests after reading seven publications (listed at the end). Three general rules follow.

1. **A control for every effect.** An effect counts only if it exceeds what the programmed rules alone predict (for instance the fixed decay of fear), or if it disappears in a simulator control where the mechanism is switched off.
2. **Behaviour rather than weights.** Two networks can compute the same function with their hidden units in a different order (Stanley & Miikkulainen 2002). Comparisons between citizens, or between parents and offspring, are therefore made on their responses to the same battery of inputs.
3. **What the program imposes scores at most 0.5.** A birth triggered by a rule, or selection on a score written into the program, is not equivalent to reproduction or selection that emerges from the agents themselves (Ray 1991).

## The 18 criteria

| No. | Capacity | Test (version 2) | Measurable with | Ceiling (current design) |
|---|---|---|---|---|
| 01 | Individuality | Citizens of the same region keep different states that are stable over time. | current data | 1 |
| 02 | Perception | After a disaster in a region, fear rises there more than elsewhere. The perceived inputs are chosen by the designer, not acquired by the agents (in Steels's 2015 sense). | current data | 1 |
| 03 | Reactivity | The number of rebels varies with the region's anger and censorship. | current data | 1 |
| 04 | Memory | A past experience changes the present response beyond what the programmed decay of fear alone predicts; then, with exported weights, against a control whose state is reset. | current data, then firmware 0.8 | 1 |
| 05 | Learning | The learning weights change durably, and behaviour differs from a simulator control without learning (same seeds). | firmware 0.8 | 1 |
| 06 | Internal regulation | After a shock, the return to normal is faster than the programmed constants alone predict. | current data | 1 |
| 07 | Decisional autonomy | Decisions are computed by each citizen in its region, with no central draw of the outcome and no human intervention on the decision during the period. | code reading (when the firmware is released) | 1 |
| 08 | Social interactions | The state of one region predicts that of another one hour later, beyond shared events, against a control in which the order of regions is shuffled. | current data | 0.5 (no direct citizen-to-citizen exchange) |
| 09 | Communication | (a) Convention: communicative success and lexical coherence (Steels 2015). (b) Communication in the strong sense: the word heard changes a behaviour (causal influence, Lowe et al. 2019, as summarised by Lazaridou & Baroni 2020). | current data; broadcast agreement with firmware 0.8 | 0.5 (words do not currently enter citizens' decisions) |
| 10 | Cultural transmission | (a) Diffusion: time for a new word to reach 5 regions out of 6; in the simulator, does a reset lexicon recover the existing words? (b) Transmission from one generation to the next. | current data (a); later (b) | 0.5 |
| 11 | Reproduction | Births occur. 1 point only if they depend on the agents' own decisions. | later | 0 (no births at present) |
| 12 | Heredity | Offspring respond like their parents to the same battery of inputs. | later | 0 |
| 13 | Heritable variation | Differences between siblings are passed on to the next generation. With a fixed architecture, only weight variation is possible. | later | 0 |
| 14 | Selection | Inherited traits affect the number of descendants, against a control era without heredity. 1 point only if no selection score is written into the program. | later | 0 |
| 15 | Collective adaptation | The population's average properties change in response to environmental constraints. | firmware 0.8 (learning only), then generations | 0.5 |
| 16 | Open-ended evolution | Lasting novelties appear that were not enumerated in advance. Impossible with a fixed list of concepts and a fixed architecture. | later | 0 |
| 17 | Self-maintenance | The agent actively preserves its own organisation, beyond a programmed gauge. | later | 0 |
| 18 | Causal individuality | Given identical inputs, two citizens decide differently because of their weights. | firmware 0.8 | 1 |

"Ceiling": the highest score possible with the current design of the system, not a result. With the current data the index cannot exceed 7.5 out of 18 (42%); with firmware 0.8, 10 out of 18 (56%).

## Publications read for this version

- Ray, T. S. (1991). An approach to the synthesis of life. *Artificial Life II*, 371-408.
- Stanley, K. O., & Miikkulainen, R. (2002). Evolving neural networks through augmenting topologies. *Evolutionary Computation*, 10(2), 99-127.
- Steels, L. (2015). *The Talking Heads experiment: Origins of words and meanings*. Language Science Press.
- Mordatch, I., & Abbeel, P. (2018). Emergence of grounded compositional language in multi-agent populations. *AAAI*.
- Lazaridou, A., & Baroni, M. (2020). Emergent multi-agent communication in the deep learning era. arXiv:2006.02419.
- Park, J. S., et al. (2023). Generative agents: Interactive simulacra of human behavior. *UIST '23*.
- Banbury, C., et al. (2021). MLPerf Tiny benchmark. arXiv:2106.07597. (Method for measuring energy on microcontrollers; it bears on none of the criteria.)

Found an error, or a test you disagree with? Open an issue on the repository.
