#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Propose des coupes SOBRES à partir d'une transcription horodatée (sortie de transcrire.py) : retirer les silences excessifs,
les faux départs et les répétitions évidentes, en gardant un rythme naturel et le sens complet.  Python 3 standard seulement.

Principes (documentés dans clients/dimitri/montage-long.md) :
  * seuls les SILENCES excessifs sont retirés automatiquement ; tout retrait de TEXTE est une proposition « à valider »,
    sauf une répétition évidente (au moins 2 mots répétés tels quels) qui ne contient ni réserve connue ni chiffre ;
  * un passage [incompris] n'est jamais retiré ni reconstruit : il reste dans le plan et est signalé ;
  * tout retrait qui touche une réserve, une condition ou un chiffre est classé risque « élevé » et à valider ;
  * si la langue n'a pas de liste de réserves connue (--reserves absent), TOUS les retraits de texte sont à valider ;
  * les listes de mots (réserves, formules de redémarrage, parasites) sont PROVISOIRES et non exhaustives ;
  * les temps des mots viennent d'un modèle automatique (imprécision possible de quelques dixièmes de seconde) :
    le calage des coupes est à vérifier à l'écoute.

Sorties (dossier --sortie) : coupes.csv, coupes.md, plan_<rush>.csv (pour capcut_projet.py --rushes), sous-titres_apres-coupes.srt
(temps du rush source, découpé par segment gardé), texte_apres_coupes.txt, resume.json.
Décisions : --decisions "C03=appliquee;C05=refusee" met à jour le statut d'une proposition puis régénère le plan.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

RESERVES = {
    'en': ['unless', 'except', 'only if', 'provided that', 'however', 'depends', 'depending', 'in principle', 'generally', 'usually',
           'in some cases', 'not legal advice', 'but', 'if', 'only', 'subject to', 'may', 'might'],
    'fr': ['sauf', 'à moins', 'sous réserve', 'cela dépend', 'dépend', 'en principe', 'généralement', 'dans certains cas', 'toutefois',
           'cependant', 'mais', 'si', 'uniquement', 'seulement', 'peut', 'pourrait', 'pas un avis', 'pas de conseil'],
}
REDEMARRAGE = {
    'en': ['let me start again', 'let me start over', 'let me rephrase', 'start again'],
    'fr': ['je recommence', 'je reprends', 'laissez-moi recommencer', 'je reformule', 'on recommence'],
}
PARASITES = {'en': ['um', 'uh', 'er', 'erm'], 'fr': ['euh', 'hum', 'heu']}


def norm(m):
    return re.sub(r"^[^\w]+|[^\w]+$", '', m.strip().lower())


def tc(s):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return '%02d:%02d:%02d,%03d' % (h, m, sec, ms)


def tc_pt(s):
    return tc(s).replace(',', '.')


def texte_mots(ms):
    return re.sub(r'\s+', ' ', ''.join(m['mot'] for m in ms)).strip()


def contient(liste, mots_norm_texte):
    """vrai si une des expressions (mots entiers) figure dans le texte normalisé."""
    t = ' ' + mots_norm_texte + ' '
    return [e for e in liste if (' ' + e + ' ') in t]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--transcription', required=True, help='fichier .json produit par transcrire.py')
    ap.add_argument('--rush', required=True, help='nom du fichier rush (avec extension) tel qu\'utilisé par capcut_projet.py --rushes')
    ap.add_argument('--sortie', required=True)
    ap.add_argument('--langue', default='', help='code de langue des listes de mots (en, fr) ; vide = listes inconnues, tout retrait de texte est à valider')
    ap.add_argument('--pause-max', type=float, default=0.9, help='pause (s) au-delà de laquelle on coupe')
    ap.add_argument('--marge-debut', type=float, default=0.12, help='souffle conservé avant le premier mot d\'un segment (s)')
    ap.add_argument('--marge-fin', type=float, default=0.30, help='souffle conservé après le dernier mot d\'un segment (s)')
    ap.add_argument('--parasites', default='', help='mots-parasites à PROPOSER (ex. "um,uh") : toujours à valider')
    ap.add_argument('--reserves', default='', help='remplace la liste de réserves, séparées par des virgules')
    ap.add_argument('--decisions', default='', help='"C03=appliquee;C05=refusee"')
    a = ap.parse_args()

    j = json.load(open(a.transcription, encoding='utf-8'))
    segs = j['segments']
    duree_src = j['meta']['duree_audio_s']
    lg = a.langue.lower()
    reserves = [x.strip().lower() for x in a.reserves.split(',') if x.strip()] if a.reserves else RESERVES.get(lg, [])
    redem = REDEMARRAGE.get(lg, [])
    parasites = [x.strip().lower() for x in a.parasites.split(',') if x.strip()] if a.parasites else []
    liste_connue = bool(reserves)

    # ---- jeton = mot (ou passage incompris protégé)
    mots, douteux = [], []
    for i, sg in enumerate(segs):
        if 'incompris' in sg['drapeaux']:
            mots.append({'mot': ' [incompris]', 'debut': sg['debut'], 'fin': sg['fin'], 'proba': 0.0, 'n': '[incompris]', 'seg': i,
                         'protege': True, 'seg_drap': sg['drapeaux']})
            continue
        if sg['drapeaux'] and len(sg['mots']) <= 2 and (sg['fin'] - sg['debut']) < 1.0:
            douteux.append(sg)
            continue
        for w in sg['mots']:
            mots.append(dict(w, n=norm(w['mot']), seg=i, protege=False, seg_drap=sg['drapeaux']))
    mots.sort(key=lambda m: (m['debut'], m['fin']))
    if not mots:
        raise SystemExit('Aucun mot exploitable dans la transcription.')

    cand = []          # propositions
    retires = {}       # index de mot -> id de proposition appliquée

    def nouvelle(type_, deb, fin, texte, justif, risque, statut, idx_mots=None, note=''):
        cid = 'C%02d' % (len(cand) + 1)
        cand.append({'id': cid, 'type': type_, 'debut': round(deb, 3), 'fin': round(fin, 3), 'duree': round(fin - deb, 3), 'texte': texte,
                     'justification': justif, 'risque': risque, 'statut': statut, 'idx': idx_mots or [], 'note': note})
        return cid

    def risque_texte(idxs):
        ms = [mots[k] for k in idxs]
        t = ' '.join(m['n'] for m in ms)
        trouve = contient(reserves, t)
        chiffres = re.search(r'\d', t)
        faibles = [m for m in ms if m['proba'] < 0.40]
        if trouve or chiffres or any(m['protege'] for m in ms):
            return 'élevé', 'contient %s' % (('la réserve « %s »' % trouve[0]) if trouve else ('un chiffre' if chiffres else 'un passage incompris'))
        if faibles:
            return 'moyen', 'mots à faible probabilité'
        return 'faible', ''

    pris = set()

    # ---- répétitions immédiates (n-grammes identiques), du plus long au plus court
    i = 0
    while i < len(mots):
        fait = False
        for n in (4, 3, 2, 1):
            if i + 2 * n <= len(mots):
                s1 = [mots[k]['n'] for k in range(i, i + n)]
                s2 = [mots[k]['n'] for k in range(i + n, i + 2 * n)]
                if s1 == s2 and all(s1) and not any(mots[k]['protege'] for k in range(i, i + 2 * n)) and not any(k in pris for k in range(i, i + n)):
                    idxs = list(range(i, i + n))
                    risque, raison = risque_texte(idxs)
                    if parasites and all(x in parasites for x in s1):
                        break
                    auto = (n >= 2 and liste_connue and risque == 'faible')
                    nouvelle('répétition', mots[i]['debut'], mots[i + n]['debut'], texte_mots([mots[k] for k in idxs]),
                             'répétition immédiate de %d mot(s) ; la deuxième occurrence est conservée' % n,
                             risque, 'appliquée' if auto else 'à valider', idxs,
                             ('1 mot répété : peut être une insistance' if n == 1 else '') + (' ; ' + raison if raison else '') +
                             ('' if liste_connue else ' ; liste de réserves inconnue : retrait à valider'))
                    pris.update(idxs)
                    i += n
                    fait = True
                    break
        if not fait:
            i += 1

    # ---- mots-parasites proposés (jamais appliqués d'office)
    for k, m in enumerate(mots):
        if parasites and m['n'] in parasites and k not in pris and not m['protege']:
            nouvelle('parasite', m['debut'], m['fin'], m['mot'].strip(), 'mot-parasite proposé (peut porter une hésitation utile)', 'faible', 'à valider', [k])
            pris.add(k)

    # ---- passages : séparés par une pause longue ou une ponctuation de fin de phrase
    chunks, cur = [], []
    for k, m in enumerate(mots):
        if cur:
            pause = m['debut'] - mots[cur[-1]]['fin'] >= a.pause_max
            fin_phrase = mots[cur[-1]]['mot'].strip()[-1:] in '.?!'
            if pause or fin_phrase:
                chunks.append(cur)
                cur = []
        cur.append(k)
    if cur:
        chunks.append(cur)

    # ---- formules de redémarrage explicites
    for ci_r, ch in enumerate(chunks):
        t = ' '.join(mots[k]['n'] for k in ch)
        for f in redem:
            if (' ' + f + ' ') in (' ' + t + ' '):
                idxs = [k for k in ch if k not in pris]
                if idxs and len(ch) <= len(f.split()) + 2:
                    nouvelle('faux départ (formule)', mots[idxs[0]]['debut'], mots[idxs[-1]]['fin'], texte_mots([mots[k] for k in idxs]),
                             'formule de redémarrage explicite', 'moyen', 'à valider', idxs,
                             "seule la formule est proposée ; le passage qui la précède n'est PAS retiré d'office (à décider avec l'écoute)")
                    pris.update(idxs)
                    prec = [k for k in chunks[ci_r - 1] if k not in pris] if ci_r > 0 else []
                    if prec and not any(mots[k]['protege'] for k in prec):
                        risque_p, raison_p = risque_texte(prec)
                        nouvelle('passage possiblement remplacé', mots[prec[0]]['debut'], mots[prec[-1]]['fin'], texte_mots([mots[k] for k in prec]),
                                 'passage placé juste avant une formule de redémarrage : il a peut-être été refait juste après',
                                 'élevé' if risque_p == 'élevé' else 'moyen', 'à valider', prec,
                                 "ne retirer qu'après écoute : ce qui est dit après peut être différent ou plus court" + ((' ; ' + raison_p) if raison_p else ''))
                        pris.update(prec)

    # ---- faux départ probable : un court passage dont les mots se retrouvent au début du passage suivant
    def sans_parasite(ch):
        return [k for k in ch if mots[k]['n'] and mots[k]['n'] not in (PARASITES.get(lg, []) + parasites)]
    for ci in range(len(chunks) - 1):
        A = sans_parasite(chunks[ci])
        B = sans_parasite(chunks[ci + 1])
        if not A or not B or len(A) > 8 or len(B) <= len(A) or any(k in pris for k in A) or any(mots[k]['protege'] for k in A):
            continue
        tete = [mots[k]['n'] for k in B[:len(A) + 4]]
        it = iter(tete)
        if all(mots[k]['n'] in it for k in A):
            idxs = chunks[ci]
            risque, raison = risque_texte(idxs)
            nouvelle('faux départ probable', mots[idxs[0]]['debut'], mots[idxs[-1]]['fin'], texte_mots([mots[k] for k in idxs]),
                     'passage repris presque tel quel au début du passage suivant', 'élevé' if risque == 'élevé' else 'moyen', 'à valider', idxs,
                     'à confirmer à l\'écoute' + ((' ; ' + raison) if raison else ''))
            pris.update(idxs)

    # ---- bruit probable (segment très court de faible confiance)
    for sg in douteux:
        nouvelle('bruit probable', sg['debut'], sg['fin'], sg['texte'], 'segment très court de faible confiance (probable fausse détection)', 'moyen', 'à valider', [],
                 'texte brut du brouillon conservé ici ; absent du plan tant que non validé')

    # ---- silences excessifs entre mots voisins
    for k in range(len(mots) - 1):
        m1, m2 = mots[k], mots[k + 1]
        gap = m2['debut'] - m1['fin']
        if gap > a.pause_max:
            gardee = a.marge_fin + a.marge_debut
            dans = [sg for sg in douteux if sg['debut'] < m2['debut'] and sg['fin'] > m1['fin']]
            statut = 'à valider' if dans else 'appliquée'
            note = ("contient un segment douteux (« %s ») : à valider avec la proposition correspondante" % dans[0]['texte']) if dans else ''
            nouvelle('silence', m1['fin'] + a.marge_fin, m2['debut'] - a.marge_debut, '',
                     'pause de %.2f s, réduite à %.2f s' % (gap, gardee), 'faible', statut, [], note)
            cand[-1]['paire'] = k

    # ---- décisions
    if a.decisions:
        for paire in a.decisions.split(';'):
            if not paire.strip():
                continue
            cid, _, st = paire.partition('=')
            cible = next((c for c in cand if c['id'] == cid.strip()), None)
            if cible is None:
                raise SystemExit('Proposition inconnue : %s' % cid)
            st = st.strip().lower()
            if st not in ('appliquee', 'appliquée', 'refusee', 'refusée'):
                raise SystemExit('Statut illisible pour %s : %s (appliquee ou refusee)' % (cid, st))
            cible['statut'] = 'appliquée' if st.startswith('appliqu') else 'refusée'
            cible['note'] = (cible['note'] + ' ; ' if cible['note'] else '') + 'décision utilisateur'

    for c in cand:
        if c['statut'] == 'appliquée':
            for k in c['idx']:
                retires[k] = c['id']
    silences_appliques = {c['paire'] for c in cand if c['type'] == 'silence' and c['statut'] == 'appliquée'}

    # ---- segments gardés : mots non retirés, scindés à chaque retrait ou silence appliqué
    gardes = [k for k in range(len(mots)) if k not in retires]
    runs, cur = [], []
    for k in gardes:
        if cur:
            prec = cur[-1]
            entre_retire = any(x in retires for x in range(prec + 1, k))
            coupe_silence = any(x in silences_appliques for x in range(prec, k))
            if entre_retire or coupe_silence:
                runs.append(cur)
                cur = []
        cur.append(k)
    if cur:
        runs.append(cur)

    plan = []
    for r in runs:
        premier, dernier = mots[r[0]], mots[r[-1]]
        deb = premier['debut'] - a.marge_debut
        fin = dernier['fin'] + a.marge_fin
        if r[0] > 0:
            deb = max(deb, mots[r[0] - 1]['fin'] + 0.03)
        if r[-1] < len(mots) - 1:
            fin = min(fin, mots[r[-1] + 1]['debut'] - 0.03)
        deb = max(0.0, deb)
        fin = min(duree_src, fin)
        if fin - deb < 0.2:
            continue
        plan.append({'debut': round(deb, 3), 'duree': round(fin - deb, 3), 'mots': r})
    for k in range(len(plan) - 1):       # jamais de chevauchement
        fin_k = plan[k]['debut'] + plan[k]['duree']
        if fin_k > plan[k + 1]['debut']:
            plan[k]['duree'] = round(plan[k + 1]['debut'] - plan[k]['debut'], 3)

    sortie = Path(a.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    stem = Path(a.rush).stem
    with open(sortie / ('plan_%s.csv' % stem), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['ordre', 'rush', 'debut', 'duree', 'nom', 'note'])
        for n, p in enumerate(plan, 1):
            extrait = texte_mots([mots[k] for k in p['mots'][:8]])
            w.writerow([n, a.rush, ('%.3f' % p['debut']).replace('.', ','), ('%.3f' % p['duree']).replace('.', ','), 'P%02d' % n, extrait[:70]])
    with open(sortie / 'coupes.csv', 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['id', 'type', 'debut_source', 'fin_source', 'duree_retiree', 'texte_retire', 'justification', 'risque_sens', 'statut', 'note'])
        for c in cand:
            w.writerow([c['id'], c['type'], tc_pt(c['debut']), tc_pt(c['fin']), ('%.2f' % c['duree']).replace('.', ','), c['texte'], c['justification'], c['risque'], c['statut'], c['note']])

    # ---- sous-titres APRÈS coupes (temps du rush source, découpés dans chaque segment gardé)
    def cues_run(r):
        out, cur2 = [], []

        def vider():
            if cur2:
                texte = re.sub(r'\s+', ' ', ''.join(mots[k]['mot'] for k in cur2)).strip()
                douteux_c = any(mots[k]['proba'] < 0.40 or ('à vérifier' in mots[k]['seg_drap']) for k in cur2 if not mots[k]['protege'])
                out.append((mots[cur2[0]]['debut'], mots[cur2[-1]]['fin'], ('[à vérifier] ' if douteux_c else '') + texte))
        for k in r:
            m = mots[k]
            if m['protege']:
                vider()
                cur2.clear()
                out.append((m['debut'], m['fin'], '[incompris]'))
                continue
            if cur2:
                texte_cur = ''.join(mots[x]['mot'] for x in cur2).strip()
                if len(texte_cur) + len(m['mot'].strip()) + 1 > 70 or (m['fin'] - mots[cur2[0]]['debut']) > 5.5 or (m['debut'] - mots[cur2[-1]]['fin']) > 0.6 \
                        or (texte_cur[-1:] in '.?!' and len(texte_cur) >= 25):
                    vider()
                    cur2.clear()
            cur2.append(k)
        vider()
        fusion = []                      # pas de sous-titre orphelin de 1 ou 2 mots : rattaché au précédent
        for c in out:
            if fusion and len(c[2].split()) <= 2 and not c[2].startswith('[') and not fusion[-1][2].startswith('[incompris') and c[0] - fusion[-1][1] <= 0.6:
                fusion[-1] = (fusion[-1][0], c[1], fusion[-1][2] + ' ' + c[2])
            else:
                fusion.append(c)
        return fusion
    with open(sortie / 'sous-titres_apres-coupes.srt', 'w', encoding='utf-8', newline='\n') as f:
        n = 0
        for p in plan:
            for d, fi, tx in cues_run(p['mots']):
                n += 1
                f.write('%d\n%s --> %s\n%s\n\n' % (n, tc(d), tc(fi), tx))
    with open(sortie / 'texte_apres_coupes.txt', 'w', encoding='utf-8', newline='\n') as f:
        f.write('# BROUILLON : texte conservé après les coupes appliquées (temps du rush source). Non relu.\n')
        for n, p in enumerate(plan, 1):
            f.write('P%02d [%s -> %s] %s\n' % (n, tc_pt(p['debut']), tc_pt(p['debut'] + p['duree']), texte_mots([mots[k] for k in p['mots']])))

    duree_finale = sum(p['duree'] for p in plan)
    par_type = {}
    for c in cand:
        par_type.setdefault(c['type'], {}).setdefault(c['statut'], 0)
        par_type[c['type']][c['statut']] += 1
    resume = {'rush': a.rush, 'duree_source_s': duree_src, 'duree_apres_coupes_s': round(duree_finale, 3), 'segments_gardes': len(plan),
              'propositions': par_type, 'langue_listes': lg or '(aucune)', 'liste_reserves_connue': liste_connue,
              'reglages': {'pause_max': a.pause_max, 'marge_debut': a.marge_debut, 'marge_fin': a.marge_fin}}
    (sortie / 'resume.json').write_text(json.dumps(resume, ensure_ascii=False, indent=1), encoding='utf-8')

    with open(sortie / 'coupes.md', 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Coupes proposées : %s\n\nSource : %.1f s ; après coupes appliquées : %.1f s en %d segment(s). Brouillon : le calage se vérifie à l\'écoute.\n\n' % (
            a.rush, duree_src, duree_finale, len(plan)))
        f.write('| Id | Type | Début → fin (source) | Texte retiré | Justification | Risque sur le sens | Statut |\n| --- | --- | --- | --- | --- | --- | --- |\n')
        for c in cand:
            note = (' (' + c['note'] + ')') if c['note'] else ''
            f.write('| %s | %s | %s → %s | %s | %s%s | %s | **%s** |\n' % (c['id'], c['type'], tc_pt(c['debut']), tc_pt(c['fin']), c['texte'].replace('|', '/') or '(silence)',
                                                                       c['justification'], note.replace('|', '/'), c['risque'], c['statut']))
    print('Propositions : %d ; appliquées : %d ; à valider : %d ; refusées : %d' % (len(cand), sum(c['statut'] == 'appliquée' for c in cand),
                                                                                   sum(c['statut'] == 'à valider' for c in cand), sum(c['statut'] == 'refusée' for c in cand)))
    print('Durée source %.1f s -> après coupes %.1f s (%d segments gardés)' % (duree_src, duree_finale, len(plan)))
    print('Sorties : %s' % sortie)


if __name__ == '__main__':
    main()
