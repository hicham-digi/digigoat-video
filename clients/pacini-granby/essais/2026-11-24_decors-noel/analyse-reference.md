# Analyse de la référence de style — Bella Italia (essai Décors de Noël)

Fichier : `C:\Users\Hicham\Desktop\Videos référence\Dinner at Bella Italia Ristorante in Naples, FL 🎄✨The cozy, festive holiday atmosphere makes it.mp4`

> Cette vidéo vient d'un **autre restaurant**. Tu l'as fournie pour guider le style du montage. Tu autorises à t'inspirer de son rythme, de la durée des plans et des transitions, sans reprendre ses images, sa musique ni son identité. Rien de son contenu n'est repris dans l'essai.
> Tout ce qui suit est **observé**, pas une règle. Une caractéristique ne devient une règle de montage que si tu la valides.

## Ce que j'ai réellement pu analyser

| Aspect | Méthode | Résultat |
| --- | --- | --- |
| Format | `ffprobe` | 720×1280 (9:16), 24 images/s, 12,7 s |
| Coupes | Score de changement calculé pour chaque image (302 images), puis vérification visuelle des cas douteux | **10 coupes confirmées**, donc **11 plans** |
| Durée des plans | Calculée à partir des coupes | De 0,75 s à 1,67 s, **moyenne 1,15 s** (1,08 / 1,38 / 0,75 / 0,83 / 1,67 / 1,00 / 0,92 / 0,87 / 1,54 / 1,00 / 1,66 s) |
| Transitions | Profil du score de changement autour de chaque coupe | **Coupes franches** : le changement tient en une seule image, les images voisines sont stables. Aucun fondu enchaîné ni fondu au noir détecté |
| Texte à l'écran | Images examinées | Petite légende blanche, centrée, qui reste affichée tout au long de la vidéo |
| Ambiance visuelle | Images examinées | Éclairage chaud et sombre, plats, vin, sapin |
| Niveau sonore | `ffmpeg volumedetect` | Moyenne −16,5 dB, pic −0,7 dB (le niveau seulement, pas le contenu) |

### Correction d'un chiffre précédent

Mon analyse initiale annonçait 8 coupes et un plan toutes les 1,4 s environ. Le seuil de détection était trop haut et avait manqué 2 coupes (à 6,7 s et 11,0 s). Les chiffres ci-dessus sont les bons. J'ai écarté 3 autres détections (à 4,96 s, 8,92 s et 9,42 s) après vérification visuelle : ce sont des mouvements dans un même plan (fourchette, cuillère), pas des coupes.

## Ce que je n'ai pas pu analyser

- **La musique** : titre, tempo, style, et synchronisation des coupes avec le rythme. Je ne peux pas écouter.
- **Les voix et les sons**.
- **Les mouvements de caméra** et les effets subtils (zoom, glissement) : je n'ai vu que des images fixes.
- **L'étalonnage** de manière chiffrée : seulement une impression visuelle.
- **L'intention** : pourquoi ces choix ont été faits.

## Comparaison avec le prémontage V1/V2

| Aspect | Référence Bella Italia | Prémontage (V1 et V2) | Retrouvé dans le prémontage ? |
| --- | --- | --- | --- |
| Format | 9:16 | 9:16 (1080×1920) | Oui |
| Transitions | Coupes franches | Coupes franches | Oui |
| Nombre de plans | 11 | 10 | À peu près |
| Durée moyenne d'un plan | 1,15 s | 1,96 s (de 1,5 à 2,5 s) | **Non : mon prémontage est environ 1,7 fois plus lent** |
| Durée totale | 12,7 s | 19,6 s | Non (la durée de 15 à 25 s venait de tes paramètres de test) |
| Légende persistante | Oui | Non (tu n'en as pas demandé) | Non |
| Ouverture | Non analysée | Mouvement de caméra sur les cadeaux | Non comparable |
| Musique | Non analysée | Piste que tu as fournie | Non comparable |

## Ce que cela signifie

- Le prémontage V1 a été construit à partir de tes rushes et de tes paramètres de test, **pas à partir des mesures de la référence**. Le seul point réellement commun est le choix de coupes franches, avec le format 9:16.
- Le rythme du prémontage est plus lent que celui de la référence. Tu as dit que le rythme te convient : je ne l'ai pas modifié.
- Si tu veux t'en rapprocher, une variante avec des plans d'environ 1,1 à 1,5 s est possible. Il faudrait alors retirer des plans ou utiliser des segments plus courts. Elle n'a **pas** été produite.
