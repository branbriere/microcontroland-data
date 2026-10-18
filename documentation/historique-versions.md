# Historique des versions

*[English version](historique-versions.en.md)*

Chaque version qui change ce que le pays mesure, publie ou raconte est notée ici, avec sa date de livraison (l'installation suit en général dans les 24 h). Les données d'un jour sont toujours à lire avec la version du firmware indiquée dans le fichier.

| Livrée le | Firmware | Mise à jour | Ce qui change pour les données |
| --- | --- | --- | --- |
| 9 oct. 2026 | 0.3 | Mise en production | Début de l'ère 1. Le journal paraît à 20 h. Pas encore d'export brut. |
| 10 oct. 2026 | 0.4 | MAJ 1a | Le journal raconte ce qui a changé depuis la veille (moins de répétitions), rubrique tournante, « Chiffre du jour ». Maintenance sans câble. Format de sauvegarde inchangé. |
| 11 oct. 2026 | 0.5 | MAJ 1b-1 « Les petites histoires » | Le journal suit les personnages (ministres qui survivent, « Que devient… ? », candidats, premières fois). Démentis de l'Ambassade. Format de sauvegarde inchangé. |
| 13 oct. 2026 (installation prévue le 14 oct., 21 h) | 0.6 | MAJ 1b-2 « La rédaction » | **Export brut quotidien** vers ce dépôt (format 1), manifeste SHA-256, notes système. Journalistes citoyens, rubriques, billet, édition du dimanche, presse censurée (articles seulement, jamais les chiffres). Publication du site en un seul commit. Corrections : « d'électricité », départage par la colère, pas de brève « humeur satisfaite », 4ᵉ démenti. Format de sauvegarde du pays inchangé (3440 octets). Premier fichier brut attendu le 15 octobre ; il commence à l'installation (`heuresManquantes` = `null`). |
| 18 oct. 2026 (installation à 21 h) | 0.7 | MAJ 1b-3, étape « graines et prise » | **Format 2** du fichier brut : bloc `graines` (graine de l'ère, graines de la passerelle et de chaque région, nouvelles graines du jour avec l'heure et la carte) ; **relevé horaire de la prise Shelly** (`heures[].prise` : puissance et compteur d'énergie du pays entier, lus en local) ; **relance Wi-Fi** de la passerelle toutes les 5 min après une coupure, notée dans `systeme.notes` (type `wifi`). Protocole radio version 4 (le message de présentation d'une région porte ses deux graines, 25 octets) : les 7 cartes sont mises à jour ensemble ; une carte d'une autre version est refusée et signalée (note `version`). Pays, journal et format de sauvegarde du pays inchangés (3440 octets). Premier fichier au format 2 attendu le 19 octobre. |
| à venir | 0.8 | MAJ 1b-3, suite « Les élections » | Export des poids des cerveaux, migration du format de sauvegarde (4) avec champs réservés (généalogie, médecine). |

Les jours du 9 au 14 octobre 2026 sont disponibles en version reconstituée (`donnees/ere-001/reconstitue/`).
