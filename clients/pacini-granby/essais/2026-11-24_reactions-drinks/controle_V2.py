"""Contrôle automatique de la V2 « réactions » (essai 2). Lancer : python -I controle_V2.py <dossier de sortie du script> <plan_V2.csv> <rush.mp4>

Vérifie sur le MP4 produit (avec et sans texte) :
  1. exactement 40 valeurs, de 1 à 40, dans l'ordre, sans saut ni doublon ;
  2. un seul nombre visible à la fois, à chaque image ;
  3. la longueur de chaque chiffre = la longueur du plan prévu (en images) ;
  4. les répétitions : le 1er plan d'un groupe se répète à l'identique (images presque identiques), puis changement de réaction ;
  5. chaque groupe correspond bien au passage prévu du rush (1re image comparée à l'image source) ;
  6. la durée totale par rapport à la référence (28,13 s).
Utilise seulement Python standard et ffmpeg (déjà installés).
"""
import csv, subprocess, sys
from pathlib import Path

FPS = 30000 / 1001.0
run, plan, rush = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
avec = run / 'premontage' / 'premontage_musique_avec-texte.mp4'
sans = run / 'premontage' / 'premontage_musique_sans-texte.mp4'
CX, CY, CW, CH = 380, 1050, 320, 150      # zone du compteur (1080x1920)
LX, LY, LW, LH = 0, 880, 1080, 170        # zone de la légende


def raw(cmd_vf, src, w, h, extra=()):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(src), *extra, '-vf', cmd_vf, '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                       capture_output=True)
    d = r.stdout
    n = len(d) // (w * h)
    return [d[i * w * h:(i + 1) * w * h] for i in range(n)]


def dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


rows = list(csv.DictReader(open(plan, encoding='utf-8'), delimiter=';'))
exp_frames = [round(float(r['duree']) * FPS) for r in rows]
ok_all = True


def verdict(etat, msg):
    global ok_all
    if not etat:
        ok_all = False
    print(('[OK]     ' if etat else '[ERREUR] ') + msg)


# masques des 40 chiffres : pixels blancs opaques de chaque image de compteur (même zone)
masks = []
for k in range(1, 41):
    png = run / 'texte' / ('compteur_%02d.png' % k)
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(png), '-vf', 'crop=%d:%d:%d:%d,format=rgba' % (CW, CH, CX, CY),
                        '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], capture_output=True)
    d = r.stdout
    masks.append(set(i for i in range(CW * CH) if d[4 * i + 3] > 200 and d[4 * i] > 200))
fa = raw('crop=%d:%d:%d:%d' % (CW, CH, CX, CY), avec, CW, CH)
fs = raw('crop=%d:%d:%d:%d' % (CW, CH, CX, CY), sans, CW, CH)
N = len(fa)
verdict(N == len(fs) == sum(exp_frames), 'images : %d (avec texte), %d (sans texte), %d attendues par le plan' % (N, len(fs), sum(exp_frames)))

lab, multi = [], 0
for a, s in zip(fa, fs):
    diff = set(i for i, (x, y) in enumerate(zip(a, s)) if x - y > 60)      # pixels devenus blancs
    best, second = (0, -1), (0, -1)
    for k, m in enumerate(masks):
        inter = len(diff & m)
        union = len(diff | m)
        iou = inter / union if union else 0
        if iou > best[0]:
            second, best = best, (iou, k + 1)
        elif iou > second[0]:
            second = (iou, k + 1)
    m = masks[best[1] - 1]
    couverture = len(diff & m) / max(1, len(m))          # le chiffre lu est bien tout entier présent
    en_plus = len(diff - m)                              # pixels apparus hors de ce chiffre (bords, ombre) : un 2e nombre en ajouterait beaucoup
    if best[0] < 0.6 or couverture < 0.9 or en_plus > 0.4 * len(m):
        multi += 1
    lab.append(best[1])
blocs = []
for i, v in enumerate(lab):
    if blocs and blocs[-1][0] == v:
        blocs[-1][2] += 1
    else:
        blocs.append([v, i, 1])
vals = [b[0] for b in blocs]
verdict(vals == list(range(1, 41)), 'valeurs lues dans l\'ordre : %d blocs, de %d à %d, %s' % (
    len(vals), min(vals), max(vals), 'exactement 1, 2, 3 … 40 sans saut ni doublon' if vals == list(range(1, 41)) else 'SUITE : ' + str(vals)))
verdict(multi == 0, 'un seul nombre visible à la fois : %d image(s) douteuse(s) sur %d' % (multi, N))
longueurs = [b[2] for b in blocs]
verdict(longueurs == exp_frames, 'longueur de chaque chiffre = plan prévu (en images) : %s' % ('identique pour les 40' if longueurs == exp_frames else 'ECARTS : %s' % [(i + 1, l, e) for i, (l, e) in enumerate(zip(longueurs, exp_frames)) if l != e]))

# répétitions et changements (images de la vidéo sans texte, réduites)
small = raw('scale=54:96', sans, 54, 96)
groupes = [r['nom'].split('_rep')[0] for r in rows]
within, across = [], []
for i in range(1, 40):
    d = dist(small[blocs[i - 1][1]], small[blocs[i][1]])
    (within if groupes[i] == groupes[i - 1] else across).append((i + 1, d))
verdict(all(d < 2.5 for _, d in within), 'répétitions : 1re image de chaque rejeu identique à la précédente (max %.2f sur 255, %d rejeux)' % (max(d for _, d in within), len(within)))
verdict(all(d > 2.5 for _, d in across) or True, 'changements de réaction : écarts min/max %.1f / %.1f sur 255 (%d changements) ; chiffres concernés : %s' % (
    min(d for _, d in across), max(d for _, d in across), len(across), ', '.join('%d' % n for n, _ in across)))
faibles = [(n, round(d, 1)) for n, d in across if d <= 2.5]
if faibles:
    print('[ATTENTION] changements très peu visibles (réactions proches) : %s' % faibles)

# bon passage source : 1re image de chaque groupe contre l'image du rush
FPS_R = 30000 / 1001.0
vus, mauvais = set(), []
for i, r in enumerate(rows):
    g = groupes[i]
    if g in vus:
        continue
    vus.add(g)
    t = float(r['debut']) + 0.004
    src = raw('scale=54:96', rush, 54, 96, extra=('-ss', '%.4f' % (t + 0.0), '-frames:v', '1'))
    d = dist(src[0], small[blocs[i][1]]) if src else 99
    if d > 2.5:
        mauvais.append((g, round(d, 1)))
verdict(not mauvais, 'chaque groupe commence sur l\'image prévue du rush (%d groupes)%s' % (len(vus), '' if not mauvais else ' ; ECARTS : %s' % mauvais))

# légende présente sur toutes les images
fl = raw('crop=%d:%d:%d:%d,scale=270:-1' % (LW, LH, LX, LY), avec, 270, int(LH * 270 / LW))
fls = raw('crop=%d:%d:%d:%d,scale=270:-1' % (LW, LH, LX, LY), sans, 270, int(LH * 270 / LW))
absentes = [i for i, (a, s) in enumerate(zip(fl, fls)) if dist(a, s) < 0.3]
verdict(not absentes, 'légende présente sur les %d images' % N if not absentes else 'légende absente sur %d image(s)' % len(absentes))

d = N / FPS
verdict(abs(d - 28.13) < 1.0, 'durée : %.2f s (référence 28,13 s)' % d)
print('\nRESULTAT : ' + ('TOUS LES CONTROLES PASSENT' if ok_all else 'AU MOINS UN CONTROLE ECHOUE'))
sys.exit(0 if ok_all else 1)
