# Commandes et paramètres — essai 2 (2026-11-24)

Depuis le dossier du dépôt (`cd C:\Users\Hicham\Documents\GitHub\digigoat-video`). Le rush est copié dans `C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_reactions-drinks\rushes\` (l'original reste dans Téléchargements).

## MP4 de prévisualisation

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\premontage.ps1 -Rushes "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_reactions-drinks\rushes" -Brief clients\pacini-granby\essais\2026-11-24_reactions-drinks\brief.md -Client clients\pacini-granby -Sortie "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\sorties-script" -Plan clients\pacini-granby\essais\2026-11-24_reactions-drinks\plan.csv -Orientation aucune -Musique "C:\Users\Hicham\Desktop\RÉFÉRENCE\Musique référence\snapgram.io_kixa7ebkaxsq.mp3" -Texte "Notre réaction au nombre|de drinks que tu commandes" -TexteCentreY 0.52 -Compteur "1;2;3;4;5;6;10;15;20;30" -CompteurCentreY 0.585 -DureeCible "15-20"
```

Sortie : `...\sorties-script\2026-11-24_141355_reactions-selon-le-nombre-de-drinks-essa\` (copies : `previsualisation_reactions-drinks.mp4` et `..._sans-texte.mp4` dans le dossier de l'essai). Le départ musical (0,04 s) a été proposé par le script.

## Projet CapCut (CapCut fermé)

```powershell
python -I scripts\capcut_projet.py --nom "Pacini Granby - Reactions drinks" --plan clients\pacini-granby\essais\2026-11-24_reactions-drinks\plan.csv --rushes "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_reactions-drinks\rushes" --musique "C:\Users\Hicham\Desktop\RÉFÉRENCE\Musique référence\snapgram.io_kixa7ebkaxsq.mp3" --depart 0.04 --fondu-entree 0.15 --fondu-sortie 2.0 --texte "Notre réaction au nombre|de drinks que tu commandes" --police "C:/Users/Hicham/AppData/Local/Microsoft/Windows/Fonts/Montserrat-Regular.ttf" --police-nom "Montserrat" --taille-capcut 8.1 --texte-y -0.04 --compteur "1;2;3;4;5;6;10;15;20;30" --compteur-y -0.17 --sauvegarde "C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES"
```

- Aucune orientation à fournir : le rush est vertical (largeur < hauteur), sans rotation intégrée.
- Sauvegarde faite avant l'écriture : `C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES\capcut-projets_avant-pacini_granby_reactions_drinks_20261124_1416` (1 009 fichiers, contrôlée). Index : `root_meta_info.json.bak_before_pacini_granby_reactions_drinks` dans le dossier des projets.
- Conversion des positions de texte : position CapCut y = 1 − 2 × (fraction de la hauteur) → légende 0,52 → −0,04 ; compteur 0,585 → −0,17. Taille CapCut = pixels / 6,42 (52 px → 8,1).

## Nouveautés des outils pour cet essai

- `premontage.ps1` : `-Compteur "1;2;…"` (un chiffre par plan, même style que `-Texte`, exige `-Texte`) et `-CompteurCentreY` (défaut 0,585). Sans ces options, rien ne change.
- `capcut_projet.py` : `--compteur` et `--compteur-y` (une piste de texte séparée, un clip par plan).
- Contrôle après l'ajout : la même commande sans `-Compteur` redonne une vidéo sans texte identique (SSIM 1,000000) et un script qui se termine normalement. Dans la zone de la légende, la vidéo avec compteur diffère très légèrement de celle sans compteur (SSIM 0,990, arrondis de la chaîne de superposition). Les essais précédents (Décors de Noël) n'ont **pas** été rejoués après cet ajout.

## V2 — mécanique de la référence (40 plans, compteur 1 à 40)

Plans : `plan_V2.csv` (CapCut) et `plan_V2_mp4.csv` (MP4). Dossier du rush et musique : voir ci-dessus. Chiffres : `-Compteur "1;2;…;40"` / `--compteur "1;2;…;40"`.

```powershell
$e = "clients\pacini-granby\essais\2026-11-24_reactions-drinks"
$cnt = (1..40) -join ';'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\premontage.ps1 -Rushes "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_reactions-drinks\rushes" -Brief "$e\brief.md" -Client clients\pacini-granby -Sortie "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\sorties-script" -Plan "$e\plan_V2_mp4.csv" -Orientation aucune -Musique "C:\Users\Hicham\Desktop\RÉFÉRENCE\Musique référence\snapgram.io_kixa7ebkaxsq.mp3" -Texte "Notre réaction au nombre|de drinks que tu commandes" -TexteCentreY 0.52 -Compteur $cnt -CompteurCentreY 0.585 -DureeCible "26-30"
python -I scripts\capcut_projet.py --nom "Pacini Granby - Reactions drinks V2" --plan "$e\plan_V2.csv" --rushes "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_reactions-drinks\rushes" --musique "C:\Users\Hicham\Desktop\RÉFÉRENCE\Musique référence\snapgram.io_kixa7ebkaxsq.mp3" --depart 0.04 --fondu-entree 0.15 --fondu-sortie 2.0 --texte "Notre réaction au nombre|de drinks que tu commandes" --police "C:/Users/Hicham/AppData/Local/Microsoft/Windows/Fonts/Montserrat-Regular.ttf" --police-nom "Montserrat" --taille-capcut 8.1 --texte-y -0.04 --compteur $cnt --compteur-y -0.17 --sauvegarde "C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES"
python -I "$e\controle_V2.py" "<dossier de sortie du script>" "$e\plan_V2_mp4.csv" "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_reactions-drinks\rushes\DJI_20000116224450_0013_D.MP4"
```

- Sortie MP4 V2 : `...\sorties-script\2026-11-24_145805_reactions-selon-le-nombre-de-drinks-essa\` (copies dans le dossier de l'essai : `previsualisation_reactions-drinks_V2.mp4` et `_sans-texte`).
- Sauvegarde des projets CapCut avant la V2 : `C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES\capcut-projets_avant-pacini_granby_reactions_drinks_v2_20261124_1504` (1 045 fichiers, contrôlée). Index : `root_meta_info.json.bak_before_pacini_granby_reactions_drinks_v2`.
- Correction faite dans `premontage.ps1` (option `-Compteur`) : les changements de chiffre sont calés sur des **numéros d'image** et non des secondes (le 1er essai décalait un chiffre d'une image et faisait apparaître deux chiffres sur l'image de coupe). Les générateurs n'ont pas été modifiés autrement.
- Plans en images (à 29,97 i/s) : 12 × 3 rejeux + 1 × 4 ; premier jeu de plans `plan.csv` (V1) conservé.

## V3 — version corrigée de l'export de l'utilisateur (20 chiffres, 6 réactions)

```powershell
$e = "clients\pacini-granby\essais\2026-11-24_reactions-drinks"
$cnt = (1..20) -join ';'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\premontage.ps1 -Rushes "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_reactions-drinks\rushes" -Brief "$e\brief.md" -Client clients\pacini-granby -Sortie "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\sorties-script" -Plan "$e\plan_V3_mp4.csv" -Orientation aucune -Musique "C:\Users\Hicham\Desktop\RÉFÉRENCE\Musique référence\snapgram.io_kixa7ebkaxsq.mp3" -Texte "Notre réaction au nombre|de drinks que tu commandes" -PoliceTexte "$env:LOCALAPPDATA\Microsoft\Windows\Fonts\Montserrat-Bold.ttf" -TexteTaille 53 -TexteCentreY 0.52 -Compteur $cnt -CompteurCentreY 0.585 -DureeCible "15-20"
python -I scripts\capcut_projet.py --nom "Pacini Granby - Reactions drinks V3" --plan "$e\plan_V3.csv" --rushes "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_reactions-drinks\rushes" --musique "C:\Users\Hicham\Desktop\RÉFÉRENCE\Musique référence\snapgram.io_kixa7ebkaxsq.mp3" --depart 0.04 --fondu-entree 0.15 --fondu-sortie 2.0 --texte "Notre réaction au nombre|de drinks que tu commandes" --police "C:/Users/Hicham/AppData/Local/Microsoft/Windows/Fonts/Montserrat-Bold.ttf" --police-nom "Montserrat Bold" --taille-capcut 8.26 --texte-y -0.04 --compteur $cnt --compteur-y -0.17 --sauvegarde "C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES"
```

- Sortie MP4 V3 : `...\sorties-script\2026-11-24_154052_reactions-selon-le-nombre-de-drinks-essa\` (copie : `previsualisation_reactions-drinks_V3.mp4`). Sauvegarde : `...\SAUVEGARDES\capcut-projets_avant-pacini_granby_reactions_drinks_v3_20261124_1543` (1 085 fichiers). Aucun générateur modifié pour la V3.
