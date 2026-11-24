# Instructions permanentes — digigoat-video

Ce fichier est lu par Claude Code au début de chaque session. Il décrit comment travailler dans ce dépôt.

> **Quand on reprend le projet (nouvelle session, contexte perdu, ou « on reprend »), lis d'abord `REPRISE.md`** : état du système, ce qui est testé, état du montage CapCut de l'utilisateur (à ne pas modifier), décisions ouvertes et prochaine étape. Mets-le à jour en fin de session si l'état change.

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
   - `retours-client.md` : corrections validées et règles à appliquer ;
   - si présents : `offres-et-services.md` (services, produits, offres datées) et `organisation.md` (contacts, responsabilités, circuit de validation). Index : `clients/README.md`.
3. Les procédures du dossier `sops/` (montage, contrôle qualité, emplacements des fichiers).

## Flux par défaut pour une nouvelle vidéo

L'utilisateur fournit seulement **le dossier des rushes, le sujet, la référence et ses consignes**. Suis `sops/workflow-nouvelle-video.md` :

- livrable = **projet CapCut modifiable** (`scripts/capcut_projet.py`), pas un MP4 fusionné ;
- **modèle autonome** `templates/capcut/modele_technique_v1/modele.json` ;
- plans **liés aux rushes sources** (`--rushes`) avec points d'entrée et de sortie, donc rallongeables ;
- **orientation analysée par toi fichier par fichier** sur l'image de test de chaque rush, jamais présumée ; ne demande à l'utilisateur que pour les fichiers **restés ambigus**, **dans un seul message groupé**, sans validation manuelle systématique ;
- **plan CSV préparé par toi** à partir des médias réellement analysés, avec une note par ligne ; **évalue d'abord la matière** (réactions distinctes, pertinence des répétitions) et adapte nombre et durée s'ils sont indicatifs ;
- format **« Réactions avec compteur »** : suis `sops/format-reactions-compteur.md` (principes confirmés, chiffre synchronisé avec la coupe par défaut, contrôles de production courts) ;
- avant toute modification du dossier des projets CapCut : CapCut fermé, sauvegarde complète vérifiée (`--sauvegarde`), chemin confirmé à l'utilisateur ; ne jamais toucher un projet existant, ni piloter CapCut pendant que l'utilisateur y travaille.

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
10. **Modification ciblée = on conserve le reste.** Quand l'utilisateur demande un changement précis, garde les autres éléments validés (police, taille et position du texte, passages, musique…). Un réglage introuvable se cherche d'abord dans le projet CapCut source, en lecture seule ; toute approximation est signalée avant d'être appliquée (voir `sops/workflow-nouvelle-video.md`).
11. **Un champ resté entre crochets ne confirme jamais une information** (règle de l'utilisateur, 2026-11-24). Libellé de modèle (« [NOM] », « [CANAUX UTILISÉS] »), menu d'options (« [OUI / NON] », « [COURRIEL, WHATSAPP] ») ou valeur qui reprend le libellé : ne rien déduire, ne rien enregistrer comme réponse. Écrire « À compléter » (champ vide) ou « À confirmer » (valeur seulement vue dans un champ resté entre crochets). Une valeur n'est confirmée que si elle est écrite explicitement par l'utilisateur, avec sa source.
12. **Production : ne demander que le nécessaire.** Lors d'une vidéo, ne demander que les informations manquantes **utiles à cette vidéo**, en un seul message groupé. Ne jamais bloquer un montage sur des coordonnées, tarifs, contacts ou autres champs « À compléter » qui ne seront pas utilisés dans la vidéo. Les fiches de marque restent partiellement renseignées et servent de base (décision du 2026-11-24 : l'enrichissement documentaire est arrêté pour le moment).
13. **Fiches de marque : une information, un seul fichier.** Pour chaque information, indique la source et la date, et distingue directive actuelle / exemple historique / à confirmer. Les légendes ou textes de référence ne deviennent pas des directives de montage sans confirmation.

## État actuel du projet

- La structure, la documentation et les modèles existent.
- Un script de prémontage existe, à la demande de l'utilisateur : `scripts/premontage.ps1` (mode d'emploi : `scripts/README.md`). Il utilise seulement PowerShell et ffmpeg, déjà installés.
- La procédure est dans `sops/procedure-premontage.md`. Elle sépare trois catégories : les étapes techniques réutilisables, les préférences de marque **confirmées par l'utilisateur**, et les choix **propres à un essai**.
- Il n'y a pas encore d'agents spécialisés actifs (`.claude/agents/` est vide).

Les choix d'un essai (durée, sélection et ordre des plans, passage musical, fondus, rotation propre à des fichiers) ne deviennent jamais des règles permanentes sans confirmation explicite de l'utilisateur.

## Carte du dépôt

| Emplacement | Contenu |
| --- | --- |
| `CLAUDE.md` | Ces instructions générales |
| `README.md` | Mode d'emploi pour l'utilisateur et Guan |
| `sops/` | Procédures de montage et de contrôle qualité |
| `clients/` | Directives propres à chaque marque (5 dossiers) |
| `templates/brief-video.md` | Formulaire à remplir pour chaque nouvelle vidéo |
| `scripts/` | Script de prémontage `premontage.ps1` et son mode d'emploi |
| `.claude/agents/` | Futures instructions d'agents spécialisés |
| `.gitignore` | Fichiers exclus du dépôt (rushes, exports, clés) |
