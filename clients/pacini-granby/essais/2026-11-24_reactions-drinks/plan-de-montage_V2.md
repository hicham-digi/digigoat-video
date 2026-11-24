# Plan de montage V2 — réalisé (principe validé par l'utilisateur)

**Livré** : MP4 `previsualisation_reactions-drinks_V2.mp4` (+ `_sans-texte`) et projet CapCut « Pacini Granby - Reactions drinks V2 » (40 plans liés au rush, 40 textes de chiffres sur une piste, légende et musique séparées). V1 conservée (MP4 et projet « Pacini Granby - Reactions drinks »).

**Contrôles automatiques** (`controle_V2.py`, résultat dans `controle_V2_resultat.txt`) : 844 images ; chiffres lus 1 à 40 dans l'ordre, sans saut ni doublon ; un seul nombre visible sur les 844 images ; longueur de chaque chiffre = plan prévu (40 sur 40) ; 27 rejeux identiques au précédent (écart max 0,27/255) et 12 changements de réaction (écarts 3,3 à 21,5) ; chaque groupe commence sur l'image prévue du rush ; légende sur toutes les images ; durée 28,16 s (référence 28,13 s). Projet CapCut : durée 28,16 s, 40 clips contigus, 40 textes alignés un à un sur les clips, valeurs 1 à 40 sans chevauchement ; ouvert dans CapCut puis refermé sans modification (le chiffre affiché à 14 s 20 images est bien le 21).

**Ajustements faits pendant la réalisation** : groupes 12 et 13 décalés d'une image vers le début (16,38 s et 16,95 s) pour que le dernier groupe garde ses 13 images ; changement de chiffre calé sur des numéros d'image (et non des secondes) dans `premontage.ps1`, après un décalage d'une image repéré par le contrôle.


La V1 (`plan.csv`, `plan-de-montage.md`) est conservée. Principe repris de la référence (voir `analyse-reference_V2.md`) : **13 passages courts, chacun joué 3 fois de suite (le 5ᵉ 4 fois), le compteur monte de 1 à chaque rejeu, puis changement de réaction.** Compteur : 1 à 40, sans saut, indépendant de ce que dit l'employée. Légende fixe sur toute la durée.

| Réaction | Passage du rush (s) | Images | Reps | Chiffres | Durée du groupe | Contenu |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0,40 → 1,03 | 19 | 3 | 1–3 | 1,90 s | sourire calme |
| 2 | 1,30 → 1,94 | 19 | 3 | 4–6 | 1,90 s | les mains montent, pouces |
| 3 | 5,44 → 6,17 | 22 | 3 | 7–9 | 2,20 s | tête penchée, mains ouvertes |
| 4 | 8,01 → 8,74 | 22 | 3 | 10–12 | 2,20 s | regard de côté |
| 5 | 9,94 → 10,67 | 22 | **4** | 13–16 | 2,94 s | elle parle en souriant |
| 6 | 11,24 → 12,07 | 25 | 3 | 17–19 | 2,50 s | mains ouvertes, doigts écartés |
| 7 | 12,21 → 13,21 | 30 | 3 | 20–22 | 3,00 s | doigts écartés qui bougent |
| 8 | 13,21 → 13,98 | 23 | 3 | 23–25 | 2,30 s | mains qui redescendent |
| 9 | 14,21 → 15,17 | 29 | 3 | 26–28 | 2,90 s | mains sur la tête |
| 10 | 15,21 → 15,68 | 14 | 3 | 29–31 | 1,40 s | les mains retombent |
| 11 | 15,78 → 16,41 | 19 | 3 | 32–34 | 1,90 s | elle rit |
| 12 | 16,38 → 16,95 | 17 | 3 | 35–37 | 1,70 s | elle rit encore |
| 13 | 16,95 → 17,38 | 13 | 3 | 38–40 | 1,30 s | dernier geste |

Total : **844 images, 28,16 s** (référence : 28,13 s). Les longueurs de boucle sont celles de la référence, réaction par réaction. Chaque rejeu est un plan à part dans CapCut (40 plans), avec son propre chiffre (40 textes sur une piste).

Passages choisis sur les mouvements du rush (début et fin des gestes mesurés image par image) et vérifiés sur images (début, milieu, fin de chaque passage).

Choix de cette V2 (pas des règles) : ordre = ordre du rush ; longueurs de boucle copiées de la référence ; mêmes légende et style que la V1.

Fichiers : `plan_V2.csv` (40 lignes, pour CapCut : début de chaque plan sur la 1re image), `plan_V2_mp4.csv` (mêmes plans, début 4 ms plus tôt pour que ffmpeg garde la 1re image), `plan_demo.csv` (extrait). Commandes : `commandes-et-parametres.md`.

**Musique (V2)** : mêmes réglages que la V1, recalculés pour 28,16 s : départ 0,04 s, fondu d'entrée 0,15 s, fondu de sortie 2,0 s, aucun quasi-silence dans la fenêtre ; −14,9 LUFS, pic −2,9 dBFS. Non écoutée ; autorisation inconnue.
