#!/usr/bin/env python3
"""Build emotions_paragraphs.json — the emotion analog of biber_paragraphs.json.

This is the emotion-side counterpart to the Biber MDA website data. Where the Biber file
ranks grammatical features by their factor loading and shows paragraph pairs that contrast
on that factor, this file:

  1. EMOTION LOADINGS (corpus-wide, all 6 genres): for each GoEmotions category, the log2
     ratio of an AI group's sentence-level firing rate to the human firing rate. A sentence
     "fires" emotion e iff prob_e >= the per-label threshold (cirimus model card, matches
     4b/6/6a). Positive loading = the AI group expresses that emotion MORE than humans;
     negative = less. Rates are add-0.5 (Laplace) smoothed before the ratio so zero-count
     cells stay finite instead of going to +/-inf. Loadings are emitted per model family
     (gemma / gpt / llama / claude), per individual model (gpt-4o, gpt-5-mini, …), AND for
     all 12 LLMs pooled ("machine"), each vs human.

  2. CONTRAST PAIRS (acad only): parallel human <-> gemma-2-9b-it documents (shared base_id)
     ranked by how different their per-emotion firing profiles are (L1 distance over the
     fired-fraction vectors). The top N pairs are emitted with every sentence tagged by its
     fired emotions, so the front-end can show two emotionally-divergent versions of the
     same prompt side by side.

Reads data_processed/goemotions_sentence_probs.parquet (one row per sentence: `sentence`
text + 28 prob_<emotion> cols + HAP-E metadata doc_id/author/genre/base_id/source_tag/
sent_idx). Writes emotions_paragraphs.json alongside this script. Pure pandas/numpy — no
spaCy/pybiber/MDA needed (unlike the Biber path in HAP-E_website_json.ipynb).

Decisions baked in (set by the user 2026-06-27): AI groups = per-family + pooled machine;
loadings span all genres, example pairs stay in acad; metric = raw log2 ratio (smoothed).

Authored by Claude.
"""
from pathlib import Path
import json

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SENT_PATH = HERE / 'data_processed' / 'goemotions_sentence_probs.parquet'
OUT_PATH  = HERE / 'emotions_paragraphs.json'

# ── Config ────────────────────────────────────────────────────────────────────
AUTHOR_A      = 'human'           # Style A — the human baseline
AUTHOR_B      = 'gemma-2-9b-it'   # Style B — the concrete LLM shown in the example pairs
EXAMPLE_GENRE = 'acad'            # example pairs are drawn from this register
N_PAIRS       = 3                 # how many contrasting pairs to emit
SMOOTH        = 0.5               # Laplace add-k on firing COUNTS before the log2 ratio

# How a sentence's sigmoid score becomes a fired/not-fired decision.
#   'perlabel' — the per-label cuts below, tuned for cirimus/modernbert-large-go-emotions (the
#                model that produced our probabilities). Default: model-matched calibration.
#   'google'   — Google's published GoEmotions cutoff, a flat 0.3 (eval_prob_threshold in
#                goemotions/bert_classifier.py). Tuned for THEIR BERT, not for ModernBERT.
# Checked 2026-07-13: the two agree closely on this corpus (overall AI-vs-human direction
# +0.17 vs +0.17 on HAP-E, -0.95 vs -0.94 on the abstracts, same top emotions), so this is a
# calibration preference, not a result-changing choice. Switching needs no re-scoring — the
# probabilities are cached; just re-run 6b / 6c and inject_json.py.
THRESHOLD_MODE  = 'perlabel'     # 'perlabel' | 'google'
GOOGLE_FLAT_THR = 0.30

# Per-label tuned thresholds (cirimus/modernbert-large-go-emotions "Optimal Results");
# identical to 4b / 6 / 6a / the website notebook. A sentence fires e iff prob_e >= THR[e].
_PER_LABEL = {
    'admiration': 0.40, 'amusement': 0.45, 'anger': 0.25, 'annoyance': 0.30,
    'approval': 0.30, 'caring': 0.35, 'confusion': 0.30, 'curiosity': 0.40,
    'desire': 0.40, 'disappointment': 0.30, 'disapproval': 0.35, 'disgust': 0.25,
    'embarrassment': 0.35, 'excitement': 0.25, 'fear': 0.40, 'gratitude': 0.50,
    'grief': 0.35, 'joy': 0.50, 'love': 0.45, 'nervousness': 0.45,
    'optimism': 0.25, 'pride': 0.15, 'realization': 0.25, 'relief': 0.25,
    'remorse': 0.65, 'sadness': 0.30, 'surprise': 0.40, 'neutral': 0.40,
}
DROP_EMOTIONS = {'neutral'}       # fires on most sentences; excluded from the analysis

EMO_POSITIVE = {'admiration', 'amusement', 'approval', 'caring', 'desire', 'excitement',
                'gratitude', 'joy', 'love', 'optimism', 'pride', 'relief'}
EMO_NEGATIVE = {'anger', 'annoyance', 'disappointment', 'disapproval', 'disgust',
                'embarrassment', 'fear', 'grief', 'nervousness', 'remorse', 'sadness'}

def valence(e):
    if e in EMO_POSITIVE: return 'positive'
    if e in EMO_NEGATIVE: return 'negative'
    return 'ambiguous'            # confusion / curiosity / realization / surprise

# AI groups compared against human, each a list of `author` labels. "machine" = all LLMs.
FAMILIES = {
    'gemma':  ['gemma-2-9b', 'gemma-2-9b-it', 'gemma-2-27b', 'gemma-2-27b-it'],
    'gpt':    ['gpt-4o', 'gpt-4o-mini', 'gpt-5-mini'],
    'llama':  ['llama-3-70b', 'llama-3-70b-instruct', 'llama-3-8b', 'llama-3-8b-instruct'],
    'claude': ['claude-haiku-4-5'],
}

HAPE_COLS = ('doc_id', 'author', 'genre', 'base_id', 'source_tag', 'sent_idx', 'sentence')


def build_emotions_blob(sent_path=SENT_PATH):
    """Compute the full emotions_paragraphs.json blob and return it as a dict.

    Pure read — does no file writing, so the website notebook can import this and
    write the JSON itself (single source of truth shared with the CLI `main`)."""
    sent_path = Path(sent_path)
    if not sent_path.exists():
        raise SystemExit(f'{sent_path} not found — run 4a first.')
    sp = pd.read_parquet(sent_path)
    missing = [c for c in HAPE_COLS if c not in sp.columns]
    if missing:
        raise SystemExit(f'{sent_path} missing HAP-E column(s) {missing} — rerun 4a.')

    EMOTIONS = [c[5:] for c in sp.columns if c.startswith('prob_') and c[5:] not in DROP_EMOTIONS]
    thr   = np.array([THRESHOLDS[e] for e in EMOTIONS])
    fired = sp[[f'prob_{e}' for e in EMOTIONS]].to_numpy() >= thr      # (n_sent, n_emo) bool
    fd = pd.DataFrame(fired, columns=EMOTIONS)
    fd['author'] = sp['author'].values
    fd['genre']  = sp['genre'].values
    fd['base_id'] = sp['base_id'].values

    present = set(sp['author'].unique())
    machine = [a for a in present if a != AUTHOR_A]

    # ── 1. Corpus-wide emotion loadings (all genres) ─────────────────────────────
    def group_rates(authors):
        sub = fd[fd['author'].isin(authors)]
        return sub[EMOTIONS].sum(), len(sub)          # raw fire counts, n sentences

    h_counts, h_n = group_rates([AUTHOR_A])
    h_rate = h_counts / max(h_n, 1)

    def log2_loadings(g_counts, g_n):
        # add-0.5 smoothed rates so empty cells stay finite; raw log2 ratio per the user's choice.
        gr = (g_counts + SMOOTH) / (g_n + 2 * SMOOTH)
        hr = (h_counts + SMOOTH) / (h_n + 2 * SMOOTH)
        return np.log2(gr / hr)

    # Each individual model also gets its own group (keyed by its `author` label) so the
    # front-end can break a family down into specific LLMs (e.g. gpt -> gpt-4o / gpt-5-mini).
    per_model = {m: [m] for members in FAMILIES.values() for m in members}
    groups = {'machine': machine, **FAMILIES, **per_model}
    emotion_loadings, emotion_rates = {}, {
        AUTHOR_A: {'n': int(h_n), 'rates': {e: float(h_rate[e]) for e in EMOTIONS}}
    }
    for gname, authors in groups.items():
        authors = [a for a in authors if a in present]      # never assume membership == corpus
        if not authors:
            continue
        g_counts, g_n = group_rates(authors)
        load = log2_loadings(g_counts, g_n)
        emotion_loadings[gname] = {e: float(load[e]) for e in EMOTIONS}
        emotion_rates[gname] = {'n': int(g_n),
                                'rates': {e: float(g_counts[e] / max(g_n, 1)) for e in EMOTIONS}}

    # ── 2. Emotion-contrast example pairs (acad, human vs gemma-2-9b-it) ──────────
    ac = fd[fd['genre'] == EXAMPLE_GENRE]
    def doc_profile(author):
        sub = ac[ac['author'] == author]
        prof = sub.groupby('base_id')[EMOTIONS].mean()       # fired-fraction per doc
        return prof
    pa, pb = doc_profile(AUTHOR_A), doc_profile(AUTHOR_B)
    shared = sorted(set(pa.index) & set(pb.index))
    contrast = pd.DataFrame({
        'base_id': shared,
        'l1': [np.abs(pa.loc[b] - pb.loc[b]).sum() for b in shared],
    }).sort_values('l1', ascending=False).reset_index(drop=True)

    sp_ac = sp[sp['genre'] == EXAMPLE_GENRE]
    def sentences(author, base_id):
        rows = sp_ac[(sp_ac['author'] == author) & (sp_ac['base_id'] == base_id)].sort_values('sent_idx')
        out = []
        for _, r in rows.iterrows():
            e = [em for em in EMOTIONS if r[f'prob_{em}'] >= THRESHOLDS[em]]
            out.append({'s': r['sentence'], 'e': e})
        return out

    def emo_summary(sents):
        pos = sum(1 for s in sents if any(valence(e) == 'positive' for e in s['e']))
        neg = sum(1 for s in sents if any(valence(e) == 'negative' for e in s['e']))
        return {'nSent': len(sents), 'nPos': pos, 'nNeg': neg,
                'nEmo': sum(1 for s in sents if s['e'])}

    paragraphs, picks = [], contrast.head(N_PAIRS)
    for _, row in picks.iterrows():
        b = row['base_id']
        a_s, b_s = sentences(AUTHOR_A, b), sentences(AUTHOR_B, b)
        paragraphs.append({'baseId': b, 'contrast': float(row['l1']),
                           'examples': [{'aSentences': a_s, 'bSentences': b_s,
                                         'aSummary': emo_summary(a_s), 'bSummary': emo_summary(b_s)}]})

    # ── 3. Assemble ──────────────────────────────────────────────────────────────
    return {
        'authorA': AUTHOR_A, 'authorB': AUTHOR_B,
        'exampleGenre': EXAMPLE_GENRE,
        'metric': 'log2_ratio_vs_human (add-0.5 smoothed)',
        'emotionMeta': {e: {'valence': valence(e)} for e in EMOTIONS},
        'emotionLoadings': emotion_loadings,     # {group: {emotion: log2 ratio vs human}}
        'emotionRates': emotion_rates,           # {group|human: {n, rates:{emotion: fire rate}}}
        'paragraphs': paragraphs,
    }


def report(blob):
    """Print a human-readable summary of a blob from build_emotions_blob()."""
    rates, loadings = blob['emotionRates'], blob['emotionLoadings']
    h_rate = rates[blob['authorA']]['rates']
    print(f"Built emotions blob ({len(blob['emotionMeta'])} emotions, all genres for loadings, "
          f"{blob['exampleGenre']} for pairs)")
    print(f"  {blob['authorA']} sentences (corpus): {rates[blob['authorA']]['n']:,}")
    for gname in loadings:
        print(f"  {gname:8s} sentences: {rates[gname]['n']:,}")
    for gname in ('machine', 'gemma'):
        if gname not in loadings:
            continue
        load = pd.Series(loadings[gname])
        ranked = load.reindex(load.abs().sort_values(ascending=False).index).head(8)
        print(f'\nTop emotions where {gname} diverges from human (log2 ratio):')
        for e, v in ranked.items():
            arrow = 'AI>human' if v > 0 else 'AI<human'
            print(f'  {e:14s} {v:+6.2f}  ({arrow})   human {h_rate[e]:.4f}  {gname} {rates[gname]["rates"][e]:.4f}')
    print(f"\nTop {len(blob['paragraphs'])} contrasting {blob['exampleGenre']} pairs "
          f"({blob['authorA']} vs {blob['authorB']}):")
    for p in blob['paragraphs']:
        a, b = p['examples'][0]['aSummary'], p['examples'][0]['bSummary']
        print(f"  {p['baseId']}  L1={p['contrast']:.3f}  "
              f"human[{a['nPos']}+/{a['nNeg']}- of {a['nSent']}]  "
              f"gemma[{b['nPos']}+/{b['nNeg']}- of {b['nSent']}]")


def main():
    blob = build_emotions_blob()
    OUT_PATH.write_text(json.dumps(blob, indent=2))
    print(f'Wrote {OUT_PATH.name}')
    report(blob)


if __name__ == '__main__':
    main()
