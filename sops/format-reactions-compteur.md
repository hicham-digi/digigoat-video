# Format « Réactions avec compteur »

Format de vidéo courte : une personne réagit de plus en plus fort pendant qu'un **compteur** monte, avec une **légende fixe** (principe repéré dans la vidéo de référence de l'essai 2 de Pacini Granby). Cette fiche sépare trois niveaux : **principes réutilisables du format**, **choix propres à une vidéo**, **ce qui ne vaut pas pour toute la marque**. Origine : essai 2 « Réactions selon le nombre de drinks » (2026-11-24), `clients/pacini-granby/essais/2026-11-24_reactions-drinks/`.

## Mécanique observée dans la référence (constat, pas une règle)

Mesurée sur la vidéo de référence : 28,13 s ; compteur de 1 à 40, +1 à chaque changement ; chaque changement de chiffre est une coupe sur un **rejeu du même passage** (boucle) ; 13 réactions rejouées 3 fois, une 4 fois ; boucles de plus en plus courtes vers la fin. Détail : `analyse-reference_V2.md` de l'essai.

## A. Principes réutilisables du format — confirmés par l'utilisateur (2026-11-24)

1. **Sélectionner les réactions les plus nettes, lisibles et contrastées.**
2. **Écarter les passages faibles ou redondants.**
3. **Adapter le compteur et la durée à la matière disponible.** Nombre et durée indicatifs : Claude peut les adapter et explique brièvement son choix. Nombre et durée imposés explicitement : signaler le conflit avec les rushes avant le rendu.
4. **Faire varier le nombre de répétitions selon leur intérêt humoristique.**
5. **Construire une progression et terminer sur une réaction forte.**
6. **Compteur continu** : 1, 2, 3 … jusqu'au nombre retenu, +1 à chaque changement, aucun saut, un seul nombre visible à la fois (directive du 2026-11-24).
7. **Par défaut, le changement de chiffre est synchronisé avec la coupe** : le nouveau chiffre apparaît sur la première image du plan qui le porte, **sauf indication contraire** de l'utilisateur (directive du 2026-11-24). Un décalage constaté dans l'export de l'essai 2 était involontaire : c'est un défaut, pas un style.
8. **Légende fixe** sur toute la durée, compteur sous la légende (observé dans la référence ; repris dans l'essai).
9. **Lisibilité du texte** : pour ce format, l'utilisateur préfère le rendu de **son export** de l'essai 2 (texte plus gras et plus grand, de l'ordre de +12 à +16 % par rapport à ma V2) comme **référence visuelle**. La police exacte de cet export n'est pas identifiée : **ne pas inventer son nom**. Voir la section C.

## B. Choix propres à la vidéo de l'essai 2 — pas des valeurs fixes

- 20 chiffres (1 à 20) et une durée de 15,23 s.
- 6 réactions : sourire calme, pouces, tête penchée et mains ouvertes, regard de côté, doigts écartés, mains sur la tête.
- Répétitions 3, 4, 3, 3, 3, 4 (pouces et mains sur la tête à 4).
- Les passages précis du rush, l'ordre du rush, les longueurs de boucle (19 à 29 images), la légende « Notre réaction au nombre / de drinks que tu commandes », la musique et son départ.
- Le nombre de réactions, de chiffres et de répétitions dépend **toujours** du rush : jamais repris tel quel d'une vidéo à l'autre.

## C. Limites : ce qui n'est pas généralisé

- Le style de texte de l'export (gras, plus grand) est une **référence visuelle pour ce format**, pas une règle de la **marque** Pacini Granby. Le guide de marque cite **Montserrat Regular** : l'écart est connu et n'est pas tranché pour toute la marque. Ne pas l'appliquer à d'autres formats ni à d'autres marques sans confirmation.
- Les positions du texte (légende vers 52 %, compteur vers 58,5 % de la hauteur) viennent de la référence mesurée et ont été gardées par l'utilisateur ; elles restent **à confirmer** pour un autre rush.
- Musique : non écoutée, autorisation non confirmée (voir `REPRISE.md`).

## Contrôles de production pour ce format (courts)

1. Plan : chaque passage existe dans le rush ; nombre d'images par passage ; durée totale.
2. Compteur : valeurs 1 à N sans saut, une valeur par plan, **début et durée de chaque chiffre identiques à ceux de son plan** (valeurs et timecodes, dans le plan puis dans le projet).
3. Images : contrôler seulement quelques images aux changements (dernière image du plan précédent, première du suivant : le chiffre change **sur** la coupe).
4. Contrôle exhaustif image par image (`controle_V2.py` de l'essai 2) : **seulement** si une anomalie apparaît ou si la fonction du compteur est modifiée.

## Limites de CapCut à rappeler

Les chiffres sont sur une piste séparée. Si l'utilisateur supprime ou raccourcit un plan, son chiffre et ceux qui suivent ne bougent pas : à recaler ou à supprimer à la main.
