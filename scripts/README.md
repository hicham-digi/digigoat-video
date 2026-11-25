# scripts/

## premontage.ps1

Prépare un prémontage vertical à partir de rushes : vérifications, orientation, conversion, segments séparés, assemblage, musique et texte facultatifs, contrôles techniques et rapport.

- **Outils** : Windows PowerShell 5.1 et ffmpeg/ffprobe, déjà installés sur ce poste. Rien n'est installé ni téléchargé.
- **Originaux** : jamais modifiés. Le script refuse une sortie placée dans le dossier des rushes.
- **Sorties** : un **nouveau dossier horodaté** à chaque exécution. Rien n'est écrasé.
- **Procédure complète** (trois catégories de choix) : `sops/procedure-premontage.md`.

### Ce qu'il faut fournir

| Paramètre | Obligatoire | Rôle |
| --- | --- | --- |
| `-Rushes` | Oui | Dossier des rushes (`.mov`, `.mp4`, `.m4v`, `.mkv`, `.avi`, `.mts`, `.mxf`) |
| `-Brief` | Oui | Fichier du brief (`.md`). Seuls le titre et le nombre de « À compléter » sont lus. Une copie est gardée |
| `-Client` | Oui | Dossier du client, par exemple `clients\pacini-granby`. Le script y lit `parametres-script.json` |
| `-Sortie` | Oui | Dossier parent des sorties. Le script y crée un sous-dossier pour cet essai |
| `-Plan` | Non (recommandé) | Fichier CSV des plans choisis (voir plus bas). **Sans plan, le script s'arrête après avoir proposé un plan** |
| `-Orientation` | Selon les rushes | `anti-horaire`, `horaire`, `recadrer-centre`, `aucune`. Par défaut `demander` : arrêt avec image de test si les rushes sont en paysage sans indicateur de rotation |
| `-OrientationParRush` | Non | Décision rush par rush, prioritaire sur `-Orientation` : `"DGM_3828=anti-horaire;DGM_3832=horaire"`. À utiliser quand des rushes d'une même session n'ont pas tous la même orientation. Sans décision, le script s'arrête et crée **une image de test par rush** concerné |
| `-Musique` | Non | Piste `.mp3` ou autre. Le départ et les fondus sont proposés par analyse du signal |
| `-Texte` | Non | Texte à afficher pendant toute la vidéo. Un `|` force un saut de ligne ; sinon le script coupe en deux lignes si c'est trop large |
| `-PoliceTexte` | Non | Fichier de police (`.ttf`) à utiliser à la place de celle du client. Refusé s'il n'existe pas |
| `-TexteTaille` | Non | Taille du texte en pixels (sur la hauteur de sortie), à la place de la valeur du client |
| `-TexteCentreY` | Non | Position verticale : centre du bloc de texte, en fraction de la hauteur (`0.5` = milieu). Remplace la marge basse. Le script mesure le texte réellement dessiné et le recentre, quelle que soit la police |
| `-TexteInterligne` | Non | Interligne, en multiple de la taille (défaut 1,27) |
| `-TexteOmbreFlou`, `-TexteOmbreDecalage` | Non | Flou et décalage vertical de l'ombre, en pixels (défauts 6 et 3). À réduire avec la taille du texte |
| `-Compteur` | Non | Un chiffre par plan, affiché pendant ce plan, avec la police, la taille et le style du texte : `"1;2;3;..."`. Exige `-Texte`. Sortie : `texte\compteur_NN.png` et `compteur.txt`. Ajouté pour l'essai « réactions » |
| `-CompteurCentreY` | Non | Position verticale du compteur, en fraction de la hauteur (défaut `0.585`) |
| `-DepartMusique`, `-FonduEntree`, `-FonduSortie`, `-GainMusiqueDb` | Non | Pour imposer un réglage musical (secondes, dB). Avec `-DepartMusique`, le script **garde ce départ** mais analyse la fenêtre et la fin de la musique à partir de lui : il signale un quasi-silence dans la fenêtre et ajuste les fondus (d'entrée et de sortie) à la durée de la vidéo. Utile quand la vidéo change de durée mais que le départ musical est validé |
| `-SonOrigine` | Non | `couper` (par défaut, version muette) ou `garder` |
| `-DureeCible` | Non | Par exemple `"15-25"` : avertissement seulement |
| `-DureePlan` | Non | Durée (s) de chaque extrait dans la proposition automatique |
| `-Transcription` | Non | Fichier SRT **que vous avez déjà**. Le script ne transcrit pas |
| `-Auto` | Non | Produit à partir de la proposition technique, sans plan validé. Sortie marquée « NON VALIDÉE » |

Les valeurs propres à une marque (police, taille et marges du texte, format, etc.) viennent de `parametres-script.json` du dossier client. Chaque valeur y porte un **statut** : `valide`, `essai`, `a-valider` ou `a-completer`. Le rapport indique, pour chaque paramètre utilisé, d'où il vient et son statut.

### Format du plan (CSV, séparateur `;`)

```
ordre;rush;debut;duree;nom;note
01;DGM_3793;0.5;1.5;cadeaux;Ouverture sur le mouvement
02;DGM_3787;0.2;1.8;lutin-lampe;
```

`rush` : nom du fichier avec ou sans extension. `debut` et `duree` en secondes, décimales avec un point. Exemple réel : `clients\pacini-granby\essais\2026-11-24_decors-noel\plan.csv`.

### Ce que le script automatise, et ce qui reste humain

| | Script | Décision humaine |
| --- | --- | --- |
| Vérification des fichiers, conversion, découpe, assemblage, export, contrôles | Oui | Non |
| Orientation | Applique une rotation lue dans le fichier | **Choisir le sens si le fichier n'en porte pas** |
| Sélection des plans | Propose les extraits les plus nets | **Choisir réellement les plans** (contenu, promotions, personnes, marques) |
| Ordre et rythme | Applique le plan fourni | **Ordre, durée de chaque plan, rythme** |
| Musique | Propose un départ net et des fondus | **Écouter, licence, goût** |
| Texte | Rend et mesure | **Contenu, lisibilité, test sur téléphone** |
| SRT de parole | Non (copie un SRT fourni) | **Transcription fiable** |

### Ce que contient un dossier de sortie

```
AAAA-MM-JJ_HHMMSS_<titre>\
  segments\                un fichier par plan (1080x1920, son d'origine conservé)
  premontage\              premontage_<muet|musique|audio-origine>[_avec-texte|_sans-texte].mp4
  texte\                   (si -Texte) texte.txt, texte.srt, texte_overlay.png, texte_parametres.md
  sous-titres\             (seulement si -Transcription valide) transcription.srt
  controle\
    rapport.md             contrôles, paramètres et statuts, ce qui reste à vérifier
    commandes.log          commandes ffmpeg exactes
    planche-rushes-*.png   5 images par rush, orientation appliquée
    planche-premontage.png une image toutes les 0,5 s
    plan-propose.csv       (sans plan) la proposition technique
    plan-utilise.csv, plan-fourni.csv, brief-utilise.md, parametres-client-utilises.json
```

### Codes de sortie

| Code | Signification |
| --- | --- |
| 0 | Terminé, ou arrêt volontaire pour un plan à valider (aucun prémontage produit) |
| 1 | Erreur (message affiché, détail dans le rapport si le dossier existe) |
| 3 | Arrêt volontaire : orientation à décider |

### Mode d'emploi simple

Toutes les commandes se lancent depuis le dossier du dépôt. Pour l'ouvrir dans PowerShell :

```powershell
cd C:\Users\Hicham\Documents\GitHub\digigoat-video
```

**1. Premier passage, sans rien décider.** Le script vérifie les fichiers. Si l'orientation est inconnue, il s'arrête et crée une image de test dans `controle\`. Regardez-la : de gauche à droite, image d'origine, rotation horaire, rotation anti-horaire. Choisissez celle où le décor est à l'endroit.

**2. Relancer avec l'orientation, sans plan.** Le script crée les planches de contrôle et `controle\plan-propose.csv`, puis s'arrête.

**3. Corriger le plan.** Copiez `plan-propose.csv`, retirez les rushes à écarter, réordonnez, ajustez `debut` et `duree`, puis enregistrez-le (par exemple dans le dossier de l'essai).

**4. Produire.** Relancez avec `-Plan`, et si voulu `-Musique` et `-Texte`.

**5. Lire `controle\rapport.md`**, regarder les planches et la vidéo, puis finir dans CapCut.

Un exemple générique (à adapter) :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\premontage.ps1 -Rushes "D:\rushes" -Brief clients\x\essais\e\brief.md -Client clients\x -Sortie "D:\sorties" -Plan clients\x\essais\e\plan.csv -Orientation anti-horaire
```

## capcut_projet.py

Crée un **projet CapCut modifiable** (un clip par plan, texte modifiable, musique sur sa propre piste) à partir d'un plan et de segments déjà préparés. Python 3 (déjà installé) et ffprobe. Aucun MP4 fusionné.

- Il ajoute un **nouveau** dossier de projet et une entrée dans l'index `root_meta_info.json`, après en avoir fait une sauvegarde (`root_meta_info.json.bak_before_<nom>`). Il ne modifie aucun projet existant et n'écrase jamais un projet du même nom.
- **CapCut doit être fermé** (il refuse sinon).
- Il utilise un **modèle technique autonome**, sans média ni texte d'un ancien montage : `templates/capcut/modele_technique_v1/modele.json` (documenté dans `templates/capcut/modele_technique_v1/LISEZ-MOI.md`). Plus aucune dépendance à un de tes projets CapCut. Il lit seulement les identifiants d'appareil dans un de tes projets récents, sans les stocker.
- `--essai-local <dossier>` écrit le projet dans un dossier au lieu de CapCut (aucun index modifié). `--limiter N` ne garde que les N premiers plans (projet de test).

**Deux façons de relier les plans** (exactement une des deux) :

| Option | Durée des plans dans CapCut | Quand l'utiliser |
| --- | --- | --- |
| `--segments <dossier>` | **Fixe** : chaque clip a exactement la durée exportée. On peut le **raccourcir**, pas le rallonger | Reproduire une version déjà exportée (c'est le cas de la V5) |
| `--rushes <dossier> --orientation <sens>` | **Rallongeable** : chaque clip pointe vers le rush avec son point d'entrée et sa durée (colonnes `debut` et `duree` du plan). On peut le rallonger, le raccourcir ou le décaler tant qu'il reste du rush de chaque côté | **Les prochaines productions** |

Avec `--rushes`, le script applique la rotation et l'échelle que CapCut utilise lui-même pour ces rushes (−90° et 1,7778 pour des rushes 4K filmés à la verticale sans indicateur : valeurs identiques à celles de ton projet « Pates flambees »).

**L'orientation se décide fichier par fichier** : pour un rush paysage sans rotation intégrée, le script refuse de deviner. Le flux :

```powershell
# 1. une image de test par rush (origine | horaire | anti-horaire), puis arrêt
python -I scripts\capcut_projet.py --nom "NOM" --plan <plan.csv> --rushes "<dossier>" --tests-orientation "<dossier des images>"
# 2. après analyse de chaque image par Claude (l'utilisateur ne tranche que les rushes restés ambigus) : une décision par rush
python -I scripts\capcut_projet.py --nom "NOM" --plan <plan.csv> --rushes "<dossier>" --orientation-par-rush "DGM_0001=anti-horaire;DGM_0002=horaire" --musique "<piste>" --depart <s> --fondu-entree 0.02 --fondu-sortie 2.0 --texte "ligne 1|ligne 2" --sauvegarde "<dossier des sauvegardes>"
```

`--orientation` (sens par défaut pour tous) existe, mais n'est à utiliser que si tous les rushes du plan ont été vérifiés un à un. `--sauvegarde <dossier>` copie **tous** les projets CapCut existants (sans la corbeille) et contrôle le nombre de fichiers avant d'écrire quoi que ce soit. Test : 3 rushes dont deux sens opposés (rotations +90° et −90° appliquées), refus sans décision, images de test, sauvegarde sur un dossier factice.

Le flux complet par défaut (qui prépare le plan, quoi vérifier) : `sops/workflow-nouvelle-video.md`.
- Mode d'emploi, ce qui est modifiable et la restauration : `clients/pacini-granby/essais/2026-11-24_decors-noel/projet-capcut_V5.md`.

Projet de la V5 (la commande qui l'a créé) :

```powershell
python -I scripts\capcut_projet.py --nom "Pacini Granby - Decors Noel V5" --plan clients\pacini-granby\essais\2026-11-24_decors-noel\plan_V5.csv --segments "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_decors-noel\segments_V5" --musique "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_decors-noel\musique\snapgram.io_qk5jbiotjaut.mp3" --depart 6.7 --fondu-entree 0.02 --fondu-sortie 2.0 --texte "Une ambiance chaleureuse|pour le temps des Fêtes"
```

Options du compteur (essai « réactions », 2026-11-24) : `--compteur "1;2;3;..."` (un chiffre par plan, piste de texte séparée, mêmes police et taille que `--texte`) et `--compteur-y` (position CapCut, défaut −0,17 = 58,5 % de la hauteur). Position CapCut y = 1 − 2 × fraction de la hauteur. Police et taille se règlent avec `--police`, `--police-nom`, `--taille-capcut` (pixels / 6,42). Vérifié dans CapCut 9.8.0.4213 : ouverture, piste de chiffres, légende en Montserrat Regular. Rush **déjà vertical sans rotation intégrée** (DJI 1728×3072) : aucune rotation appliquée (rotation 0, échelle 1), plan lié au rush, image à l'endroit.

Valeurs par défaut du texte : Californian FB, taille CapCut 4,16 (= 26,7 px à 1080×1920), au centre. Le même nom de projet ne peut pas être recréé : choisis un autre `--nom`.

Vérifié dans CapCut 9.8.0.4213 : ouverture, 12 plans, texte, musique et fondus modifiables, suppression d'un plan avec fermeture de l'espace, sauvegarde, réouverture. Mode `--rushes` : ouverture, image à l'endroit et plein cadre (rotation −90°, échelle 178 %), **rallongement d'un plan** en tirant son bord droit (1 s 15 → 1 s 23). Non vérifié : une version de CapCut différente, des rushes déjà verticaux ou avec rotation intégrée en mode `--rushes`.

### Relancer exactement l'essai « Décors de Noël »

```powershell
cd C:\Users\Hicham\Documents\GitHub\digigoat-video
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\premontage.ps1 -Rushes "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\RUSHES" -Brief clients\pacini-granby\essais\2026-11-24_decors-noel\brief.md -Client clients\pacini-granby -Sortie "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\sorties-script" -Plan clients\pacini-granby\essais\2026-11-24_decors-noel\plan.csv -Orientation anti-horaire -Musique "C:\Users\Hicham\Desktop\RÉFÉRENCE\Musique référence\snapgram.io_qk5jbiotjaut.mp3" -Texte "Une ambiance chaleureuse pour le temps des Fêtes"
```

Durée : environ 2 minutes. Le résultat se retrouve dans un nouveau sous-dossier de `...\ESSAIS\sorties-script\`. C'est la **V3** (texte Montserrat 52 px, en bas).

### Relancer exactement la V4 (texte ajusté sur la référence de Noël)

Même commande, avec le texte sur deux lignes (`|`) et les réglages du texte :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\premontage.ps1 -Rushes "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\RUSHES" -Brief clients\pacini-granby\essais\2026-11-24_decors-noel\brief.md -Client clients\pacini-granby -Sortie "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\sorties-script" -Plan clients\pacini-granby\essais\2026-11-24_decors-noel\plan.csv -Orientation anti-horaire -Musique "C:\Users\Hicham\Desktop\RÉFÉRENCE\Musique référence\snapgram.io_qk5jbiotjaut.mp3" -Texte "Une ambiance chaleureuse|pour le temps des Fêtes" -PoliceTexte "C:\Windows\Fonts\CALIFR.TTF" -TexteTaille 26.7 -TexteInterligne 1.07 -TexteCentreY 0.4996 -TexteOmbreFlou 3 -TexteOmbreDecalage 2
```

Ces valeurs viennent de la mesure de **cette** référence : elles ne valent pas pour une autre vidéo.

### Relancer exactement la V5 (deux rushes ajoutés)

Même commande que la V4, avec le plan à 12 plans, l'orientation décidée pour les deux nouveaux rushes, et le départ musical de la V4 conservé :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\premontage.ps1 -Rushes "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\RUSHES" -Brief clients\pacini-granby\essais\2026-11-24_decors-noel\brief.md -Client clients\pacini-granby -Sortie "C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\sorties-script" -Plan clients\pacini-granby\essais\2026-11-24_decors-noel\plan_V5.csv -Orientation anti-horaire -OrientationParRush "DGM_3828=anti-horaire;DGM_3832=anti-horaire" -Musique "C:\Users\Hicham\Desktop\RÉFÉRENCE\Musique référence\snapgram.io_qk5jbiotjaut.mp3" -DepartMusique 6.7 -Texte "Une ambiance chaleureuse|pour le temps des Fêtes" -PoliceTexte "C:\Windows\Fonts\CALIFR.TTF" -TexteTaille 26.7 -TexteInterligne 1.07 -TexteCentreY 0.4996 -TexteOmbreFlou 3 -TexteOmbreDecalage 2
```

Durée : environ 2 minutes et demie. Les deux nouveaux plans (`DGM_3828`, `DGM_3832`) et leurs passages sont dans `plan_V5.csv`. Ces choix sont ceux de cet essai.

### Dépannage

| Message ou problème | Cause probable | Solution |
| --- | --- | --- |
| « l'exécution de scripts est désactivée » | Politique d'exécution de PowerShell | Utiliser la commande ci-dessus (`-ExecutionPolicy Bypass` ne vaut que pour cette exécution) |
| Accents illisibles dans la console | Page de codes de la console | Sans effet sur les fichiers produits, ils restent en UTF-8 |
| « Entrée introuvable » | Chemin erroné | Vérifier le chemin. Un nom avec accents peut ne pas correspondre à la saisie : le copier depuis l'Explorateur |
| Code 3, « Orientation à décider » | Rushes en paysage sans indicateur de rotation | Regarder `controle\orientation_*.png`, puis relancer avec `-Orientation` |
| Code 0 mais aucun prémontage | Pas de `-Plan` | Normal : le script attend un plan validé. Voir l'étape 3 |
| « ffmpeg et ffprobe sont introuvables » | Hors du PATH | Le script n'installe rien. Vérifier l'installation |

### Tests effectués (2026-11-24)

| Test | Résultat |
| --- | --- |
| Essai complet (plan, orientation, musique, texte) | Terminé en environ 2 min. Les deux vidéos sont **identiques** à la V3 faite à la main (SSIM 1,000000, mêmes niveaux sonores) |
| Sans orientation | Arrêt volontaire, code 3, image de test créée |
| Sans plan | Proposition technique écrite, arrêt volontaire, code 0 |
| `-Auto -SonOrigine garder`, sans musique ni texte | Prémontage `audio-origine` produit, rapport « SORTIE NON VALIDÉE » |
| Dossier de rushes inexistant | Erreur claire, code 1 |
| Sortie dans le dossier des rushes | Refusée avant toute création de dossier, code 1 (un défaut de l'ordre des opérations a été trouvé puis corrigé pendant ce test) |
| Rushes d'origine | Nom, taille et date inchangés après chaque exécution |
| Nouvelles options de texte (V4) | Calibrées en faisant rendre la phrase de la référence : largeur 172 contre 169 px, hauteur 37,3 contre 37 px, centre vertical 50,0 % contre 49,9 % (à 720×1280). La V4 sans texte est identique à la V3 sans texte (SSIM 1,000000) |
| Non-régression après ajout des options | Sans les nouvelles options, le script reproduit toujours la V3 (SSIM 1,000000, avec et sans texte) |
| Défaut corrigé | Le fichier `texte_parametres.md` généré contenait une tabulation parasite devant « texte.srt » : corrigé |
| V5 : 14 rushes, 2 orientations décidées rush par rush, départ musical imposé | Terminé en 142 s. Les 10 plans d'origine sont identiques à la V4 (SSIM 1,000000 par segment), l'audio de 0 à 15 s a la même empreinte, l'image du texte aussi |
| Non-régression après ajout de `-OrientationParRush` et de l'analyse à départ imposé | La commande de la V4 relancée avec `-DepartMusique 6.7` redonne la V4 : vidéo identique (SSIM 1,000000, avec et sans texte) et audio identique (même empreinte MD5) |
| Arrêt sur l'orientation avec 14 rushes | Une image de test par rush (14 sur 14), code 3. Un défaut a été corrigé : le nom du rush était vide dans le message |

## Montage long (client Dimitri) : outils ajoutés le 2026-11-24

Autorisés par l'utilisateur : Whisper local en environnement isolé, et adaptation du générateur CapCut. Procédure : `sops/procedure-montage-long.md`. Aucune donnée n'est envoyée à un service externe (`HF_HUB_OFFLINE=1`, pas de télémétrie).

**Environnement isolé (hors dépôt)** : `C:\Users\Hicham\Desktop\Digigoat\OUTILS\transcription\` : `venv\` (Python 3.13, faster-whisper 1.2.1, CTranslate2 4.9.1, bibliothèques CUDA 12 en paquets pip), `modeles\faster-whisper-large-v3\` (2,9 Go). Les trois scripts suivants se lancent avec `venv\Scripts\python.exe` (numpy y est installé).

| Script | Rôle | Interpréteur |
| --- | --- | --- |
| `transcrire.py` | Transcription locale horodatée au mot, **brouillon** : `.json`, `.srt` (sous-titres courts), `.txt` (timecodes), `_a-relire.md` (passages incertains). Langue **obligatoire** (`--langue fr\|en\|auto`). Marqueurs `[à vérifier]` et `[incompris]` (seuils provisoires) | venv |
| `proposer_coupes.py` | Propose des coupes sobres (silences, répétitions, faux départs) avec justification, risque sur le sens et statut (appliquée / à valider / refusée) ; écrit `coupes.csv`, `coupes.md`, le plan CSV, des sous-titres recalés sur les segments gardés | Python standard (`python -I`) |
| `caler_audio.py` | Estime le décalage entre l'audio de la caméra et un audio enregistré à part (corrélation croisée) et donne la valeur `@D` pour le générateur | venv |

**Nouvelles options de `capcut_projet.py`** (sans elles, le projet produit est identique à avant : vérifié) :

| Option | Effet |
| --- | --- |
| `--son-origine garder` | Conserve le son d'origine des prises (volume 1) ; par défaut il est coupé |
| `--audios-separes "RUSH=audio.wav@D"` | Piste audio séparée liée au rush, mêmes points d'entrée et de sortie, décalage `D` en secondes (`temps audio = temps rush + D`, valeur donnée par `caler_audio.py`). Le son de la caméra de ce rush est alors coupé |
| `--sous-titres "RUSH=fichier.srt"` | Un texte modifiable par sous-titre, placé sur la ligne de montage à partir des temps du **rush source**, coupé aux points de coupe, sur une ou plusieurs pistes (aucun chevauchement) |
| `--sous-titres-police`, `-police-nom`, `-taille`, `-y` | Style des sous-titres. Défauts **techniques neutres** (Arial, taille 5, bas de l'image), **pas une préférence** de client ; calibration de la taille non vérifiée hors 1080x1920 |
| `--canevas 1920x1080` | Taille du projet (le modèle est en 1080x1920) |
| Colonnes `zoom;cx;cy` du plan CSV (facultatives) | Recadrage d'un plan : agrandissement `zoom` (>= 1) centré sur le point `cx;cy` de l'image source (0 à 1, virgule ou point). Arrêt si le cadre sort de l'image ou si le plan est tourné. Sans ces colonnes : comportement inchangé (vérifié) |
| `--textes-libres "TEXTE\|début\|fin\|x\|y;..."` ou `--textes-libres-fichier fichier.txt` | Textes positionnés librement (une piste par texte) : secondes sur la ligne de montage (`fin` peut valoir `fin`), `x`/`y` normalisés (centre = 0, haut = +1). Le fichier évite les guillemets dans la ligne de commande (PowerShell 5.1 les coupe) ; une ligne par texte, `#` = commentaire. Utilisé pour l'essai « dispute-addition » |

**Essai synthétique du 2026-11-24** (rush de 50,6 s : voix de synthèse anglaise avec pauses, faux départ, répétitions, réserves ; audio séparé décalé de 0,3 s) :

| Test | Résultat |
| --- | --- |
| Installation | faster-whisper et bibliothèques CUDA installés ; modèle large-v3 téléchargé ; **incompatibilité constatée** entre faster-whisper 1.2.1 et PyAV 19 (lecture audio intégrée) : contournée en lisant le WAV 16 kHz dans `transcrire.py` |
| Transcription GPU (RTX 3060 Ti, float16) | 50,6 s en 3,3 s (x15 temps réel) ; chargement du modèle 6 s |
| Transcription CPU (int8) | 46 s pour 50,6 s (x1,1 temps réel) |
| Langue `auto` | anglais détecté, probabilité 1,00 |
| Texte | Transcription fidèle sur voix de synthèse (réserves « unless », « only if » conservées). Une fausse détection (« image. ») a été marquée `[à vérifier]` |
| Calage audio | -0,300 s retrouvé, confiance 32 |
| Propositions de coupes | 11 propositions : 5 appliquées (4 silences, 1 répétition de 4 mots), 6 à valider ; 50,6 s -> 36,6 s |
| Projet CapCut (local, `--essai-local`) | 6 plans liés au rush, 6 segments d'audio séparé alignés (décalage vérifié, y compris négatif), 11 sous-titres modifiables recalés sur la ligne de montage, canevas 16:9, son d'origine conservé |
| Non-régression du générateur | Mêmes arguments qu'avant : `draft_content.json` identique à celui de l'ancienne version (identifiants normalisés) |

**Non testés** : ouverture du projet dans CapCut (nouvelles pistes), voix humaine réelle, français, plusieurs voix, bruit de salle, durée longue, calibration de la taille des sous-titres en 16:9, dérive d'horloge d'un audio séparé.

**Non testés** (script de prémontage) : une orientation différente entre deux rushes dans la même exécution (seules des décisions identiques ont été exercées), rushes déjà verticaux, rushes avec rotation intégrée au fichier, `-Transcription`, `-DepartMusique` imposé, rushes sans piste audio avec `-SonOrigine garder`, d'autres marques.
