# Modèle technique CapCut (v1)

Modèle **autonome** utilisé par `scripts/capcut_projet.py` pour créer un projet CapCut. Il remplace le recours à un ancien montage.

## Fichier à conserver

| Fichier | Rôle |
| --- | --- |
| `templates/capcut/modele_technique_v1/modele.json` (33 Ko) | **Le seul fichier nécessaire.** Structure d'un projet CapCut 9.8 : champs et valeurs par défaut du projet, de la piste vidéo, de la piste audio, de la piste texte, des matériaux annexes, du fichier de méta, de l'index et des fichiers de configuration |
| `scripts/capcut_projet.py` | Le générateur qui le lit |
| `scripts/outils/construire_modele_capcut.py` | Outil pour **reconstruire** le modèle depuis un projet fait dans CapCut (seulement si une mise à jour de CapCut change le format) |

Chemin par défaut du modèle, utilisé automatiquement : `templates/capcut/modele_technique_v1/modele.json`. Pour en essayer un autre : `--modele-fichier`.

## Ce qu'il contient, ce qu'il ne contient pas

- **Contenu** : uniquement la structure (noms de champs, valeurs par défaut, objets annexes).
- **Retiré** : tous les médias, noms et chemins de fichiers, textes, polices, identifiants de projet et de matériaux, identifiants d'appareil. 70 identifiants et 17 chemins ou noms ont été retirés à la construction.
- **Vérification** : l'outil de construction **refuse d'écrire** le modèle si une trace subsiste (marqueurs de l'ancien montage, chemin Windows, identifiant, nom de fichier). Le modèle livré a passé cette vérification.
- **Identifiants d'appareil** : ils ne sont pas stockés. Le générateur les lit, au moment de créer un projet, dans un de **tes** projets CapCut récents (jamais écrits dans le dépôt).

## Contrôles effectués

| Contrôle | Résultat |
| --- | --- |
| Régénération de la V5 avec ce modèle, comparée au projet V5 vérifié dans CapCut | 60 rubriques comparées, **0 différence de structure** |
| Traces d'un ancien montage dans un projet généré | Aucune |
| Projet généré à partir du modèle, ouvert dans CapCut 9.8.0.4213 (mode rushes sources) | S'ouvre ; image à l'endroit et plein cadre ; clips, texte et musique présents |

## Quand le reconstruire

Après une mise à jour majeure de CapCut qui refuserait d'ouvrir un projet généré. Il faut alors un projet fait **dans** CapCut (peu importe son contenu), puis :

```powershell
python -I scripts\outils\construire_modele_capcut.py --projet-source "NOM DU PROJET" --sortie templates\capcut\modele_technique_v2\modele.json
```

Le projet source n'est jamais modifié (lecture seule).
