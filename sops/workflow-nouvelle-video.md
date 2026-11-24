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
