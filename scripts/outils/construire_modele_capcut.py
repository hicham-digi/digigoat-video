#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit le MODÈLE TECHNIQUE AUTONOME de projet CapCut (templates/capcut/modele_technique_v1/modele.json)
à partir d'un projet fait dans CapCut. À relancer seulement si CapCut change de version de format.

Le modèle ne garde que la STRUCTURE : champs, valeurs par défaut, objets annexes. Tout ce qui vient du
montage source est retiré : médias, chemins, noms, textes, polices, identifiants (projet, matériaux),
identifiants d'appareil. Une vérification finale refuse d'écrire le modèle si une trace subsiste.

Lecture seule sur le projet source. Usage :
  python -I scripts/outils/construire_modele_capcut.py --projet-source "Pates flambees"
"""
import argparse
import copy
import json
import os
import re
import sys
from pathlib import Path

PROJETS = Path(os.environ.get('LOCALAPPDATA', '')) / 'CapCut' / 'User Data' / 'Projects' / 'com.lveditor.draft'
SORTIE = Path(__file__).resolve().parent.parent.parent / 'templates' / 'capcut' / 'modele_technique_v1' / 'modele.json'

GUID = re.compile(r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$')
HEX32 = re.compile(r'^[0-9a-fA-F]{32}$')
CHEMIN = re.compile(r'[A-Za-z]:[\\/]')
EXTENSIONS = re.compile(r'\.(mp4|mov|mp3|wav|m4a|ttf|otf|jpg|png|mkv|avi)\b', re.I)
MARQUEURS = ['Hicham', 'AppData', 'DGM_', 'dolce', 'Bodoni', 'Pates', 'poêle', 'Downloads', 'Digigoat', 'PACINI', 'Pacini', 'BEATS',
             'Contre-filet', 'DJI_', 'Timeline 01 ']
compteur = {'guid': 0, 'chemin': 0, 'texte': 0}


def nettoyer(o):
    if isinstance(o, dict):
        return {k: nettoyer(v) for k, v in o.items()}
    if isinstance(o, list):
        return [nettoyer(v) for v in o]
    if isinstance(o, str):
        if GUID.match(o) or HEX32.match(o):
            compteur['guid'] += 1
            return ''
        if CHEMIN.search(o) or EXTENSIONS.search(o) or any(m in o for m in MARQUEURS):
            compteur['chemin'] += 1
            return ''
    return o


def charger(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--projet-source', default='Pates flambees')
    ap.add_argument('--projets', default=str(PROJETS))
    ap.add_argument('--sortie', default=str(SORTIE))
    a = ap.parse_args()

    src = Path(a.projets) / a.projet_source
    tpl = charger(src / 'draft_content.json')
    meta = charger(src / 'draft_meta_info.json')
    store = charger(src / 'draft_virtual_store.json')
    projet_json = charger(src / 'Timelines' / 'project.json')
    racine = charger(Path(a.projets) / 'root_meta_info.json')
    entree = next(e for e in racine['all_draft_store'] if e.get('draft_name') == a.projet_source)
    tl_dir = next(p for p in (src / 'Timelines').iterdir() if p.is_dir())
    id_tl, id_dr = tpl['id'], meta['draft_id']

    # ---------------------------------------------------------- prototypes
    index = {}
    for cle, arr in tpl['materials'].items():
        if isinstance(arr, list):
            for o in arr:
                if isinstance(o, dict) and 'id' in o:
                    index[o['id']] = (cle, o)

    def proto(type_piste, plus):
        pistes = [t for t in tpl['tracks'] if t['type'] == type_piste and t['segments']]
        t = max(pistes, key=lambda x: len(x['segments'])) if plus else pistes[0]
        s = t['segments'][0]
        return {'piste': {k: v for k, v in t.items() if k != 'segments'},
                'segment': s, 'materiau': index[s['material_id']][1],
                'annexes': [[index[r][0], index[r][1]] for r in s['extra_material_refs']]}

    protos = {'video': proto('video', True), 'audio': proto('audio', False), 'texte': proto('text', False)}
    protos = nettoyer(protos)

    # ---------------------------------------------------------- squelette du draft_content
    squelette = copy.deepcopy(tpl)
    squelette['tracks'] = []
    squelette['materials'] = {k: ([] if isinstance(v, list) else v) for k, v in tpl['materials'].items()}
    squelette['duration'] = 0
    squelette = nettoyer(squelette)

    # ---------------------------------------------------------- méta, index, projet
    meta_m = copy.deepcopy(meta)
    for bloc in meta_m.get('draft_materials', []):
        bloc['value'] = []
    meta_m = nettoyer(meta_m)
    store_m = copy.deepcopy(store)
    for bloc in store_m['draft_virtual_store']:
        if bloc['type'] == 1:
            bloc['value'] = []
    store_m = nettoyer(store_m)
    projet_m = nettoyer(projet_json)
    entree_m = nettoyer(entree)

    # ---------------------------------------------------------- fichiers annexes (texte), jetons à la place des identifiants
    def lire_texte(p):
        t = p.read_bytes().decode('utf-8')
        return t.replace(id_tl, '{{ID_TIMELINE}}').replace(id_dr, '{{ID_PROJET}}')

    def assainir_fichier(nom, texte):
        if not texte.strip():
            return texte
        try:
            obj = json.loads(texte.replace('{{ID_TIMELINE}}', 'ID_TL').replace('{{ID_PROJET}}', 'ID_PR'))
        except ValueError:
            return texte
        if nom == 'draft_agency_config.json':
            obj['marterials'] = []
        obj = nettoyer(obj)
        t = json.dumps(obj, separators=(',', ':'), ensure_ascii=False)
        return t.replace('ID_TL', '{{ID_TIMELINE}}').replace('ID_PR', '{{ID_PROJET}}')

    racine_fichiers = {}
    for nom in ('attachment_pc_common.json', 'draft_agency_config.json', 'draft_biz_config.json', 'performance_opt_info.json', 'timeline_layout.json'):
        p = src / nom
        if p.exists():
            racine_fichiers[nom] = assainir_fichier(nom, lire_texte(p))
    settings = (src / 'draft_settings').read_bytes().decode('utf-8')
    settings = re.sub(r'(draft_create_time=)\d+', r'\1{{S}}', settings)
    settings = re.sub(r'(draft_last_edit_time=)\d+', r'\1{{S}}', settings)
    settings = re.sub(r'(real_edit_seconds=)\d+', r'\g<1>0', settings)
    settings = re.sub(r'(real_edit_keys=)\d+', r'\g<1>0', settings)
    racine_fichiers['draft_settings'] = settings

    tl_fichiers = {}
    ignorer = {'draft_content.json', 'template-2.tmp', 'draft_cover.jpg', 'draft.extra', 'mini_draft.json'}
    for p in tl_dir.rglob('*'):
        if p.is_dir() or p.name in ignorer or p.name.endswith('.bak'):
            continue
        rel = str(p.relative_to(tl_dir)).replace('\\', '/')
        tl_fichiers[rel] = assainir_fichier(p.name, lire_texte(p))

    modele = {
        'version_modele': 1,
        'description': "Modèle technique autonome de projet CapCut : structure seulement, aucun média, texte ni identifiant d'un ancien montage.",
        'construit_avec': {'capcut': '9.8.0.4213', 'draft_new_version': tpl.get('new_version'), 'projet_source': 'projet fait dans CapCut (non conservé dans ce fichier)'},
        'draft_content': squelette,
        'prototypes': protos,
        'meta': meta_m,
        'virtual_store': store_m,
        'project': projet_m,
        'index_entree': entree_m,
        'fichiers': {'racine': racine_fichiers, 'timeline': tl_fichiers},
    }

    # ---------------------------------------------------------- vérification finale : AUCUNE trace
    texte = json.dumps(modele, ensure_ascii=False)
    problemes = []
    for m in MARQUEURS:
        if m in texte:
            problemes.append('marqueur « %s »' % m)
    for m in CHEMIN.finditer(texte):
        problemes.append('chemin « %s… »' % texte[m.start():m.start() + 30])
    for m in GUID.finditer(texte):
        problemes.append('identifiant « %s »' % m.group(0))
    for m in HEX32.finditer(texte):
        problemes.append('identifiant hexadécimal « %s »' % m.group(0))
    for m in EXTENSIONS.finditer(texte):
        problemes.append('nom de fichier « …%s »' % m.group(0))
    if problemes:
        print('REFUS : traces du montage source dans le modèle :', file=sys.stderr)
        for p in sorted(set(problemes))[:20]:
            print('  -', p, file=sys.stderr)
        sys.exit(2)

    sortie = Path(a.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    with open(sortie, 'w', encoding='utf-8', newline='') as f:
        json.dump(modele, f, separators=(',', ':'), ensure_ascii=False)
    print('Modèle écrit : %s (%d Ko)' % (sortie, sortie.stat().st_size // 1024))
    print('Valeurs retirées : %(guid)d identifiants, %(chemin)d chemins/noms de fichiers/textes personnels' % compteur)
    print('Fichiers annexes gardés : racine %d, timeline %d' % (len(racine_fichiers), len(tl_fichiers)))


if __name__ == '__main__':
    main()
