# digigoat-video

Système de travail pour le montage vidéo des marques clientes : directives par marque, procédures, modèles de brief et instructions pour Claude Code.

- Utilisateurs : le responsable du montage (À compléter) et Guan (rôle : À compléter)
- Poste : Windows · Logiciel de montage : CapCut Pro

> État actuel : structure, modèles, premières directives de Pacini Granby, un premier essai (« Décors de Noël ») et un script de prémontage (`scripts/premontage.ps1`, procédure dans `sops/procedure-premontage.md`). Il n'y a pas encore d'agents actifs. Les fichiers et champs marqués « À compléter » attendent tes informations.

## Contenu du dépôt

> **Pour reprendre le projet : `REPRISE.md`** (état, tests, décisions ouvertes, prochaine étape).

| Emplacement | À quoi ça sert |
| --- | --- |
| `REPRISE.md` | Point de reprise : état du système, montage CapCut en cours, décisions ouvertes, prochaine étape |
| `CLAUDE.md` | Instructions permanentes lues par Claude Code (comment travailler, quoi lire, quelles règles respecter) |
| `README.md` | Ce mode d'emploi |
| `sops/` | Procédures : montage, contrôle qualité, emplacements des fichiers lourds |
| `clients/` | Un dossier par marque, avec 4 fichiers : `marque.md`, `montage.md`, `references.md`, `retours-client.md` |
| `templates/brief-video.md` | Formulaire à remplir pour chaque nouvelle vidéo |
| `scripts/` | Script de prémontage `premontage.ps1` et son mode d'emploi (`scripts/README.md`) |
| `.claude/agents/` | Futurs agents spécialisés (vide pour l'instant) |
| `.gitignore` | Exclut du dépôt les rushes, exports et clés d'accès |

## Marques

| Marque | Dossier |
| --- | --- |
| Importations Alain | `clients/importations-alain/` |
| Hormeta | `clients/hormeta/` |
| Pacini Granby | `clients/pacini-granby/` |
| Pacini Marché Central | `clients/pacini-marche-central/` |
| Auto Spa Sainte-Julie | `clients/auto-spa-ste-julie/` |

Les directives de chaque marque restent séparées. Pour les deux Pacini, les offres, coordonnées et appels à l'action sont propres à chaque restaurant.

## Utiliser le système pour une nouvelle vidéo

1. Copie `templates/brief-video.md`, renomme la copie et remplis le brief.
2. Ouvre Claude Code dans ce dossier et indique la marque et le brief à utiliser.
3. Claude lit `CLAUDE.md`, le brief et les quatre fichiers de la marque, puis signale tout ce qui est encore « À compléter ».
4. Après les retours du client, ajoute les corrections validées dans `clients/<marque>/retours-client.md` (avec la date et la règle à appliquer).

## Où vont les gros fichiers

Les rushes, exports, musiques et projets CapCut restent dans tes dossiers de production ou sur ton stockage habituel, pas dans GitHub. Les emplacements sont notés dans `sops/emplacements-fichiers.md`.

Un lien Drive seul ne suffit pas : pour que Claude traite un fichier, celui-ci doit être disponible sur l'ordinateur.

## Principes

- « À compléter » = information pas encore fournie. Rien n'est inventé.
- Les exemples de style sont illustratifs, pas des directives approuvées.
- Aucun contenu existant n'est remplacé sans explication préalable.

## Pour commencer, rassemble par marque

- Deux ou trois vidéos approuvées
- Les logos et polices autorisés
- Tes règles de montage actuelles
- Les corrections récurrentes du client