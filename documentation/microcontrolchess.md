# Microcontrolchess

*Fiche factuelle, 26 octobre 2026. English: [microcontrolchess.en.md](microcontrolchess.en.md).*

## Ce que c'est
Microcontrolchess est un mini-jeu d'échecs conçu pour le projet : plateau de 5 colonnes sur 6 rangées, 9 pièces par camp, deux cases offensives (b3 et d4). Règles en vigueur : **v1.1**, figées le 25 octobre 2026.

- Victoire : mat, ou percée d'un pion sur la dernière rangée (tout droit seulement).
- Nulle : pat, triple répétition, ou 80 demi-coups sans prise ni coup de pion.
- Pion éclaireur : un pas en avant, ou en diagonale avant vers une case vide ; prise en diagonale avant ; pas de pion en diagonale au tout premier coup de la partie.
- Case offensive : la pièce qui s'y trouve peut prendre sur les 8 cases voisines.

Arbitre et IA (recherche negamax alpha-bêta, hasard à graine fixe), licence MIT : [engine.js](https://www.microcontroland.org/relique/engine.js). Le site du journal présente le jeu sous une forme satirique (« Salle de la Relique », à l'Ambassade, à partir de l'âge de la Diplomatie) ; cette fiche-ci ne décrit que les faits.

## Ce que ce n'est pas
- **Ce n'est pas une donnée d'étude.** Aucune partie de Microcontrolchess n'entre dans les études du programme.
- **Les Waïnas actuels n'y jouent pas.** Leur cerveau de 9 entrées perçoit la vie politique du pays, pas un plateau. Le firmware de la boîte ne contient pas le jeu.
- **Les parties des visiteurs ne servent à rien entraîner.** Le jeu du site tourne dans le navigateur ; les parties ne sont ni enregistrées ni envoyées.

## Usage possible plus tard (rien n'est décidé)
Microcontrolchess est peut-être prévu pour **estimer de futurs réseaux neuronaux** du projet. Il a pour cela des qualités d'épreuve standardisée :
- des règles figées et versionnées, et un arbitre public qui refuse tout coup illégal ;
- une échelle de cinq adversaires (niveaux 1 à 5, profondeur de recherche 1 à 5), dont les écarts de force sont mesurés (ci-dessous) ;
- des problèmes à solution unique vérifiée par recherche exhaustive (45 à ce jour).

Si cet usage est retenu, il fera l'objet d'un protocole pré-enregistré (hypothèses, mesures, témoins, seuils) **avant** toute donnée, comme les autres études du projet. Aucune date n'est fixée.

## Mesures d'équilibre (simulateur, 24 et 25 octobre 2026)
Parties indépendantes entre IA du simulateur, une graine distincte par partie, camps alternés. Le nombre de parties décisives est donné par camp ; test binomial bilatéral « le premier joueur gagne une partie décisive sur deux ».

| Règles | Niveaux | Premier joueur gagne | Second joueur gagne | p |
| --- | --- | --- | --- | --- |
| v1.0 | 4 contre 4 | 72 | 22 | < 0,0001 |
| **v1.1** | 4 contre 4 | 81 | 63 | 0,16 |
| **v1.1** | 3 contre 3 | 41 | 43 | (équilibré) |
| **v1.1** | 2 contre 2 | 78 | 54 | 0,045 |

Écarts entre niveaux en v1.1 (le plus fort contre le plus faible) : niveau 3 contre 2, 42 victoires à 5 ; niveau 4 contre 3, 35 à 5. Le jeu récompense donc nettement un cran de calcul en plus.

Limites connues : un léger avantage du premier joueur subsiste au niveau 2 ; le niveau 5 n'est pas un plafond (le moteur Fairy-Stockfish 14.0.1 l'a battu 6 parties à 0 le 25 octobre 2026). Correction du 25/10 : une première série comptait certaines parties deux fois (même graine pour les deux parties d'une paire) ; seuls les chiffres corrigés figurent ici.
