#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estime le décalage entre l'audio de la caméra (dans le rush) et un audio enregistré à part (micro externe).
Résultat : décalage D en secondes tel que  temps_dans_audio_séparé = temps_dans_rush + D.
C'est la valeur à donner à capcut_projet.py : --audios-separes "RUSH=audio.wav@D".

Méthode : corrélation croisée (FFT) des deux signaux ramenés à 8 kHz mono sur une fenêtre de recherche de ± --fenetre s.
C'est une mesure du SIGNAL, pas une écoute : à confirmer visuellement dans CapCut (les formes d'onde doivent coïncider).
Une confiance faible (< 5) ou un décalage qui change au fil du rush (dérive d'horloge) doit être signalé, pas ignoré.

À lancer avec le Python de l'environnement isolé (numpy y est installé) :
  C:\\Users\\Hicham\\Desktop\\Digigoat\\OUTILS\\transcription\\venv\\Scripts\\python.exe scripts\\caler_audio.py --rush R.mp4 --audio A.wav
"""
import argparse
import subprocess
import sys

import numpy as np

SR = 8000


def lire(fichier, debut, duree, flux=0):
    cmd = ['ffmpeg', '-v', 'error', '-ss', '%.3f' % debut, '-t', '%.3f' % duree, '-i', str(fichier), '-map', '0:a:%d' % flux,
           '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0 or not r.stdout:
        raise SystemExit('Lecture audio impossible : %s %s' % (fichier, r.stderr.decode('utf-8', 'replace')[:200]))
    x = np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)
    return x - x.mean()


def correler(x, y):
    n = 1
    while n < len(x) + len(y):
        n *= 2
    X = np.fft.rfft(x, n)
    Y = np.fft.rfft(y, n)
    c = np.fft.irfft(np.conj(X) * Y, n)
    return np.concatenate([c[-(len(x) - 1):], c[:len(y)]]), -(len(x) - 1)   # c[k] pour lag = k + décalage_indice


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--rush', required=True)
    ap.add_argument('--audio', required=True, help='audio enregistré à part')
    ap.add_argument('--analyse', type=float, default=120.0, help='durée analysée depuis le début de chaque fichier (s)')
    ap.add_argument('--fenetre', type=float, default=30.0, help='décalage maximal recherché, de part et d\'autre (s)')
    ap.add_argument('--flux-audio', type=int, default=0, help='flux audio du rush')
    a = ap.parse_args()

    x = lire(a.rush, 0, a.analyse, a.flux_audio)
    y = lire(a.audio, 0, a.analyse + a.fenetre)
    if np.std(x) < 1e-6 or np.std(y) < 1e-6:
        raise SystemExit('Un des deux signaux est silencieux : calage impossible.')
    c, base = correler(x / np.std(x), y / np.std(y))
    lags = (np.arange(len(c)) + base) / SR
    masque = np.abs(lags) <= a.fenetre
    cm, lm = np.abs(c[masque]), lags[masque]
    k = int(np.argmax(cm))
    pic, lag = cm[k], lm[k]
    # second pic hors de ±50 ms autour du premier : confiance = rapport des deux
    exclu = np.abs(lm - lag) > 0.05
    second = cm[exclu].max() if exclu.any() else 1e-9
    confiance = pic / second
    signe = c[masque][k] >= 0
    print('Décalage estimé D = %+.3f s  (temps dans l\'audio séparé = temps dans le rush + D)' % lag)
    print('Confiance (pic / second pic) : %.1f  %s' % (confiance, '(bonne)' if confiance >= 5 else '(FAIBLE : vérifier à la main)'))
    if not signe:
        print('Attention : corrélation négative (polarité inversée ?).')
    print('Valeur pour le générateur : --audios-separes "%s=%s@%.3f"' % (a.rush.split('\\')[-1].rsplit('.', 1)[0], a.audio, lag))


if __name__ == '__main__':
    main()
