# Commandes et paramètres — Décors de Noël · Essai V1/V2

Archive des commandes réellement utilisées pour cet essai, afin d'en faire plus tard une procédure réutilisable (après ta validation du résultat).

> **Statut : archive de la V1 et de la V2, pas une procédure.** Rien ici n'est une règle permanente. Les chemins sont ceux de cet essai.
>
> **Depuis la V3**, ces étapes (et celles de la musique et du texte) sont reprises dans `scripts/premontage.ps1`. La procédure en trois catégories est dans `sops/procedure-premontage.md`, le mode d'emploi dans `scripts/README.md`. Le départ musical de 7,4 s ci-dessous concerne la **première piste** : il est obsolète et ne doit pas être réutilisé. La V3 utilise une autre piste (départ à 6,70 s).

## Environnement

- Windows 11, PowerShell 5.1.
- FFmpeg 7.1 (`essentials_build` de gyan.dev), déjà installé sur le poste : `C:\ProgramData\chocolatey\bin\ffmpeg.exe` et `ffprobe.exe`. Rien n'a été installé pour l'essai.
- Encodeur H.264 : `libx264` (CPU).
- Non disponibles sur le poste : reconnaissance vocale en français, détection de visages, `whisper`, `pdftoppm`.

## Dossiers

| Rôle | Chemin |
| --- | --- |
| Rushes (lecture seule) | `C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\RUSHES` |
| Sorties | `C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_decors-noel\` (`segments\`, `premontage\`) |
| Musique fournie | `C:\Users\Hicham\Desktop\Digigoat\AUDIO\SONGS\Nat King Cole The Christmas Song Merry Christmas To You.mp3` |
| Documentation | `clients/pacini-granby/essais/2026-11-24_decors-noel/` |

## Paramètres

### Nécessités techniques (propres à ces rushes)

| Paramètre | Valeur | Pourquoi |
| --- | --- | --- |
| Rotation | `transpose=2` (90° anti-horaire) | Rushes filmés à la verticale sans indicateur de rotation. Vérifié sur images : `transpose=1` donne un Père Noël à l'envers |
| Taille | `scale=1080:1920:flags=lanczos` | 2160×3840 → 1080×1920, exactement 9:16, sans recadrage |
| Plage de couleurs | `in_range=full:out_range=tv`, `format=yuv420p` | La source est `yuvj420p` (plage complète) : évite un décalage de contraste |
| Images par seconde | `fps=30000/1001` (29,97) | Fréquence des rushes |
| Marquage colorimétrique | `-colorspace bt709 -color_primaries bt709 -color_trc bt709` | Source en BT.709 |

### Choix de l'essai [Test] (pas des règles)

| Paramètre | Valeur |
| --- | --- |
| Qualité vidéo | Segments : `-crf 14 -preset slow` · Prémontage : `-crf 16 -preset slow` |
| Audio des segments | AAC 256 kb/s, 48 kHz (son d'origine conservé dans les segments) |
| Coupes | Franches, sans transition |
| Fondu audio à chaque coupe (version avec audio d'origine) | 0,04 s en entrée et en sortie |
| Durée des plans | 1,5 à 2,5 s (voir `plan-de-montage.md`) |
| Durée totale | 19,6 s (cible de l'essai : 15 à 25 s) |
| Musique : point de départ | 7,4 s dans la piste (voir ci-dessous) |
| Musique : fondus | Entrée 0,15 s, sortie 1,5 s (de 18,12 s à 19,62 s) |
| Musique : niveau | Aucun gain appliqué (source conservée) |
| Résultat musique | −15,1 LUFS intégrés, pic −2,6 dBFS |

Pourquoi 7,4 s : l'analyse de l'énergie de la piste montre un début quasi silencieux (de −44 à −56 dB) pendant environ 7,5 s, puis un son net à partir de 7,5 s. Départ choisi juste avant cette attaque pour que la musique soit audible dès la première image. Je n'ai pas pu écouter : le passage choisi n'est pas validé musicalement.

## Commandes

### 1. Inspecter un fichier
```powershell
ffprobe -v error -print_format json -show_format -show_streams -- "<fichier>"
```
Les propriétés utiles : codec, résolution, images/s, rotation (`side_data_list`), `pix_fmt`, plage de couleurs, durée.

### 2. Planche de contrôle (images échantillonnées)
```powershell
# 5 images réparties sur la durée d'un rush ($d = durée en secondes), 5 colonnes
ffmpeg -v error -y -i "<rush>" -vf "transpose=2,fps=5/$d,scale=216:384,tile=5x1" -frames:v 1 "<sortie>.png"
```
Planche du prémontage fini, une image toutes les 0,5 s :
```powershell
ffmpeg -v error -y -i "<premontage>.mp4" -vf "fps=2,scale=135:240,tile=10x4" -frames:v 1 "<planche>.png"
```

### 3. Déterminer le sens de rotation
```powershell
ffmpeg -v error -y -ss 1.0 -i "<rush>" -frames:v 1 -vf "split=2[a][b];[a]transpose=1,scale=-1:640[ca];[b]transpose=2,scale=-1:640[cc];[ca][cc]hstack" "<test>.png"
```
Regarder laquelle des deux moitiés est à l'endroit (ici : la deuxième, `transpose=2`).

### 4. Exporter un segment
```powershell
ffmpeg -v error -y -ss <début> -i "<rush>.MOV" -t <durée> `
  -vf "transpose=2,scale=1080:1920:flags=lanczos:in_range=full:out_range=tv,fps=30000/1001,format=yuv420p,setsar=1" `
  -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 `
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart "<segment>.mp4"
```
Découpage utilisé (`début` et `durée` en secondes) :

| # | Rush | Début | Durée | Nom |
| --- | --- | --- | --- | --- |
| 01 | DGM_3793 | 0,5 | 1,5 | cadeaux |
| 02 | DGM_3787 | 0,2 | 1,8 | lutin-lampe |
| 03 | DGM_3790 | 1,0 | 2,2 | pere-noel-violon |
| 04 | DGM_3791 | 0,2 | 2,0 | village-neige |
| 05 | DGM_3784 | 0,4 | 2,2 | etagere-lutins |
| 06 | DGM_3792 | 0,2 | 2,0 | orignal |
| 07 | DGM_3788 | 1,0 | 1,8 | couronne-noel |
| 08 | DGM_3789 | 1,0 | 1,8 | casse-noisettes |
| 09 | DGM_3794 | 0,2 | 1,8 | lutin-bouteille |
| 10 | DGM_3795 | 2,4 | 2,5 | bas-cheminee |

Nom de fichier : `NN_RUSH_nom.mp4`.

### 5. Prémontage muet (V1)
Assemble les 10 segments (`-i` répété pour chaque segment, dans l'ordre) :
```powershell
ffmpeg -v error -y -i seg01.mp4 -i seg02.mp4 ... -i seg10.mp4 `
  -filter_complex "[0:v][1:v][2:v][3:v][4:v][5:v][6:v][7:v][8:v][9:v]concat=n=10:v=1:a=0[v]" `
  -map "[v]" -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 `
  -an -movflags +faststart "premontage_V1_sans-musique_muet.mp4"
```

### 6. Prémontage avec audio d'origine (V1)
Même assemblage, avec pour chaque segment `i` de durée `d` : `[i:a]afade=t=in:st=0:d=0.04,afade=t=out:st=<d-0.04>:d=0.04[ai]`, puis `[0:v][a0][1:v][a1]...concat=n=10:v=1:a=1[v][a]`, sorties `-c:a aac -b:a 256k -ar 48000`. Fichier : `premontage_V1_sans-musique_audio-origine.mp4`. Remplacée par la version muette + musique (V2) suite à ton retour.

### 7. Ajouter la musique (V2)
```powershell
ffmpeg -v error -y -i "premontage_V1_sans-musique_muet.mp4" -ss 7.4 -t 19.62 -i "<musique>.mp3" `
  -map 0:v:0 -map 1:a:0 -c:v copy `
  -af "afade=t=in:st=0:d=0.15,afade=t=out:st=18.12:d=1.5" `
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart "premontage_V2_musique-fournie.mp4"
```
`-map 1:a:0` ignore la pochette PNG contenue dans le MP3. La vidéo est copiée sans réencodage (588 images, identiques au V1).

### 8. Analyse de la musique
```powershell
# Début quasi silencieux ?
ffmpeg -hide_banner -i "<musique>.mp3" -t 40 -af silencedetect=n=-45dB:d=0.2 -f null NUL
# Énergie par 0,5 s
ffmpeg -v error -y -t 40 -i "<musique>.mp3" -af "asetnsamples=n=22050:p=0,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=env.txt" -f null NUL
# Loudness et pic du résultat
ffmpeg -hide_banner -i "<fichier>" -af ebur128=peak=true -vn -f null NUL
```

### 9. Analyse des coupes (référence et prémontage)
```powershell
# Score de changement pour chaque image
ffmpeg -v error -y -i "<video>.mp4" -vf "select='gte(scene,0)',metadata=print:file=scores.txt" -an -f null NUL
```
Lecture : un **pic isolé** (≥ 0,12, images voisines ≈ 0) = coupe franche. Plusieurs images élevées de suite = fondu. Les pics faibles (0,12 à 0,15) sont à vérifier visuellement avant de les compter. Détection rapide d'ensemble : `select='gt(scene,0.3)'`, mais ce seuil peut manquer des coupes.

### 10. Contrôles automatiques
```powershell
# Images noires / figées
ffmpeg -hide_banner -i "<video>.mp4" -vf "blackdetect=d=0.1:pic_th=0.98,freezedetect=n=0.001:d=0.5" -an -f null NUL
# Niveau sonore
ffmpeg -hide_banner -i "<video>.mp4" -af volumedetect -vn -f null NUL
# Nombre d'images
ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of csv=p=0 "<video>.mp4"
```

### 11. Lire le guide de marque PDF
`pdftoppm` n'est pas installé. Les pages ont été converties en images avec le lecteur PDF intégré à Windows (`Windows.Data.Pdf`, appelé depuis PowerShell 5.1), à 1400 px de large, puis lues. Le script n'a pas été conservé : à refaire si nécessaire.

## Pièges rencontrés

- **Accents dans les chemins** : le nom `Guide réseau sociaux.pdf` ne se retrouvait pas avec le chemin saisi (accent décomposé). Lister le dossier avec `Get-ChildItem` et utiliser le nom réel.
- **Emoji dans un nom de fichier** : copier d'abord la vidéo dans un dossier de travail sous un nom simple.
- **Seuil de détection de coupes** : `scene > 0.3` a manqué des coupes dans la référence. Utiliser le score par image et vérifier visuellement les cas douteux.
- **Rushes sans indicateur de rotation** : toujours regarder une image avant de décider du recadrage.

## À décider avant d'en faire une procédure

- Garder ou non `crf 14` / `crf 16`, `preset slow` et le fondu audio de 0,04 s.
- Le choix du point de départ de la musique (méthode : trouver la première attaque, puis valider à l'écoute).
- Le niveau de la musique (ici sans gain : −15,1 LUFS).
- La durée moyenne des plans (1,96 s ici, contre 1,15 s pour la référence).
- Quels paramètres deviennent des règles dans `montage.md`, un par un, après ta validation.
