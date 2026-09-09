
"""
Regenerate threshold-based multi-label sentence counts using per-label thresholds.

Drop-in alternative to the flat-0.30 baseline cell in 4a.GoEmotions_analysis_GPU.ipynb (0.30 is
Google's published GoEmotions cut -- one global threshold, no per-emotion cuts). A sentence
fires emotion e iff its sigmoid prob_e >= THRESHOLDS[e], where THRESHOLDS is the published
per-label "Optimal Results" vector from the cirimus/modernbert-large-go-emotions model card
(tuned on its own training set for per-label F1). Reads the cached per-sentence probabilities
(goemotions_sentence_probs.parquet, CPU-only) and writes a new parquet; the flat-0.30 output
(goemotions_sentence_counts_threshold.parquet) is left untouched.

Counts are grouped by (doc_id, author, genre, base_id) so downstream notebooks (4c, 6, 6a)
can slice by register (genre) or align human vs LLM on the shared parallel key (base_id).
This per-label parquet is the canonical single-sentence tag count for HAP-E.

Source of thresholds: https://huggingface.co/cirimus/modernbert-large-go-emotions
("Optimal Results" table, best per-label threshold tuned on the training set).

Authored by Claude.
"""

from pathlib import Path

import numpy as np
import pandas as pd

# Resolve data paths relative to THIS file (not the shell's cwd), so the script runs from
# any working directory -- matches 6a.export_sentence_sentiment.py.
HERE = Path(__file__).resolve().parent
SENT_PROBS_PATH = HERE / 'data_processed' / 'goemotions_sentence_probs.parquet'
OUT_PATH        = HERE / 'data_processed' / 'goemotions_sentence_counts_threshold_perlabel.parquet'

# Published per-label thresholds for THIS BERT model we used (cirimus/modernbert-large-go-emotions model card, Optimal Results).
THRESHOLDS = {
    'admiration': 0.40, 'amusement': 0.45, 'anger': 0.25, 'annoyance': 0.30,
    'approval': 0.30, 'caring': 0.35, 'confusion': 0.30, 'curiosity': 0.40,
    'desire': 0.40, 'disappointment': 0.30, 'disapproval': 0.35, 'disgust': 0.25,
    'embarrassment': 0.35, 'excitement': 0.25, 'fear': 0.40, 'gratitude': 0.50,
    'grief': 0.35, 'joy': 0.50, 'love': 0.45, 'nervousness': 0.45,
    'optimism': 0.25, 'pride': 0.15, 'realization': 0.25, 'relief': 0.25,
    'remorse': 0.65, 'sadness': 0.30, 'surprise': 0.40, 'neutral': 0.40,
}

sp = pd.read_parquet(SENT_PROBS_PATH)

EMOTIONS  = [c[5:] for c in sp.columns if c.startswith('prob_')]
missing   = [e for e in EMOTIONS if e not in THRESHOLDS]
if missing:
    raise KeyError(f'prob columns with no published threshold: {missing}')

probs = sp[[f'prob_{e}' for e in EMOTIONS]].to_numpy()
thr   = np.array([THRESHOLDS[e] for e in EMOTIONS], dtype=np.float64)  # aligned to EMOTIONS
fires = (probs >= thr).astype(np.int64)

fd = pd.DataFrame(fires, columns=[f'emo_{e}' for e in EMOTIONS])
# Carry genre/base_id/source_tag when present (HAP-E); fall back to (doc_id, author) for older caches.
GROUP_KEYS = [k for k in ('doc_id', 'author', 'genre', 'base_id', 'source_tag') if k in sp.columns]
fd[GROUP_KEYS] = sp[GROUP_KEYS].values
thresh_counts = (fd.groupby(GROUP_KEYS, as_index=False)
                   [[f'emo_{e}' for e in EMOTIONS]].sum())
thresh_counts.to_parquet(OUT_PATH, index=False)

M = thresh_counts[[f'emo_{e}' for e in EMOTIONS]].to_numpy()
print(f'Wrote {OUT_PATH}: {thresh_counts.shape} (per-label thresholds)')
print(f'mean emotions fired/doc {M.sum(1).mean():.2f}  |  '
      f'sentences firing nothing {(fires.sum(1) == 0).mean():.1%}  |  '
      f'firing >=2 {(fires.sum(1) >= 2).mean():.1%}')
print(f'per-emotion mean count/doc range {M.mean(0).min():.4f}-{M.mean(0).max():.3f}')
