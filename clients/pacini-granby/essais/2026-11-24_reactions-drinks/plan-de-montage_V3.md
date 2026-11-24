# V3 — version corrigée de l'export de l'utilisateur (2026-11-24)

Reprend **la structure de la version exportée par l'utilisateur** (20 chiffres, 6 réactions, répétitions 3, 4, 3, 3, 3, 4 ; 15,22 s) en corrigeant le défaut involontaire : **chaque chiffre change exactement sur la coupe**. Son projet « Pacini Granby - Reactions drinks V2 » n'a pas été touché (dernière écriture 15:21:09, avant et après). V1 et V2 conservées.

## Livré

- **Projet CapCut** « Pacini Granby - Reactions drinks V3 » (nouveau, premier de la liste) : 20 plans liés au rush et rallongeables, 20 chiffres sur une piste séparée (chacun a **le même début et la même durée que son plan**), légende sur sa piste, musique sur sa piste.
- **MP4** `previsualisation_reactions-drinks_V3.mp4` (1080×1920, 15,2 s, 456 images). Pas de version sans texte copiée (elle est dans le dossier de sortie du script).

## Plan (retrouvé image par image dans l'export de l'utilisateur)

| Réaction | Rush (images, 29,97 i/s) | Répétitions | Chiffres |
| --- | --- | --- | --- |
| Sourire calme | 13 → 31 (19 images) | 3 | 1–3 |
| Pouces | 40 → 58 (19) | 4 | 4–7 |
| Tête penchée, mains ouvertes | 164 → 185 (22) | 3 | 8–10 |
| Regard de côté | 241 → 262 (22) | 3 | 11–13 |
| Doigts écartés | 338 → 362 (25) | 3 | 14–16 |
| Mains sur la tête | 427 → 455 (29) | 4 | 17–20 |

Seule différence de structure avec son export : le 2ᵉ rejeu du sourire calme dure 19 images (20 dans son export). Fichiers : `plan_V3.csv` (CapCut), `plan_V3_mp4.csv` (MP4).

## Texte (choix de cette V3, **pas** celui de son export)

- Montserrat **Bold** (installée sur le poste), 53 px (taille CapCut 8,26), mêmes positions que sa version : légende centrée à 52 %, compteur à 58,5 %. Largeur de la deuxième ligne mesurée : 810 px (son export : 858 px ; V2 en Regular : 764 px).
- **La police de son export n'est pas identifiée** : « Montserrat Bold » est mon choix par défaut, pas une déduction. La taille est limitée à 53 px par la marge latérale de 130 px (hypothèse de zone de sécurité) ; son export va un peu au-delà.
- À ajuster dans CapCut (police, taille) si le rendu ne correspond pas à ce que l'utilisateur préfère.

## Contrôles de production (courts)

- Plan : chaque passage donne bien le nombre d'images prévu (6 sur 6) ; valeurs 1 à 20 sans saut (2,6 s).
- Compteur (MP4) : valeurs et timecodes contigus ; **19 changements contrôlés sur images : le chiffre change sur la coupe (image avant = n−1, image après = n) pour les 19** (3,6 s).
- Compteur (projet CapCut) : 20 clips contigus, 20 textes alignés un à un (même début, même durée), valeurs 1 à 20 ; ouverture dans CapCut vérifiée (20 plans, légende en gras, durée 15 s 07 images), puis fermeture sans modification.
- Le contrôle exhaustif image par image n'a pas été relancé : aucune anomalie.

## Temps par étape (horodatages réels)

| Étape | Durée |
| --- | --- |
| Contrôle du plan avant rendu | 2,6 s |
| Script du MP4 (456 images, 20 plans) | 104 s (15:40:51 → 15:42:35) |
| dont export des 20 segments | 28 s |
| dont légende + 20 chiffres | 9 s |
| dont encodage sans texte / avec texte | 12 s / 37 s |
| Contrôle rapide du compteur | 3,6 s |
| Sauvegarde des projets + projet CapCut | 5 s (1 085 fichiers, contrôlée) |

Non mesuré : l'analyse de l'export de l'utilisateur, la vérification dans l'interface de CapCut (ouverture et fermeture), la documentation. Pour comparaison, la V2 : 252 s pour le dernier lancement (40 plans), 4 lancements au total.

## À vérifier par l'utilisateur

- Le texte (police, épaisseur, taille) par rapport à son export.
- Musique : même piste et même départ (0,04 s) que sa version ; non écoutée, autorisation inconnue.
- Rappel CapCut : si un plan est supprimé ou raccourci, son chiffre ne suit pas.
