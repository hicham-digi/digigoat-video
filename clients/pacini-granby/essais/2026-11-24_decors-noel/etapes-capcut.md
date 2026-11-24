# Étapes de finition dans CapCut — Décors de Noël · Essai V1

Pour CapCut Pro sur Windows. Les noms de menus peuvent varier un peu selon la version : si un bouton n'a pas le même nom, cherche son équivalent.

Dossier des fichiers : `C:\Users\Hicham\Desktop\Digigoat\PACINI GRANBY\ESSAIS\2026-11-24_decors-noel\`

> Les paramètres ci-dessous sont ceux **de cet essai** [Test]. Ce ne sont pas des règles permanentes.

## 1. Avant de commencer

1. Regarde le prémontage muet en entier :
   `premontage\premontage_V1_sans-musique_muet.mp4`.
2. Vérifie les points de la section « À vérifier par toi » de `brief.md` : personnes visibles, marques tierces (plan 08), flou (plans 07 et 09).
3. Écoute le son : ouvre `premontage\premontage_V1_sans-musique_audio-origine.mp4`. Y a-t-il des voix, de la musique de la salle ou des paroles explicites ?

## 2. Créer le projet

1. Ouvre CapCut, puis **Nouveau projet**.
2. Règle les proportions à **9:16** (vertical).
3. Nomme le projet : `PaciniGranby_DecorsNoel_V1`.

## 3. Importer et assembler

1. **Importer** : pour la V5 (version actuelle, 12 plans), sélectionne les 12 fichiers du dossier `segments_V5\`, numérotés 01 à 12. Pour les versions V1 à V4, utilise les 10 fichiers de `segments\`. Les deux jeux ne sont pas interchangeables : la numérotation diffère.
2. Glisse-les sur la timeline dans l'ordre 01 → 10. Ils sont déjà coupés : il n'y a rien à rogner.
3. Durée attendue : environ 19,6 s. Garde les coupes franches (pas de transition) pour cet essai.
4. Pour retirer un plan (ex. 08), clique dessus puis **Supprimer**. La durée baissera d'environ 1,8 s, ce qui reste dans les 15 à 25 s visées.
5. Alternative plus rapide : importer directement `premontage_V1_sans-musique_muet.mp4`. Les plans seront alors collés et il faudra les séparer avec **Diviser** pour retirer ou déplacer l'un d'eux. Les segments séparés sont plus simples à réorganiser.

## 4. Son

1. **Son d'origine** : tu as choisi la version muette. Les segments (`segments\`) contiennent encore le son d'origine de la salle : après les avoir glissés dans la timeline, coupe leur son (volume à 0, ou option **Couper le son**). Ou importe `premontage_V1_sans-musique_muet.mp4`, qui est déjà muet.
2. **Musique** : piste fournie par toi : `C:\Users\Hicham\Desktop\RÉFÉRENCE\Musique référence\snapgram.io_qk5jbiotjaut.mp3`. Importe-la, place-la sous la vidéo, **fais-la commencer à 6,7 s dans la piste** (première attaque nette après un creux presque silencieux, choisie sur le signal et non à l'oreille), puis coupe-la à la fin de la vidéo (19,6 s) avec un fondu de sortie d'environ 2 s. Autres départs possibles : 7,76 s, 11,06 s, 14,16 s.
   - La version déjà assemblée est `premontage\premontage_V3_musique_avec-texte.mp4` (sans texte : `premontage_V3_musique_sans-texte.mp4`). La V2 utilisait une autre piste et un autre départ : ils sont obsolètes.
   - **Confirme l'autorisation d'utilisation** de la piste avant de publier (voir `brief.md` §9).
   - N'utilise pas une piste de la bibliothèque de CapCut tant que tu n'as pas confirmé qu'elle est autorisée pour ce client et cet usage.
3. Si la piste n'est finalement pas autorisée : publie sans musique (V1 muette) ou remplace-la par une piste que tu as le droit d'utiliser.
4. Ambiance recherchée : un peu décontractée. [Toi]
5. Écarte toute musique avec des paroles explicites. [Guide, à valider]

## 5. Sous-titres (seulement s'il y a de la parole)

Aucune parole n'a été confirmée dans les rushes. Saute cette étape sauf si tu entends quelqu'un parler.

S'il y en a, voici les paramètres de l'essai [Test] :
- Texte blanc, police Montserrat Regular (installée sur ton poste).
- Deux lignes maximum, bien lisibles.
- Position à tester : essaie deux positions et compare. Par exemple dans le bas de l'image, puis plus haut vers le centre. Vérifie que rien ne se chevauche avec l'interface de la plateforme.

Pour importer un SRT, si j'en prépare un : dans le menu **Texte** ou **Sous-titres**, cherche une option d'import de fichier de sous-titres.

Si Montserrat n'apparaît pas dans la liste des polices de CapCut, dis-le-moi : je ne peux pas vérifier ce point d'ici.

## 6. Ce qu'il ne faut pas ajouter pour cet essai

- Pas de logo. [Toi]
- Pas d'écran final. [Toi]
- Pas d'offre, de prix, de promotion ni de coordonnées. [Toi]

Le seul texte ajouté est « Une ambiance chaleureuse pour le temps des Fêtes ». Pour le refaire ou le modifier dans CapCut, voir `texte\texte_V4_parametres.md` (version actuelle : police approchant la référence, petite taille, au milieu de l'image) ou `texte\texte_V3_parametres.md` (version précédente : Montserrat 52 px, en bas), dans le dossier de l'essai.

## 7. Exporter

1. Clique sur **Exporter**.
2. Réglages conseillés : résolution 1080p (1080×1920), 30 images/s, format MP4. La source est à 29,97 i/s.
3. Nom du fichier : `PaciniGranby_DecorsNoel_V1.mp4`
4. Dossier : crée un sous-dossier `export-final` dans `...\ESSAIS\2026-11-24_decors-noel\` et enregistre-le là.

## 8. Contrôle avant envoi

- [ ] Vidéo regardée en entier, au volume habituel.
- [ ] Aucune personne identifiable, sauf autorisation confirmée. [Guide, à valider]
- [ ] Aucune promotion ni texte d'offre. [Guide, à valider]
- [ ] Pas de musique à paroles explicites, ni de musique non autorisée. [Guide, à valider]
- [ ] Format 9:16, durée entre 15 et 25 s (si tu veux rester dans le test).
- [ ] Rendu des couleurs vérifié sur un téléphone.

## 9. Après l'envoi au client

1. Note les retours dans `clients/pacini-granby/retours-client.md` (date, correction, règle à appliquer), seulement une fois confirmés.
2. Dis-moi ce que tu retiens de l'essai : je proposerai de transformer ce qui a marché en règles dans `montage.md`, et je n'enregistrerai rien sans ta validation.
