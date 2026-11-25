# Procédure : montage long avec transcription (client Dimitri, essai)

> Statut : **procédure d'essai du 2026-11-24**, testée seulement sur un rush synthétique. Outils : `scripts/README.md`, section « Montage long ». Aucun choix créatif d'un autre client n'est repris. Une transcription est **toujours un brouillon** à relire par un humain qui écoute.

## Principes

1. **Je n'écoute pas** : seul le texte de la transcription, les images et le signal audio sont analysés. Le signal (silences, niveaux) n'est pas une écoute.
2. **Le sens passe avant le rythme** : conditions, réserves, exceptions, chiffres, références et négations ne sont jamais retirés sans validation.
3. **Rien n'est reconstruit** : un passage incompris reste `[incompris]` avec son timecode.
4. **Coupe ambiguë = proposition** : seuls les silences excessifs (et les répétitions évidentes sans réserve ni chiffre, si la langue a une liste de réserves) sont appliqués d'office. Tout autre retrait de texte attend ta décision.
5. **Rien ne sort de l'ordinateur** : transcription locale, aucun service externe, aucune dépense sans accord.
6. Aucun projet CapCut existant n'est modifié ; CapCut fermé et sauvegarde vérifiée avant d'ajouter un projet.

## Étapes

| # | Étape | Outil | Contrôle (court) |
| --- | --- | --- | --- |
| 1 | Inventaire du rush (durée, flux audio, orientation, images/s) ; copie dans `...\DIMITRI\ESSAIS\<essai>\rushes\` ; originaux intacts | `ffprobe` | Rush lisible, nombre de flux audio noté |
| 2 | Si audio séparé : calage | `caler_audio.py` | Confiance ≥ 5, décalage noté ; à confirmer sur les formes d'onde dans CapCut |
| 3 | Transcription (langue **donnée**) | `transcrire.py` | Texte complet ; passages `[à vérifier]` et `[incompris]` listés avec timecodes |
| 4 | Propositions de coupes | `proposer_coupes.py` | `coupes.md` lu ; aucune réserve retirée sans validation |
| 5 | Validation de l'utilisateur (coupes à valider, passages incertains) ; écoute des passages à enjeu | humain | Décisions notées (`--decisions`) |
| 6 | Plan final, sous-titres recalés, projet CapCut | `proposer_coupes.py --decisions`, `capcut_projet.py` | Projet ouvert dans CapCut, son présent, plans rallongeables, sous-titres modifiables, texte relu |
| 7 | Compte rendu : projet, transcription avec timecodes, liste des coupes et justifications, points à valider, temps par étape, limites | — | Temps relevés sur horodatages réels |

## Commande type (exemple, à adapter)

```powershell
$v = "C:\Users\Hicham\Desktop\Digigoat\OUTILS\transcription\venv\Scripts\python.exe"
$e = "C:\Users\Hicham\Desktop\Digigoat\DIMITRI\ESSAIS\essai-long_01"
& $v scripts\transcrire.py --entree "$e\rushes\RUSH.mp4" --langue <fr|en|...> --sortie "$e\sorties\transcription"
python -I scripts\proposer_coupes.py --transcription "$e\sorties\transcription\RUSH.json" --rush RUSH.mp4 --sortie "$e\sorties\coupes" --langue <fr|en>
python -I scripts\capcut_projet.py --nom "Dimitri - essai long 01" --plan "$e\sorties\coupes\plan_RUSH.csv" --rushes "$e\rushes" --canevas <LxH> --son-origine garder --sous-titres "RUSH=$e\sorties\coupes\sous-titres_apres-coupes.srt" --sauvegarde "C:\Users\Hicham\Desktop\Digigoat\SAUVEGARDES"
```

Avec audio séparé : ajouter `--audios-separes "RUSH=<audio>@<décalage de caler_audio.py>"`. Le canevas (`1920x1080` ou autre) dépend des plateformes (**À compléter**).

## Limites connues

- Imprécision possible de quelques dixièmes de seconde sur les temps des mots : le calage des coupes se vérifie à l'écoute.
- Les listes de mots (réserves, formules de redémarrage, parasites) existent pour l'anglais et le français, sont **provisoires** et non exhaustives. Pour une autre langue : tout retrait de texte est « à valider ».
- Seuils de confiance de `transcrire.py` provisoires : à recalibrer sur de vraies voix. Absence de marqueur ≠ exactitude.
- Hallucinations possibles du modèle dans les silences ou le bruit (observé : un mot inventé sur 0,2 s) : repérées par la confiance et par `proposer_coupes.py` (« bruit probable »).
- Voix multiples, accents marqués, vocabulaire juridique pointu, bruit : qualité non mesurée. Le champ `--vocabulaire` de `transcrire.py` aide pour les noms et termes attendus.
- La taille des sous-titres n'est pas calibrée en 16:9 ; la police par défaut (Arial) est un défaut technique, pas un choix de marque.
