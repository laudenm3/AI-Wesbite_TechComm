#!/usr/bin/env python3
"""Build emotions_abstracts.json — the abstract-pair data for the Emotional Tone tab.

Same job as 6b, different corpus. 6b compares human vs LLM across the six HAP-E genres, where
the "parallel" texts share a prompt but not their content. This file works over
`master_parallel_abs.parquet` (scored by 4d): human and AI abstracts of the SAME paper, keyed by
doi — a strictly one-to-one comparison, which is what makes the emotional-tone contrast clean.

Emits the same schema as emotions_paragraphs.json so the website renders it with the same code:

  · emotionLoadings[group][emotion] = log2(AI firing rate / human firing rate) over every
    sentence of every abstract. A sentence fires emotion e iff prob_e >= THRESHOLDS[e]
    (per-label cuts imported from 6b — single source of truth). Add-0.5 smoothed. One group per
    AI author in the parquet, plus a pooled "machine" group when there is more than one.
  · paragraphs[] = the N human/AI abstract pairs whose per-emotion firing profiles diverge most
    (L1 distance over fired-fraction vectors), every sentence tagged with the emotions it fired.

Reads  data_processed/goemotions_abstract_sentence_probs.parquet   (produced by 4d)
Writes emotions_abstracts.json                                     (inlined by inject_json.py)

Usage:  python GoEmotions-Analysis/6c.emotions_abstracts_json.py
Authored by Claude.
"""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SENT_PATH = REPO / 'data_processed' / 'goemotions_abstract_sentence_probs.parquet'
OUT_PATH  = REPO / 'emotions_abstracts.json'

# ── Config ────────────────────────────────────────────────────────────────────
AUTHOR_A = 'human'            # baseline; the other authors in the parquet are the LLMs
AUTHOR_B = None               # AI author shown in the example pairs; None = first non-human found
N_PAIRS  = 3                  # how many contrasting abstract pairs to emit
SMOOTH   = 0.5                # Laplace add-k on firing COUNTS before the log2 ratio (as in 6b)

# Reuse 6b's per-label thresholds, valence map and dropped labels rather than restating them —
# the module name starts with a digit, so it can't be a plain import.
_spec = importlib.util.spec_from_file_location('emo6b', HERE / '6b.emotions_paragraphs_json.py')
_6b = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_6b)
THRESHOLDS, DROP_EMOTIONS, valence = _6b.THRESHOLDS, _6b.DROP_EMOTIONS, _6b.valence


def build_abstracts_blob(sent_path=SENT_PATH, author_b=AUTHOR_B, n_pairs=N_PAIRS):
    sent_path = Path(sent_path)
    if not sent_path.exists():
        raise SystemExit(f'{sent_path} not found — run 4d.score_abstracts_goemotions.py first.')
    sp = pd.read_parquet(sent_path)
    need = {'doc_id', 'author', 'base_id', 'source_tag', 'sent_idx', 'sentence'}
    missing = need - set(sp.columns)
    if missing:
        raise SystemExit(f'{sent_path.name} missing column(s) {sorted(missing)} — rerun 4d.')

    EMOTIONS = [c[5:] for c in sp.columns if c.startswith('prob_') and c[5:] not in DROP_EMOTIONS]
    thr   = np.array([THRESHOLDS[e] for e in EMOTIONS])
    fired = sp[[f'prob_{e}' for e in EMOTIONS]].to_numpy() >= thr        # (n_sent, n_emo) bool
    fd = pd.DataFrame(fired, columns=EMOTIONS)
    fd['author']  = sp['author'].values
    fd['base_id'] = sp['base_id'].values

    ai_authors = [a for a in sp['author'].unique() if a != AUTHOR_A]
    if not ai_authors:
        raise SystemExit(f'no non-{AUTHOR_A} author in {sent_path.name}')
    author_b = author_b or ai_authors[0]
    if author_b not in ai_authors:
        raise SystemExit(f'AUTHOR_B={author_b!r} not in the parquet (have {ai_authors})')

    # ── 1. Emotion loadings: each AI author vs human, over every abstract sentence ────
    def counts(authors):
        sub = fd[fd['author'].isin(authors)]
        return sub[EMOTIONS].sum(), len(sub)

    h_counts, h_n = counts([AUTHOR_A])
    h_rate = h_counts / max(h_n, 1)

    groups = {a: [a] for a in ai_authors}
    if len(ai_authors) > 1:
        groups = {'machine': ai_authors, **groups}     # pooled group only when it means something

    emotion_loadings = {}
    emotion_rates = {AUTHOR_A: {'n': int(h_n), 'rates': {e: float(h_rate[e]) for e in EMOTIONS}}}
    for gname, authors in groups.items():
        g_counts, g_n = counts(authors)
        gr = (g_counts + SMOOTH) / (g_n + 2 * SMOOTH)
        hr = (h_counts + SMOOTH) / (h_n + 2 * SMOOTH)
        load = np.log2(gr / hr)
        emotion_loadings[gname] = {e: float(load[e]) for e in EMOTIONS}
        emotion_rates[gname] = {'n': int(g_n),
                                'rates': {e: float(g_counts[e] / max(g_n, 1)) for e in EMOTIONS}}

    # ── 2. The most emotionally divergent human/AI abstract pairs (same doi) ─────────
    def profile(author):
        return fd[fd['author'] == author].groupby('base_id')[EMOTIONS].mean()

    pa, pb = profile(AUTHOR_A), profile(author_b)
    shared = sorted(set(pa.index) & set(pb.index))
    if not shared:
        raise SystemExit(f'no base_id shared by {AUTHOR_A} and {author_b}')
    contrast = (pd.DataFrame({'base_id': shared,
                              'l1': [float(np.abs(pa.loc[b] - pb.loc[b]).sum()) for b in shared]})
                  .sort_values('l1', ascending=False).reset_index(drop=True))

    doi_of = sp.drop_duplicates('base_id').set_index('base_id')['source_tag'].to_dict()

    def sentences(author, base_id):
        rows = sp[(sp['author'] == author) & (sp['base_id'] == base_id)].sort_values('sent_idx')
        return [{'s': r['sentence'],
                 'e': [e for e in EMOTIONS if r[f'prob_{e}'] >= THRESHOLDS[e]]}
                for _, r in rows.iterrows()]

    def emo_summary(sents):
        return {'nSent': len(sents),
                'nPos': sum(1 for s in sents if any(valence(e) == 'positive' for e in s['e'])),
                'nNeg': sum(1 for s in sents if any(valence(e) == 'negative' for e in s['e'])),
                'nEmo': sum(1 for s in sents if s['e'])}

    paragraphs = []
    for i, row in contrast.head(n_pairs).iterrows():
        b = row['base_id']
        a_s, b_s = sentences(AUTHOR_A, b), sentences(author_b, b)
        paragraphs.append({
            'baseId': b,
            'doi': doi_of.get(b, ''),
            'topic': f'Abstract {i + 1}',          # front-end button label — edit freely
            'contrast': float(row['l1']),
            'examples': [{'aSentences': a_s, 'bSentences': b_s,
                          'aSummary': emo_summary(a_s), 'bSummary': emo_summary(b_s)}],
        })

    n_papers = len(shared)
    return {
        'authorA': AUTHOR_A, 'authorB': author_b,
        'source': 'abstracts',
        'exampleGenre': 'abs',
        # Rendered verbatim in the chart caption, where the HAP-E blob says "across all six genres".
        'scopeLabel': f'across {n_papers:,} parallel abstracts (same paper, human vs AI)',
        'metric': 'log2_ratio_vs_human (add-0.5 smoothed)',
        'emotionMeta': {e: {'valence': valence(e)} for e in EMOTIONS},
        'emotionLoadings': emotion_loadings,
        'emotionRates': emotion_rates,
        'paragraphs': paragraphs,
    }


def main():
    blob = build_abstracts_blob()
    OUT_PATH.write_text(json.dumps(blob, indent=2))
    print(f'Wrote {OUT_PATH.name}  ({blob["scopeLabel"]})')
    rates = blob['emotionRates']
    for g, load in blob['emotionLoadings'].items():
        s = pd.Series(load)
        top = s.reindex(s.abs().sort_values(ascending=False).index).head(8)
        print(f"\n{g} vs human ({rates[g]['n']:,} vs {rates[blob['authorA']]['n']:,} sentences) — "
              f'top divergences (log2 ratio):')
        for e, v in top.items():
            print(f"  {e:14s} {v:+6.2f}  ({'AI>human' if v > 0 else 'AI<human'})")
    print(f"\nTop {len(blob['paragraphs'])} contrasting pairs:")
    for p in blob['paragraphs']:
        a, b = p['examples'][0]['aSummary'], p['examples'][0]['bSummary']
        print(f"  {p['baseId']}  {p['doi']}  L1={p['contrast']:.3f}  "
              f"human[{a['nPos']}+/{a['nNeg']}- of {a['nSent']}]  "
              f"ai[{b['nPos']}+/{b['nNeg']}- of {b['nSent']}]")
    print('\nNext: python inject_json.py')


if __name__ == '__main__':
    main()
