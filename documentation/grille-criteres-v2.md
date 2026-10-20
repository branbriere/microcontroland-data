# Grille des critères de vie artificielle, version 2

*Version 2, validée par l'auteur le 19 octobre 2026. Elle remplace la version 1 (brouillon du même jour). La version anglaise (`grille-criteres-v2.en.md`) fait référence. Les seuils chiffrés de chaque test seront écrits et datés avant le premier calcul ; aucun résultat n'a encore été calculé.*

## Ce que mesure cette grille

La grille liste 18 aptitudes souvent associées au vivant. Pour chacune, un test sur les données publiques dit si elle est **présente** (1 point), **partielle** (0,5) ou **absente** (0). Un critère qui ne peut pas encore être mesuré compte 0 et s'affiche « pas encore mesurable », jamais « absent ». Les 18 critères ont le même poids. L'indice vaut la somme divisée par 18.

Il n'existe pas de grille consensuelle de la vie artificielle. Celle-ci est la nôtre : explicite, versionnée, ouverte à la critique. Un score élevé voudrait dire « ces 18 propriétés sont observées dans les données », pas « ces agents sont vivants ». Aucune grille ne mesure une expérience vécue ou une conscience.

## Ce qui a changé depuis la version 1

La version 2 garde les mêmes 18 aptitudes, avec les mêmes numéros. Elle durcit les tests après la lecture de sept publications (liste en fin de document). Trois règles générales en sortent.

1. **Un témoin pour chaque effet.** Un effet ne compte que s'il dépasse ce que prédisent les seules règles programmées (par exemple la décroissance fixe de la peur), ou s'il disparaît dans un témoin du simulateur où le mécanisme est coupé.
2. **Le comportement plutôt que les poids.** Deux réseaux peuvent calculer la même chose avec des neurones cachés dans un ordre différent (Stanley & Miikkulainen 2002). Les comparaisons entre citoyens, ou entre parents et enfants, se font donc sur leurs réponses à une même batterie d'entrées.
3. **Ce que le programme impose vaut au plus 0,5.** Une naissance déclenchée par une règle, ou une sélection selon un score écrit dans le programme, ne vaut pas une reproduction ou une sélection qui émerge des agents eux-mêmes (Ray 1991).

## Les 18 critères

| N° | Aptitude | Test (version 2) | Mesurable avec | Plafond (conception actuelle) |
|---|---|---|---|---|
| 01 | Individualité | Les citoyens d'une même région gardent des états différents et stables dans le temps. | données actuelles | 1 |
| 02 | Perception | Après une catastrophe dans une région, la peur y monte plus qu'ailleurs. Les entrées perçues sont choisies par le concepteur, pas acquises par les agents (au sens de Steels 2015). | données actuelles | 1 |
| 03 | Réactivité | Le nombre de rebelles varie avec la colère et la censure de la région. | données actuelles | 1 |
| 04 | Mémoire | Une expérience passée change la réponse présente, au-delà de ce que prédit la seule décroissance programmée de la peur ; puis, avec les poids exportés, contre un témoin dont l'état est remis à zéro. | données actuelles, puis firmware 0.8 | 1 |
| 05 | Apprentissage | Les poids qui apprennent changent durablement, et le comportement diffère d'un témoin du simulateur sans apprentissage (mêmes graines). | firmware 0.8 | 1 |
| 06 | Régulation interne | Après un choc, le retour à la normale est plus rapide que ce que prédisent les seules constantes programmées. | données actuelles | 1 |
| 07 | Autonomie décisionnelle | Les décisions sont calculées par chaque citoyen dans sa région, sans tirage central du résultat et sans intervention humaine sur la décision pendant la période. | lecture du code (à la publication du firmware) | 1 |
| 08 | Interactions sociales | L'état d'une région prédit celui d'une autre l'heure suivante, au-delà des événements communs, contre un témoin où l'ordre des régions est mélangé. | données actuelles | 0,5 (pas d'échange direct de citoyen à citoyen) |
| 09 | Communication | (a) Convention : succès communicatif et cohérence lexicale (Steels 2015). (b) Communication au sens fort : le mot entendu change un comportement (influence causale, Lowe et al. 2019, résumé par Lazaridou & Baroni 2020). | données actuelles ; accord diffusé avec le firmware 0.8 | 0,5 (aujourd'hui, les mots n'entrent pas dans les décisions des citoyens) |
| 10 | Transmission culturelle | (a) Diffusion : temps pour qu'un mot nouveau gagne 5 régions sur 6 ; dans le simulateur, un lexique remis à zéro retrouve-t-il les mots existants ? (b) Transmission d'une génération à la suivante. | données actuelles (a) ; plus tard (b) | 0,5 |
| 11 | Reproduction | Des naissances ont lieu. 1 point seulement si elles dépendent de décisions des agents eux-mêmes. | plus tard | 0 (pas de naissances aujourd'hui) |
| 12 | Hérédité | Les réponses des enfants ressemblent à celles de leurs parents, sur une même batterie d'entrées. | plus tard | 0 |
| 13 | Variation héritable | Des différences entre frères et sœurs se transmettent à la génération suivante. Avec une architecture fixe, seule la variation des poids est possible. | plus tard | 0 |
| 14 | Sélection | Les traits hérités influencent le nombre de descendants, contre une ère témoin sans hérédité. 1 point seulement si aucun score de sélection n'est écrit dans le programme. | plus tard | 0 |
| 15 | Adaptation collective | Les propriétés moyennes de la population changent face aux contraintes du milieu. | firmware 0.8 (apprentissage seul), puis générations | 0,5 |
| 16 | Évolution ouverte | Des nouveautés durables apparaissent, qui n'étaient pas énumérées à l'avance. Impossible avec une liste d'idées et une architecture fixes. | plus tard | 0 |
| 17 | Maintien de soi | L'agent préserve activement son organisation, au-delà d'une jauge programmée. | plus tard | 0 |
| 18 | Individualité causale | À entrées égales, deux citoyens décident différemment à cause de leurs poids. | firmware 0.8 | 1 |

« Plafond » : la note maximale possible avec la conception actuelle du système, pas un résultat. Avec les données actuelles, l'indice ne peut pas dépasser 7,5 sur 18 (42 %) ; avec le firmware 0.8, 10 sur 18 (56 %).

## Publications lues pour cette version

- Ray, T. S. (1991). An approach to the synthesis of life. *Artificial Life II*, 371-408.
- Stanley, K. O., & Miikkulainen, R. (2002). Evolving neural networks through augmenting topologies. *Evolutionary Computation*, 10(2), 99-127.
- Steels, L. (2015). *The Talking Heads experiment: Origins of words and meanings*. Language Science Press.
- Mordatch, I., & Abbeel, P. (2018). Emergence of grounded compositional language in multi-agent populations. *AAAI*.
- Lazaridou, A., & Baroni, M. (2020). Emergent multi-agent communication in the deep learning era. arXiv:2006.02419.
- Park, J. S., et al. (2023). Generative agents: Interactive simulacra of human behavior. *UIST '23*.
- Banbury, C., et al. (2021). MLPerf Tiny benchmark. arXiv:2106.07597. (Méthode de mesure de l'énergie sur microcontrôleur ; ne touche aucun critère.)

Une erreur, un test à contester ? Ouvrez une *issue* sur le dépôt.
