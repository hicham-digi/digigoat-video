#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcription LOCALE horodatée (faster-whisper) d'un rush : BROUILLON à relire par un humain.
Rien n'est envoyé à un service externe : le modèle est lu sur le disque (HF_HUB_OFFLINE=1), pas de télémétrie.

Ce script doit être lancé avec le Python de l'environnement isolé (hors dépôt) :
  C:\\Users\\Hicham\\Desktop\\Digigoat\\OUTILS\\transcription\\venv\\Scripts\\python.exe scripts\\transcrire.py ^
      --entree <rush ou audio> --langue fr|en|auto --sortie <dossier>

La LANGUE est obligatoire (aucune n'est présumée) ; « auto » détecte la langue et affiche la probabilité.
Sorties dans le dossier : <nom>.json (segments + mots + confiance), <nom>.srt (brouillon, temps du fichier source),
<nom>.txt (timecodes + marqueurs), <nom>_a-relire.md (passages incertains avec timecode).

Marqueurs (seuils PROVISOIRES, à recalibrer sur de vraies voix) :
  [à vérifier]  confiance faible (avg_logprob < -1,0) ou un mot de probabilité < 0,40, ou rapport de compression > 2,4
  [incompris]   très faible confiance (avg_logprob < -1,5 ou probabilité de non-parole > 0,80) : le texte brut est conservé
                dans le .json et le .txt, mais le .srt affiche « [incompris] » : on ne propose jamais un texte reconstruit.
Une transcription sans marqueur N'EST PAS une transcription exacte : le contenu juridique doit être relu en écoutant.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault('HF_HUB_OFFLINE', '1')
os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY', '1')

MODELE_DEFAUT = Path(r'C:\Users\Hicham\Desktop\Digigoat\OUTILS\transcription\modeles\faster-whisper-large-v3')
SEUIL_VERIFIER = -1.0
SEUIL_INCOMPRIS = -1.5
SEUIL_MOT = 0.40
SEUIL_COMPRESSION = 2.4
SEUIL_NON_PAROLE = 0.80


def tc(s, virgule=True):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return '%02d:%02d:%02d%s%03d' % (h, m, sec, ',' if virgule else '.', ms)


def ajouter_dll_cuda():
    """Rend visibles les bibliothèques CUDA installées en paquets pip dans le même environnement."""
    for rac in sys.path:
        p = Path(rac) / 'nvidia'
        if p.is_dir():
            for b in p.glob('*/bin'):
                try:
                    os.add_dll_directory(str(b))
                except (OSError, AttributeError):
                    pass
                os.environ['PATH'] = str(b) + os.pathsep + os.environ.get('PATH', '')


def faire_cues(segments, max_car=70, max_duree=5.5, max_pause=0.6, min_car_fin_phrase=25):
    """Découpe les mots en sous-titres courts (temps du fichier source). Un passage incompris reste « [incompris] » ;
    un passage à faible confiance est préfixé « [à vérifier] » : aucun texte n'est reconstruit."""
    cues = []
    for sg in segments:
        if 'incompris' in sg['drapeaux']:
            cues.append((sg['debut'], sg['fin'], '[incompris]'))
            continue
        mots = sg['mots']
        if not mots:
            cues.append((sg['debut'], sg['fin'], ('[à vérifier] ' if sg['drapeaux'] else '') + sg['texte']))
            continue
        morceaux, cur = [], []
        for m in mots:
            if cur:
                texte_cur = ''.join(x['mot'] for x in cur).strip()
                trop_long = len(texte_cur) + len(m['mot'].strip()) + 1 > max_car or (m['fin'] - cur[0]['debut']) > max_duree
                pause = (m['debut'] - cur[-1]['fin']) > max_pause
                fin_phrase = texte_cur[-1:] in '.?!' and len(texte_cur) >= min_car_fin_phrase
                if trop_long or pause or fin_phrase:
                    morceaux.append(cur)
                    cur = []
            cur.append(m)
        if cur:
            morceaux.append(cur)
        for mo in morceaux:
            texte = ''.join(x['mot'] for x in mo).strip()
            douteux = any(x['proba'] < SEUIL_MOT for x in mo) or ('à vérifier' in sg['drapeaux'] and not any(x['proba'] < SEUIL_MOT for x in sg['mots']))
            cues.append((mo[0]['debut'], mo[-1]['fin'], ('[à vérifier] ' if douteux else '') + texte))
    return cues


def extraire_audio(entree, flux, sortie_wav):
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', str(entree), '-map', '0:a:%d' % flux, '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', str(sortie_wav)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('ffmpeg n\'a pas pu extraire le flux audio %d de %s : %s' % (flux, entree, r.stderr.strip()))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--entree', required=True, help='rush vidéo ou fichier audio')
    ap.add_argument('--langue', required=True, help='code de langue (fr, en, ...) ou "auto" : AUCUNE langue par défaut')
    ap.add_argument('--sortie', required=True, help='dossier de sortie')
    ap.add_argument('--modele', default=str(MODELE_DEFAUT), help='dossier du modèle faster-whisper')
    ap.add_argument('--appareil', default='auto', choices=['auto', 'cuda', 'cpu'])
    ap.add_argument('--flux-audio', type=int, default=0, help='numéro du flux audio du fichier (0 = premier)')
    ap.add_argument('--vocabulaire', default='', help='termes attendus (noms propres, termes techniques), séparés par des virgules : aide la reconnaissance')
    ap.add_argument('--garder-wav', action='store_true', help='conserver le WAV 16 kHz extrait')
    a = ap.parse_args()

    entree = Path(a.entree)
    if not entree.exists():
        raise SystemExit('Fichier introuvable : %s' % entree)
    sortie = Path(a.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    modele = Path(a.modele)
    if not (modele / 'model.bin').exists():
        raise SystemExit('Modèle introuvable (model.bin) dans %s' % modele)

    ajouter_dll_cuda()
    from faster_whisper import WhisperModel

    t0 = time.time()
    wav = sortie / (entree.stem + '_16k.wav')
    extraire_audio(entree, a.flux_audio, wav)
    t_extraction = time.time() - t0

    appareil, calcul = None, None
    t1 = time.time()
    modele_obj = None
    essais = [('cuda', 'float16'), ('cpu', 'int8')] if a.appareil == 'auto' else ([('cuda', 'float16')] if a.appareil == 'cuda' else [('cpu', 'int8')])
    erreurs = []
    for dev, ct in essais:
        try:
            modele_obj = WhisperModel(str(modele), device=dev, compute_type=ct)
            if dev == 'cuda':
                # le chargement CUDA peut réussir sans que l'inférence fonctionne (DLL manquantes) : test immédiat
                import numpy as np
                list(modele_obj.transcribe(np.zeros(16000, dtype='float32'), language='en')[0])
            appareil, calcul = dev, ct
            break
        except Exception as e:  # noqa: BLE001
            erreurs.append('%s/%s : %s' % (dev, ct, str(e)[:160]))
            modele_obj = None
    if modele_obj is None:
        raise SystemExit('Aucun appareil utilisable : ' + ' | '.join(erreurs))
    t_chargement = time.time() - t1

    langue = None if a.langue.lower() == 'auto' else a.langue.lower()
    # le WAV 16 kHz mono est lu ici (bibliothèque standard + numpy) : la lecture audio intégrée de faster-whisper
    # (PyAV) est incompatible avec la version de PyAV installée (constaté le 2026-11-24)
    import wave
    import numpy as np
    with wave.open(str(wav), 'rb') as w:
        audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    t2 = time.time()
    segments_gen, info = modele_obj.transcribe(
        audio, language=langue, beam_size=5, word_timestamps=True, vad_filter=True,
        vad_parameters={'min_silence_duration_ms': 500}, condition_on_previous_text=False,
        temperature=[0.0, 0.2, 0.4], initial_prompt=(a.vocabulaire.replace(',', ', ') if a.vocabulaire else None))
    segments = []
    for sg in segments_gen:
        mots = [{'debut': round(w.start, 3), 'fin': round(w.end, 3), 'mot': w.word, 'proba': round(w.probability, 3)} for w in (sg.words or [])]
        drapeaux = []
        if sg.avg_logprob < SEUIL_INCOMPRIS or sg.no_speech_prob > SEUIL_NON_PAROLE:
            drapeaux.append('incompris')
        elif sg.avg_logprob < SEUIL_VERIFIER or sg.compression_ratio > SEUIL_COMPRESSION or any(m['proba'] < SEUIL_MOT for m in mots):
            drapeaux.append('à vérifier')
        faibles = [m for m in mots if m['proba'] < SEUIL_MOT]
        segments.append({'debut': round(sg.start, 3), 'fin': round(sg.end, 3), 'texte': sg.text.strip(), 'avg_logprob': round(sg.avg_logprob, 3),
                         'no_speech_prob': round(sg.no_speech_prob, 3), 'compression_ratio': round(sg.compression_ratio, 3),
                         'drapeaux': drapeaux, 'mots_faibles': [{'mot': m['mot'].strip(), 'debut': m['debut'], 'proba': m['proba']} for m in faibles], 'mots': mots})
    t_transcription = time.time() - t2

    duree_audio = float(info.duration)
    meta = {'fichier': entree.name, 'flux_audio': a.flux_audio, 'langue_demandee': a.langue, 'langue_detectee': info.language,
            'proba_langue': round(info.language_probability, 3), 'duree_audio_s': round(duree_audio, 3), 'modele': modele.name,
            'appareil': appareil, 'calcul': calcul, 'statut': 'BROUILLON AUTOMATIQUE : non relu',
            'seuils': {'verifier_avg_logprob': SEUIL_VERIFIER, 'incompris_avg_logprob': SEUIL_INCOMPRIS, 'mot_proba': SEUIL_MOT,
                       'compression': SEUIL_COMPRESSION, 'non_parole': SEUIL_NON_PAROLE},
            'temps_s': {'extraction_audio': round(t_extraction, 1), 'chargement_modele': round(t_chargement, 1),
                        'transcription': round(t_transcription, 1), 'total': round(time.time() - t0, 1)},
            'vitesse_x_temps_reel': round(duree_audio / t_transcription, 2) if t_transcription > 0 else None}
    base = sortie / entree.stem
    with open(str(base) + '.json', 'w', encoding='utf-8') as f:
        json.dump({'meta': meta, 'segments': segments}, f, ensure_ascii=False, indent=1)

    cues = faire_cues(segments)
    with open(str(base) + '.srt', 'w', encoding='utf-8', newline='\n') as f:
        for k, (d, fi, texte) in enumerate(cues, 1):
            f.write('%d\n%s --> %s\n%s\n\n' % (k, tc(d), tc(fi), texte))

    with open(str(base) + '.txt', 'w', encoding='utf-8', newline='\n') as f:
        f.write('# BROUILLON AUTOMATIQUE : non relu. Fichier : %s. Langue : %s (détectée %s, %.2f). Modèle : %s (%s).\n' % (
            entree.name, a.langue, info.language, info.language_probability, modele.name, appareil))
        for sg in segments:
            marque = (' {' + ', '.join(sg['drapeaux']) + '}') if sg['drapeaux'] else ''
            f.write('[%s -> %s] %s%s\n' % (tc(sg['debut'], False), tc(sg['fin'], False), sg['texte'], marque))

    a_relire = [sg for sg in segments if sg['drapeaux']]
    with open(str(base) + '_a-relire.md', 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Passages incertains : %s\n\nBrouillon automatique. Seuils provisoires. Une absence de marqueur ne garantit pas l\'exactitude.\n\n' % entree.name)
        if not a_relire:
            f.write('Aucun passage marqué par les seuils. **La relecture reste obligatoire.**\n')
        else:
            f.write('| Timecode | Marqueur | Texte brut du brouillon | Mots à faible probabilité |\n| --- | --- | --- | --- |\n')
            for sg in a_relire:
                faibles = ', '.join('%s (%s, p=%.2f)' % (m['mot'], tc(m['debut'], False), m['proba']) for m in sg['mots_faibles']) or '—'
                f.write('| %s → %s | %s | %s | %s |\n' % (tc(sg['debut'], False), tc(sg['fin'], False), ', '.join(sg['drapeaux']), sg['texte'].replace('|', '/'), faibles))

    if not a.garder_wav:
        try:
            wav.unlink()
        except OSError:
            pass
    print('Transcription : %d segment(s), %d marqué(s) ; langue %s (%.2f) ; audio %.1f s' % (len(segments), len(a_relire), info.language, info.language_probability, duree_audio))
    print('Appareil : %s/%s ; temps : extraction %.1f s, chargement %.1f s, transcription %.1f s (x%.2f temps réel)' % (
        appareil, calcul, t_extraction, t_chargement, t_transcription, meta['vitesse_x_temps_reel'] or 0))
    print('Sorties : %s.{json,srt,txt} et %s_a-relire.md' % (base, base))


if __name__ == '__main__':
    main()
