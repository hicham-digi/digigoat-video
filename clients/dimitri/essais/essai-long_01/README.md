# Essai de montage long n° 1 : Dimitri

> Statut au 2026-11-24 : **préparé, en attente du rush d'essai.** Rien n'a été fait sur un vrai rush de Dimitri. Informations inconnues : « À compléter ». Aucun choix créatif d'un autre client n'est repris. Procédure : `sops/procedure-montage-long.md`.

## Où déposer les fichiers

| Quoi | Chemin exact |
| --- | --- |
| **Rush d'essai** (une vidéo, extrait représentatif de 2 à 3 minutes, ou plus long avec l'indication du passage à traiter) | `C:\Users\Hicham\Desktop\Digigoat\DIMITRI\ESSAIS\essai-long_01\rushes\` |
| **Audio enregistré à part** (micro externe, enregistreur), s'il existe | `C:\Users\Hicham\Desktop\Digigoat\DIMITRI\ESSAIS\essai-long_01\audio-separe\` |

Copier les fichiers (ne pas déplacer les originaux). Les dossiers existent déjà.

## À joindre avec le rush

- **La langue parlée** dans la vidéo (obligatoire : aucune langue n'est présumée).
- Le passage à traiter, si le fichier est plus long que l'extrait voulu (début et fin approximatifs).
- **Si l'audio est séparé** : le fichier audio de **la même prise** (de préférence WAV non compressé), le nombre de micros ou de voix, et si un **claquement ou un signal de synchronisation** a été fait au début (facultatif : le calage se fait automatiquement par corrélation, la confiance est vérifiée).
- Si plusieurs fichiers vidéo forment la prise (plusieurs caméras ou plans) : tous, avec leur ordre.
- Le **format d'image** voulu (paysage, vertical, carré) si connu ; sinon celui du rush est repris (**À compléter**).
- Si des **sous-titres** sont voulus pour l'essai (par défaut : oui, modifiables, style neutre technique).
- Les noms propres et termes techniques à reconnaître (facultatif : améliore la transcription).

## Montage attendu pour l'essai [Toi, 2026-11-24]

Sobre : retirer les silences excessifs, les faux départs et les répétitions évidentes ; rythme naturel ; sens complet des propos. **Pas de musique ni d'habillage élaboré.** Transcription = brouillon à relire ; passages incertains signalés avec timecode, `[incompris]` au besoin ; conditions et réserves conservées ; coupes ambiguës proposées pour validation.

## Ce qui sera remis à la fin de l'essai

1. Le projet CapCut modifiable (prises liées au rush, son conservé, audio séparé sur sa piste, sous-titres modifiables).
2. La transcription avec timecodes (brouillon).
3. La liste des coupes avec leur justification et leur risque sur le sens.
4. Les points à valider (coupes ambiguës, passages incertains).
5. Le temps de traitement par étape et les limites constatées.

## État des préparatifs

| Élément | Statut |
| --- | --- |
| Transcription locale (faster-whisper, modèle large-v3, GPU) | **Préparée et testée** sur un rush synthétique anglais ; **non testée** sur voix humaine ni en français |
| Propositions de coupes, plan et sous-titres recalés | **Préparés et testés** sur le rush synthétique |
| Calage d'un audio séparé | **Préparé et testé** (synthétique, décalage retrouvé) |
| Générateur CapCut (son conservé, audio séparé, sous-titres, canevas) | **Adapté et testé structurellement** (projet local) ; **ouverture dans CapCut non testée** ; régression nulle sur l'ancien comportement |
| Rush d'essai, langue, format, plateformes, durée finale | **Bloqué** : en attente de ta part |
| Calibration des seuils (confiance, silences) et des sous-titres (taille en 16:9) | **Bloqué** : nécessite un vrai rush |
| Validation par Dimitri ou le client | **À compléter** |

Détail des tests : `scripts/README.md` (section « Montage long »).
