# Procédure de prémontage vertical (finition dans CapCut)

> **Statut : première version, issue de l'essai « Décors de Noël » de Pacini Granby (2026-11-24).** Elle sépare strictement trois catégories pour que les choix d'un essai ne deviennent pas des règles par accident. Rien n'est enregistré comme préférence de marque sans ta confirmation explicite.
>
> Le script correspondant est `scripts/premontage.ps1` (mode d'emploi : `scripts/README.md`).

## Vue d'ensemble

1. Vérifier les fichiers.
2. Décider l'orientation (jamais présumée).
3. Choisir les plans (décision humaine) et écrire le plan.
4. Convertir et découper en segments.
5. Assembler le prémontage (avec musique et texte si demandés).
6. Contrôler techniquement.
7. Regarder, écouter, décider (humain).
8. Finir dans CapCut.
9. Noter les retours du client.

---

## Catégorie 1 — Étapes techniques réutilisables

Valables pour toute marque et toute vidéo. Les valeurs sont des réglages techniques par défaut, modifiables.

| # | Étape | Ce qui est fait | Fait par le script |
| --- | --- | --- | --- |
| 1 | **Vérifier les fichiers** | Les rushes, le brief, les paramètres du client, la musique et le plan existent et sont lisibles. Codec, résolution, images/s, durée, rotation, son et plage de couleurs sont relevés. Les fichiers illisibles sont signalés et ignorés | Oui |
| 2 | **Orientation** | Si le fichier porte une indication de rotation, elle est appliquée. Sinon, si les rushes sont en paysage et la sortie en vertical, **le script s'arrête** et produit une image de test (originale / rotation horaire / rotation anti-horaire). Une personne regarde l'image, puis relance avec `-Orientation`. **Chaque rush est vérifié séparément** (`-OrientationParRush` permet des sens différents) : un rush filmé à la verticale dans la même session que les autres n'a pas forcément le même sens, et une vue en plongée n'a pas de haut évident (indices utiles : gravité, texte, verre à l'endroit) | Partiellement : détecte, mais ne décide jamais |
| 3 | **Conversion** | Sortie 1080×1920, fréquence d'images du premier rush, `yuv420p`. Plage de couleurs complète → plage TV quand la source est en plage complète. Marquage BT.709 quand la source l'est | Oui |
| 4 | **Découpe** | Un fichier par plan, selon le plan fourni, en H.264 `crf 14`, `preset slow`. Le son d'origine est conservé dans les segments quand il existe | Oui |
| 5 | **Assemblage** | Coupes franches, dans l'ordre du plan. Version muette par défaut (le son d'origine n'est pas écouté). `-SonOrigine garder` ajoute des fondus de 0,04 s à chaque coupe | Oui |
| 6 | **Musique (facultative)** | Analyse du début de la piste pour proposer un départ net, fondus ajustés à l'extrait, assemblage, mesure du niveau. Aucun gain par défaut. Si le départ est déjà validé et que la durée change, `-DepartMusique` le conserve et le script ajuste les fondus et contrôle la fenêtre à partir de lui | Oui, comme **proposition** |
| 7 | **Texte (facultatif)** | Image transparente du texte (police, taille, marges), coupure en deux lignes si trop large, ombre douce sans boîte. Fichiers `texte.txt`, `texte.srt` (légende d'habillage, pas une transcription) et `texte_overlay.png`. Version avec et sans texte | Oui |
| 8 | **Export** | H.264 `crf 16`, `preset slow`, AAC 256 kb/s 48 kHz, `faststart` | Oui |
| 9 | **Contrôle technique** | Dimensions, durée, nombre d'images, images noires ou figées, loudness et pic réel, marges du texte, rushes d'origine inchangés (nom, taille, date) | Oui |
| 10 | **Nouvelle sortie à chaque essai** | Un dossier horodaté et nommé d'après le titre du brief. Rien n'est écrasé. Le script refuse une sortie placée dans le dossier des rushes | Oui |
| 11 | **Traçabilité** | `controle\rapport.md` (contrôles, paramètres et leur statut, à vérifier), `commandes.log` (commandes exactes), copies du brief, du plan et des paramètres | Oui |
| 12 | **Finition CapCut** | Voir `clients/<marque>/essais/<essai>/etapes-capcut.md` | Non |

---

## Catégorie 2 — Préférences de Pacini Granby explicitement validées

Seulement ce que tu as confirmé toi-même. Détail dans `clients/pacini-granby/` (`marque.md`, `montage.md`, `references.md`, `parametres-script.json`).

| Préférence | Valeur confirmée |
| --- | --- |
| Langue | Français québécois |
| Public | Familles de classe moyenne et élevée |
| Ton | Gourmand, naturel et énergique |
| Rythme et transitions (intention) | Montage dynamique qui garde les spectateurs intéressés |
| Musique (style) | Ambiance un peu décontractée |
| Couleurs, polices, logo | Ceux du guide « Guide réseau sociaux » : Montserrat Regular ; rouge `B9242B`, gris `595959`, blanc `FFFFFF`. Le noir est **à confirmer** (le guide écrit `00000`). Aucun fichier de logo utilisable fourni |
| Référence « Parmesan » | À reproduire : l'effet humoristique du montage. À éviter : rien de particulier |
| Référence « Je pensais venir manger… » | À reproduire : le dynamisme. À éviter : rien de particulier |
| Offres et éléments d'autres restaurants | Ne jamais reprendre automatiquement les offres, montants ou éléments propres à un autre restaurant présents dans les références. Les deux Pacini restent séparés |

### Appliqué à l'essai, pas encore confirmé comme règle permanente

- Les consignes du guide de marque pour les vidéos (musique sans paroles explicites, personnes identifiables avec consentement, promotions seulement avec l'autorisation du siège, « MD » dans « Bar à PainMD », format 9:16). Elles sont appliquées dans l'essai et marquées « À valider » dans `marque.md`.
- Ne pas utiliser de plans montrant des personnes identifiables sans autorisation confirmée.

### Préférences validées pour un **format** (pas pour toute la marque)

- Format « Réactions avec compteur » : principes confirmés le 2026-11-24 (réactions nettes et contrastées, passages faibles écartés, compteur et durée adaptés à la matière, répétitions variables, progression terminant sur une réaction forte, changement de chiffre synchronisé avec la coupe par défaut, lisibilité du texte de l'export de l'utilisateur comme référence visuelle). Détail, limites et choix propres à la vidéo : **`sops/format-reactions-compteur.md`**.

---

## Catégorie 3 — Choix propres à l'essai « Décors de Noël »

**Ne pas les appliquer tels quels aux prochaines vidéos.** Ils sont enregistrés comme statut « essai » dans `parametres-script.json` ou comme valeurs de la ligne de commande.

| Choix | Valeur de l'essai |
| --- | --- |
| Durée | 19,6 s (cible testée : 15 à 25 s) |
| Sélection des plans | 10 rushes sur 12 ; `DGM_3785` et `DGM_3786` écartés (marques tierces, affiche de promotion) ; plans flous 07 et 09 conservés |
| Ordre et rythme des plans | Fichier `plan.csv` de l'essai (plans de 1,5 à 2,5 s, coupes franches) |
| Ouverture | Sur un mouvement (cadeaux) |
| Écran final | Aucun |
| Orientation | Rotation **anti-horaire**, parce que **ces** rushes ont été filmés à la verticale sans indicateur de rotation |
| Son d'origine | Version muette |
| Musique | Piste `snapgram.io_qk5jbiotjaut.mp3` ; départ à **6,70 s** (propre à ce fichier) ; fondu d'entrée 0,02 s, fondu de sortie 2,0 s (propres à cet extrait) ; aucun gain |
| Texte (V3) | « Une ambiance chaleureuse pour le temps des Fêtes » ; Montserrat Regular 52 px, blanc, sans boîte, ombre douce (opacité 0,7, flou 6 px) ; deux lignes centrées ; marge basse 458 px, marges latérales 130 px minimum (hypothèses de zones de sécurité) |
| Texte (V4, version actuelle) | Même texte, ajusté sur la référence de Noël : **Californian FB** (approximation de la police de la référence, non identifiée), **26,7 px**, interligne 1,07, centre du bloc à **49,96 %** de la hauteur, ombre réduite proportionnellement (flou 3 px, décalage 2 px). Valeurs obtenues en mesurant le texte de la référence et en calibrant le rendu sur sa phrase ; elles viennent de **cette** référence et ne valent pas pour une autre. S'écarte de la police de marque (Montserrat) : accord du client à obtenir. **Direction visuelle validée par l'utilisateur pour cette vidéo** (2026-11-24) : ce n'est pas une préférence permanente de la marque |
| Ajout de deux rushes (V5) | `DGM_3828` (spaghettis, passage de 3,3 à 5,4 s) et `DGM_3832` (versement de vin, passage de 1,8 à 4,2 s), insérés après « casse-noisettes » et après « lutin-bouteille ». Durée totale 24,12 s. Orientation anti-horaire pour les deux, vérifiée rush par rush. Départ musical conservé à 6,70 s, fondu de sortie de 2,0 s ajusté à la nouvelle durée. Choix propres à cet essai |
| Logo | Absent : le bon fichier n'est pas fourni |
| Format | 9:16, 1080×1920 (proposé comme test) |

Les anciens choix musicaux (départ à 7,4 s pour la première piste) sont obsolètes et ne doivent pas être repris.

---

## Ce que le script automatise réellement pour la sélection des plans et le rythme

| Sujet | Automatisé | Reste humain |
| --- | --- | --- |
| Sélection | **Sans plan fourni** : propose, pour chaque rush, l'extrait le plus net (mesure de flou) d'une durée donnée, et signale les rushes plus flous que la médiane | **Tout le reste** : pertinence, rushes à écarter (marques tierces, promotions, personnes, alcool, sujet hors thème), composition, qualité |
| Ordre | Reprend l'ordre du plan fourni, ou l'ordre des noms de fichiers pour la proposition | **L'ordre narratif** |
| Durées | Applique les durées du plan, avertit si le total sort de la cible | **La durée de chaque plan et le rythme** |
| Arrêt | Sans plan, le script **s'arrête** après la proposition. `-Auto` le force à produire, avec la mention « SORTIE NON VALIDÉE » | Valider ou corriger le plan, puis relancer avec `-Plan` |

Sur cet essai, la proposition automatique aurait inclus `DGM_3785` et `DGM_3786`, que j'avais écartés après avoir vu les images : le script ne peut pas juger du contenu.

---

## Décisions humaines obligatoires pour chaque vidéo

1. L'orientation, si les rushes n'ont pas d'indicateur de rotation.
2. Le choix des plans, leur ordre et leur durée.
3. Regarder la vidéo en entier : personnes, promotions, marques tierces, alcool.
4. Écouter le son et la musique : voix, paroles explicites, goût.
5. Confirmer le droit d'utiliser la musique.
6. Valider le texte (contenu, lisibilité) et le tester sur téléphone.
7. L'approbation du client.

## Limites connues

- Pas de transcription : aucune reconnaissance vocale française sur le poste. Un SRT n'est produit que si **tu en fournis un** (`-Transcription`) ; le script vérifie son format, pas son contenu.
- Pas de détection de visages, de logos ni de texte promotionnel.
- Le départ musical est choisi sur le signal, pas à l'oreille. L'alignement des attaques avec les coupes est un indice faible.
- Les zones de sécurité des réseaux sociaux (haut 250 px, bas 450 px, côtés 130 px) sont des hypothèses non vérifiées dans les applications.
- L'identification d'une police à partir d'une vidéo n'est pas possible de façon certaine : le script n'identifie rien. La proximité d'une police se mesure à la main (rapports largeur/hauteur des lignes, hauteur d'x) sur les polices installées.
- Un texte placé au centre d'une image qui change à chaque plan peut tomber sur un fond très clair : le script ne mesure pas la lisibilité (la mesure de luminosité derrière le texte a été faite à la main sur cet essai).
- Le brief n'est lu que pour son titre et le nombre de « À compléter » : les paramètres de l'essai passent par la ligne de commande, le plan et `parametres-script.json`.
- Les rushes avec rotation intégrée dans le fichier ou en format déjà vertical n'ont pas été testés : seul le cas de cet essai l'a été.
- Testé uniquement sur cet essai (voir `scripts/README.md`).
