# clients/

Un dossier par marque. Chaque dossier contient les mêmes quatre fichiers, plus deux fichiers facultatifs ajoutés quand ils servent.

## Index : où trouver quoi

| Marque | Dossier | Fichiers facultatifs présents | État de la documentation (2026-11-24) |
| --- | --- | --- | --- |
| Importations Alain | `importations-alain/` | `offres-et-services.md`, `organisation.md` | Complétée le 2026-11-24 avec les documents Drive lus ; restent à compléter : usage des couleurs, tutoiement, canaux, offres actuelles, références approuvées |
| Hormeta Canada | `hormeta/` | `offres-et-services.md`, `organisation.md` | Première version le 2026-11-24 (chartes graphiques lues) ; restent : public, langues par contenu, validation, références, offres actuelles |
| Pacini Granby | `pacini-granby/` | — (offres et coordonnées dans `marque.md`) | Partiellement remplie ; essais de montage dans `essais/` |
| Pacini Marché Central | `pacini-marche-central/` | `offres-et-services.md`, `organisation.md` | Première version le 2026-11-24 (portée des documents communs Pacini vérifiée) ; restent : contact, validation, public, langue, offres confirmées, références |
| Auto Spa Sainte-Julie | `auto-spa-ste-julie/` | `offres-et-services.md`, `organisation.md` | Première version le 2026-11-24 (spécification du site, scripts, recherche de marché lus ; couleurs, police et règles de logo vérifiées sur le guide de logo via l'aperçu Drive) ; restent : contact, validation, tarifs confirmés, langue et ton des vidéos, références |

## Les fichiers d'une marque

| Fichier | Contenu | Où **ne pas** le mettre |
| --- | --- | --- |
| `marque.md` | Activité, public cible, langue, ton, couleurs, polices, logos officiels, éléments à éviter | Contacts, offres, règles de montage |
| `montage.md` | Directives et formats vidéo **validés** : rythme, transitions, cadrage, sous-titres, musique, introduction et fin | Ton général (voir `marque.md`) |
| `references.md` | Vidéos approuvées, avec ce qu'il faut reproduire précisément | Légendes seules : ce ne sont pas des directives |
| `retours-client.md` | Corrections validées, datées, avec la règle à appliquer aux prochains montages | Préférences non confirmées |
| `offres-et-services.md` *(facultatif)* | Services, produits, marques partenaires et offres, **avec leurs dates** | Coordonnées de contact |
| `organisation.md` *(facultatif)* | Contacts, responsabilités et circuit de validation | Directives créatives |

Chaque information vit dans **un seul** fichier ; les autres y renvoient. Pour chaque information : source et date, et statut (**actuel** / **historique** = exemple du passé / **à confirmer**).

## Règles

- Les directives de chaque marque restent **séparées**, même si le même contact client gère plusieurs marques.
- Pour les deux Pacini, les offres, coordonnées et appels à l'action de chaque restaurant sont distincts (section dédiée dans leur `marque.md`).
- « À compléter » signifie : information pas encore fournie. Ne rien inventer.
- Les exemples de style sont illustratifs, jamais des directives approuvées.
- Aucun fichier vidéo ici : seulement les emplacements et les instructions (voir `sops/emplacements-fichiers.md`).

## Ordre conseillé pour remplir un dossier

1. Rassembler : deux ou trois vidéos approuvées, logos et polices autorisés, règles de montage actuelles, corrections récurrentes du client.
2. Remplir `marque.md`, puis `montage.md`.
3. Ajouter les vidéos dans `references.md`.
4. Reporter les corrections dans `retours-client.md`.
