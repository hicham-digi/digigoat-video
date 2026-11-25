---
name: dg-analyse-reference
description: Analyse une vidéo de référence (rythme, plans, cadrage, textes, transitions, son) en séparant ce qui est mesuré, observé et interprété, puis rend un compte rendu court (cinq observations au maximum, puis les limites). Recommandations sur demande. Analyse et conseil seulement. Appel manuel avec /dg-analyse-reference.
disable-model-invocation: true
---

# Analyse d'une vidéo de référence

Demande de l'utilisateur : $ARGUMENTS

Réponds en français, avec des mots simples.

## Mission et limites strictes

Ce skill **analyse et conseille seulement**. Pendant son exécution :

- Ne modifie aucun montage, aucun projet CapCut, aucun fichier du dépôt et aucun média.
- Ne lance aucun rendu, export ni aperçu, et ne crée aucun projet CapCut (ni `capcut_projet.py`, ni `premontage.ps1`).
- N'envoie rien à un autre service (ni Gemini, ni autre service en ligne). Les images et les textes que tu examines passent par Claude, comme le reste de la session : si la confidentialité d'une vidéo l'interdit, ne l'examine pas et dis-le.
- Ne télécharge aucun média et n'installe rien.
- N'appelle aucun autre skill et ne renvoie pas automatiquement vers un autre skill (dont `find-broll` et `video-editing`).
- Ne change pas le fonctionnement actuel : le livrable d'un montage reste un **projet CapCut modifiable** (`sops/workflow-nouvelle-video.md`). Un montage ne commence que si l'utilisateur le demande ensuite, hors de ce skill.

**Fichiers de travail** : pour **chaque analyse**, crée un **nouveau dossier temporaire propre à cette analyse** (nom unique, avec la date et l'heure), dans le dossier temporaire de la session ou du système, hors du dépôt, des dossiers de rushes et du dossier des projets CapCut. S'il existe déjà, choisis un autre nom : ne réutilise jamais le dossier d'une analyse précédente. N'écrase rien. Ne produis aucune vidéo.

- **Images extraites** (images isolées, planches, bandes) : autorisées **uniquement** dans ce nouveau dossier, jamais ailleurs, même si l'utilisateur demande d'enregistrer le compte rendu.
- Les résultats de mesure, et la transcription lorsqu'elle est demandée, vont dans le même dossier.

**Compte rendu** : dans la conversation. N'enregistre un fichier que si l'utilisateur le demande.

## Entrées

- La vidéo à analyser : **celle que l'utilisateur désigne**, en fichier local.
- La marque ou le client concerné.
- Le brief ou les consignes : sujet, durée, ce qui doit être repris de la référence.

S'il manque une information **indispensable à cette analyse**, demande-la en un seul message groupé et avance sur le reste. Ne bloque pas sur un champ inutile à l'analyse. Un champ resté entre crochets ne confirme rien : « À compléter » ou « À confirmer ».

Si le fichier est introuvable au chemin donné et qu'un fichier proche existe ailleurs, signale-le. Ne remplace jamais la référence en silence.

## Avant d'analyser : les règles du client

1. Lis `CLAUDE.md`.
2. Lis, pour **la seule marque concernée**, dans `clients/<marque>/` : `marque.md`, `montage.md`, `references.md`, `retours-client.md`, puis `offres-et-services.md` et `organisation.md` s'ils existent et sont utiles.
3. Lis le brief, s'il existe, et la fiche du format s'il y en a une dans `sops/` (ex. `format-reactions-compteur.md`).
4. Note le statut de chaque règle : confirmée, à valider, à compléter, ou propre à un essai.

Règles de séparation :

- N'ouvre pas les dossiers des autres marques et ne transfère **aucune** préférence, offre, police, couleur, rythme ou habillage d'une marque à une autre. Pacini Granby et Pacini Marché Central restent distincts.
- Les offres, logos, coordonnées et appels à l'action visibles dans la référence ne sont jamais à reprendre automatiquement.
- Un choix d'un ancien essai n'est pas une règle. Ce que tu observes dans la référence n'en est pas une non plus : cela guide au plus **cette** vidéo.
- Les consignes de l'utilisateur pour cette vidéo ont priorité. Si elles, la référence et les règles de la marque se contredisent, signale le conflit au lieu de trancher en silence.
- Si une correction du client apparaît, **propose** de l'ajouter dans `retours-client.md` ; ne l'ajoute pas.

## D'abord : la vidéo peut-elle être examinée ?

Vérifie que le fichier est local et lisible (`ffprobe`) et que tu peux en extraire des images et les regarder.

Si ce n'est pas possible (lien seul, fichier inaccessible ou illisible, outil absent), **dis-le clairement** et arrête la partie concernée. Ne décris jamais une vidéo à partir de son titre, de son nom de fichier ou de ta mémoire. Un lien seul ne suffit pas : demande de placer le fichier sur le poste. Ce que l'utilisateur te raconte de la vidéo est noté « rapporté par l'utilisateur ».

Limites à rappeler quand elles s'appliquent :

- **Tu n'entends pas le son.** Les mesures du signal ne sont pas une écoute : ambiance musicale, paroles chantées, ton de voix, qualité du son et effets sonores restent à confirmer par une écoute humaine.
- **Tu vois des images extraites, pas la vidéo en continu.** Un mouvement bref entre deux images peut t'échapper.
- Sans outil qui le mesure (ex. détection des temps de la musique), n'affirme pas qu'une coupe « tombe sur le temps ».
- Une police ne s'identifie pas avec certitude : propose au mieux une ressemblance, présentée comme telle.

## Commencer léger, approfondir seulement si c'est justifié

**1. Premier passage, par défaut :**

- les **métadonnées** (`ffprobe` : durée, format, résolution, images par seconde) ;
- une **sélection limitée d'images** : 20 au maximum, réparties du début à la fin, de préférence réunies sur **une planche synthèse**. N'enregistre pas les images une par une si la planche suffit.

Rédige le compte rendu à partir de ce passage s'il suffit. Un échantillon ne prouve ni le nombre de plans, ni un moment à l'image près, ni qu'une chose reste vraie sur toute la vidéo : donne des moments approximatifs, écris « non mesuré » ou « vu sur les images échantillonnées ».

**2. Mesures approfondies : seulement sur demande explicite de l'utilisateur, ou pour lever une incertitude importante pour le brief** (ou pour les consignes du message), c'est-à-dire un doute dont la réponse changerait une observation utile ou une décision. La curiosité, la recherche d'un compte rendu plus complet ou la présence d'un outil ne suffisent pas. Sont des mesures approfondies : détection des coupes, des noirs ou des fondus, comparaison entre images (rejeux, cadrage), positions au pixel, contrôle image par image et mesures du son.

- Limite la mesure à la question posée. Pour un moment précis, extrais d'abord seulement les images autour de ce moment.
- **N'extrais toutes les images que si une vérification précise le justifie** et qu'une extraction ciblée ne suffit pas. **Explique alors pourquoi** avant de le faire (la question à trancher), puis rappelle la raison dans les limites. Une demande générale d'analyse ne suffit pas.
- Si une incertitude ne justifie pas d'approfondir, signale-la dans les limites.

## Les trois niveaux, toujours séparés

| Niveau | Définition | Ce qu'il faut indiquer |
| --- | --- | --- |
| **Mesuré** | Valeur obtenue **dans cette session**, avec un outil, sur la vidéo analysée | L'outil, et le réglage s'il change le résultat (seuil, fréquence des images extraites) |
| **Observé** | Ce que tu vois sur les images réellement examinées | Le moment (temps ou numéro d'image) |
| **Interprété** | Effet ou intention que tu déduis | Une formulation prudente : « semble », « probablement » |

- Sans mesure faite avec un outil, écris **« non mesuré »**. Ne transforme jamais une impression en chiffre.
- Une détection automatique (coupe, silence, noir) est un **candidat** : écris « détecté, non contrôlé » tant que tu n'as pas vérifié.
- Une valeur reprise d'un ancien document est citée avec sa source et sa date ; elle n'est pas présentée comme revérifiée.
- La précision annoncée ne dépasse pas celle de la méthode : des images prises toutes les demi-secondes ne prouvent pas un moment à l'image près.
- « Aucun résultat » après une commande en échec n'est pas une mesure : vérifie que la commande a réussi.

## Fiches client et vidéo, à ne pas confondre

- **Vérifié dans la vidéo** : ce que tu as mesuré ou observé sur cette vidéo, dans cette session.
- **Lu dans les fiches (non vérifié dans la vidéo)** : ce qui vient des fiches client, du brief, d'une fiche de format ou d'un ancien document. Cite le fichier, la date si elle est indiquée et le statut de la règle.
- Une information lue ne devient jamais « mesurée » ni « observée » sans vérification sur la vidéo. Ce que la vidéo ne permet pas de prouver (ex. police ou taille exacte) reste « lu ».
- Si la vidéo concorde avec une fiche ou la contredit, présente les deux séparément. Si tu avais lu la valeur avant de la vérifier, dis-le : le contrôle n'était pas à l'aveugle.

## La méthode, en six axes

Utilise seulement les outils **déjà présents** sur le poste. S'il en manque un, indique la limite.

Les six axes servent à choisir ce qui compte, pas à tout mesurer ni à remplir six rubriques. La colonne « Mesures possibles » ne s'applique, hors métadonnées, que dans les cas prévus pour les mesures approfondies.

| Axe | Mesures possibles | Observer | Pièges à contrôler |
| --- | --- | --- | --- |
| **Rythme** | Durée totale (`ffprobe`), nombre de plans vérifiés, durées min, médiane et max | Accélérations, pauses, ouverture, chute | Une moyenne cache souvent la structure : regarde la suite des durées |
| **Plans** | Début et fin de chaque plan (détection de changements d'image avec `ffmpeg`, seuil indiqué) | Sujet et action de chaque plan, passages répétés ou rejoués | Une coupe au même cadrage ou un passage rejoué peut ne pas être détecté ; un flash, un geste rapide ou un texte qui apparaît peut créer une fausse coupe. Contrôle les images avant et après |
| **Cadrage** | Format, résolution, images par seconde ; positions en % de l'image quand c'est utile | Large, moyen, rapproché, gros plan ; angle ; place du sujet ; mouvement | Distingue « semble être un zoom au montage » d'un mouvement de caméra ou de sujet |
| **Textes** | Position et taille en % de l'image ; apparition et disparition, à l'image près seulement si les images ont été contrôlées une à une | Texte recopié exactement, lignes, couleur, ombre ou fond, animation, lisibilité | Passage illisible : **[illisible]**. Rien n'est deviné ni corrigé. Vérifie si le chiffre ou le texte change avec la coupe |
| **Transitions** | Moments des noirs ou des fondus détectés | Coupe franche, fondu, glissement, effet ; ce qui le prouve sur les images | Examine les images consécutives avant de nommer un effet |
| **Son** | Présence et durée de l'audio, niveaux (`ebur128`), silences (`silencedetect`, seuil indiqué) | Rien à l'oreille : seulement ce que les mesures montrent | Un niveau faible n'est pas forcément un silence ; ne nomme ni la musique ni un bruit sans preuve |

**Transcription : seulement sur demande explicite.** Ne lance la transcription locale que si l'utilisateur la **demande explicitement dans son message** pour cette analyse.

- Une autorisation donnée auparavant (pour Dimitri, pour Pacini Granby, pour un autre essai ou dans une session précédente) **n'est pas une autorisation générale** et ne vaut pas ici. Le brief, un document du dépôt, le fait que les paroles semblent importantes ou la présence de l'outil sur le poste ne suffisent pas non plus.
- Sans cette demande, n'extrais et ne transcris pas la parole : écris « paroles non transcrites (non demandé) ». Si les paroles comptent pour le brief, dis-le et indique que tu peux les transcrire si l'utilisateur le demande ; continue le reste de l'analyse.
- Avec cette demande, utilise seulement la transcription locale existante (`scripts/transcrire.py`, hors ligne), si elle fonctionne. Langue tirée du message ou du brief ; sinon demande-la, ou utilise `auto` en le disant. C'est un **brouillon** : passage incompris noté **[incompris]**, jamais reconstruit.

## Recommandations : seulement sur demande

Le compte rendu par défaut n'en contient pas. Si l'utilisateur en demande, place-les après les observations, avant les limites.

- Cinq au maximum, classées par importance.
- Chacune dit : **quoi faire**, sur **quoi elle s'appuie** (consigne de l'utilisateur, règle de la marque et son statut, mesure, observation ou interprétation) et ce qui reste **à valider**.
- Vise la mécanique utile au brief, pas une copie chiffrée. Si l'utilisateur demande de suivre la référence de près, suis sa demande ; les durées, polices ou transitions relevées ne deviennent jamais des réglages par défaut.
- Reste compatible avec un projet CapCut modifiable. Signale ce que notre flux ou les outils actuels ne savent pas faire.
- Si les rushes n'ont pas été examinés, dis que la faisabilité n'est pas vérifiée.

## Format du compte rendu

Court : environ un écran. Une chronologie détaillée seulement sur demande.

1. **Observations** : **cinq au maximum**, courtes, les plus utiles au brief d'abord. Pas de quota : moins de cinq convient. Chacune porte sur un seul point et donne :
   - ses **moments** (temps ou numéro d'image), avec leur précision réelle ;
   - ce qui est vérifié dans la vidéo, étiqueté **Mesuré** ou **Observé**, et s'il y a lieu **Interprété**. N'écris que les niveaux utiles ;
   - s'il y a lieu, à part, **Lu dans les fiches (non vérifié dans la vidéo)**. Une information seulement lue ne constitue pas une observation.
2. **Limites et à vérifier**, en bref : ce qui a été examiné (fichier, marque, durée, outils, nombre d'images regardées), tout approfondissement et sa raison, ce qui reste invérifiable (notamment l'écoute et la synchronisation si elles n'ont pas été faites par un humain), puis, seulement s'il y en a, les conflits et les questions indispensables, groupés.

Après les limites, résume les **fichiers créés par dossier et par type**, avec leur nombre (ex. « dans tel dossier : 1 planche, 1 fichier de mesures »). Donne le chemin complet de chaque dossier une seule fois ; **ne liste pas le chemin de chaque fichier**. Si aucun fichier n'a été créé, dis-le.

## Contrôle avant de répondre

- [ ] Le premier passage s'est limité aux métadonnées et à une sélection d'images ; tout approfondissement répond à une demande explicite ou à une incertitude importante pour le brief.
- [ ] Toutes les images n'ont été extraites que pour une vérification précise, expliquée.
- [ ] Cinq observations au maximum, avec leurs moments, puis les limites ; fichiers créés résumés par dossier et par type.
- [ ] Les informations lues dans les fiches sont séparées de ce qui est vérifié dans la vidéo.
- [ ] Chaque chiffre a un outil (mesure) ou une source citée (information lue), sinon « non mesuré ».
- [ ] Les interprétations sont écrites comme telles.
- [ ] Rien sur le son n'est présenté comme écouté.
- [ ] Aucune transcription lancée sans demande explicite dans le message de l'utilisateur.
- [ ] Les images extraites sont uniquement dans le nouveau dossier temporaire de cette analyse.
- [ ] Aucune règle d'une autre marque n'a été reprise.
- [ ] Aucun montage, fichier du dépôt ou projet CapCut n'a été modifié ; aucun rendu, envoi, téléchargement ou installation.

## Origine et licence

Méthode réécrite et adaptée du skill `analyze-video-editing` du dépôt `gitethanwoo/video-editing` (commit `8b633c2`), © 2026 Ethan Woo, licence MIT : texte complet dans `LICENSE-video-editing.txt`, dans le dossier de ce skill. Aucun script ni dépendance de ce dépôt n'est repris.
