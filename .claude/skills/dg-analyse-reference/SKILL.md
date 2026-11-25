---
name: dg-analyse-reference
description: Analyse une vidéo de référence (rythme, plans, cadrage, textes, transitions, son) en séparant ce qui est mesuré, observé et interprété, puis rend un compte rendu court avec des recommandations liées au brief. Analyse et conseil seulement. Appel manuel avec /dg-analyse-reference.
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

## D'abord : la vidéo peut-elle être examinée ?

Vérifie que le fichier est local et lisible (`ffprobe`) et que tu peux en extraire des images et les regarder.

Si ce n'est pas possible (lien seul, fichier inaccessible ou illisible, outil absent), **dis-le clairement** et arrête la partie concernée. Ne décris jamais une vidéo à partir de son titre, de son nom de fichier ou de ta mémoire. Un lien seul ne suffit pas : demande de placer le fichier sur le poste. Ce que l'utilisateur te raconte de la vidéo est noté « rapporté par l'utilisateur ».

Limites à rappeler quand elles s'appliquent :

- **Tu n'entends pas le son.** Les mesures du signal ne sont pas une écoute : ambiance musicale, paroles chantées, ton de voix, qualité du son et effets sonores restent à confirmer par une écoute humaine.
- **Tu vois des images extraites, pas la vidéo en continu.** Un mouvement bref entre deux images peut t'échapper.
- Sans outil qui le mesure (ex. détection des temps de la musique), n'affirme pas qu'une coupe « tombe sur le temps ».
- Une police ne s'identifie pas avec certitude : propose au mieux une ressemblance, présentée comme telle.

## Les trois niveaux, toujours séparés

| Niveau | Définition | Ce qu'il faut indiquer |
| --- | --- | --- |
| **Mesuré** | Valeur obtenue **dans cette session** avec un outil, ou lue dans une preuve disponible | L'outil ou la preuve, et le réglage s'il change le résultat (seuil, fréquence des images extraites) |
| **Observé** | Ce que tu vois sur les images réellement examinées | Le moment (temps ou numéro d'image) |
| **Interprété** | Effet ou intention que tu déduis | Une formulation prudente : « semble », « probablement » |

- Sans outil ni preuve, écris **« non mesuré »**. Ne transforme jamais une impression en chiffre.
- Une détection automatique (coupe, silence, noir) est un **candidat** : écris « détecté, non contrôlé » tant que tu n'as pas vérifié.
- Une valeur reprise d'un ancien document est citée avec sa source et sa date ; elle n'est pas présentée comme revérifiée.
- La précision annoncée ne dépasse pas celle de la méthode : des images prises toutes les demi-secondes ne prouvent pas un moment à l'image près.
- « Aucun résultat » après une commande en échec n'est pas une mesure : vérifie que la commande a réussi.

## La méthode, en six axes

Utilise seulement les outils **déjà présents** sur le poste. S'il en manque un, indique la limite.

| Axe | Mesurer | Observer | Pièges à contrôler |
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

## Recommandations liées au brief

- Cinq au maximum, classées par importance.
- Chacune dit : **quoi faire**, sur **quoi elle s'appuie** (consigne de l'utilisateur, règle de la marque et son statut, mesure, observation ou interprétation) et ce qui reste **à valider**.
- Vise la mécanique utile au brief, pas une copie chiffrée. Si l'utilisateur demande de suivre la référence de près, suis sa demande ; les durées, polices ou transitions relevées ne deviennent jamais des réglages par défaut.
- Reste compatible avec un projet CapCut modifiable. Signale ce que notre flux ou les outils actuels ne savent pas faire.
- Si les rushes n'ont pas été examinés, dis que la faisabilité n'est pas vérifiée.
- Si une correction du client apparaît, **propose** de l'ajouter dans `retours-client.md` ; ne l'ajoute pas.

## Format du compte rendu

Court : environ un écran. Une chronologie détaillée seulement sur demande.

1. **En bref** : ce que fait la référence et ce qui compte pour ce brief (2 ou 3 phrases).
2. **Source et méthode** : fichier, marque, durée, outils utilisés, ce qui a été examiné.
3. **Analyse** : tableau `Axe | Mesuré | Observé | Interprété`, six lignes. Une case sans information porte « non mesuré », « non observé » ou « non examinable », avec la raison.
4. **Recommandations pour ce brief**.
5. **Conflits et questions** : seulement l'indispensable, groupé.
6. **Limites et à vérifier** : notamment l'écoute et la synchronisation si elles n'ont pas été faites par un humain.

## Contrôle avant de répondre

- [ ] Chaque chiffre a un outil ou une preuve, sinon « non mesuré ».
- [ ] Les interprétations sont écrites comme telles.
- [ ] Rien sur le son n'est présenté comme écouté.
- [ ] Aucune transcription lancée sans demande explicite dans le message de l'utilisateur.
- [ ] Les images extraites sont uniquement dans le nouveau dossier temporaire de cette analyse.
- [ ] Aucune règle d'une autre marque n'a été reprise.
- [ ] Aucun montage, fichier du dépôt ou projet CapCut n'a été modifié ; aucun rendu, envoi, téléchargement ou installation.

## Origine et licence

Méthode réécrite et adaptée du skill `analyze-video-editing` du dépôt `gitethanwoo/video-editing` (commit `8b633c2`), © 2026 Ethan Woo, licence MIT : texte complet dans `LICENSE-video-editing.txt`, dans le dossier de ce skill. Aucun script ni dépendance de ce dépôt n'est repris.
