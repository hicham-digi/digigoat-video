# Flux par défaut pour une nouvelle vidéo

> Ce que tu fournis : **le dossier des rushes, le sujet, la vidéo de référence et tes consignes.** Claude prépare le reste (analyse, plan CSV, projet CapCut) à partir des médias **réellement analysés**. Le flux technique est décrit dans `sops/procedure-premontage.md` et `scripts/README.md`.

## Valeurs par défaut

| Sujet | Par défaut |
| --- | --- |
| Livrable | Un **projet CapCut modifiable** (un clip par plan, texte modifiable, musique sur sa piste), pas un MP4 fusionné. Un prémontage MP4 n'est produit que sur demande |
| Structure du projet | **Modèle technique autonome** `templates/capcut/modele_technique_v1/modele.json` |
| Liaison des plans | **Rushes sources** avec points d'entrée et de sortie (`--rushes`) : les plans restent rallongeables dans CapCut |
| Orientation | Analysée par Claude **fichier par fichier** sur l'image de test de chaque rush, jamais présumée ni déduite de la session de tournage. L'utilisateur n'est sollicité que pour les fichiers **restés ambigus**, dans **un seul message** groupé |
| Plan CSV | **Préparé par Claude** après analyse des médias, avec une note par ligne |
| Sons d'origine | Coupés dans le projet (sons non écoutés par Claude) |

## Étapes (faites par Claude)

1. **Lire** `CLAUDE.md`, les fichiers de la marque dans `clients/<marque>/` et le brief s'il existe. Repérer les champs « À compléter » et ne rien inventer.
2. **Inventorier les rushes** en lecture seule (`ffprobe` : format, durée, rotation, fréquence, son). Rien n'est modifié ni déplacé.
3. **Orientation de chaque fichier** : `capcut_projet.py --tests-orientation <dossier>` crée une image par rush (origine | horaire | anti-horaire). Claude **regarde chaque image lui-même** et décide en citant l'indice (texte lisible, verre ou objet à l'endroit, gravité, bas du cadre, personnes). Il n'y a **pas de validation manuelle systématique** de chaque rush par l'utilisateur.
   - **Décidé** : au moins un indice net et aucun indice contradictoire. La décision et son indice sont notés dans `plan-de-montage.md`.
   - **Ambigu** : aucun indice net (vue en plongée, mur ou nappe uniforme, flou), ou indices contradictoires. Claude cherche d'abord des indices supplémentaires (autres images du même rush, reflets, gravité, rushes voisins). S'il reste un doute, le fichier est **ambigu**.
   - **Questions** : les fichiers ambigus, et eux seulement, sont présentés à l'utilisateur dans **un seul message groupé** (nom du fichier, image de test, hypothèse et raison du doute). Tant qu'ils ne sont pas tranchés, le projet n'est pas généré.
4. **Analyser les médias** : planches de 5 images ou plus par rush (orientation appliquée), netteté (`blurdetect`), niveau sonore, et repérage de ce que l'outil ne détecte pas : personnes identifiables, promotions, marques tierces, alcool, éléments hors sujet. Les rushes écartés et les raisons sont écrits.
5. **Analyser la référence** par mesures (nombre de coupes, durée des plans, transitions, texte à l'écran), en séparant **observé** et **consigne de l'utilisateur**. Une caractéristique observée n'est pas une règle.
6. **Préparer le plan CSV** (`clients/<marque>/essais/<date>_<sujet>/plan.csv`, colonnes `ordre;rush;debut;duree;nom;note`) : passages choisis, ordre, durées, selon le sujet, la référence et les consignes. Un fichier `plan-de-montage.md` explique chaque choix et chaque rejet.
7. **Musique et texte** : selon les consignes. Le départ musical est analysé sur le signal (pas à l'oreille) ; la police, la taille et la position viennent des consignes ou de la référence mesurée.
8. **Sauvegarde avant toute modification des projets CapCut** : CapCut **fermé**, puis `--sauvegarde <dossier>` (copie complète des projets, contrôlée) et sauvegarde de l'index. Le chemin de la copie est confirmé à l'utilisateur.
9. **Générer le projet CapCut** (`scripts/capcut_projet.py --rushes … --orientation-par-rush …`). Aucun projet existant n'est touché : seul l'index reçoit une entrée.
10. **Vérifier l'ouverture dans CapCut** quand c'est possible : le projet s'ouvre, les plans sont à l'endroit, le texte et la musique sont présents et modifiables. Rapporter ce qui est vérifié et ce qui ne l'est pas.
11. **Compte rendu court** : ce qui est prêt, ce qui est vérifié, ce qui reste à vérifier par l'utilisateur (son, musique, licence, personnes, rendu sur téléphone).

## Rappels

- Les choix d'une vidéo (plans, ordre, durées, départ musical, rotation de **ces** fichiers) ne deviennent jamais des règles permanentes sans confirmation.
- Un projet CapCut existant n'est jamais modifié sans demande explicite. Si l'utilisateur travaille dans CapCut, ne pas piloter son interface ni écrire dans son projet.
- Les rushes, musiques et exports restent hors du dépôt.

## Efficacité et contrôles — directives de l'utilisateur (2026-11-24, après l'essai 2)

Contexte : la V2 « réactions » a pris environ 24 min de traitement (mesures : `clients/pacini-granby/essais/2026-11-24_reactions-drinks/mesures-temps_V2.md`). L'utilisateur demande, pour les prochaines productions :

1. **Réutiliser les outils corrigés et les formats déjà validés.** Ne pas développer de nouvelle fonction si elle n'est pas nécessaire au brief. Les outils actuels (`premontage.ps1`, `capcut_projet.py`, `controle_V2.py`) couvrent déjà le texte fixe, le compteur et les plans répétés.
2. **Séparer les contrôles de production et les contrôles de développement.**

| | Contrôles de production (toujours) | Contrôles de développement (seulement si besoin) |
| --- | --- | --- |
| Quand | À chaque vidéo | Un défaut détecté, ou une fonction de l'outil modifiée |
| Contenu | Rush lisible et orientation décidée ; plan (rush, début, durée, total) ; durée du MP4 ou du projet ; texte, musique et plans présents ; ouverture du projet ; sauvegarde faite ; rushes d'origine intacts | Analyse image par image du MP4 (ex. `controle_V2.py`), non-régression SSIM d'anciens essais, comparaisons exhaustives |
| Coût mesuré | secondes | quelques dizaines de secondes à plusieurs minutes |

3. **Compteur** : vérifier d'abord les **valeurs et les timecodes** dans le plan et dans le projet (40 valeurs de 1 à 40, +1 à chaque fois, chaque valeur alignée sur le début et la durée de son plan, aucun chevauchement) ; puis contrôler seulement **quelques images aux changements** (première image de chaque nouveau chiffre, dernière du précédent). Relancer le contrôle exhaustif (`controle_V2.py`) **seulement si une anomalie apparaît**.
4. **Questions** : les regrouper en **un seul message**. Comptes rendus **courts**.
5. **Temps par étape** : relever à chaque production le temps de l'analyse, de la génération, du rendu, de la sauvegarde et des contrôles, **à partir d'horodatages réels** (jamais d'estimations), puis nommer les étapes les plus longues. Modèle : `mesures-temps_V2.md`. Ce qui n'est pas mesuré est écrit comme tel.

Rappel de prudence : un projet CapCut que l'utilisateur a modifié n'est **jamais régénéré** ni modifié. S'il est ouvert dans CapCut (vérifier `Get-Process CapCut` et l'heure de dernière écriture du projet), ne pas l'ouvrir, même en lecture, sans en avoir parlé.

Les ajustements que l'utilisateur fait lui-même dans CapCut ne deviennent des préférences qu'après qu'il en a **donné la liste** et dit lesquels sont réutilisables (choix de la vidéo ou règle).

## Évaluer la matière avant de construire le découpage — directive de l'utilisateur (2026-11-24, après la V2 de l'essai 2)

Constat : pour la vidéo « réactions », l'objectif de 40 chiffres a été suivi sans se demander si le rush le permettait. L'utilisateur a ramené la vidéo à 20 chiffres et 15 s (6 réactions, `analyse-export-utilisateur_V2.md`). Pour les prochaines vidéos, **avant de bâtir le plan** :

1. **Repérer les réactions (ou plans) distincts et réellement exploitables** dans le rush : gestes nets, contrastés, utilisables seuls.
2. **Évaluer la pertinence des répétitions**, pas seulement leur faisabilité technique : une réaction répétée doit rester drôle ou utile à chaque rejeu.
3. **Adapter le compteur et la durée au contenu disponible**, tout en gardant une **progression continue** du compteur jusqu'au nombre retenu (1, 2, 3 … N, +1 à chaque fois, aucun saut).
4. **Utiliser la référence comme guide de mécanique et de style**, pas comme un gabarit chiffré à copier.
5. **Nombre et durée indicatifs** (ex. « 15-20 s », « 1, 2, 3, etc. », un nombre cité en exemple) : Claude **peut les adapter** et explique son choix en une ou deux phrases.
6. **Nombre et durée imposés explicitement** comme contraintes obligatoires : si les rushes ne les soutiennent pas, **signaler le conflit avant le rendu** (avec ce que la matière permet), sans rendre d'abord.

**Format « Réactions avec compteur »** : les principes confirmés par l'utilisateur (2026-11-24), la synchronisation par défaut du chiffre avec la coupe, ce qui est propre à la vidéo et ce qui n'est pas généralisé à la marque sont dans **`sops/format-reactions-compteur.md`**.

Pour l'essai 2, la version exportée par l'utilisateur est **la référence du résultat qu'il préfère** pour cette vidéo : l'analyser avant de lui demander de décrire ses changements. Ses ajustements restent des choix de cette vidéo tant qu'il ne les a pas confirmés comme règles.

**Piège constaté (essai 2, confirmé involontaire par l'utilisateur)** : dans CapCut, supprimer ou raccourcir des plans ne déplace pas les textes des chiffres, qui sont sur une piste séparée. Dans la version modifiée, 7 chiffres sont apparus 3 images (0,1 s) après la coupe. Conséquences : (1) c'est un défaut, jamais une préférence ; (2) au contrôle de production, vérifier l'alignement du chiffre sur la coupe aux changements ; (3) après une modification de l'utilisateur dans CapCut, rappeler que les chiffres sont à recaler ou à supprimer avec leur plan. Aucune fonction n'est ajoutée pour l'instant.

## Modification ciblée : conserver les éléments validés — directive de l'utilisateur (2026-11-24, validation de la V3 de l'essai 2)

Quand l'utilisateur demande **une modification ciblée** (ex. corriger l'alignement du chiffre), seul ce qui est demandé change. Tout le reste, **déjà validé ou choisi par lui**, est conservé tel quel : notamment **la police, la taille et la position du texte**, mais aussi les passages, l'ordre, la musique et les durées. Ne rien remplacer sans demande explicite.

1. **Reprendre les valeurs de la version précédente**, pas des valeurs par défaut (une police ou une taille « par défaut » n'est jamais un réglage validé).
2. **Réglage introuvable** (police, taille, position, couleur) : le chercher d'abord dans le **projet CapCut source**, quand c'est possible, **en lecture seule** : le projet de l'utilisateur n'est jamais modifié, CapCut n'est pas piloté s'il y travaille (voir « Rappel de prudence »), et la lecture se fait si besoin sur une copie.
3. **Approximation nécessaire** (valeur introuvable, mesurée à l'œil ou par proxy) : la **signaler à l'utilisateur avant de l'appliquer**, avec la valeur proposée et son origine. Pas d'application silencieuse.
4. Si un changement hors demande semble utile, le **proposer** en une phrase au lieu de l'appliquer.

Origine : la V3 de l'essai 2 avait repris un réglage de texte choisi par Claude faute de connaître celui de l'export de l'utilisateur ; la V3 a été **validée pour cet essai** (2026-11-24) avec cette correction de méthode pour la suite.
