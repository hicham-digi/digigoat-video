# Montage long — Dimitri : diagnostic technique et plan d'essai

> Statut (mis à jour le 2026-11-24) : diagnostic initial puis **préparation technique faite avec ton autorisation** (Whisper local isolé, générateur CapCut adapté). **Aucun rush de Dimitri n'a encore été analysé** (le Drive et le poste ne contiennent aucune vidéo de Dimitri) : tout a été testé sur un rush **synthétique**. Les outils communs sont réutilisés ; **aucun choix créatif d'un autre client n'est transféré**. Procédure : `sops/procedure-montage-long.md` ; dépôt du rush : `essais/essai-long_01/README.md`.
> Légende : **vérifié** = constaté sur ce poste le 2026-11-24 ; **non vérifié** = affirmé par une documentation ou à tester ; **non disponible** = absent.

## 0. Où en est-on : préparé, testé, bloqué

| | Élément |
| --- | --- |
| **Préparé et testé (rush synthétique)** | Transcription locale horodatée au mot (faster-whisper, large-v3, GPU : x15 temps réel ; CPU : x1,1) ; propositions de coupes sobres avec justification et risque sur le sens ; calage d'un audio séparé ; sous-titres recalés sur les segments gardés ; projet CapCut local : prises liées, son conservé, audio séparé, sous-titres modifiables, canevas au choix ; non-régression du générateur |
| **Préparé, non testé** | Ouverture du projet dans CapCut (nouvelles pistes) ; calibration de la taille des sous-titres en 16:9 |
| **Bloqué (il faut le rush)** | Qualité de la transcription sur la vraie voix et la langue réelle ; seuils de confiance et de silence ; durée longue ; plusieurs voix ; dérive d'horloge d'un audio séparé |
| **Bloqué (il faut tes réponses)** | Langue, plateformes, durée finale, identité visuelle, niveau d'habillage, qui relit, validation du client |

## 1. Ce que je peux réellement analyser

| Élément | Ce que je peux faire | Ce que je ne peux pas faire |
| --- | --- | --- |
| **Parole** | Lire un **texte** de transcription (SRT ou texte horodaté) et le comparer aux coupes | **Écouter.** Je n'entends pas le son. Sans transcription fournie par un outil ou par un humain, je ne connais pas le contenu de la parole |
| **Images** | Extraire des images (ffmpeg) puis les **regarder** : cadrage, personnes, décor, texte à l'écran, arrière-plan, changements de scène (**vérifié**, même méthode que les essais précédents) | Voir en continu : je ne vois que les images échantillonnées |
| **Changements de caméra** | Détection par le signal (`scdet` : **vérifié** présent), puis contrôle visuel des images autour de chaque détection | Garantir qu'aucun changement n'est manqué (zoom numérique, fondu lent) ni qu'une détection est un vrai changement sans regarder |
| **Audio** | **Signal seulement** : nombre de pistes, durée, silences (`silencedetect`), niveau et pics (`ebur128`, `astats`) : **vérifié** présents | **Ce n'est pas une écoute.** Le signal ne dit ni ce qui est dit, ni si la voix est intelligible, ni la nature d'un bruit. Un « silence » détecté peut être une pause de réflexion à conserver |
| **Pistes audio séparées** | Lister les flux audio de chaque fichier (`ffprobe`) ; comparer durées et niveaux | Synchroniser automatiquement un enregistrement externe avec une vidéo (non construit) |

## 2. Transcription fiable et horodatée : outils disponibles

Matériel (**vérifié**) : Ryzen 7 3700X (8 cœurs), 16 Go de RAM, GeForce RTX 3060 Ti, 114 Go libres. Suffisant en principe pour un modèle local de reconnaissance vocale ; capacité réelle **non vérifiée**.

| Option | État sur ce poste | Remarques |
| --- | --- | --- |
| Filtre de reconnaissance vocale de ffmpeg | **Non disponible** : absent de la version 7.1 installée (liste des filtres vérifiée) | — |
| Modules Python de reconnaissance vocale | **Non disponibles** : aucun module correspondant détecté (`pip list`, 2026-11-24). Python 3.13 | — |
| Reconnaissance vocale de Windows | **Non utilisable** : un seul moteur installé, **anglais (États-Unis)**. Le français canadien est dans la liste des langues de l'utilisateur, mais sans moteur de reconnaissance | Dépend de la langue des vidéos (**À compléter**) |
| Programme local de type Whisper (modèle multilingue, horodatage au mot) | **Installé le 2026-11-24 avec ton accord**, en environnement isolé hors dépôt (faster-whisper 1.2.1, modèle large-v3, CUDA 12) ; compatible Python 3.13 après un contournement (lecture du WAV par le script). **Testé sur voix de synthèse anglaise seulement** : x15 temps réel sur GPU, x1,1 sur CPU | Outil retenu pour l'essai. Qualité sur voix humaine et en français : **non mesurée**. Fonctionne hors ligne (aucun envoi) |
| Sous-titres automatiques de **CapCut Pro** (faits par toi dans CapCut) | **Non vérifié** : disponibilité, langue prise en charge et qualité à vérifier dans ta version (9.8.0.4213) | Je peux ensuite lire le projet CapCut **en lecture seule** pour récupérer le texte horodaté. Service en ligne : confidentialité des rushes d'un avocat à confirmer avant tout envoi |
| Transcription automatique du connecteur Drive | **Non vérifié** : la documentation de l'outil parle de vidéos « quand une transcription est disponible » | Non contrôlable, non testé ; n'est pas une solution de production |
| Transcription fournie par le client ou relue par un humain | Possible | **La plus fiable pour du contenu juridique** |

**Position retenue** : toute transcription automatique est un **brouillon**. Elle doit être **relue par un humain qui écoute** les passages à enjeu avant toute coupe définitive. Confidentialité : un outil local évite d'envoyer les rushes à un service externe ; à confirmer avec le client.

## 3. Découpage qui préserve le sens

1. **Rien n'est reconstruit.** Un passage que l'outil ou moi ne comprenons pas est marqué `[incompris hh:mm:ss–hh:mm:ss]` et signalé ; je ne propose jamais un texte « probable ».
2. **Les réserves sont intouchables sans validation** : conditions, exceptions, restrictions, degrés de certitude (« en principe », « dans certains cas », « cela dépend »), renvois à une règle, délais, montants, dates, références légales, négations, noms de personnes ou d'institutions. La liste précise de marqueurs sera établie **dans la langue des vidéos** (**À compléter**, rien n'est présumé).
3. **Coupe = justification écrite** : chaque coupe est consignée (timecode source, dernier et premier mot conservés, risque de sens : faible, moyen, élevé). Une coupe à risque « élevé » est soumise avant le rendu.
4. **Pas de réordonnancement** de passages dans un même raisonnement. Un déplacement qui change la portée d'une explication est exclu.
5. **Pas de suppression d'hésitations** qui portent une nuance (« je pense que », « normalement ») : seules les hésitations vides sont candidates, et seulement si la transcription relue le confirme.
6. **Relecture avant livraison** : qui relit (Digigoat, Dimitri, autre) : **À compléter** (`organisation.md`). Mentions ou avertissements éventuels propres à un contenu juridique : **À compléter** (non déduits).
7. Un résumé ou un extrait court ne doit pas présenter comme général ce qui est conditionnel dans le long.

## 4. Projet CapCut cible, et écarts avec l'outil actuel

| Besoin | Outil actuel (`scripts/`) | Écart |
| --- | --- | --- |
| Prises **liées aux rushes sources**, avec points d'entrée et de sortie, rallongeables | `capcut_projet.py --rushes` + plan CSV (`ordre;rush;debut;duree;nom;note`) : **testé** sur des essais de 10 à 40 plans | Aucun pour le principe. **Non testé** avec des rushes de longue durée ni des centaines de plans |
| **Son d'origine conservé** sur les prises | **Fait** : `capcut_projet.py --son-origine garder` (défaut inchangé : coupé) | Testé structurellement (volume 1 sur chaque prise) ; ouverture dans CapCut non testée |
| **Pistes audio séparées lorsqu'elles existent** | **Fait** : `--audios-separes "RUSH=audio@D"` (piste audio séparée liée au rush, mêmes points d'entrée et de sortie ; son de la caméra coupé pour ce rush) ; `scripts/caler_audio.py` estime `D` | Testé structurellement, décalage positif et négatif. Plusieurs flux audio d'un **même** fichier : **non géré** (à lister avec `ffprobe`, à traiter au cas par cas) |
| **Sous-titres ou textes modifiables par segment** | **Fait** : `--sous-titres "RUSH=fichier.srt"` (un texte par sous-titre, recalé sur les coupes, sans chevauchement, coupé aux points de coupe) ; sous-titres générés par `transcrire.py` / `proposer_coupes.py` | Testé structurellement. Style par défaut **neutre technique** (Arial, taille 5) : taille **à calibrer** en 16:9 |
| **Format du projet** | **Fait** : `--canevas LxH` (le modèle est en 1080x1920) | Plateformes et format : **À compléter** |
| Sauvegarde avant écriture, nouvel projet, rushes d'origine intacts | **Existant et testé** | Aucun |
| Orientation fichier par fichier | **Existant** | Aucun |

Ces ajouts ont été faits sur ton accord du 2026-11-24 ; sans les nouvelles options, le projet produit est **identique** à celui de l'ancienne version (vérifié).
Un projet que tu modifies dans CapCut n'est jamais régénéré. Rappel du piège connu : dans CapCut, supprimer ou raccourcir un plan ne déplace pas les textes d'une piste séparée.

## 5. Premier essai proposé (rien n'est lancé)

**Principe** : un **court extrait représentatif de 2 à 3 minutes**, avant toute vidéo longue complète.

**Choix de l'extrait** (avec toi) : un passage où l'intervenant explique un point **avec au moins une condition ou une réserve**, une prise avec hésitations ou reprises, et si possible un changement de caméra et deux voix.

| Étape | Contenu | Contrôle de production (court) |
| --- | --- | --- |
| 1 | Inventaire (`ffprobe`) : durée, nombre de flux audio, orientation, fréquence d'images ; copie du rush dans un dossier d'essai (original intact) | Rush lisible, originaux inchangés |
| 2 | Signal : silences, niveau, changements de scène ; images de contrôle | Liste des détections, images regardées |
| 3 | **Transcription** par l'option retenue, avec horodatage | Texte complet, passages `[incompris]` listés |
| 4 | **Relecture humaine** (toi ou la personne désignée) des passages à enjeu | Réserves et conditions confirmées mot à mot |
| 5 | Plan de coupe annoté (CSV) avec la justification de chaque coupe | Aucune réserve supprimée ; coupes à risque soumises |
| 6 | Projet CapCut : prises liées, son conservé, sous-titres si demandés (après adaptation minimale du générateur, sur accord) | Projet ouvert dans CapCut, son présent, plans rallongeables, sous-titres modifiables |
| 7 | Compte rendu court avec **temps par étape** (horodatages réels) | Ce qui n'est pas mesuré est écrit comme tel |

**Critères de réussite** : transcription vérifiée mot à mot sur l'extrait, aucune réserve perdue, projet fonctionnel dans CapCut, temps de traitement acceptable pour une vidéo longue.

## 6. Ce qu'il faut pour démarrer l'essai

Indispensable : un **rush d'essai** (dépôt : `C:\Users\Hicham\Desktop\Digigoat\DIMITRI\ESSAIS\essai-long_01\rushes\`, audio séparé éventuel dans `...\audio-separe\`) et **sa langue**. Montage attendu pour l'essai [Toi, 2026-11-24] : sobre (silences excessifs, faux départs, répétitions évidentes), sens complet, sans musique ni habillage élaboré. Le reste (plateformes, durées finales, identité visuelle) sera précisé ensuite. Détail : `essais/essai-long_01/README.md`.

## 7. Essai : ce qui sera remis

Projet CapCut modifiable ; transcription avec timecodes (brouillon) ; liste des coupes avec justification et risque sur le sens ; points à valider ; temps de traitement par étape et limites constatées.
