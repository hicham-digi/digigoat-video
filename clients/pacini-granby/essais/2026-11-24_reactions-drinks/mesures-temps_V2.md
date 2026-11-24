# Temps passé par étape — V2 « réactions » (2026-11-24)

Source : horodatages des fichiers (création et dernière écriture) et chronométrage d'un contrôle relancé à la demande. **Rien n'est estimé** : ce qui n'a pas pu être mesuré est indiqué comme tel.

## Mesuré (dernier lancement de `premontage.ps1`, 844 images, 40 plans)

| Étape | Début → fin | Durée |
| --- | --- | --- |
| Vérifications d'entrée, planche du rush | 14:58:05 → 14:58:08 | 3 s |
| Export des 40 segments | 14:58:08 → 14:59:00 | 52 s |
| Analyse de la musique | (entre la fin des segments et le texte) | < 1 s |
| Image de la légende + 40 images de chiffres | 14:59:01 → 14:59:19 | 18 s |
| Encodage MP4 **sans texte** | 14:59:20 → 14:59:41 | 21 s |
| Encodage MP4 **avec texte** (40 superpositions de chiffres) | 14:59:43 → 15:01:56 | **133 s** |
| Contrôles techniques, planche du prémontage, rapport | 15:01:56 → 15:02:17 | 21 s |
| **Total du script** | 14:58:05 → 15:02:17 | **252 s (4 min 12 s)** |

## Mesuré (autres étapes)

| Étape | Durée |
| --- | --- |
| Sauvegarde complète des projets CapCut (1 045 fichiers, contrôlée) | 5 s (15:04:29 → 15:04:34) |
| Création du projet CapCut (écriture + index) | moins d'1 s après la sauvegarde (créé à 15:04:35) |
| Contrôle exhaustif image par image `controle_V2.py` (844 images, 40 chiffres) | 48 s (chronométré à la demande) |
| Contrôle rapide du plan (40 valeurs, durée) | 0,08 s |
| Pour comparaison, V1 : script complet (10 plans, 15,2 s) | 75 s ; sauvegarde 2 s |
| Pour comparaison, extrait de démonstration (6 plans, 4,1 s) | 26 s |

## Fenêtre globale (mesurée)

- Premier lancement de la V2 à **14:40:18**, création du projet CapCut à **15:04:35** : **24 min 17 s**.
- Dans cette fenêtre, `premontage.ps1` a été lancé **4 fois** (départs à 14:40:18, 14:46:02, 14:51:05, 14:58:05, soit 5 min 44 s, 5 min 03 s et 7 min 00 s entre les départs). **Seule la durée du dernier lancement (4 min 12 s) est mesurée** : les trois premiers dossiers ont été supprimés, leur fin n'est pas connue.

## Non mesuré (aucun horodatage disponible)

- L'analyse de la référence et du rush avant le plan.
- La vérification dans l'interface de CapCut (ouverture, lecture, fermeture).
- Le temps de développement entre les lancements (écriture et mise au point de `controle_V2.py`, réglage des plans).
- La rédaction de la documentation.

## Étapes les plus longues (d'après les mesures)

1. **Les 4 lancements du script** : la V2 a nécessité 4 rendus (plan qui perdait des images ; changement de chiffre décalé d'une image ; dernier groupe tronqué). Chaque rendu complet ≈ 4 min ; les défauts auraient été vus **avant** le rendu par un contrôle du plan.
2. **Encodage du MP4 avec texte : 133 s sur 252 s (53 %)**, à cause des 40 superpositions chaînées.
3. **Export des 40 segments : 52 s (21 %)**.
4. Le contrôle exhaustif (48 s), la sauvegarde (5 s) et la génération du projet CapCut (< 1 s) sont **courts**.

## Pistes (hypothèses, **non mesurées**, à valider avant de les appliquer)

- Contrôler le plan avant tout rendu (nombre d'images de chaque passage, valeurs et timecodes du compteur) : secondes au lieu de minutes.
- Ne produire la version « sans texte » que si elle est demandée (21 s) ; ne produire le MP4 que si l'utilisateur en a besoin (le projet CapCut est le livrable par défaut).
- N'exporter qu'une fois chaque passage répété : non étudié, rien de mesuré.
