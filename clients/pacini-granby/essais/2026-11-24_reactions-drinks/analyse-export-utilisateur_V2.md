# Analyse de l'export modifié par l'utilisateur — V2 « réactions » (2026-11-24)

Comparaison en **lecture seule** de deux MP4 : mon export V2 (`previsualisation_reactions-drinks_V2.mp4`, 28,16 s) et la version modifiée et exportée par l'utilisateur (`...\REEL FINIS\Pacini Granby - Reactions drinks V2.mp4`, 15,23 s). Aucun rendu, aucune ouverture de son projet CapCut. Les passages sont retrouvés en comparant chaque image au rush (écart 0,6 sur 255 : correspondance exacte).

## Constats mesurés

| | Mon export V2 | Export de l'utilisateur |
| --- | --- | --- |
| Durée | 28,16 s (844 images) | **15,23 s** (457 images, 30 i/s) |
| Format | 1080×1920, 29,97 i/s | 2160×3840 HEVC, 30 i/s |
| Compteur | 1 à 40 | **1 à 20**, +1 à chaque changement, aucun saut |
| Réactions (passages du rush) | 13 | **6**, dans l'ordre du rush |
| Répétitions | 3 par réaction (4 pour la 5ᵉ) | 3, **4**, 3, 3, 3, **4** |
| Texte | « Notre réaction au nombre / de drinks que tu commandes » | **même texte** |

Réactions conservées, avec leurs répétitions et leurs chiffres (passage source identique à mon plan, à 1 image près) :

| Réaction | Passage du rush | Répétitions | Chiffres |
| --- | --- | --- | --- |
| Sourire calme | 0,43 → 1,03 s | 3 | 1–3 |
| Pouces | 1,33 → 1,94 s | **4** (j'en avais 3) | 4–7 |
| Tête penchée, mains ouvertes | 5,47 → 6,17 s | 3 | 8–10 |
| Regard de côté | 8,04 → 8,74 s | 3 | 11–13 |
| Doigts écartés (montée) | 11,28 → 12,08 s | 3 | 14–16 |
| Mains sur la tête | 14,25 → 15,18 s | **4** (j'en avais 3) | 17–20 |

Réactions supprimées (de mon plan) : « elle parle », « doigts qui bougent », « mains qui redescendent », « mains qui retombent », « rire » ×2, « main au visage ». La vidéo se termine sur le sommet de la réaction (mains sur la tête, 4ᵉ répétition).

## Tableau : différence, effet, enseignement potentiel

Les **constats** sont mesurés. Les **interprétations** sont de moi et ne sont pas confirmées.

| Différence constatée | Effet sur le montage | Enseignement potentiellement réutilisable (**à confirmer**, pas une règle) |
| --- | --- | --- |
| 40 → **20** chiffres ; 28,16 → **15,23 s** | Vidéo deux fois plus courte, dans la fourchette de ta demande initiale (15 à 20 s) | Interprétation : ce rush (17 s, environ 6 réactions nettes) soutient naturellement ~20 chiffres, pas 40. Adapter le nombre et la durée à la matière |
| 13 → **6** réactions, ordre du rush conservé | Chaque réaction est un geste net et très différent de la précédente ; plus de réactions « molles » (parler, rire) | Interprétation : garder les réactions distinctes et lisibles, écarter les passages sans geste fort |
| Répétitions 3/4/3/3/3/4 au lieu de 3 partout | Pouces et mains sur la tête durent plus longtemps : insistance sur les deux réactions les plus marquées, et fin plus appuyée | Interprétation : le nombre de rejeux peut varier selon la force de la réaction (la référence a aussi un groupe à 4) |
| Durées de boucle inchangées (19, 22, 25, 29 images ; une répétition de 20 images) | Même rythme que ma V2, un peu plus lent que la référence sur la fin (29 images contre 13 à 17) | Constat seul : il a gardé mes longueurs de boucle, sans les copier de la référence jusqu'au bout |
| Compteur continu 1 à 20, sans saut | Conforme à la mécanique demandée | Constat : progression continue jusqu'au nombre retenu |
| **Chiffre décalé de 3 images (0,1 s) après la coupe** pour les chiffres 8 à 13 (1 image pour le 14) ; aligné ailleurs | Pendant 0,1 s on voit la nouvelle réaction avec l'ancien chiffre, 7 fois | Interprétation possible : textes non recalés après la suppression de plans. **Confirmé par l'utilisateur : involontaire** (2026-11-24). Défaut d'alignement, **pas une préférence**. Cause probable (non vérifiée) : plans supprimés ou raccourcis dans CapCut sans recaler les textes des chiffres |
| Texte **plus gras et plus gros** : chiffre « 1 » de 43 px contre 37 (+16 %), largeur du chiffre 19 contre 12 px, légende +12 % de largeur | Plus lisible et plus proche de la référence (grosse, grasse) | Interprétation : pour ce type de vidéo, texte gras plus gros. **Écart avec le guide** (Montserrat Regular seulement). Police exacte non identifiée |
| Position du texte **inchangée** : légende centrée à ~52 % (50,2 et 53,8 %), compteur à 58,5 % | Aucun | Constat : les positions de la référence ont été gardées |
| Export 4K HEVC | Qualité de sortie, sans effet sur le montage | Constat : réglage d'export, pas un choix de montage |

## Musique : limites de mon analyse

- **Mesuré** : sa musique est la même piste, démarrant au même endroit (≈ 0,05 s dans la piste, corrélation de l'enveloppe sonore 0,92 contre 0,96 pour la mienne), même niveau (−14,9 LUFS, pic −3,0 dBFS), coupée à 15,25 s avec un fondu final rapide (durée non mesurée avec précision).
- **Non déterminable** : je n'ai écouté aucune des deux versions. Je ne peux pas dire si la musique suit mieux ou moins bien les coupes, ni si un volume ou un effet a été modifié au-delà du niveau global, ni l'agrément du passage choisi. L'analyse porte uniquement sur l'enveloppe sonore.

## Ce qui reste à confirmer avec toi

- ~~Le décalage de 0,1 s du chiffre après la coupe~~ : **involontaire** (confirmé). Il faut le corriger dans CapCut si l'utilisateur veut un alignement parfait ; ce n'est pas une règle.
- Le texte gras et plus gros : choix de cette vidéo ou préférence, et accord du client (le guide cite Montserrat Regular).
- Tout le reste ci-dessus reste un **choix de cette vidéo** tant que tu ne l'as pas confirmé comme règle.

## Suites décidées par l'utilisateur (2026-11-24)

- Le décalage du chiffre est **involontaire** : à corriger dans une version corrigée (à produire ; son projet actuel n'est pas modifié).
- **Confirmés comme principes réutilisables du format « Réactions avec compteur »** : réactions nettes, lisibles et contrastées ; passages faibles ou redondants écartés ; compteur et durée adaptés à la matière ; répétitions variables selon l'intérêt humoristique ; progression terminant sur une réaction forte ; chiffre synchronisé avec la coupe par défaut. Voir `sops/format-reactions-compteur.md`.
- **Restent des choix propres à cette vidéo** : 20 chiffres, 6 réactions, répétitions de 3 ou 4, durée de 15,23 s.
- **Texte** : pour ce format, l'utilisateur préfère la lisibilité de son export, utilisé comme **référence visuelle**. La police n'est pas nommée (non identifiée) et le style n'est **pas** généralisé à la marque.

## Statut de cette version

Ta version exportée est **la référence du résultat que tu préfères pour cette vidéo** (directive du 2026-11-24). Elle n'est pas, à elle seule, une règle de marque.
