# Architecture de Microcontrôland

*[English version](architecture.en.md)* · Version de la documentation : firmware 0.6 (MAJ 1b-2), 14 octobre 2026

## Vue d'ensemble

Microcontrôland tourne sur **7 cartes ESP32-S3** qui se parlent par radio (ESP-NOW), sans câble entre elles.

| Carte | Rôle |
| --- | --- |
| Passerelle (ESP32-S3 N16R8) | Horloge du pays, politique (élections, gouvernement, révoltes), bourse, langue, rédaction du journal, publication sur Internet. |
| 6 régions (Mines, Champs, Raffineries, Barrage, Port, Ville) | 20 citoyens chacune. Chaque citoyen est un petit réseau de neurones (81 connexions) qui décide, apprend et se souvient. |

Une **heure du pays dure une vraie heure** et suit l'heure française. À chaque heure, la passerelle envoie un « TICK » aux régions ; chaque région fait vivre ses citoyens et répond avec son état (satisfaction, peur, colère, rebelles, croyants, production, mot proposé pour l'idée du moment).

## Ce qui n'est pas scénarisé

Aucun événement n'est écrit à l'avance. Les élections, les révoltes, les mots communs et les croyances viennent des décisions des citoyens. La passerelle applique des **règles fixes** (publiées sur le site, page « Règles ») ; elle ne choisit pas les résultats.

## Le cycle d'une journée

1. **Chaque heure** : TICK → réponses des régions → la passerelle met à jour le pays et enregistre l'heure dans un tampon de données brutes (copié en mémoire flash pour survivre à un redémarrage).
2. **18 h** : relevé des cours réels de la Banque centrale européenne (4 monnaies de pays producteurs, mesurées en dollars). Week-ends et jours fériés : bourse fermée.
3. **20 h** : la passerelle écrit l'édition de *La Puce Libre* (français et anglais) et le **fichier brut de la journée**.
4. **Publication** :
   - le journal part sur le site en **un seul commit** (API Git Data de GitHub) ;
   - puis le fichier brut et le manifeste partent dans ce dépôt, en un commit séparé. Un échec ici ne bloque jamais le journal : nouvel essai toutes les heures.

## Faits, interprétations, hypothèses

| Couche | Où | Nature |
| --- | --- | --- |
| Faits | `donnees/…/quotidien/` | Mesures des cartes, échelle brute 0-255, valeurs absentes = `null`. |
| Interprétation | Le journal, l'Ambassade | Récit écrit par la passerelle à partir des faits. Peut être censuré par un président (les chiffres du panneau « État du pays » ne le sont jamais). |
| Hypothèses | `protocoles/`, `etudes/` | Questions posées par les études, déposées avant l'analyse. |

## La rédaction (depuis la MAJ 1b-2)

Quatre citoyens tiennent les rubriques (politique, économie, société, billet d'humour). Ils signent, avec un style tiré de leur caractère du jour. Un journaliste qui devient président ou ministre quitte la rédaction ; un rebelle reste. Quand un président censure au moins 6 citoyens, la politique est confiée à un correspondant agréé par le palais, certains chiffres des articles sont remplacés par « ████ » et un bandeau prévient le lecteur. À la fin de la censure paraît « Ce que nous ne pouvions pas écrire ». L'état de la rédaction est sauvegardé à part et n'entre pas dans les données brutes.

## Matériel et sûreté

- Passerelle : sortante seulement (Internet), plus la mise à jour sans fil sur le réseau local. Aucun port ouvert vers Internet.
- Sauvegarde du pays : chaque heure en mémoire flash, chaque soir sur le site (`data/sauvegarde.json`).
- Redémarrage automatique hebdomadaire vers 4 h ; chien de garde de 3 minutes.
- Le texte venu du public n'entre jamais tel quel dans le pays (votes comptés, réponses filtrées par la langue du pays).

## Code source

Firmware (C++/Arduino) : logique du pays dans `lib/mcl_core`, matériel dans `src/`. Le même cœur tourne sur PC pour les tests (simulation de plusieurs années, vecteurs SHA-256 officiels, faux serveur GitHub). Licence MIT.
