# Analyse de la référence — V2 (mécanique mesurée en entier)

Remplace les constats de `analyse-reference.md` sur le rythme (cette V1 est conservée). Mesures faites le 2026-11-24 sur `New Fall Menu got our ticket printer working overtime…mp4`.

## Observé (mesuré)

- **Durée réelle : 28,13 s** (844 images à 30 i/s, 720×1280). Ma première indication (« 15-20 s ») venait de ta demande ; la référence dure 28 s.
- **Compteur : exactement 40 valeurs, 1 à 40, +1 à chaque changement**, un seul nombre à l'écran à la fois. 39 changements, relevés à l'image près (compteur lu sur 10 images/s au début, puis sur les changements d'image).
- **Chaque changement de chiffre est une coupe franche, et le plan qui suit est la répétition du précédent** : entre deux plans de la même série, l'image diffère de moins de 1,2 niveau de gris sur 255 (début et fin identiques), alors que le saut à la coupe est de 3 à 36. Il y a donc une **boucle** : un court passage rejoué.
- **13 réactions** ; chacune est rejouée **3 fois** (une seule, la 5ᵉ, **4 fois**) : 12 × 3 + 4 = 40.
- Les boucles sont plus courtes vers la fin (de 1,0 s à 0,43 s) : le rythme s'accélère.
- La légende est fixe sur toute la durée ; le compteur est sous la légende.

| # | Chiffres | Reps | Durée d'une boucle | Réaction (lecture visuelle, approximative) |
| --- | --- | --- | --- | --- |
| 1 | 1–3 | 3 | 0,63 s (19 im.) | sourire calme (saut presque nul) |
| 2 | 4–6 | 3 | 0,63 s (19) | sourire franc vers la caméra |
| 3 | 7–9 | 3 | 0,73 s (22) | sourire, il parle |
| 4 | 10–12 | 3 | 0,73 s (22) | surprise, bouche en « o » |
| 5 | 13–16 | **4** | 0,73 s (22) | sourcils levés, inquiet |
| 6 | 17–19 | 3 | 0,83 s (25) | perplexe |
| 7 | 20–22 | 3 | 1,00 s (30) | il parle, inquiet |
| 8 | 23–25 | 3 | 0,77 s (23) | il parle, inquiet |
| 9 | 26–28 | 3 | 0,97 s (29) | regard baissé de côté |
| 10 | 29–31 | 3 | 0,47 s (14) | regard levé de côté |
| 11 | 32–34 | 3 | 0,63 s (19) | mains ouvertes, effrayé |
| 12 | 35–37 | 3 | 0,57 s (17) | mains sur la tête |
| 13 | 38–40 | 3 | 0,43 s (13) | regard levé, soupir |

Total : 844 images = 28,13 s. Les durées de boucle et les nombres de répétitions sont mesurés ; les descriptions des réactions sont mes lectures d'images.

## Ce que je ne peux pas déterminer

- Si les répétitions sont une boucle exacte d'un même extrait ou des reprises très proches : les images sont identiques à moins de 1,2/255, donc une boucle, mais je n'ai pas le fichier source.
- Le son (non analysé) et la synchronisation éventuelle avec les chiffres.
- La police exacte du compteur (grande, grasse, avec contour : plus visible que la nôtre).
- Pourquoi la 5ᵉ réaction a 4 répétitions (choix de l'auteur, sans autre indice).

## Application à notre rush (V2)

Rush de 17,4 s : 13 passages courts de 13 à 30 images, **dans l'ordre du rush**, chacun répété 3 fois (la 5ᵉ 4 fois), avec **les mêmes longueurs de boucle que la référence** (donc 844 images, **28,16 s**). Tableau et passages choisis : `plan-de-montage_V2.md`.
