# Dictionnaire des données

*[English version](dictionnaire-donnees.en.md)* · Format des fichiers quotidiens : **4** (firmware 0.9, à partir du 2 novembre 2026, sous réserve de l'installation du 1er novembre) ; format **3** (firmware 0.8) du 26 octobre au 1er novembre 2026 ; format **2** (firmware 0.7) du 19 au 25 octobre 2026 ; format **1** (firmware 0.6) du 15 au 18 octobre 2026

## Règles générales

- **Un fichier par jour** : `donnees/ere-NNN/quotidien/AAAA-MM-JJ.json`, écrit par la passerelle à 20 h, publié juste après le journal, **jamais modifié ensuite**.
- **Échelle brute** : les grandeurs d'humeur des citoyens et des régions vont de **0 à 255** (255 = maximum). Les moyennes du pays sont données en **millièmes** (0 à 1000).
- **`null` = absent** (région muette, heure perdue, valeur inconnue). Jamais remplacé par 0.
- **Heures** : `tick` est le numéro de l'heure du pays depuis le début de l'ère (1, 2, 3…). Il sert à comparer réel et simulation en heures vécues, pas en jours de calendrier.
- **Vérification** : chaque fichier figure dans `donnees/ere-NNN/manifeste.json` avec sa taille en octets et son empreinte SHA-256 (`sha256sum fichier.json`).
- Les noms de champs sont en français ; les textes sont en français et en anglais (`fr`, `en`).

## Racine du fichier

| Champ | Type | Sens |
| --- | --- | --- |
| `format` | entier | Version du format (1 ; 2 depuis le firmware 0.7, qui ajoute `graines` et `heures[].prise` ; 3 depuis le firmware 0.8, qui ajoute `heures[].porteVoix`, les mesures des régions, `poids`, `lexiques`, `election`, `sondage`, `nouveautes`, `notoriete` et `langue.idees[].depouilleTick` ; 4 depuis le firmware 0.9, qui ajoute `biographies` et deux nouveautés ; 5 depuis le firmware 0.10, qui ajoute `poidsPresident` et `nouveautes.arts`). |
| `source` | texte | `passerelle` (mesuré) ; `reconstitue` pour les jours rebâtis après coup (dossier `reconstitue/`). |
| `firmware` | texte | Version du programme de la passerelle, ex. `0.6`. |
| `parametres` | objet | `heureDuPaysMs` (durée d'une heure du pays en ms), `regions`, `citoyensParRegion`, `connexionsParCerveau`, `idees` (nombre d'idées du lexique), `seuilMotCommun` (régions qui doivent s'accorder pour qu'un mot soit commun), `echelle` (255). |
| `ere` | entier | Numéro de l'ère (un « Grand Reset » ouvre une nouvelle ère). |
| `date` | texte | Date française de l'édition (AAAA-MM-JJ). |
| `jourEre` | entier | Jour de l'ère. |
| `edition` | entier | Numéro de l'édition du journal du même soir. |
| `heuresVecues` | entier | Heures du pays vécues depuis le début de l'ère, au moment de l'édition. |
| `genereUtc` | texte / null | Heure UTC d'écriture du fichier (ISO 8601). |
| `heures` | liste | Une entrée par heure enregistrée depuis l'édition précédente (voir ci-dessous). |
| `heuresManquantes` | liste / null | `tick` des heures attendues mais absentes (redémarrage, coupure). `null` si le début de la journée est inconnu (premier fichier après un démarrage). |
| `evenements` | liste | Les faits du jour notés par la passerelle. |
| `pays` | objet | État du pays au moment de l'édition. |
| `citoyens` | liste de 120 | Un objet par citoyen (ou `null` si sa région n'a jamais répondu). |
| `langue` | objet | État de la langue commune. |
| `journal` | objet | Renvoi vers l'édition (interprétation) : `edition`, `fichier` (chemin sur le site). |
| `graines` | objet | Graines du hasard (format 2, voir plus bas). Absent des fichiers au format 1. |
| `poids` | objet | Format 3 : les 81 poids de chacun des 120 cerveaux, figés au début du jour (voir plus bas). |
| `lexiques` | liste de 6 | Format 3 : le mot de chaque région pour les 48 idées, figé au même moment (voir plus bas). |
| `election` | objet / null | Format 3 : détail du dernier scrutin s'il a eu lieu ce jour-là (date du calendrier), sinon `null` (voir plus bas). |
| `sondage` | objet / null | Format 3 : sondage réalisé ce jour-là, sinon `null` (voir plus bas). |
| `nouveautes` | objet | Format 3 : nouveautés électorales du firmware 0.8 ouvertes à l'édition (`abstention`, `voteBlanc`, `sondages`, `notoriete`, vrai ou faux ; format 4 : aussi `binai`, le journal des rebelles, et `biographies` ; format 5 : aussi `arts`, la rubrique Arts de l'édition). Elles s'ouvrent une par soir ; tant qu'une règle est fermée, son comportement n'existe pas (aucune abstention possible avant `abstention`). |
| `notoriete` | liste de 120 | Format 3 : notoriété de chaque citoyen (0-255), dans l'ordre des identifiants. Calculée chaque soir par la passerelle (rôles et faits du jour, oubli d'environ 3 % par jour) ; elle n'influence le vote qu'une fois `nouveautes.notoriete` ouverte. |
| `systeme` | objet | `notes` : événements techniques (voir plus bas). |

## `heures[]`

| Champ | Sens |
| --- | --- |
| `tick` | Numéro de l'heure du pays. |
| `heure` | Heure française (0-23). |
| `utc` | Heure UTC réelle de l'enregistrement, ou `null` (heure Internet indisponible). |
| `regions` | 6 entrées dans l'ordre Mines, Champs, Raffineries, Barrage, Port, Ville ; `null` si la région n'a pas répondu cette heure-là. |
| `idee` | L'idée sur laquelle les régions ont proposé un mot cette heure-là : `id`, `fr`, `en`. `null` si aucune. |
| `porteVoix` | Format 3 : la leçon de l'heure. `idee` (identifiant), `oratrice` (région tirée au sort, dont les autres apprennent), `motDiffuse` (`syllabes`, `ecrit` : le mot qu'elle a dit) et `accordDiffuse` (régions d'accord avec ce mot, 0-6). `null` si aucune leçon cette heure-là (moins de 2 régions, pas d'idée). |
| `prise` | Format 2 : relevé de la prise Shelly qui alimente tout le pays, lu par la passerelle juste après la tournée radio de l'heure, sur le réseau local. `puissanceW` (puissance instantanée, W) et `compteurWh` (compteur d'énergie cumulé de la prise, Wh), 3 décimales. La consommation moyenne entre deux heures = écart de `compteurWh` / durée. `null` si la prise n'a pas répondu. Le compteur repart de zéro si la prise est réinitialisée : un compteur qui baisse signale une remise à zéro, pas une consommation négative. |
| `systeme` | `memoireLibre`, `psramLibre` (octets), `dureeHeureMs` (temps de la tournée radio), `paquetsPerdus` (paquets reçus mais jetés faute de place dans la file de réception de la passerelle, depuis l'heure précédente ; ce n'est pas le nombre de régions muettes, qui se lit dans `regions`), `temperatureC` (format 3 : capteur interne de la puce de la passerelle, °C, précision de quelques degrés ; `null` si illisible) ; `null` si non mesuré. |

### `heures[].regions[]`

| Champ | Échelle | Sens |
| --- | --- | --- |
| `cerveaux` | 0-20 | Citoyens actifs. |
| `satisfaction`, `peur`, `colere` | 0-255 | Moyennes de la région. |
| `rebelles`, `censures`, `croyants`, `athees` | 0-20 | Nombre de citoyens. |
| `production`, `objectif` | brut | Production de la région et objectif fixé. |
| `mot` | objet / null | Mot proposé pour l'idée de l'heure : `syllabes` (indices), `ecrit` (forme écrite). |
| `systeme` | objet / null | Format 3 : mesures de la carte de la région. `memoireLibre` (octets), `calculMs` (durée du calcul de l'heure pour les 20 cerveaux, ms, arrondie), `reponseMs` (délai entre l'envoi de l'heure par la passerelle et la réception de la réponse de la région : radio + calcul + créneau d'attente de la région, ms ; `null` si non mesuré), `temperatureC` (capteur interne de la puce, °C, `null` si illisible). |

## `evenements[]`

| Champ | Sens |
| --- | --- |
| `tick`, `heure` | Moment de l'événement. |
| `type` | Lettre : `e` élection · `o` ouverture de campagne/scrutin · `c` révolte · `k` coup de palais · `b` bascule de régime · `p` report d'élection · `m` gouvernement · `s` censure · `v` région injoignable · `x` bourse · `n` nature (tempête, épidémie, récolte…) · `f` foi · `W` mot commun (première fois) · `w` mot commun retrouvé, `a` = l'idée (format 4, firmware 0.9 : l'idée avait eu un mot commun, l'avait perdu, et en retrouve un, qui peut être un autre mot) · `a` nouvel âge · `R` record · `l` lettre de l'ambassadeur · `S` signal émis · `g` signal reçu · `q` écoute · `r` début d'ère · `u` nouveauté ouverte (format 3 ; `sous` : 0 abstention, 1 vote blanc, 2 sondages, 3 notoriété ; format 4 : 4 Binaï, 5 biographies ; format 5 : 6 rubrique Arts) · `P` sondage (format 3 ; `a` candidat en tête, `b` sa part en %, `c` personnes interrogées). |
| `sous`, `a`, `b`, `c`, `d` | Paramètres bruts de l'événement (identifiants de citoyens, régions, valeurs). |
| `texte` | Phrase du carnet, `fr` et `en` (non censurée). |

## `pays`

| Champ | Sens |
| --- | --- |
| `president` | Identifiant du président (1-120), `null` si vacance. |
| `capitale` | Région du président, `null` si vacance. |
| `regime` | Démocratie, Démocratie fragile, Oligarchie, Autocratie, Junte, Dictature, Agitation révolutionnaire. |
| `ministres` | Identifiants des ministres. |
| `objectifAtteint`, `ressources` | Millièmes (0-1000). |
| `satisfactionMoyenne`, `peurMoyenne`, `colereMoyenne` | Millièmes (0-1000). |
| `rebelles` | Rebelles dans les régions qui ont répondu. |
| `croyantsPct`, `atheesPct` | Pourcentages. |
| `age` | Âge de la civilisation atteint (0 = Fondation). |
| `elections`, `revolutions`, `coupsDePalais`, `reports` | Compteurs depuis le début de l'ère. |
| `bourse` | `statut` (`reels`, `simules`, `fermee`, `echec`, `aucune`) et `variations` (4 valeurs en %, cuivre, blé, pétrole, électricité ; `null` si pas de cotation). |

## `citoyens[]`

| Champ | Sens |
| --- | --- |
| `id` | 1-120 (1-20 Mines, 21-40 Champs… 101-120 Ville). |
| `region` | Région. |
| `satisfaction`, `colere`, `peur`, `foi` | 0-255. |
| `etat` | Situation au moment de l'édition : `rebelle`, `censure`, `vote-president`, `ministre`, `president`. |
| `jour` | Ce qui lui est arrivé dans la journée : `rebelle`, `censure`, `entre-gouvernement`, `quitte-gouvernement`, `elu`, `renverse`, `candidat`. |

## `langue`

| Champ | Sens |
| --- | --- |
| `motsCommuns` | Nombre d'idées dont le dernier dépouillement donne au moins 5 régions d'accord. |
| `idees[]` | Pour chaque idée apparue : `id`, `fr`, `en`, `motNational` (mot le plus partagé), `accord` (régions d'accord, 0-6), `commun` (vrai si accord ≥ 5). `motNational` et `accord` sont le résultat du **dernier dépouillement** de l'idée (dernière heure où elle a été demandée et où au moins 2 régions ont répondu), conservé ensuite : ce n'est pas l'état du jour. Format 3 : `depouilleTick`, l'heure du pays (`tick`) de ce dernier dépouillement, pour lire l'âge de la valeur ; `null` si l'idée n'a pas été dépouillée depuis l'installation du firmware 0.8. |
| `comprehension` | Matrice 6 × 6 : compréhension entre régions, 0-255 (255 sur la diagonale). Moyenne mobile (pas de 1/16) mise à jour à chaque dépouillement. |

## `graines` (format 2)

Le hasard du pays réel n'est **pas rejouable** : chaque carte mélange un aléa matériel (bruit radio de l'ESP32) à sa graine à chaque démarrage. Ce bloc le trace et le date, sans permettre de le rejouer. La reproductibilité passe par le simulateur sur PC (graines fixes). Générateur : xoshiro128** initialisé par splitmix32 (`mcl_rng.h`). Les graines sont des entiers non signés de 32 bits (0 à 4 294 967 295).

| Champ | Sens |
| --- | --- |
| `ere` | Graine de l'ère, tirée par la passerelle au début de l'ère (elle fixe aussi les prénoms). |
| `passerelle` | Dernières graines connues de la passerelle (objet ci-dessous) ; `null` si inconnues. |
| `regions` | 6 objets dans l'ordre Mines, Champs, Raffineries, Barrage, Port, Ville : dernières graines annoncées par chaque région ; `null` si la passerelle ne les a jamais reçues (région muette depuis l'installation du firmware 0.7, ou mémoire de la passerelle perdue). |
| `nouvelles` | Graines **nouvelles** reçues depuis l'édition précédente, dans l'ordre d'arrivée, avec `carte` (`passerelle` ou nom de la région) : démarrage ou redémarrage d'une carte, nouvelle population (Grand Reset), ou première réception après une perte de mémoire de la passerelle. Une même annonce répétée n'est notée qu'une fois. |
| `nouvellesNonNotees` | Nombre de nouvelles graines au-delà de 24 dans la journée, comptées mais non détaillées. |

Chaque objet de graines : `ere` (ère annoncée par la carte ; 0 = population provisoire d'une carte neuve, remplacée dès le premier TICK), `grainePopulation` (régions : graine qui a créé la population de 20 cerveaux ; passerelle : graine de l'ère), `graineHasard` (graine réellement donnée au générateur : au redémarrage d'une région, graine de population ⊕ heures vécues ⊕ aléa matériel ; à la création d'une population, la graine de population elle-même), `tick` (heure du pays à la réception par la passerelle), `tickCarte` (dernière heure du pays vécue par la carte), `utc` (heure réelle de réception, `null` si inconnue).

## `systeme.notes[]`

`tick`, `utc`, `type`, `detail`. Types : `migration` (firmware 0.8 : sauvegarde du pays convertie du format 3 au format 4, une seule fois, à l'installation), `temperature` (firmware 0.8 : puce de la passerelle au-dessus de 70 °C), `demarrage` (avec la cause du redémarrage), `maintenance`, `publication` (échec d'un envoi), `perte` (fichier brut abandonné faute de place), `version` (firmware 0.7 : paquet radio d'une carte qui n'a pas la même version du protocole, refusé ; au plus une note par heure), `wifi` (firmware 0.7 : connexion perdue, relance par la passerelle — la première puis une par heure —, rétablissement avec sa durée en minutes, le nombre de relances et le canal). `biographies` (firmware 0.9 : carnet des biographies absent, abîmé ou en retard sur le pays au démarrage, réamorcé avec les Archives). Ces notes expliquent les trous des données ; elles ne les comblent pas.

## `poids` et `lexiques` (format 3)

Chaque région fige, à la première heure de chaque jour, les poids des 20 cerveaux et son mot pour les 48 idées, puis les envoie à la passerelle en 9 morceaux, un par heure, à la suite de sa réponse (morceaux perdus renvoyés les heures suivantes). Rien dans la vie du pays ne dépend de ce relevé.

| Champ | Sens |
| --- | --- |
| `poids.echelle` | Conversion : poids réel = valeur × 5 / 127 (les poids sont bornés à ± 5 et arrondis sur un octet signé, -127 à 127). |
| `poids.regions` | 6 entrées dans l'ordre des régions : `tick` (heure du pays où le relevé a été figé) et `citoyens`, 20 listes de 81 entiers dans l'ordre des identifiants de la région ; `null` si le relevé de la région n'est pas complet à l'édition (région muette, redémarrée dans la journée). Jamais complété par des zéros. |
| `lexiques` | 6 entrées : 48 mots (`syllabes`, `ecrit`), un par idée dans l'ordre des identifiants d'idées, **les 48 sans exception** (une région ne sait pas quelles idées le pays a vécues ; `langue.idees` le dit) ; `null` comme pour `poids`. |

Ordre des 81 poids d'un cerveau (réseau 9 entrées → 6 neurones cachés → 3 sorties) : d'abord la couche cachée, neurone par neurone (9 poids des entrées puis le biais, soit 6 × 10), puis la couche de sortie, sortie par sortie (6 poids des neurones cachés puis le biais, soit 3 × 7). Entrées : performance perçue du président, satisfaction, peur, colère, ego, charisme, ambition, charisme du président, menace. Sorties : soutien au président, envie d'être candidat, envie de se rebeller.

## `poidsPresident` (format 5)

Le cerveau qui gouverne (réseau 8 entrées → 5 neurones cachés → 5 sorties, 75 poids) du président en exercice au moment du relevé du matin, figé par sa région avec les autres poids et envoyé dans les mêmes 9 morceaux. Ce cerveau ne sert que pendant le mandat, et il apprend pendant le mandat. `null` : pas de président ce matin-là, relevé de sa région incomplet, ou région encore en 0.8.1. Jamais complété par des zéros.

| Champ | Contenu |
| --- | --- |
| `id` | Identifiant du président au moment du relevé (il peut avoir changé avant l'édition : comparer avec `pays.president`). |
| `region` | Région qui a envoyé le relevé (0 à 5). |
| `tick` | Heure du pays où le relevé a été figé. |
| `reseau`, `ordre` | « 8-5-5 » ; ordre des poids : couche cachée, neurone par neurone (8 entrées puis le biais, 5 × 9), puis sorties, sortie par sortie (5 neurones cachés puis le biais, 5 × 6). |
| `poids` | 75 entiers, même échelle que `poids` (valeur × 5 / 127). |

Entrées : performance réelle, colère moyenne, peur moyenne, temps avant l'élection, ego, taille du gouvernement, hostilité extérieure (réservée), ressources. Sorties : équité, répression, envie de reporter, ouverture du gouvernement, hostilité (réservée).

## `election` (format 3)

| Champ | Sens |
| --- | --- |
| `heure` | Heure française du dépouillement. |
| `inscrits` | 20 × régions comptées. |
| `exprimes`, `abstentions`, `blancs` | Bulletins pour un candidat, citoyens restés chez eux, bulletins blancs. Votants = exprimés + blancs. Les pourcentages de chaque candidat sont calculés sur les **exprimés**. |
| `abstentionPermise`, `blancPermis` | Règles en vigueur ce jour-là. |
| `candidats[]` | `id`, `nom`, `region`, `voix`, `pct`. |
| `regions` | 6 entrées : `voix` (une par candidat, dans l'ordre de `candidats`), `abstentions`, `blancs` ; `null` si la région n'a pas été comptée. |
| `sondage` | Présent si un sondage a porté sur ce scrutin (moins de 48 h avant, mêmes candidats) : la part annoncée de chaque candidat, en %. |

Les présidents, ministres et candidats votent toujours ; seuls les simples citoyens peuvent s'abstenir ou voter blanc.

## `sondage` (format 3)

À mi-campagne, la passerelle tire au sort, sans remise, 20 réponses parmi celles des citoyens des régions qui répondent cette heure-là.

| Champ | Sens |
| --- | --- |
| `tick`, `heure` | Moment du sondage. |
| `interroges` | Personnes tirées au sort (20, moins si peu de régions répondent). |
| `regionsRepondantes` | Taille de la population interrogeable (citoyens des régions qui ont répondu). |
| `candidats[]` | `id`, `reponses` (dans l'échantillon), `pct` (part annoncée, en % des réponses pour un candidat), `veritePct` (ce que pensait vraiment toute la population interrogeable à ce moment, en %). L'écart entre `pct` et `veritePct` est l'erreur d'échantillonnage. |
| `abstentions`, `blancs` | Réponses de l'échantillon. |

Les électeurs les moins sûrs d'eux peuvent suivre le sondage publié le jour du vote : son effet se mesure en comparant `veritePct` au résultat.

## `biographies` (format 4)

Firmware 0.9 (MAJ 1b-4). La passerelle tient pour chaque citoyen un carnet d'au plus 16 étapes de vie, publié sur le site (page « Mon citoyen », à partir de l'âge de l'État civil). Le fichier du jour donne les étapes **ajoutées depuis l'édition précédente**.

| Champ | Description |
|---|---|
| `depuis` | Date (AAAA-MM-JJ) à partir de laquelle chaque étape est notée. |
| `amorce` | `naissance` : carnet commencé au début de l'ère ; `archives` : carnet (ré)amorcé en cours d'ère avec ce que savaient les Archives (installation du firmware, carnet perdu ou en retard sur le pays après un retour arrière). Ce qui s'est passé avant `depuis` n'est pas noté, sauf l'étape `ARCHIVES`. |
| `etapesRetirees` | Nombre total d'étapes retirées des carnets pleins depuis `depuis` (la naissance et les 2 dernières restent ; part d'abord la moins marquante). Les fichiers quotidiens, eux, gardent toutes les étapes publiées. |
| `nouvelles[]` | `id` (citoyen) et `etape`, un tableau `[jour, heure, type, fois, contexte, satisfaction, colère, peur, a]`. |

Dans `etape` : `jour` = jour de l'ère ; `heure` 0-23 (`null` pour la naissance et les Archives) ; `fois` = combien de fois ce fait est arrivé à ce citoyen (compte gardé même quand une répétition remplace la précédente dans le carnet) ; `satisfaction`, `colère`, `peur` en % au moment de l'étape (`null` si inconnues).

`type` : 1 naissance (`a` = région) · 2 Archives (`a` = drapeaux : 1 ancien président, 2 renversé par une révolution, 4 trahi, 8 auteur d'un coup, 16 limogé, 32 battu, 64 ancien ministre ; `fois` = passages au pouvoir) · 3 rejoint la rébellion (après 3 h d'affilée) · 4 la quitte (après 24 h de calme) · 5 censuré · 6 candidat · 7 élu (`a` = % des voix, + 256 si réélu) · 8 renversé (`a` 1 révolution, 2 coup de palais) · 9 auteur d'un coup de palais · 10 battu aux élections · 11 entre au gouvernement (`a` = président) · 12 quitte le gouvernement (`a` 1 = limogé) · 13 entre au journal (`a` = rubrique 0-3) · 14 quitte le journal (`a` mod 256 : 1 gouvernement, 2 palais, 3 rébellion) · 15 record du plus long règne.

`contexte` (bits) : 1 tempête dans sa région · 2 épidémie dans sa région · 4 censure en vigueur · 8 jour de scrutin · 16 révolution ou coup de palais cette heure-là · 32 pénurie. C'est ce qui se passait **au même moment**, mesuré par la passerelle : jamais une cause. Le journal l'écrit « alors que », jamais « parce que ».

## Fichiers reconstitués (`donnees/ere-001/reconstitue/`)

Les jours publiés avant l'export brut (9 au 14 octobre 2026) ont été rebâtis à partir des éditions du site (`tools/recherche/reconstitue.py`). Ils portent `"source": "reconstitue"`, `"reconstitue": true`, l'origine (commit du site) et la méthode. Ils ne contiennent **que** ce que le journal publiait : pourcentages arrondis (0-100), humeur et rebelles par région, bourse, faits du jour, langue. `heures`, `heuresVecues` et `heuresManquantes` valent `null`. Ils ont leur propre manifeste et ne doivent pas être mélangés aux mesures sans le signaler.
