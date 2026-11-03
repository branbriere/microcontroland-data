# Relevé des agents IA / AI-agent log

**Français** · [English below](#english)

Ce dossier contient, mois par mois, le nombre de visites des **robots déclarés** (moteurs de recherche, robots d'entraînement, agents qui lisent une page à la demande d'un utilisateur) sur les deux sites de Microcontrôland : `www.microcontroland.org` (journal) et `donnees.microcontroland.org` (données). Ce relevé ne touche ni les cartes ni le firmware du pays.

## Comment c'est mesuré

- Un Worker Cloudflare placé devant les sites reconnaît le nom déclaré du robot (en-tête User-Agent) et ajoute 1 à un compteur par jour × heure × site × robot × page × statut HTTP. Sans IP, sans cookie, sans rien qui identifie une personne. Les visiteurs humains ne sont pas comptés.
- Si le compteur tombe en panne, le site reste servi : la visite est perdue, jamais inventée.
- Début du relevé : 21 octobre 2026 vers 9 h 50 (heure de Paris). Heure de passage enregistrée depuis le 21 octobre 2026, 19 h 18 ; avant, `heure` vaut `null`.
- Un robot qui ne se déclare pas, ou dont le nom n'est pas dans la liste du Worker, n'apparaît pas. L'absence d'un robot ne prouve donc pas qu'il n'est pas venu.

## Fichiers

| Fichier | Contenu |
| --- | --- |
| `AAAA-MM.json` | Export d'un mois terminé, déposé tel que le Worker le fournit. Jamais modifié ensuite. |
| `manifeste.json` | Taille et empreinte SHA-256 de chaque export. |

Champs de chaque ligne : `jour` (AAAA-MM-JJ, heure de Paris), `heure` (0 à 23 ou `null`), `site`, `robot` (nom déclaré), `operateur`, `type` (`entrainement` : collecte pour entraîner un modèle ; `recherche` : index d'un moteur de réponse ; `demande` : lecture à la demande d'un utilisateur ; `moteur` : moteur de recherche classique, groupe témoin), `page`, `statut` (code HTTP), `n` (nombre de visites).

## Visites de test et visites provoquées

Les exports sont bruts : les vérifications de l'installation y sont **comptées** et doivent être retirées avant toute analyse.

| Mois | Lignes à retirer (tests) |
| --- | --- |
| 2026-10 | les 3 lignes `GPTBot` du 2026-10-21, page `/`, n = 2 + 1 + 1 (toutes des tests ; aucun autre passage de GPTBot en octobre) |

Des visites réelles ont aussi été **provoquées** par l'auteur ou ses proches (questions posées à ChatGPT, Mistral ou Claude pour vérifier la lecture des sites, notamment le 21 octobre 2026). Elles sont gardées et signalées : jours concernés en octobre 2026 : 21, 22 et 23 (ChatGPT-User, MistralAI-User, Claude-User).

## Ce que ces données ne disent pas

Ce sont des comptages de requêtes. Ils ne disent rien de l'intention ni de la « curiosité » d'un système : on écrit « a suivi le lien », jamais « s'est intéressé à ».

---

## English

This folder holds, month by month, the number of visits by **declared robots** (search engines, training crawlers, agents fetching a page at a user's request) to the two Microcontrôland sites: `www.microcontroland.org` (newspaper) and `donnees.microcontroland.org` (data). This log does not touch the country's boards or firmware.

## How it is measured

- A Cloudflare Worker in front of the sites recognises the robot's declared name (User-Agent header) and adds 1 to a counter per day × hour × site × robot × page × HTTP status. No IP, no cookie, nothing that identifies a person. Human visitors are not counted.
- If the counter fails, the site is still served: the visit is lost, never invented.
- Log start: 21 October 2026 around 09:50 (Paris time). Hour of visit recorded since 21 October 2026, 19:18; before that, `heure` is `null`.
- A robot that does not declare itself, or whose name is not in the Worker's list, does not appear. A robot's absence does not prove it did not visit.

## Files

| File | Contents |
| --- | --- |
| `AAAA-MM.json` | Export of a completed month, filed as served by the Worker. Never modified afterwards. |
| `manifeste.json` | Size and SHA-256 checksum of each export. |

Fields of each row: `jour` (day, YYYY-MM-DD, Paris time), `heure` (hour, 0-23 or `null`), `site`, `robot` (declared name), `operateur` (operator), `type` (`entrainement`: crawling to train a model; `recherche`: answer-engine index; `demande`: fetch at a user's request; `moteur`: classic search engine, control group), `page`, `statut` (HTTP status), `n` (number of visits).

## Test visits and prompted visits

Exports are raw: installation checks are **counted** in them and must be removed before any analysis.

| Month | Rows to remove (tests) |
| --- | --- |
| 2026-10 | the 3 `GPTBot` rows of 2026-10-21, page `/`, n = 2 + 1 + 1 (all tests; no other GPTBot visit in October) |

Some real visits were also **prompted** by the author or people close to the author (questions put to ChatGPT, Mistral or Claude to check how the sites are read, notably on 21 October 2026). They are kept and flagged: days concerned in October 2026: 21, 22 and 23 (ChatGPT-User, MistralAI-User, Claude-User).

## What these data do not say

These are request counts. They say nothing about a system's intent or "curiosity": we write "followed the link", never "took an interest in".
