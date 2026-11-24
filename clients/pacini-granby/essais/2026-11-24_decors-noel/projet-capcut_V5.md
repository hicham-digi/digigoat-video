# Projet CapCut modifiable — V5

Projet créé : **« Pacini Granby - Decors Noel V5 »** (24,13 s, 9:16, 30 i/s). Vérifié dans CapCut 9.8.0.4213 le 2026-11-24.

## Ouvrir le projet

1. Ouvre CapCut. Le projet est **le premier** de la liste « Projects ».
2. Double-clique dessus.

Il ne faut pas déplacer ni renommer `segments_V5\` et `musique\` (dans le dossier de l'essai) : CapCut les relie par leur chemin.

## Ce qui est réellement modifiable (vérifié dans CapCut)

| Élément | Dans la timeline | Vérifié |
| --- | --- | --- |
| **12 plans séparés** | Une piste vidéo, un clip par plan, nommés `01_DGM_3793_cadeaux` à `12_DGM_3795_bas-cheminee`. Sons d'origine à 0 | Ouverture, sélection, suppression, annulation |
| **Texte** | Un clip texte modifiable : contenu, police, taille, couleur, position | Sélectionné, panneau Texte ouvert, texte lisible dans l'éditeur |
| **Musique** | Une piste audio indépendante : départ à 6,70 s dans la piste, fondu d'entrée 0,02 s, fondu de sortie 2,0 s, volume 0 dB | Panneau Audio : volume et fondus réglables |
| **Format** | 9:16, 1080×1920, 30 i/s | Panneau Détails |

Les coupes sont franches (aucune transition). Il n'y a pas de réglage visuel à reproduire : la V5 n'en avait pas.

## Supprimer un plan en refermant l'espace

1. Clique sur le plan dans la piste vidéo, puis appuie sur **Suppr**. L'espace se referme tout seul : les plans suivants se décalent vers la gauche. Testé sur le plan 09 : l'espace s'est fermé, le texte et la musique n'ont pas bougé.
2. **Attention au plan 01** : le texte commence au même instant que lui, et CapCut les lie. Supprimer le plan 01 supprime aussi le texte (annulable avec Ctrl+Z). Pour retirer un autre plan, aucun souci.

## Ajuster le texte et la musique à la nouvelle durée

Après la suppression, le texte et la musique dépassent la fin des plans. Pour chacun :

1. Place la souris sur le **bord droit** du clip (texte, puis musique). Le curseur change.
2. Fais glisser ce bord vers la gauche jusqu'à la **fin du dernier plan**.

Testé : la durée totale passe bien à la nouvelle valeur (24 s 04 → 22 s 01 en retirant 2,1 s), et le **fondu de sortie de 2,0 s reste attaché à la nouvelle fin de la musique**. Le départ de la musique (6,70 s) ne change pas. Vérifie à l'écoute que la fin te convient : le passage musical qui précède la coupure a changé.

## Réglages du texte (à connaître)

- Police : Californian FB. CapCut l'affiche « System » dans la liste des polices : c'est normal pour une police chargée depuis le système, le rendu est bien en police à empattements. Si tu la rechoisis, ajoute-la depuis la liste.
- Taille : réglée à 4,16 (CapCut l'affiche « 4 »), équivalent à 26,7 px à 1080×1920 (1 unité CapCut = 6,42 px, calibrée sur un de tes projets exportés). Position : centre de l'image.
- Ombre : approximative (noire à 70 %, vers le bas). Le rendu exact de la V5 vient de ffmpeg, pas de CapCut : compare à `premontage_V5_musique_avec-texte.mp4` si tu veux l'ajuster.
- Interligne : celui par défaut de CapCut (un peu plus serré que dans la V5).

## Sauvegardes et restauration

| Quoi | Où |
| --- | --- |
| Copie complète de tes **projets d'avant** (26 projets, 1 326 fichiers, vérifiée par empreintes) | `C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES\capcut-projets_avant-V5_2026-11-24\` |
| Index des projets avant le projet de test | `...\com.lveditor.draft\root_meta_info.json.bak_before_test_v5_pacini_a_supprimer` |
| Index avant le projet V5 | `...\com.lveditor.draft\root_meta_info.json.bak_before_pacini_granby_decors_noel_v5` |

(`...\com.lveditor.draft` = `C:\Users\Hicham\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft`)

Seuls ont été modifiés dans ce dossier : l'index `root_meta_info.json` (deux entrées ajoutées) et deux nouveaux dossiers de projet. Aucun des 26 projets existants n'a été touché (comparaison par empreinte avant et après).

**Pour tout défaire** (CapCut fermé) :

```powershell
$p = "$env:LOCALAPPDATA\CapCut\User Data\Projects\com.lveditor.draft"
Copy-Item "$p\root_meta_info.json.bak_before_test_v5_pacini_a_supprimer" "$p\root_meta_info.json" -Force
Remove-Item "$p\Pacini Granby - Decors Noel V5", "$p\TEST V5 Pacini (a supprimer)" -Recurse -Force
```

**Pour restaurer un projet précis abîmé** (CapCut fermé), recopie son dossier depuis la sauvegarde :

```powershell
robocopy "C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES\capcut-projets_avant-V5_2026-11-24\NOM DU PROJET" "$env:LOCALAPPDATA\CapCut\User Data\Projects\com.lveditor.draft\NOM DU PROJET" /E
```

## Durée des plans : peut-on les rallonger ?

**Non dans ce projet.** Les 12 clips pointent vers les segments déjà exportés, découpés à la durée exacte de la V5 : CapCut peut les **raccourcir**, pas les rallonger (il n'y a plus de matière avant ni après). Pour rallonger un plan de la V5, il faut ajouter le rush d'origine dans CapCut et refaire le plan à la main.

**Pour les prochaines productions**, le générateur sait lier chaque clip au **rush source** avec son point d'entrée et sa durée (`--rushes`). Le clip peut alors être rallongé ou décalé dans CapCut tant qu'il reste du rush. Vérifié : le plan 1 d'un projet de test est passé de 1 s 15 à 1 s 23 en tirant son bord droit. Détail dans `scripts/README.md`.

## Projets de test

Mes deux projets de test (« TEST V5 Pacini » et « TEST rushes ») ont été supprimés via l'interface CapCut. Ils sont dans la **corbeille de CapCut** (30 jours), donc récupérables. Ton projet V5 et tes 26 projets d'origine n'ont pas été touchés.

## Nettoyage effectué dans ton projet V5 (2026-11-24)

Le fichier `draft_agency_config.json` contenait le chemin d'un autre montage (« Reel Contre-filet.mp4 »), recopié depuis l'ancien modèle lors de la première génération. **Seule** la liste `marterials` de ce fichier a été vidée : le reste du fichier est inchangé.

- Sauvegarde préalable du projet dans son état de ce moment (tes 11 plans et tes ajustements) : `C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES\capcut-V5_etat-actuel_2026-11-24_1345\` (39 fichiers, vérifiés).
- Contrôle : seul ce fichier différait de la sauvegarde ; la timeline (`draft_content.json`) était identique à l'octet près.
- Ouverture dans CapCut : le projet s'ouvre, 11 plans dans ton ordre, texte et musique présents, durée 21 s 03.
- CapCut ré-enregistre le projet à l'ouverture ; la seule différence de contenu constatée ensuite est un arrondi d'une microseconde sur la durée d'un plan (sans effet visible). Le nettoyage tient toujours.

## Limites

- Testé uniquement dans CapCut 9.8.0.4213. Après une mise à jour majeure, le générateur (`scripts/capcut_projet.py`) pourrait devoir être revu.
- Le générateur utilise un modèle technique autonome (`templates/capcut/modele_technique_v1/`) : plus aucun projet CapCut existant n'est nécessaire.
- CapCut doit être **fermé** quand le générateur ajoute un projet (il réécrit l'index en se fermant).
