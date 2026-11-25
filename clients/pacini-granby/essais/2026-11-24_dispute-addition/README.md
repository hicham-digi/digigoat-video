# Essai Pacini Granby — « Dispute pour l'addition » V1 (2026-11-24)

> Choix d'un essai : **aucun n'est une règle permanente** sans confirmation de l'utilisateur.

## Brief reçu (message de l'utilisateur, 2026-11-24)

- Rush : `DJI_20000116223917_0012_D.MP4` (1728x3072, 29,97 i/s, 11,3 s de matière utile) ; audio séparé : aucun.
- Sujet : la serveuse voit des clients se disputer pour payer, s'impatiente et se met à manger ce qu'il y a sur la table.
- Durée : « autour de 9 secondes » ; texte à afficher : « Je paie, non, je paie » ; musique : `snapgram.io_uqkhzxpnr1z6.mp3` ; référence : « Morale de l'histoire… ».
- Format : le champ du brief était resté sur le gabarit (« ex. vertical 9:16 ») ; 9:16 retenu, puis **confirmé par l'utilisateur en chat le 2026-11-24** (« Oui, tout bon »), pour cet essai.

## Ce qui a été produit

| Élément | Emplacement |
| --- | --- |
| Projet CapCut **modifiable** « Pacini Granby - Dispute addition V1 » | dossier des projets CapCut (nouveau projet ; sauvegarde complète `...\SAUVEGARDES\capcut-projets_avant-pacini_granby_dispute_addition_v1_20261124_2336`, 283 fichiers) |
| Aperçu MP4 de contrôle (1080x1920, 9,076 s) | `C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_dispute-addition\sorties\previsualisation_dispute-addition_V1.mp4` |
| Plan et textes | `plan.csv`, `textes.txt` (ce dossier) |

Montage : 2 plans liés au rush (rallongeables) : A = 1,202 s + 2,769 s (clients qui se disputent, recadrage 1,4x), B = 5,005 s + 6,306 s (elle mange puis boit, recadrage 1,75x) ; musique 9,075 s depuis 0 ; son d'origine du rush conservé (volume 1) ; deux textes `"Je paie"` (dès 0,8 s) et `"Non, je paie"` (dès 1,7 s), Montserrat Bold taille CapCut 8,26, blanc, ombre, placés près de chaque main comme sur la référence.

## Commande (exécutée CapCut fermé)

```powershell
python -I scripts\capcut_projet.py --nom "Pacini Granby - Dispute addition V1" `
  --plan clients\pacini-granby\essais\2026-11-24_dispute-addition\plan.csv `
  --rushes "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_dispute-addition\rushes" `
  --musique "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_dispute-addition\musique\snapgram.io_uqkhzxpnr1z6.mp3" `
  --depart 0 --son-origine garder `
  --police "C:/Users/Hicham/AppData/Local/Microsoft/Windows/Fonts/Montserrat-Bold.ttf" --police-nom "Montserrat Bold" --taille-capcut 8.26 `
  --textes-libres-fichier clients\pacini-granby\essais\2026-11-24_dispute-addition\textes.txt `
  --sauvegarde C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES
```

## Réellement vérifié

- Copies du rush et de la musique identiques aux originaux (SHA256) ; originaux non modifiés.
- Coupes à l'image près (images 36–118 et 150–338 du rush) ; aperçu : 272 images, durée 9,076 s, audio 9,076 s, pic -2,3 dBFS.
- Images de l'aperçu regardées (recadrages, textes, guillemets) ; le bandeau noir en haut vient du plafond du rush.
- Projet CapCut ouvert dans CapCut 9.8 : 9:16, 30 i/s, 2 plans (2 s 24 i et 6 s 09 i), 2 pistes de texte, musique ; rendu à 2,1 s et 5,1 s conforme à l'aperçu (cadrage, position et police des textes).
- Autres projets CapCut (V3, V5, Décors de Noël…) non touchés.

## Non vérifié / à corriger

- **Aucune écoute** : le son du rush (ambiance, pas de parole détectée par la transcription locale : 0 segment) et la musique n'ont pas été entendus ; la synchronisation coupe/musique n'est pas contrôlée à l'oreille.
- Musique : origine et licence inconnues (probablement l'audio de la référence).
- Texte : « Je paie, non, je paie » compte trois parties ; rendu en **deux bulles** comme la référence (`"Je paie"`, `"Non, je paie"`) : **confirmé par l'utilisateur le 2026-11-24** pour cet essai (pas une règle permanente de la marque).
- Police Montserrat Bold = approximation (police de la référence non identifiée) ; pas de fondu d'apparition des textes (≈ 0,1 s sur la référence).
- Recadrage 1,75x sur une source 1728x3072 : léger agrandissement.
- Identité et accord de la personne filmée : non documentés.
