#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère un projet CapCut (Windows) modifiable : un plan par clip sur la piste vidéo, une piste de musique
indépendante (départ et fondus) et un texte modifiable. Python 3 standard + ffprobe/ffmpeg déjà installés.

Deux façons de relier les plans :
  --segments <dossier>   segments déjà découpés (NN_RUSH_nom.mp4) : chaque clip a EXACTEMENT la durée exportée
                         et ne peut pas être rallongé dans CapCut (seulement raccourci).
  --rushes <dossier>     rushes sources + points d'entrée/sortie du plan (colonnes debut et duree) : le clip pointe
                         vers le rush ; on peut le rallonger ou le décaler dans CapCut tant qu'il reste du rush.
                         Le sens de chaque rush paysage sans rotation intégrée est décidé FICHIER PAR FICHIER
                         (--tests-orientation pour les images de test, --orientation-par-rush pour décider) : jamais deviné.

Structure : MODÈLE TECHNIQUE AUTONOME (templates/capcut/modele_technique_v1/modele.json), sans média ni texte d'un
ancien montage. On n'écrit que dans un NOUVEAU dossier de projet. Le seul fichier existant modifié est l'index
`root_meta_info.json`, sauvegardé avant (root_meta_info.json.bak_before_<nom>).
Mode d'emploi : scripts/README.md
"""
import argparse
import copy
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

PROJETS_DEFAUT = Path(os.environ.get('LOCALAPPDATA', '')) / 'CapCut' / 'User Data' / 'Projects' / 'com.lveditor.draft'
MODELE_DEFAUT = Path(__file__).resolve().parent.parent / 'templates' / 'capcut' / 'modele_technique_v1' / 'modele.json'
EXT_VIDEO = ('.mov', '.mp4', '.m4v', '.mkv', '.avi', '.mts', '.mxf')


def guid():
    return str(uuid.uuid4()).upper()


def fwd(p):
    return str(p).replace('\\', '/')


def charger(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)


def ecrire(p, obj):
    with open(p, 'w', encoding='utf-8', newline='') as f:
        json.dump(obj, f, separators=(',', ':'), ensure_ascii=False)


def sonde(chemin):
    """ffprobe : durée (µs) du flux vidéo (ou du conteneur), dimensions, présence d'audio."""
    r = subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', '--', str(chemin)],
                       capture_output=True, text=True, encoding='utf-8')
    if r.returncode != 0:
        raise SystemExit('ffprobe a échoué pour %s : %s' % (chemin, r.stderr.strip()))
    j = json.loads(r.stdout)
    v = next((s for s in j['streams'] if s['codec_type'] == 'video' and s.get('codec_name') != 'png'), None)
    a = next((s for s in j['streams'] if s['codec_type'] == 'audio'), None)
    dur = float(v['duration']) if (v is not None and v.get('duration')) else float(j['format']['duration'])
    rot = 0
    if v is not None:
        for sd in v.get('side_data_list', []) or []:
            if 'rotation' in sd:
                rot = int(sd['rotation'])
    return {'us': int(round(dur * 1e6)), 'w': int(v['width']) if v else 0, 'h': int(v['height']) if v else 0,
            'audio': a is not None, 'taille': os.path.getsize(chemin), 'rotation_fichier': rot}


def capcut_ouvert():
    r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq CapCut.exe'], capture_output=True, text=True)
    return 'CapCut.exe' in r.stdout


def plateforme_locale(projets):
    """Identifiants d'appareil de CETTE machine, lus dans un projet CapCut récent (jamais stockés dans le dépôt)."""
    candidats = []
    for d in Path(projets).iterdir():
        f = d / 'draft_content.json'
        if d.is_dir() and not d.name.startswith('.') and f.exists():
            candidats.append((f.stat().st_mtime, f))
    for _, f in sorted(candidats, reverse=True)[:5]:
        try:
            j = charger(f)
            if j.get('platform', {}).get('device_id'):
                return j['platform'], j.get('last_modified_platform', j['platform'])
        except Exception:
            continue
    return None, None


def lire_plan(chemin, limite):
    lignes = []
    with open(chemin, 'r', encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f, delimiter=';'):
            lignes.append(r)
    lignes.sort(key=lambda r: int(r['ordre']))
    return lignes[:limite] if limite else lignes


def trouver_rush(dossier, nom):
    base = Path(nom).stem.lower()
    for p in sorted(Path(dossier).iterdir()):
        if p.is_file() and p.suffix.lower() in EXT_VIDEO and p.stem.lower() == base:
            return p
    raise SystemExit('Rush introuvable : %s dans %s' % (nom, dossier))


def echelle_remplissage(w, h, rot, L, H):
    """Échelle CapCut pour que le média (tourné de rot degrés) remplisse le canevas L x H."""
    ajust = min(L / float(w), H / float(h))
    dw, dh = w * ajust, h * ajust
    if abs(rot) in (90, 270):
        dw, dh = dh, dw
    return max(L / dw, H / dh)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--nom', required=True, help='Nom du projet CapCut à créer (dossier ASCII conseillé)')
    ap.add_argument('--modele-fichier', default=str(MODELE_DEFAUT), help='modèle technique autonome (modele.json)')
    ap.add_argument('--plan', required=True, help='plan CSV (ordre;rush;debut;duree;nom;note)')
    ap.add_argument('--segments', default='', help='dossier des segments préparés (NN_RUSH_nom.mp4)')
    ap.add_argument('--rushes', default='', help='dossier des rushes sources (liens avec points d\'entrée et de sortie)')
    ap.add_argument('--orientation', default='', choices=['', 'anti-horaire', 'horaire', 'aucune'], help='sens par défaut des rushes paysage sans rotation intégrée (facultatif : sinon décider rush par rush)')
    ap.add_argument('--orientation-par-rush', default='', help='sens décidé rush par rush : "DGM_0001=horaire;DGM_0002=anti-horaire" (prioritaire sur --orientation)')
    ap.add_argument('--tests-orientation', default='', help='dossier où écrire une image de test par rush (origine | horaire | anti-horaire) puis s\'arrêter')
    ap.add_argument('--musique', default='', help='piste musicale (facultative)')
    ap.add_argument('--depart', type=float, default=0.0, help='départ dans la piste, en secondes')
    ap.add_argument('--fondu-entree', type=float, default=0.0)
    ap.add_argument('--fondu-sortie', type=float, default=0.0)
    ap.add_argument('--volume-musique', type=float, default=1.0)
    ap.add_argument('--texte', default='', help='texte ; "|" = saut de ligne')
    ap.add_argument('--police', default='C:/Windows/Fonts/CALIFR.TTF', help='fichier de police du texte')
    ap.add_argument('--police-nom', default='Californian FB')
    ap.add_argument('--taille-capcut', type=float, default=4.16, help='taille de texte CapCut (1 unité = 6,42 px à 1080x1920)')
    ap.add_argument('--texte-y', type=float, default=0.0, help='position verticale CapCut : 0 = milieu, + = vers le haut')
    ap.add_argument('--compteur', default='', help='un chiffre par plan, sur une piste de texte séparée : "1;2;3;..." (même police et même taille que --texte)')
    ap.add_argument('--compteur-y', type=float, default=-0.17, help='position verticale CapCut du compteur (0 = milieu, + = vers le haut ; -0,17 = 58,5 %% de la hauteur)')
    ap.add_argument('--limiter', type=int, default=0, help='ne garder que les N premiers plans (projet de test)')
    ap.add_argument('--projets', default=str(PROJETS_DEFAUT), help='dossier des projets CapCut')
    ap.add_argument('--essai-local', default='', help='écrire le projet dans ce dossier au lieu de CapCut (aucun index modifié)')
    ap.add_argument('--sauvegarde', default='', help='dossier où copier TOUS les projets CapCut existants (avec vérification) AVANT de créer le projet')
    a = ap.parse_args()

    if bool(a.segments) == bool(a.rushes):
        raise SystemExit('Indiquez exactement un des deux : --segments (plans découpés) ou --rushes (liens aux rushes sources).')

    projets = Path(a.projets)
    local = bool(a.essai_local)
    if not local and capcut_ouvert():
        raise SystemExit("CapCut est ouvert : fermez-le complètement (il réécrit l'index des projets en se fermant), puis relancez.")
    if not Path(a.modele_fichier).exists():
        raise SystemExit('Modèle technique introuvable : %s' % a.modele_fichier)
    racine_sortie = Path(a.essai_local) if local else projets
    nouveau = racine_sortie / a.nom
    if nouveau.exists():
        raise SystemExit('Le projet existe déjà (jamais écrasé) : %s' % nouveau)

    M = charger(a.modele_fichier)
    if M.get('version_modele') != 1:
        raise SystemExit('Version de modèle non gérée : %s' % M.get('version_modele'))
    tpl = M['draft_content']
    P = M['prototypes']
    canvas_l, canvas_h = tpl['canvas_config']['width'], tpl['canvas_config']['height']

    # ------------------------------------------------------------ plan et médias
    lignes = lire_plan(a.plan, a.limiter)
    segs = []
    for r in lignes:
        if a.segments:
            pref = '%02d_%s_' % (int(r['ordre']), r['rush'])
            trouves = sorted(p for p in Path(a.segments).glob('*.mp4') if p.name.startswith(pref))
            if not trouves:
                raise SystemExit('Segment introuvable pour la ligne %s (%s) dans %s' % (r['ordre'], r['rush'], a.segments))
            fichier = trouves[0]
            info = sonde(fichier)
            deb, dur = 0, info['us']
        else:
            fichier = trouver_rush(a.rushes, r['rush'])
            info = sonde(fichier)
            deb = int(round(float(str(r['debut']).replace(',', '.')) * 1e6))
            dur = int(round(float(str(r['duree']).replace(',', '.')) * 1e6))
            if deb + dur > info['us'] + 50000:
                raise SystemExit('Plan hors du rush %s : début %.2f + durée %.2f > %.2f s' % (fichier.name, deb / 1e6, dur / 1e6, info['us'] / 1e6))
        segs.append({'fichier': fichier, 'info': info, 'deb': deb, 'dur': dur, 'nom': r.get('nom', '')})

    # ------------------------------------------------------------ orientation : décidée fichier par fichier, jamais devinée
    carte = {}
    for paire in re.split(r'[;,]', a.orientation_par_rush):
        if not paire.strip():
            continue
        m = re.match(r'^\s*([^=]+?)\s*=\s*(\S+)\s*$', paire)
        if not m or m.group(2) not in ('aucune', 'anti-horaire', 'horaire'):
            raise SystemExit('--orientation-par-rush : entrée illisible « %s » (attendu NOM=aucune|anti-horaire|horaire)' % paire)
        carte[Path(m.group(1)).stem.lower()] = m.group(2)
    if a.rushes:
        besoin = []
        for s in segs:
            i = s['info']
            s['orient'] = carte.get(s['fichier'].stem.lower(), a.orientation)
            s['besoin'] = (i['rotation_fichier'] == 0 and i['w'] > i['h'] and canvas_h > canvas_l)
            if s['besoin'] and not s['orient'] and s['fichier'] not in besoin:
                besoin.append(s['fichier'])
        inconnus = [k for k in carte if k not in {s['fichier'].stem.lower() for s in segs}]
        if inconnus:
            print('Attention : --orientation-par-rush cite des rushes absents du plan : %s' % ', '.join(inconnus))
        if a.tests_orientation:
            dossier = Path(a.tests_orientation)
            dossier.mkdir(parents=True, exist_ok=True)
            faits = []
            for s in segs:
                if s['besoin'] and s['fichier'] not in faits:
                    faits.append(s['fichier'])
                    sortie_img = dossier / ('orientation_%s.png' % s['fichier'].stem)
                    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '%.2f' % (s['info']['us'] / 2e6), '-i', str(s['fichier']), '-frames:v', '1',
                                    '-filter_complex', 'split=3[a][b][c];[a]scale=-1:640[o];[b]transpose=1,scale=-1:640[h];[c]transpose=2,scale=-1:640[ah];[o][h][ah]hstack=inputs=3',
                                    str(sortie_img)])
                    print('Image de test : %s' % sortie_img)
            print("De gauche à droite : image d'origine | rotation HORAIRE | rotation ANTI-HORAIRE. Repérez celle où le décor est à l'endroit, pour CHAQUE rush.")
            sys.exit(0)
        if besoin:
            raise SystemExit("Orientation à décider (jamais devinée) pour : %s.\nGénérez les images de test avec --tests-orientation <dossier>, regardez-les, puis relancez avec --orientation-par-rush \"NOM=horaire;NOM2=anti-horaire\"." % ', '.join(f.name for f in besoin))
    total = sum(s['dur'] for s in segs)

    mats = {k: ([] if isinstance(v, list) else copy.deepcopy(v)) for k, v in tpl['materials'].items()}
    maintenant_us = int(time.time() * 1e6)
    maintenant_s = int(time.time())
    entrees_meta = []
    ids_locaux = []

    def ajouter_extras(annexes, modif=None):
        refs = []
        for cle, obj in annexes:
            n = copy.deepcopy(obj)
            n['id'] = guid()
            if modif:
                modif(cle, n)
            mats[cle].append(n)
            refs.append(n['id'])
        return refs

    # ------------------------------------------------------------ piste vidéo
    segments_video = []
    debut = 0
    for s in segs:
        i = s['info']
        m = copy.deepcopy(P['video']['materiau'])
        local_id = str(uuid.uuid4())
        m.update({'id': guid(), 'unique_id': uuid.uuid4().hex, 'type': 'video', 'duration': i['us'], 'path': fwd(s['fichier']),
                  'media_path': '', 'has_audio': i['audio'], 'width': i['w'], 'height': i['h'],
                  'material_name': s['fichier'].name, 'local_material_id': local_id})
        mats['videos'].append(m)
        ids_locaux.append(local_id)
        entrees_meta.append({'ai_group_type': '', 'create_time': maintenant_s, 'duration': i['us'], 'enter_from': 0,
                             'extra_info': s['fichier'].name, 'file_Path': fwd(s['fichier']), 'height': i['h'], 'id': local_id,
                             'import_time': maintenant_s, 'import_time_ms': maintenant_us, 'item_source': 1,
                             'material_color_tag': '', 'md5': '', 'metetype': 'video',
                             'roughcut_time_range': {'duration': i['us'], 'start': 0},
                             'sub_time_range': {'duration': -1, 'start': -1}, 'type': 0, 'width': i['w']})
        g = copy.deepcopy(P['video']['segment'])
        g['id'] = guid()
        g['material_id'] = m['id']
        g['source_timerange'] = {'start': s['deb'], 'duration': s['dur']}
        g['target_timerange'] = {'start': debut, 'duration': s['dur']}
        g['speed'] = 1.0
        g['volume'] = 0.0                      # sons d'origine coupés (la V5 n'a que la musique)
        g['last_nonzero_volume'] = 1.0
        rotation, echelle = 0.0, 1.0
        if a.rushes and s.get('besoin'):
            if s['orient'] == 'anti-horaire':
                rotation = -90.0
            elif s['orient'] == 'horaire':
                rotation = 90.0
            if rotation:
                echelle = echelle_remplissage(i['w'], i['h'], 90, canvas_l, canvas_h)
        g['clip']['scale'] = {'x': echelle, 'y': echelle}
        g['clip']['rotation'] = rotation
        g['clip']['transform'] = {'x': 0.0, 'y': 0.0}
        g['uniform_scale'] = {'on': True, 'value': echelle}
        g['extra_material_refs'] = ajouter_extras(P['video']['annexes'])
        g['render_index'] = 0
        g['track_render_index'] = 0
        segments_video.append(g)
        debut += s['dur']

    pistes = []
    piste_v = copy.deepcopy(P['video']['piste'])
    piste_v.update({'id': guid(), 'segments': segments_video, 'flag': 0})
    pistes.append(piste_v)

    # ------------------------------------------------------------ piste audio (musique)
    musique_info = None
    mi = None
    if a.musique:
        mus = Path(a.musique)
        if not mus.exists():
            raise SystemExit('Musique introuvable : %s' % mus)
        mi = sonde(mus)
        depart_us = int(round(a.depart * 1e6))
        if depart_us + total > mi['us'] + 1000:
            raise SystemExit('La piste (%.1f s) est trop courte pour un départ à %.2f s et une durée de %.2f s.' % (mi['us'] / 1e6, a.depart, total / 1e6))
        local_id = str(uuid.uuid4())
        m = copy.deepcopy(P['audio']['materiau'])
        m.update({'id': guid(), 'unique_id': uuid.uuid4().hex, 'type': 'extract_music', 'name': mus.name, 'duration': mi['us'],
                  'path': fwd(mus), 'category_name': 'local', 'music_id': str(uuid.uuid4()), 'local_material_id': local_id})
        mats['audios'].append(m)
        ids_locaux.append(local_id)
        entrees_meta.append({'ai_group_type': '', 'create_time': maintenant_s, 'duration': mi['us'], 'enter_from': 0,
                             'extra_info': mus.name, 'file_Path': fwd(mus), 'height': 0, 'id': local_id,
                             'import_time': maintenant_s, 'import_time_ms': maintenant_us, 'item_source': 1,
                             'material_color_tag': '', 'md5': '', 'metetype': 'music',
                             'roughcut_time_range': {'duration': mi['us'], 'start': 0},
                             'sub_time_range': {'duration': -1, 'start': -1}, 'type': 0, 'width': 0})

        def modif_audio(cle, n):
            if cle == 'audio_fades':
                n['fade_type'] = 0
                n['fade_in_duration'] = int(round(a.fondu_entree * 1e6))
                n['fade_out_duration'] = int(round(a.fondu_sortie * 1e6))
        g = copy.deepcopy(P['audio']['segment'])
        g['id'] = guid()
        g['material_id'] = m['id']
        g['source_timerange'] = {'start': depart_us, 'duration': total}
        g['target_timerange'] = {'start': 0, 'duration': total}
        g['volume'] = a.volume_musique
        g['last_nonzero_volume'] = 1.0
        g['extra_material_refs'] = ajouter_extras(P['audio']['annexes'], modif_audio)
        g['track_render_index'] = 1
        piste_a = copy.deepcopy(P['audio']['piste'])
        piste_a.update({'id': guid(), 'segments': [g], 'flag': 0})
        pistes.append(piste_a)
        musique_info = {'nom': mus.name}

    # ------------------------------------------------------------ piste texte (modifiable)
    def faire_texte(contenu_texte, debut_us, duree_us, y, idx_piste):
        texte = '\n'.join(x.strip() for x in contenu_texte.split('|'))
        m = copy.deepcopy(P['texte']['materiau'])
        police = fwd(a.police)
        contenu = {'text': texte, 'styles': [{
            'fill': {'content': {'render_type': 'solid', 'solid': {'color': [1, 1, 1]}}},
            'font': {'path': police, 'id': ''}, 'size': a.taille_capcut, 'useLetterColor': True, 'range': [0, len(texte)]}]}
        m.update({
            'id': guid(), 'type': 'text', 'content': json.dumps(contenu, separators=(',', ':'), ensure_ascii=False),
            'font_name': a.police_nom, 'font_title': 'none', 'font_path': police, 'font_id': '', 'font_resource_id': '',
            'font_url': '', 'font_source_platform': 1, 'fonts': [], 'font_size': a.taille_capcut, 'text_color': '#ffffff',
            'text_alpha': 1.0, 'alignment': 1, 'line_spacing': 0.0, 'letter_spacing': 0.0, 'bold_width': 0.0, 'italic_degree': 0,
            'has_shadow': True, 'shadow_color': '#000000', 'shadow_alpha': 0.7, 'shadow_smoothing': 0.45,
            'shadow_distance': 2.0, 'shadow_angle': -90.0, 'shadow_point': {'x': 0.0, 'y': -0.9},
            'check_flag': 47, 'background_alpha': 1.0, 'font_category_name': '', 'font_third_resource_id': ''})
        mats['texts'].append(m)
        g = copy.deepcopy(P['texte']['segment'])
        g['id'] = guid()
        g['material_id'] = m['id']
        g['source_timerange'] = None
        g['target_timerange'] = {'start': debut_us, 'duration': duree_us}
        g['clip']['scale'] = {'x': 1.0, 'y': 1.0}
        g['clip']['rotation'] = 0.0
        g['clip']['transform'] = {'x': 0.0, 'y': y}
        g['uniform_scale'] = {'on': True, 'value': 1.0}
        g['extra_material_refs'] = ajouter_extras(P['texte']['annexes'])
        g['track_render_index'] = idx_piste
        return g

    if a.texte:
        piste_t = copy.deepcopy(P['texte']['piste'])
        piste_t.update({'id': guid(), 'segments': [faire_texte(a.texte, 0, total, a.texte_y, 2)], 'flag': 0})
        pistes.append(piste_t)

    # ------------------------------------------------------------ piste du compteur : un texte par plan, sur sa propre piste
    if a.compteur:
        valeurs = [v.strip() for v in re.split(r'[;,]', a.compteur) if v.strip()]
        if len(valeurs) != len(segs):
            raise SystemExit('--compteur : %d valeur(s) pour %d plan(s) : il en faut une par plan.' % (len(valeurs), len(segs)))
        segs_c = []
        t0 = 0
        for v, s in zip(valeurs, segs):
            segs_c.append(faire_texte(v, t0, s['dur'], a.compteur_y, 3))
            t0 += s['dur']
        piste_c = copy.deepcopy(P['texte']['piste'])
        piste_c.update({'id': guid(), 'segments': segs_c, 'flag': 0})
        pistes.append(piste_c)

    # ------------------------------------------------------------ draft_content
    id_timeline = guid()
    id_projet = guid()
    d = copy.deepcopy(tpl)
    d['id'] = id_timeline
    d['duration'] = total
    d['tracks'] = pistes
    d['materials'] = mats
    d['name'] = ''
    pf, pf_modif = plateforme_locale(projets)
    if pf:
        d['platform'] = pf
        d['last_modified_platform'] = pf_modif

    # ------------------------------------------------------------ contrôle d'intégrité
    ids = set()
    for arr in mats.values():
        if isinstance(arr, list):
            for o in arr:
                if isinstance(o, dict) and 'id' in o:
                    ids.add(o['id'])
    for t in pistes:
        for g in t['segments']:
            for r in [g['material_id']] + list(g['extra_material_refs']):
                if r not in ids:
                    raise SystemExit('Contrôle interne : référence manquante %s' % r)
    if max(g['target_timerange']['start'] + g['target_timerange']['duration'] for g in segments_video) != total:
        raise SystemExit('Contrôle interne : durée incohérente')

    # ------------------------------------------------------------ sauvegarde complète des projets existants (avant toute écriture)
    if a.sauvegarde and not local:
        slug_s = re.sub(r'[^A-Za-z0-9]+', '_', a.nom).strip('_').lower()
        dest = Path(a.sauvegarde) / ('capcut-projets_avant-%s_%s' % (slug_s, time.strftime('%Y%m%d_%H%M')))
        if dest.exists():
            raise SystemExit('La sauvegarde existe déjà : %s' % dest)
        shutil.copytree(projets, dest, ignore=shutil.ignore_patterns('.recycle_bin'))

        def compter(rac):
            n = 0
            for r, ds, fs in os.walk(rac):
                ds[:] = [d for d in ds if d != '.recycle_bin']
                n += len(fs)
            return n
        if compter(projets) != compter(dest):
            raise SystemExit('Sauvegarde incomplète (%d fichiers sur %d) : abandon avant toute modification.' % (compter(dest), compter(projets)))
        print('Sauvegarde des projets : %s (%d fichiers)' % (dest, compter(dest)))

    # ------------------------------------------------------------ écriture du projet
    nouveau.mkdir(parents=True)
    for sous in ('adjust_mask', 'common_attachment', 'matting', 'qr_upload', 'Resources', 'smart_crop', 'subdraft', 'Timelines'):
        (nouveau / sous).mkdir()
    tl_new = nouveau / 'Timelines' / id_timeline
    tl_new.mkdir()

    def jetons(t):
        return t.replace('{{ID_TIMELINE}}', id_timeline).replace('{{ID_PROJET}}', id_projet)

    for nom, texte_f in M['fichiers']['racine'].items():
        if nom == 'draft_settings':
            texte_f = texte_f.replace('{{S}}', str(maintenant_s))
        (nouveau / nom).write_bytes(jetons(texte_f).encode('utf-8'))
    for rel, texte_f in M['fichiers']['timeline'].items():
        cible = tl_new / rel
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_bytes(jetons(texte_f).encode('utf-8'))
    (tl_new / 'attachment' / 'patch').mkdir(parents=True, exist_ok=True)
    (nouveau / 'key_value.json').write_text('{}', encoding='utf-8')

    ecrire(nouveau / 'draft_content.json', d)
    ecrire(tl_new / 'draft_content.json', d)
    shutil.copyfile(nouveau / 'draft_content.json', nouveau / 'template-2.tmp')
    shutil.copyfile(nouveau / 'draft_content.json', tl_new / 'template-2.tmp')

    cover = nouveau / 'draft_cover.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '%.2f' % (segs[0]['deb'] / 1e6 + 0.5), '-i', str(segs[0]['fichier']), '-frames:v', '1',
                    '-vf', 'scale=540:-2', '-q:v', '3', str(cover)])
    if cover.exists():
        shutil.copyfile(cover, tl_new / 'draft_cover.jpg')

    taille = sum(s['info']['taille'] for s in segs) + (mi['taille'] if mi else 0)
    meta = copy.deepcopy(M['meta'])
    meta.update({'draft_id': id_projet, 'draft_name': a.nom, 'draft_fold_path': fwd(nouveau), 'draft_root_path': fwd(racine_sortie),
                 'tm_draft_create': maintenant_us, 'tm_draft_modified': maintenant_us, 'tm_duration': total,
                 'draft_timeline_materials_size_': taille})
    for bloc in meta['draft_materials']:
        bloc['value'] = entrees_meta if bloc['type'] == 0 else []
    ecrire(nouveau / 'draft_meta_info.json', meta)

    vs = copy.deepcopy(M['virtual_store'])
    for bloc in vs['draft_virtual_store']:
        if bloc['type'] == 1:
            bloc['value'] = [{'child_id': x, 'parent_id': ''} for x in ids_locaux]
    ecrire(nouveau / 'draft_virtual_store.json', vs)

    pj = copy.deepcopy(M['project'])
    pj['id'] = guid()
    pj['main_timeline_id'] = id_timeline
    pj['create_time'] = maintenant_us
    pj['update_time'] = maintenant_us
    for t in pj['timelines']:
        t['id'] = id_timeline
        t['create_time'] = maintenant_us
        t['update_time'] = maintenant_us
    ecrire(nouveau / 'Timelines' / 'project.json', pj)
    shutil.copyfile(nouveau / 'Timelines' / 'project.json', nouveau / 'Timelines' / 'project.json.bak')

    # ------------------------------------------------------------ index des projets (seul fichier existant modifié)
    if not local:
        racine_meta = projets / 'root_meta_info.json'
        slug = re.sub(r'[^A-Za-z0-9]+', '_', a.nom).strip('_').lower()
        sauvegarde = projets / ('root_meta_info.json.bak_before_' + slug)
        k = 1
        while sauvegarde.exists():
            k += 1
            sauvegarde = projets / ('root_meta_info.json.bak_before_%s_%d' % (slug, k))
        shutil.copyfile(racine_meta, sauvegarde)
        rm = charger(racine_meta)
        e = copy.deepcopy(M['index_entree'])
        e.update({'draft_cover': fwd(nouveau) + '\\draft_cover.jpg', 'draft_fold_path': fwd(nouveau), 'draft_id': id_projet,
                  'draft_json_file': fwd(nouveau) + '\\draft_content.json', 'draft_name': a.nom, 'draft_root_path': fwd(projets),
                  'draft_timeline_materials_size': taille, 'tm_draft_create': maintenant_us, 'tm_draft_modified': maintenant_us,
                  'tm_duration': total, 'streaming_edit_draft_ready': True})
        rm['all_draft_store'].insert(0, e)
        rm['draft_ids'] = int(rm['draft_ids']) + 1
        tmp = projets / 'root_meta_info.json.tmp_ecriture'
        ecrire(tmp, rm)
        os.replace(tmp, racine_meta)
        print('Index mis à jour. Sauvegarde : %s' % sauvegarde.name)

    print('Projet créé : %s' % nouveau)
    print('Plans : %d (%s) ; durée %.3f s ; musique : %s ; texte : %s' % (
        len(segs), 'liés aux rushes sources, rallongeables' if a.rushes else 'segments découpés, durée fixe', total / 1e6,
        ('%s (départ %.2f s, fondus %.2f/%.2f s)' % (musique_info['nom'], a.depart, a.fondu_entree, a.fondu_sortie)) if musique_info else 'aucune',
        'oui' if a.texte else 'non'))


if __name__ == '__main__':
    main()
