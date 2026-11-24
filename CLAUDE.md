# Instructions permanentes — digigoat-video

Ce fichier est lu par Claude Code au début de chaque session. Il décrit comment travailler dans ce dépôt.

## Contexte

- Dépôt de travail pour le montage vidéo de plusieurs marques clientes.
- Poste de travail : Windows. Logiciel de montage : CapCut Pro.
- L'utilisateur débute avec Claude Code : explique simplement, étape par étape, en français.
- Marques gérées : Importations Alain, Hormeta, Pacini Granby, Pacini Marché Central, Auto Spa Sainte-Julie.

## Documents à lire avant de travailler sur une vidéo

1. Le brief de la vidéo, rempli à partir de `templates/brief-video.md`.
2. Les quatre fichiers de la marque concernée, dans `clients/<marque>/` :
   - `marque.md` : public, langue, ton, couleurs, polices, logos, éléments à éviter ;
   - `montage.md` : rythme, transitions, cadrage, sous-titres, musique, introduction, fin ;
   - `references.md` : vidéos approuvées et ce qu'il faut reproduire ;
   - `retours-client.md` : corrections validées et règles à appliquer.
3. Les procédures du dossier `sops/` (montage, contrôle qualité, emplacements des fichiers).

## Règles à respecter

1. **N'invente aucune directive.** Si une information est marquée « À compléter » (ou absente), ne la devine pas : signale-le et demande-la à l'utilisateur.
2. **Une marque = ses propres fichiers.** Ne mélange jamais les directives de deux marques, même si le même contact client en gère plusieurs.
3. **Les deux Pacini restent distincts** : offres, coordonnées et appels à l'action de Pacini Granby et de Pacini Marché Central ne se partagent pas.
4. **Les exemples de style sont illustratifs.** Un exemple dans un modèle ou dans ce dépôt n'est pas une directive approuvée. Seul ce qui est écrit dans `references.md` ou `retours-client.md` d'une marque, avec un statut approuvé, fait foi.
5. **Conserve le contenu existant.** Avant de remplacer ou de réécrire un fichier qui contient déjà du texte, explique la modification et attends l'accord de l'utilisateur.
6. **Gros fichiers hors dépôt.** Rushes, exports, musiques et projets CapCut restent dans les dossiers de production de l'utilisateur. Dans le dépôt, on garde seulement leurs emplacements et les instructions pour les utiliser (voir `sops/emplacements-fichiers.md`). Ne commite jamais de vidéos, d'exports, de clés d'accès ni de mots de passe.
7. **Un lien Drive seul ne suffit pas.** Pour traiter un fichier, il doit être accessible localement. Si ce n'est pas le cas, demande à l'utilisateur de le placer à l'emplacement prévu.
8. **Nouvelle correction du client ?** Propose de l'ajouter dans `retours-client.md` de la marque, avec la date et la règle à appliquer aux prochains montages.
9. **N'installe aucun outil et ne crée aucun script ou agent actif sans l'accord explicite de l'utilisateur.**

## État actuel du projet

Seuls la structure, la documentation et les modèles existent. Il n'y a pas encore :

- de scripts d'automatisation (`scripts/` est vide) ;
- d'agents spécialisés actifs (`.claude/agents/` est vide).

## Carte du dépôt

| Emplacement | Contenu |
| --- | --- |
| `CLAUDE.md` | Ces instructions générales |
| `README.md` | Mode d'emploi pour l'utilisateur et Guan |
| `sops/` | Procédures de montage et de contrôle qualité |
| `clients/` | Directives propres à chaque marque (5 dossiers) |
| `templates/brief-video.md` | Formulaire à remplir pour chaque nouvelle vidéo |
| `scripts/` | Futurs programmes d'automatisation |
| `.claude/agents/` | Futures instructions d'agents spécialisés |
| `.gitignore` | Fichiers exclus du dépôt (rushes, exports, clés) |
