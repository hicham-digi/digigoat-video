# REPRISE — état du projet (2026-11-24)

> À lire en premier quand on reprend le projet. Concis : les détails sont dans les documents cités.

## 1. Objectif du système

Produire des vidéos courtes pour les marques clientes de Digigoat (Pacini Granby, Pacini Marché Central, Importations Alain, Hormeta, Auto Spa Sainte-Julie), à partir de rushes, d'un sujet, d'une vidéo de référence et de consignes. **Livrable par défaut : un projet CapCut modifiable** (un clip par plan, texte modifiable, musique sur sa piste), que l'utilisateur finit lui-même dans CapCut Pro (Windows). Seule Pacini Granby a été travaillée. L'utilisateur débute avec Claude Code : explications simples, comptes rendus courts, en français.

## 2. Ce qui fonctionne, et ce qui a réellement été testé

| Brique | État | Testé |
| --- | --- | --- |
| Structure du dépôt, fichiers de marque (`clients/`) | En place. Pacini Granby partiellement remplie, les 4 autres marques en modèles « À compléter » | — |
| `scripts/premontage.ps1` (prémontage MP4, segments, musique, texte) | Fonctionne | Sur l'essai Décors de Noël : reproduit la V3 et la V4 à l'identique (SSIM 1,000000, audio identique) ; arrêts volontaires (orientation, plan) ; refus d'une sortie dans les rushes |
| `scripts/capcut_projet.py` (projet CapCut) | Fonctionne | Dans **CapCut 9.8.0.4213** : ouverture, 12 plans, texte, musique, fondus modifiables ; suppression d'un plan avec fermeture de l'espace ; ajustement du texte et de la musique ; sauvegarde et réouverture ; mode `--rushes` : image à l'endroit, plan rallongé en tirant son bord |
| Modèle technique autonome `templates/capcut/modele_technique_v1/modele.json` | Fonctionne, sans trace d'un ancien montage | 0 différence de structure sur 60 rubriques face au projet vérifié ; vérification finale intégrée |
| Orientation fichier par fichier (`--tests-orientation`, `--orientation-par-rush`) | Fonctionne | Sur copies et dossiers factices uniquement (rotations opposées, refus sans décision, images de test, sauvegarde). **Pas encore sur une vraie nouvelle production** |
| Sauvegarde automatique des projets (`--sauvegarde`) | Fonctionne | Sur un dossier factice, jamais sur les vrais projets (la sauvegarde réelle a été faite à la main) |
| Dépôt GitHub | Commit `6cf1247` poussé, local et distant identiques | Vérifié après le push (fait par l'utilisateur dans GitHub Desktop) |

**Non testé** : une autre version de CapCut ; rushes déjà verticaux ou avec rotation intégrée en mode `--rushes` ; `-Transcription` ; une autre marque ; un export final depuis CapCut comparé à la V5 ffmpeg.

## 3. Fichiers et commandes nécessaires

- Instructions permanentes : `CLAUDE.md`. Flux par défaut d'une nouvelle vidéo : `sops/workflow-nouvelle-video.md`. Procédure technique en 3 catégories (technique / préférences validées / choix d'un essai) : `sops/procedure-premontage.md`. Modes d'emploi et commandes exactes : `scripts/README.md`. Projet CapCut V5, sauvegardes, restauration : `clients/pacini-granby/essais/2026-11-24_decors-noel/projet-capcut_V5.md`.
- Paramètres de marque avec statuts (valide / essai / à valider / à compléter) : `clients/pacini-granby/parametres-script.json`.
- Outils déjà installés (rien à installer) : Windows PowerShell 5.1, ffmpeg 7.1 et ffprobe (Chocolatey), Python 3.13 (toujours lancer `python -I`), git de GitHub Desktop (`%LOCALAPPDATA%\GitHubDesktop\app-*\resources\app\git\cmd\git.exe`).
- Commande type d'une nouvelle production (CapCut **fermé**) :

```powershell
python -I scripts\capcut_projet.py --nom "NOM" --plan <plan.csv> --rushes "<dossier>" --tests-orientation "<dossier des images>"
python -I scripts\capcut_projet.py --nom "NOM" --plan <plan.csv> --rushes "<dossier>" --orientation-par-rush "DGM_0001=anti-horaire;..." --musique "<piste>" --depart <s> --fondu-entree 0.02 --fondu-sortie 2.0 --texte "ligne 1|ligne 2" --sauvegarde "C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES"
```

- Emplacements locaux (hors dépôt) : rushes Pacini Granby `C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\RUSHES` ; essais `...\PACINI GRANBY\ESSAIS\` (V1 à V5, `segments_V5\`, `musique\`, `texte\`, `sorties-script\`) ; sauvegardes `C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES\` ; projets CapCut `%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft`.

## 4. État actuel du montage CapCut de l'utilisateur — **ne pas modifier**

Projet **« Pacini Granby - Decors Noel V5 »** (premier de la liste CapCut). L'utilisateur l'a modifié lui-même après ma génération (12 plans à l'origine). État relevé le 2026-11-24 à 13:46 :

- **11 plans, 21,1 s** : 01 cadeaux, 02 lutin-lampe, 03 père-noel-violon, **11 vin-versé (déplacé en 4ᵉ position)**, 04 village-neige, 05 étagère-lutins, 06 orignal, 07 couronne-noel, 08 casse-noisettes, 10 lutin-bouteille, 12 bas-cheminée. **Le plan des spaghettis (09) est retiré.**
- Texte « Une ambiance chaleureuse / pour le temps des Fêtes » (Californian FB, taille CapCut 4,16, au centre) et musique (départ 6,70 s, fondus 0,02 s / 2,0 s) sur toute la durée de 21,1 s.
- Seule intervention de ma part depuis : `draft_agency_config.json` (liste `marterials` vidée, chemin résiduel d'un autre montage), avec sauvegarde préalable et contrôles (timeline identique).
- **Sauvegardes** dans `...\SAUVEGARDES\` : `capcut-projets_avant-V5_2026-11-24` (26 projets d'origine, 1 326 fichiers, vérifiée) et `capcut-V5_etat-actuel_2026-11-24_1345` (le V5 avec ses modifications, avant mon nettoyage). Index : `root_meta_info.json.bak_before_*` dans le dossier des projets. Restauration : voir `projet-capcut_V5.md`.
- Mes deux projets de test sont dans la corbeille de CapCut.
- **Règle** : ne jamais écrire dans ce projet ni piloter CapCut pendant que l'utilisateur y travaille (vérifier `Get-Process CapCut`). Le V5 final sera exporté par l'utilisateur depuis CapCut.

## 5. Décisions

**Validées par l'utilisateur** (détail dans `procedure-premontage.md`, catégorie 2) : français québécois ; public familles de classe moyenne et élevée ; ton gourmand, naturel, énergique ; montage dynamique ; musique d'ambiance un peu décontractée ; couleurs et police du guide de marque ; ne jamais reprendre d'offres ou d'éléments d'un autre restaurant ; direction visuelle de la V4 (texte) **pour cette vidéo seulement** ; flux par défaut (projet CapCut, modèle autonome, rushes sources, plan préparé par Claude) ; **orientation analysée par Claude fichier par fichier, questions à l'utilisateur seulement pour les rushes ambigus, en un seul message**.

**Choix propres à l'essai, jamais des règles permanentes** : durée, sélection et ordre des plans, départ musical à 6,70 s, fondus, rotation anti-horaire de **ces** rushes, texte (Californian FB 26,7 px, centre à 49,96 %, ombre), format 9:16 de test.

**Encore ouvertes** (rien à inventer) :
- autorisation d'utiliser la musique (fichier d'origine non identifiable) et écoute (paroles) ;
- police : licence de Californian FB et accord du client (la police de marque du guide est Montserrat Regular) ;
- points du guide de marque « à valider » : 9:16, musique sans paroles explicites, consentement des personnes, promotions autorisées par le siège, « MD » dans « Bar à PainMD » ; bouteille de vin visible (guide) ;
- code noir `000000` à confirmer ; **fichier de logo manquant** ; contact client ; approbation du client ;
- lisibilité du texte sur le plan du foyer (fond très clair) et rendu sur téléphone ; niveau sonore de la V5 (−15,6 LUFS, pic −1,0 dBFS) ;
- aucun texte de parole : pas de SRT (aucune transcription française disponible).

## 6. Limites connues et pièges

- **CapCut** : testé en 9.8.0.4213 seulement ; doit être fermé pour ajouter un projet ; supprimer le **plan 01 supprime aussi le texte** (lié, car il commence au même instant) ; ombre et interligne du texte approximatifs ; police affichée « System » ; plans en mode `--segments` non rallongeables (utiliser `--rushes`) ; chemins des médias absolus (ne pas déplacer `segments_V5\`, `musique\`).
- **Piloter l'interface** : la fenêtre de CapCut peut être réduite (la ramener avec `ShowWindow`) ; demander aussi l'accès à `capcut.exe` ; le bouton OK de « Move to Trash » chevauche la tuile Design Studio (clic parasite possible) ; l'utilisateur peut travailler en même temps.
- **Git** : le terminal n'a pas les identifiants GitHub ; le push est fait par l'utilisateur dans GitHub Desktop (« Push origin ») ou échoue. Le caractère privé du dépôt n'a pas pu être vérifié.
- **Technique** : `premontage.ps1` doit rester en UTF-8 **avec BOM** (PowerShell 5.1) ; dans les filtres ffmpeg, `metadata=print:file=` veut un chemin relatif ; pas de détection de visages, de logos ni de texte promotionnel ; zones de sécurité des réseaux (haut 250, bas 450, côtés 130 px) = hypothèses.
- Les analyses de musique (départ, fin) sont faites sur le signal, **pas à l'oreille**.

## 7. Prochaine étape : une deuxième vidéo Pacini Granby

L'utilisateur fournit : **le dossier des rushes, le sujet, la référence, ses consignes** (musique, texte, durée, ton). Ensuite, Claude suit `sops/workflow-nouvelle-video.md` : inventaire des rushes, images de test d'orientation et analyse fichier par fichier (une question groupée pour les ambigus), analyse des médias et de la référence, **plan CSV préparé par Claude** avec notes, sauvegarde complète des projets CapCut (CapCut fermé), génération du projet, vérification de l'ouverture, compte rendu court. Les éléments « encore ouverts » ci-dessus ne bloquent pas, mais sont à rappeler (musique, police, logo). Après la deuxième vidéo Pacini Granby : décider avec l'utilisateur quelles préférences de marque deviennent permanentes, puis passer aux autres marques.
