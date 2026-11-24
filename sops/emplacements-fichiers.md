# Emplacements des fichiers lourds

Les rushes, exports, musiques et projets CapCut ne sont **pas** dans GitHub. Ce fichier indique où ils se trouvent et comment les utiliser.

> Un lien Drive seul ne suffit pas : Claude doit pouvoir accéder au fichier sur l'ordinateur pour le traiter.
> Si un fichier n'est qu'en ligne, il faut d'abord le télécharger à l'emplacement local prévu.

## Dossiers de production (sur l'ordinateur)

| Contenu | Chemin Windows | Remarques |
| --- | --- | --- |
| Rushes (vidéos brutes) | Pacini Granby : `C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\RUSHES` (autres marques : À compléter) | Les clips DGM_3784 à 3795 sont filmés à la verticale sans indicateur de rotation : rotation de 90° anti-horaire nécessaire |
| Projets CapCut | `C:\Users\Hicham\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft` | Un dossier par projet + l'index `root_meta_info.json`. Ne jamais modifier un projet existant ; CapCut fermé avant d'y ajouter un projet. Corbeille de CapCut : sous-dossier `.recycle_bin` |
| Sauvegardes des projets CapCut | `C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES\` | `capcut-projets_avant-V5_2026-11-24` (26 projets d'origine) et `capcut-V5_etat-actuel_2026-11-24_1345` (V5 avec les modifications de l'utilisateur). Restauration : `clients/pacini-granby/essais/2026-11-24_decors-noel/projet-capcut_V5.md` |
| Exports finaux | À compléter (le V5 sera exporté par l'utilisateur depuis CapCut) | À compléter |
| Essais et prémontages Pacini Granby | `C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\` | Un sous-dossier par essai (ex. `2026-11-24_decors-noel`) avec `segments\` (V1 à V4), `segments_V5\`, `premontage\`, `texte\`, `musique\`, `comparaison\`, `controle_V5\`. Sorties du script : `sorties-script\`. Documentation de l'essai : `clients/pacini-granby/essais/` |
| Musiques | Copie de la piste de l'essai : `...\ESSAIS\2026-11-24_decors-noel\musique\`. Fichiers d'origine : `C:\Users\Hicham\Desktop\RÉFÉRENCE\Musique référence\` et `C:\Users\Hicham\Desktop\Digigoat\AUDIO\` | **Autorisation d'utilisation non confirmée** (voir `REPRISE.md`) |
| Logos officiels | À compléter | Aucun fichier utilisable fourni : seul le logo-texte « PACINI » du guide de marque |
| Polices autorisées | Montserrat Regular : `C:\Users\Hicham\AppData\Local\Microsoft\Windows\Fonts\Montserrat-Regular.ttf` (police du guide) | Californian FB (`C:\Windows\Fonts\CALIFR.TTF`) utilisée seulement pour le texte de la V4 à V5 : licence et accord du client à confirmer |

## Stockage habituel (en ligne)

| Contenu | Service et lien | Qui y a accès |
| --- | --- | --- |
| À compléter | À compléter | À compléter |

## Organisation par marque

Structure de dossiers de production par marque : À compléter

## Nommage des fichiers

À compléter

## Sauvegarde

- Projets CapCut : avant toute génération, copie complète vérifiée dans `C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES\` (option `--sauvegarde` de `scripts/capcut_projet.py`), plus une sauvegarde de l'index `root_meta_info.json.bak_before_<nom>` dans le dossier des projets.
- Rushes, exports, musiques : sauvegarde générale À compléter.
