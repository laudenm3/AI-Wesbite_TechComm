#!/usr/bin/env python3
"""Build emotions_paragraphs.json for the Streamlit app with samples that illustrate the bar chart.

The chart ranks emotions by the log2 ratio of the AI firing rate to the human rate. To show
what a bar means in practice, this script takes the top TOP_N_EMOTIONS emotions of the pooled
"machine" chart and, for each, picks the human <-> AI pairs (any genre, any model with a parallel
human text, same `base_id`) with the biggest gap in the share of sentences firing that emotion,
in the direction of the bar: AI higher for a positive loading, human higher for a negative one.

Reuses 6b's loadings, rates and thresholds unchanged and keeps 6b's original contrast pairs.
Each added paragraph also carries `emotion`, `direction` ('more'|'less'), `genre`, `model`
and `gap`. Writes into the Streamlit app's data/ folder, leaving the HTML site's
emotions_paragraphs.json alone.
"""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SENT_PATH = ROOT / 'data_processed' / 'goemotions_sentence_probs.parquet'
OUT_PATH = ROOT.parent / 'anti-slop-app-main' / 'data' / 'emotions_paragraphs.json'

TOP_N_EMOTIONS = 12       # matches the chart
PER_EMOTION = 2           # pairs per emotion
MIN_GAP = 0.10            # skip a pair unless the fired-sentence share differs by at least this
SENT_RANGE = (5, 30)      # both texts must be paragraph-sized (sentences)

_spec = importlib.util.spec_from_file_location('emo6b', HERE / '6b.emotions_paragraphs_json.py')
emo6b = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(emo6b)


def main():
    blob = emo6b.build_emotions_blob(SENT_PATH)
    emotions = list(blob['emotionMeta'])
    thr = np.array([emo6b.THRESHOLDS[e] for e in emotions])

    sp = pd.read_parquet(SENT_PATH).sort_values(['doc_id', 'sent_idx'])
    fired = pd.DataFrame(sp[[f'prob_{e}' for e in emotions]].to_numpy() >= thr, columns=emotions,
                         index=sp.index)
    meta = sp[['doc_id', 'author', 'genre', 'base_id']].copy()
    docs = pd.concat([meta, fired], axis=1).groupby(['doc_id', 'author', 'genre', 'base_id'])
    prof = docs[emotions].mean()
    prof['n'] = docs.size()
    prof = prof.reset_index()
    prof = prof[prof['n'].between(*SENT_RANGE)]

    human = prof[prof['author'] == emo6b.AUTHOR_A].set_index(['genre', 'base_id'])
    pairs = prof[prof['author'] != emo6b.AUTHOR_A].join(human, on=['genre', 'base_id'],
                                                        rsuffix='_h', how='inner')

    def sentences(doc_id):
        rows = sp[sp['doc_id'] == doc_id]
        return [{'s': r['sentence'], 'e': [e for e in emotions if r[f'prob_{e}'] >= emo6b.THRESHOLDS[e]]}
                for _, r in rows.iterrows()]

    def summary(sents):
        v = emo6b.valence
        return {'nSent': len(sents),
                'nPos': sum(any(v(e) == 'positive' for e in s['e']) for s in sents),
                'nNeg': sum(any(v(e) == 'negative' for e in s['e']) for s in sents),
                'nEmo': sum(bool(s['e']) for s in sents)}

    top = sorted(blob['emotionLoadings']['machine'].items(), key=lambda kv: -abs(kv[1]))[:TOP_N_EMOTIONS]
    used, added = set(), []
    for emo, load in top:
        sign = 1 if load > 0 else -1
        gap = (pairs[emo] - pairs[emo + '_h']) * sign
        cand = pairs.assign(gap=gap)[gap >= MIN_GAP].sort_values('gap', ascending=False)
        picked = 0
        for _, r in cand.iterrows():
            if r['doc_id'] in used or picked == PER_EMOTION:
                continue
            used.add(r['doc_id'])
            a_s, b_s = sentences(r['doc_id_h']), sentences(r['doc_id'])
            added.append({'baseId': r['base_id'], 'genre': r['genre'], 'model': r['author'],
                          'emotion': emo, 'direction': 'more' if sign > 0 else 'less',
                          'gap': float(r['gap']),
                          'examples': [{'aSentences': a_s, 'bSentences': b_s,
                                        'aSummary': summary(a_s), 'bSummary': summary(b_s)}]})
            picked += 1
        print(f'{emo:14s} {load:+.2f}  {picked} pair(s)'
              + ('' if picked else f'  (no pair with gap >= {MIN_GAP})'))

    blob['paragraphs'] = blob['paragraphs'] + added
    OUT_PATH.write_text(json.dumps(blob, indent=2))
    print(f'\nWrote {len(blob["paragraphs"])} pairs ({len(added)} chart samples) to {OUT_PATH}')


if __name__ == '__main__':
    main()
