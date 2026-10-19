# Registre des incidents et des corrections

**Français** · [English](registre-incidents.en.md)

Ce registre consigne les incidents techniques qui touchent les données, et les corrections. Les fichiers bruts ne sont jamais modifiés : ce registre les explique, il ne les remplace pas. Les heures sont en UTC (heure de Paris = UTC + 2 en octobre 2026). Une cause n'est écrite comme établie que si elle a été vérifiée ; sinon, elle est marquée « non établie ».

Ouvert le 19 octobre 2026. Pour signaler un incident ou une erreur : ouvrez une *issue* sur le dépôt.

## Incidents

### INC-001 — Réponses des régions manquantes, 16 octobre 2026
- **Période :** ticks 169 à 190 (16/10, de 21:00 UTC la veille à 18:00 UTC).
- **Observé dans les données :** 43 région-heures `null` dans `quotidien/2026-10-16.json`, réparties sur les six régions. Aux ticks 180, 182 et 184 (08:00, 10:00 et 12:00 UTC), aucune région n'a répondu. Aucune heure manquante (`heuresManquantes` vide) ; `paquetsPerdus` = 0 à la dernière heure.
- **Cause :** non établie.

### INC-002 — Connexion internet de la passerelle perdue, 16 octobre 2026
- **Période :** environ de 15:00 à 17:50 UTC (panne de la box internet).
- **Effet :** l'édition n° 8 du journal a été construite à 18:00 UTC sans connexion, puis publiée après redémarrage de la passerelle (commit du site à 21:15 UTC). Le fichier brut du 16/10, généré à 18:00:05 UTC, a été publié à 21:16 UTC. Le pays fonctionne en radio locale : aucune heure n'est manquante dans le fichier du jour.
- **Cause :** panne de la box internet, constatée par l'auteur.

### INC-003 — Région Barrage muette, 16-17 octobre 2026
- **Période :** du tick 189 (16/10, 17:00 UTC) au tick 215 (17/10, 19:00 UTC), soit 27 heures consécutives. Réponses irrégulières avant (ticks 180 à 187). Retour au tick 216 (17/10, 20:00 UTC), après redémarrage manuel de la carte.
- **Observé dans les données :** Barrage est `null` pendant 24 heures sur 24 dans `quotidien/2026-10-17.json`. Pendant cette période, la passerelle ne compte que 5 régions : un mot ne reste commun que si ces 5 régions sont d'accord. Les mots communs passent de 7 (16/10) à 6 (17/10).
- **Cause :** non établie (la carte n'envoyait plus de réponse reçue par la passerelle ; on ne sait pas si elle était éteinte ou si ses messages se perdaient).
- **À lire avec les études :** les réponses manquantes peuvent retarder les étapes qui dépendent du nombre de mots communs.

## Corrections

Aucune correction publiée pour l'instant.
