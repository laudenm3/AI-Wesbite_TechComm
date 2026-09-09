#!/usr/bin/env python3
"""Export the sentence-by-sentence GoEmotions sentiment for one HAP-E parallel sample.

Reads goemotions_sentence_probs.parquet (one row per sentence: `sentence` text +
28 `prob_<emotion>` columns + HAP-E metadata doc_id/author/genre/base_id/source_tag),
filters to a single `base_id` (the author-stripped parallel key, e.g. acad_0001;
`source_tag` is the doc_id @-suffix, e.g. gpt-4o-2024-08-06 or chunk_2), flags each sentence's
fired emotions (prob >= per-label threshold), and writes a long CSV with one row per
sentence, author-blocked then ordered by sent_idx. This is the per-sentence emotion data
the website draws on for a single sample.

Usage:
    python 6a.export_sentence_sentiment.py                 # uses DEFAULT_BASE_ID
    python 6a.export_sentence_sentiment.py acad_0001
    python 6a.export_sentence_sentiment.py acad_0001 --threshold 0.4 --out my.csv
    python 6a.export_sentence_sentiment.py acad_0001 --authors human gemma-2-9b-it
    python 6a.export_sentence_sentiment.py --list          # show available base_ids
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DEFAULT_SENT_PATH = HERE / 'data_processed' / 'goemotions_sentence_probs.parquet'
DEFAULT_OUT_DIR = HERE / 'data_processed'

# Parallel sample exported when no base_id is given on the command line.
DEFAULT_BASE_ID = 'acad_0001'

# Per-label tuned thresholds (cirimus model card "Optimal Results"); matches 4b / notebook 6.
# A sentence fires emotion e iff prob_e >= THRESHOLDS[e]. Used by default unless --threshold
# is passed, which overrides every emotion with a single flat cut.
THRESHOLDS = {
    'admiration': 0.40, 'amusement': 0.45, 'anger': 0.25, 'annoyance': 0.30,
    'approval': 0.30, 'caring': 0.35, 'confusion': 0.30, 'curiosity': 0.40,
    'desire': 0.40, 'disappointment': 0.30, 'disapproval': 0.35, 'disgust': 0.25,
    'embarrassment': 0.35, 'excitement': 0.25, 'fear': 0.40, 'gratitude': 0.50,
    'grief': 0.35, 'joy': 0.50, 'love': 0.45, 'nervousness': 0.45,
    'optimism': 0.25, 'pride': 0.15, 'realization': 0.25, 'relief': 0.25,
    'remorse': 0.65, 'sadness': 0.30, 'surprise': 0.40, 'neutral': 0.40,
}

# Emotions excluded from the analysis (neutral fires on nearly every sentence).
DROP_EMOTIONS = {'neutral'}

# The sentence parquet must carry these HAP-E columns (written by 4a). The pre-HAP-E LEAF
# cache lacks genre/base_id/source_tag, so we fail with a clear pointer instead of a raw
# KeyError deep inside the export.
HAPE_SENT_COLUMNS = ('doc_id', 'author', 'genre', 'base_id', 'source_tag', 'sent_idx', 'sentence')


def require_hape_columns(sp, path):
    """Raise a clear, actionable error if `sp` isn't a HAP-E sentence parquet."""
    missing = [c for c in HAPE_SENT_COLUMNS if c not in sp.columns]
    if missing:
        raise SystemExit(
            f'{path}\n  is missing HAP-E column(s): {missing}\n'
            f'  This looks like a pre-HAP-E cache (e.g. the old LEAF parquet). Regenerate it by '
            f'running 4a.GoEmotions_analysis_GPU.ipynb on the HAP-E corpus, which writes '
            f'goemotions_sentence_probs.parquet with '
            f'doc_id/author/genre/base_id/source_tag/sent_idx/sentence + prob_<emotion> columns.')

# HAP-E authors to include, in display order (human first, then the 12 LLM groups).
AUTHOR_ORDER = [
    'human',
    'gpt-4o', 'gpt-4o-mini', 'gpt-5-mini',
    'llama-3-70b', 'llama-3-70b-instruct', 'llama-3-8b', 'llama-3-8b-instruct',
    'gemma-2-9b', 'gemma-2-9b-it', 'gemma-2-27b', 'gemma-2-27b-it',
    'claude-haiku-4-5',
]


def export_sentences(base_id, sp, prob_cols, emotions, threshold=None,
                     authors=AUTHOR_ORDER, per_emotion=THRESHOLDS):
    """Return the long sentence-level frame for `base_id`; raises if the sample is absent.

    Firing threshold per emotion: `per_emotion[emo]` if present, else the scalar `threshold`.
    Passing a scalar `threshold` (e.g. via --threshold) overrides every emotion.
    """
    sub = sp[(sp['base_id'] == base_id) & (sp['author'].isin(authors))].copy()
    if sub.empty:
        raise ValueError(f'no sentences for base_id={base_id!r} (authors={authors})')

    if threshold is not None:                       # flat override for every emotion
        thr = np.full(len(prob_cols), threshold, dtype=float)
    else:                                           # per-label thresholds (default)
        thr = np.array([per_emotion[e] for e in emotions], dtype=float)
    fired = sub[prob_cols].to_numpy() >= thr
    emo_arr = np.array(emotions)
    sub['fired_emotions'] = ['; '.join(emo_arr[mask]) for mask in fired]

    sub['author'] = pd.Categorical(sub['author'], categories=authors, ordered=True)
    sub = sub.sort_values(['author', 'sent_idx'])
    keep = ['author_id', 'genre', 'source_tag', 'sent_idx', 'sentence', 'fired_emotions']
    out = sub.rename(columns={'author': 'author_id'})
    return out[[c for c in keep if c in out.columns]].reset_index(drop=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('base_id', nargs='?', default=DEFAULT_BASE_ID,
                    help=f'parallel-sample key to export (default {DEFAULT_BASE_ID})')
    ap.add_argument('--threshold', type=float, default=None,
                    help='flat fire threshold overriding the per-label cuts (default: per-label)')
    ap.add_argument('--sent-path', type=Path, default=DEFAULT_SENT_PATH,
                    help='path to goemotions_sentence_probs.parquet')
    ap.add_argument('--out', type=Path, default=None,
                    help='output CSV path (default data_processed/'
                         'qual_emotion_sentences_<base_id>.csv)')
    ap.add_argument('--authors', nargs='+', default=AUTHOR_ORDER,
                    help='authors to include, in display order')
    ap.add_argument('--list', action='store_true',
                    help='list available base_ids and exit')
    args = ap.parse_args(argv)

    if not args.sent_path.exists():
        ap.error(f'{args.sent_path} not found')

    sp = pd.read_parquet(args.sent_path)
    require_hape_columns(sp, args.sent_path)
    prob_cols = [c for c in sp.columns
                 if c.startswith('prob_') and c[len('prob_'):] not in DROP_EMOTIONS]
    emotions = [c[len('prob_'):] for c in prob_cols]

    if args.list:
        ids = sorted(sp['base_id'].unique())
        print(f'{len(ids)} base_ids:')
        print('\n'.join(ids))
        return 0

    long = export_sentences(args.base_id, sp, prob_cols, emotions,
                            threshold=args.threshold, authors=args.authors)

    out = args.out or DEFAULT_OUT_DIR / f'qual_emotion_sentences_{args.base_id}.csv'
    out.parent.mkdir(parents=True, exist_ok=True)
    long.to_csv(out, index=False)
    print(f'wrote {out}  ({len(long)} sentences)')
    print(long['author_id'].value_counts().reindex(args.authors).dropna().to_string())
    return 0


if __name__ == '__main__':
    sys.exit(main())
