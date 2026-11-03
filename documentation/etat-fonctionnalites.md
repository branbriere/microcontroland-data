# État des fonctionnalités

*[English version](etat-fonctionnalites.en.md)*

**État au 2 novembre 2026, firmware 0.9 (passerelle) et 0.8.1 (régions) en service (installés le 1er novembre).** C'est la référence unique pour savoir si une fonction annoncée sur l'un des deux sites existe. En cas de divergence, ce tableau l'emporte sur les autres pages, et le code l'emporte sur ce tableau. Il est mis à jour à chaque version.

**États :**
- **En service** : la fonction tourne dans la boîte ou sur les sites.
- **Codé, fermé** : le code est dans le firmware en service, mais la fonction ne s'ouvre qu'à un âge que le pays n'a pas encore atteint, ou attend un réglage.
- **Prévu** : rien n'est encore codé, ou le code n'est pas installé. L'ordre et le contenu peuvent changer.

Le firmware n'est pas encore public (il le sera avec les études). D'ici là, la colonne « Où le vérifier » renvoie aux données et aux pages publiques.

## La boîte et les données

| Fonction | État | Depuis | Où le vérifier |
| --- | --- | --- | --- |
| Pays de 120 citoyens sur 6 régions et une passerelle (radio ESP-NOW) | En service | 0.3, 8 oct. 2026 | [architecture.md](architecture.md) |
| Une heure du pays = une heure réelle, à l'heure française | En service | 0.3 | `heures[]` dans chaque fichier brut |
| Cours de bourse réels : taux de la Banque centrale européenne, relevés à 18 h les jours ouvrés | En service | 0.3 | `bourse` dans chaque édition |
| Ce qui entre de l'extérieur : aujourd'hui, seulement les cours de la bourse. Votes comptés et réponses au signal : voir les âges ci-dessous | En service (bourse) | 0.3 | page « Le projet » |
| Météo simulée : tempêtes, épidémies, sécheresses, crises, abondance, tirées au sort par la passerelle | En service | 0.3 | page des règles ; aucune donnée météo réelle |
| Élections tous les 3 jours, ministres, censure, report, révolte, coup de palais, vacance | En service | 0.3 | journal, `data/histoire.json` |
| Foi des citoyens (croyant, agnostique, athée) | En service | 0.3 | journal |
| Langue commune : une idée par heure, oratrice tirée au sort | En service | 0.3 | `data/langue.json` |
| Effet de la langue sur la politique : deux régions qui se comprennent mal se font moins confiance (les électeurs favorisent un candidat d'une région qui « parle comme eux », et une région qui comprend mal la capitale se fâche un peu plus). C'est une règle fixe de la passerelle et des régions. Les mots eux-mêmes ne sont pas des entrées des cerveaux, et leurs décisions n'en dépendent pas directement | En service | 0.3 | `comprehension` dans `data/langue.json` et le fichier brut ; [grille-criteres-v2.md](grille-criteres-v2.md) (critère 09) |
| Apprentissage par récompense des cerveaux (poids renforcés ou affaiblis selon la satisfaction) | En service comme mécanisme ; son effet sur le comportement n'est pas encore démontré (poids exportés chaque jour depuis la 0.8, études à venir) | 0.3 | [grille-criteres-v2.md](grille-criteres-v2.md) |
| Fichier brut quotidien avec manifeste SHA-256 | En service | 0.6, 15 oct. 2026 | [dictionnaire-donnees.md](dictionnaire-donnees.md) |
| Graines du hasard publiées (format 2) | En service | 0.7, 18 oct. 2026 | bloc `graines` du fichier brut |
| Consommation électrique relevée chaque heure (prise locale) | En service | 0.7 | `heures[].prise` |
| Relance Wi-Fi automatique après une coupure | En service | 0.7 | `systeme.notes` (type `wifi`) |
| Publication différée en cas de coupure d'Internet | En service | 0.3 | [registre-incidents.md](registre-incidents.md) |
| Copie du pays hors de la boîte chaque soir | En service | 0.3 | `data/sauvegarde.json` (site du journal) |
| Bouton RESET caché (Grand Reset) | En service | 0.3 | jamais utilisé à ce jour |
| Abstention et chronique électorale | En service depuis le 26 oct. 2026 | 0.8 | `election` du fichier brut ; brève « Chronique électorale » |
| Vote blanc | En service depuis le 27 oct. 2026 | 0.8 | `nouveautes.voteBlanc` du fichier brut |
| Sondages (20 citoyens tirés au sort, à mi-campagne) | En service depuis le 29 oct. 2026 | 0.8 | `sondage` du fichier brut |
| Notoriété (un nom connu rassure dans l'isoloir) | En service depuis le 30 oct. 2026 | 0.8 | `notoriete` du fichier brut (calculée dès la 0.8, sans effet avant l'ouverture) |
| Poids des 120 cerveaux et lexiques complets, une fois par jour | En service | 0.8 | `poids`, `lexiques` du fichier brut |
| Porte-voix de chaque heure, mesures des régions (mémoire, calcul, temps de réponse, température) | En service | 0.8 | `heures[].porteVoix`, `heures[].regions[].systeme` |
| Noms des ministres dans le journal | En service | 0.8 | panneau « État du pays » |
| Sauvegarde du pays au format 4 (champs réservés : généalogie, médecine) | En service | 0.8 | [historique-versions.md](historique-versions.md) |
| Radio renforcée : chaque région envoie son état 4 fois, la passerelle garde sa radio éveillée (environ 13 % d'heures-régions manquantes du 25 oct. au 1er nov.) | En service | 0.8.1 (régions), 0.9 (passerelle), 1er nov. 2026 | `heures[].regions` du fichier brut (`null` = région muette) |
| Fichier brut au format 4 : biographies, nouveautés de la 0.9, événement `w` (mot commun retrouvé) | En service | 0.9, 2 nov. 2026 | [dictionnaire-donnees.md](dictionnaire-donnees.md) |
| Travail, monnaie, école, générations, etc. (mises à jour 2 à 7) | Prévu | — | page des règles, « Ce qui est prévu » |

## Les âges de la civilisation

| Âge | Ce qui s'ouvre | État | Où le vérifier |
| --- | --- | --- | --- |
| Fondation | La gazette | En service depuis le 9 oct. 2026 | journal |
| Parole | La page « La langue » | En service depuis le 18 oct. 2026 | `ages` dans `data/latest.json` |
| Mémoire | La page « Histoire », les records | En service depuis le 24 oct. 2026 | même champ : progression vers l'âge |
| État civil | Adopter un citoyen | En service depuis le 28 oct. 2026 | idem |
| Diplomatie | L'ambassade, ses questions et sa lettre mensuelle | Codé, fermé | idem |
| Diplomatie | Démentis de l'Ambassade dans le journal (coquilles des éditions passées) | Codé (0.5), fermé | idem |
| Diplomatie | Votes du public sur les questions de l'ambassade (simples compteurs) | Codé, fermé, et en attente du service de vote (pas encore choisi) | page des mentions légales |
| Curiosité | Le signal du Centre de recherche et l'écoute des réponses (écrites dans la langue du pays uniquement) | Codé, fermé | idem |

## Le journal

| Fonction | État | Depuis | Où le vérifier |
| --- | --- | --- | --- |
| Journal bilingue écrit par la passerelle, chaque soir à 20 h | En service | 0.3 | `data/editions/N.json` |
| Suivi des personnages (« Que devient… ? », parcours de la semaine) | En service | 0.5 et 0.6 | éditions |
| Rubriques, journalistes citoyens signataires, billet, édition du dimanche | En service | 0.6 | `signature` dans les éditions |
| Presse censurée (articles noircis, jamais les chiffres) | En service | 0.6 | éditions sous censure |
| Biographie de chaque citoyen (16 étapes au plus : le fait, l'heure et l'humeur du moment, jamais la raison), citée par le portrait du dimanche et la page « Mon citoyen » | Codé, s'ouvre le 3 nov. 2026 (une nouveauté par soir) | 0.9 | `biographies` du fichier brut |
| Binaï, le journal des rebelles, en tête de l'édition à partir de la 3e édition consécutive sous censure | Ouvert le 2 nov. 2026 ; ne paraît que sous censure prolongée | 0.9 | `nouveautes.binai` du fichier brut |
| Retour d'un mot commun perdu (ligne de la journée ; brève une édition sur sept au plus) | En service | 0.9 | événement `w` du fichier brut |

## Les sites

| Fonction | État | Depuis | Où le vérifier |
| --- | --- | --- | --- |
| Domaine microcontroland.org (journal sur www, données sur donnees) | En service | 21 oct. 2026 | — |
| Journal lisible sans JavaScript (`journal.txt`, `/texte/`) | En service | 21 oct. 2026 | [journal.txt](https://www.microcontroland.org/journal.txt) |
| Histoire et langue sans JavaScript, robots.txt, plan du site | En service | 21 oct. 2026 | [/texte/](https://www.microcontroland.org/texte/) |
| Page « Découvrir le pays en 5 minutes » (état du pays mis à jour chaque soir) | En service | 21 oct. 2026 | [decouvrir.html](https://www.microcontroland.org/decouvrir.html) |
| Plan statique du site des données | En service | 21 oct. 2026 | [plan.html](https://donnees.microcontroland.org/plan.html) |
| Relevé anonyme des robots qui se déclarent (jour, robot, page, statut ; ni IP ni cookie) | En service | 21 oct. 2026 | export mensuel prévu dans `agents-ia/` |
| Tableau des 18 critères de vie artificielle (grille v2) | En service, états « en attente » | 19 oct. 2026 | [grille-criteres-v2.md](grille-criteres-v2.md) |
| Calcul de l'indice des critères | Prévu : seuils datés avant le premier calcul, affichage à l'âge de la Curiosité | — | idem |
| Salle de la Relique à l'Ambassade (jeu Microcontrolchess contre l'IA, galerie, problème du jour, version texte relique.txt) | Codée, fermée jusqu'à la Diplomatie | 26 oct. 2026 | [microcontrolchess.md](microcontrolchess.md) |
| Office national du tourisme (régions, religion, sites à visiter, pièce collector d'un octet au portrait du président, dépliant PDF FR/EN, version texte tourisme.txt) ; visa virtuel à l'Ambassade | Codé, fermé jusqu'à la Diplomatie | 28 oct. 2026 | [tourisme.txt](https://www.microcontroland.org/tourisme.txt) |
| Page « L'atelier » : art primitif, un dessin 5×5 par soir calculé à partir des poids publiés (règle B3), deux lignes du critique | En service (site seulement, aucun firmware) | 28 oct. 2026 | [atelier.html](https://www.microcontroland.org/atelier.html), [atelier.json](https://www.microcontroland.org/atelier.json) |
| Page « Galerie des présidents » : un portrait par président (diagramme de Hinton des 81 poids publiés de son cerveau de citoyen) et le relevé de chaque mandat ; ouverte à l'âge de la Mémoire | En service (site seulement, aucun firmware) | 28 oct. 2026 | [galerie.html](https://www.microcontroland.org/galerie.html), [galerie.json](https://www.microcontroland.org/galerie.json) |
| Page « Mon citoyen » : historique de chaque citoyen, reconstitué chaque soir à partir des fichiers bruts publiés (faits politiques depuis le 9 oct., candidatures, révolte et censure depuis le 15 oct.), jusqu'au début de sa biographie | En service (site seulement, aucun firmware) | 2 nov. 2026 | [historique.json](https://www.microcontroland.org/data/historique.json) |
| Second portrait « le président » dans la galerie (75 poids du cerveau qui gouverne, export à ajouter au fichier brut) | Prévu, MAJ 1b-5 | — | — |
| Rubrique Arts dans l'édition (même règle, calculée par la passerelle) | Prévu, MAJ 1b-5 | — | — |
| Publication du code du firmware | Prévu, avec les études | — | — |
