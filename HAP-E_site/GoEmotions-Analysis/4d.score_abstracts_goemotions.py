#!/usr/bin/env python3
"""Score the parallel ABSTRACTS corpus with GoEmotions -> one row per sentence.

Emotion-side counterpart to 4a, but over `master_parallel_abs.parquet` instead of HAP-E.
That parquet is WIDE — one row per paper, one column per author:

    doi                              | human                | gemini-3.1-pro
    10.1016/j.enconman.2022.116315   | "In electrochemical…"| "Liquid-based thermo…"

Every non-`doi` column is treated as an author (`human` = the baseline, the rest = LLMs), so
adding a second model to the parquet needs no change here. Each abstract is sentence-split and
every sentence keeps its full 28-dim sigmoid probability vector, exactly as in 4a.

Because human and AI abstracts share a `doi`, the pairs are strictly one-to-one: same paper,
same content, two authors. That is what the website's Emotional Tone tab uses for its
abstract-based comparison (see 6c.emotions_abstracts_json.py, which consumes this parquet).

OUTPUT — data_processed/goemotions_abstract_sentence_probs.parquet, deliberately the SAME
column contract as goemotions_sentence_probs.parquet so downstream code is shared:

    doc_id      f'{author}_{base_id}'      e.g. human_abs_0001
    author      'human' | 'gemini-3.1-pro' | …
    genre       'abs'                      (constant; keeps the HAP-E column contract)
    base_id     'abs_0001'                 the parallel key — shared by both authors
    source_tag  the doi                    (HAP-E puts its @-suffix metadata here)
    sent_idx    0-based sentence index within the abstract
    sentence    the sentence text
    prob_<e>    28 GoEmotions sigmoid probabilities

Usage:
    python 4d.score_abstracts_goemotions.py                  # full parquet
    python 4d.score_abstracts_goemotions.py --limit 20       # smoke test on 20 papers
    python 4d.score_abstracts_goemotions.py --device cpu --batch-size 8

Requires torch + transformers (NOT installed in this repo's .venv — install before running):
    pip install "transformers>=4.48" torch
ModernBERT needs transformers >= 4.48.

Authored by Claude.
"""
import argparse
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
IN_PATH  = REPO / 'master_parallel_abs.parquet'
OUT_PATH = REPO / 'data_processed' / 'goemotions_abstract_sentence_probs.parquet'

MODEL_NAME = 'cirimus/modernbert-large-go-emotions'   # same model as 4a/4b/6
HUMAN      = 'human'      # baseline column in master_parallel_abs.parquet
GENRE      = 'abs'        # every abstract carries this genre tag
MAX_LENGTH = 1024
BATCH_SIZE = 32


def pick_device(requested=None):
    """cuda > mps > cpu, unless the caller forces one."""
    import torch
    if requested:
        return requested
    if torch.cuda.is_available():
        return 'cuda'
    if getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available():
        return 'mps'
    return 'cpu'


def build_sentence_splitter():
    """Prefer nltk Punkt (what 4a used); fall back to a regex split so this runs anywhere."""
    try:
        import nltk
        for pkg in ('punkt_tab', 'punkt'):
            try:
                nltk.data.find(f'tokenizers/{pkg}')
                break
            except LookupError:
                try:
                    nltk.download(pkg, quiet=True)
                except Exception:
                    continue
        from nltk.tokenize import sent_tokenize
        sent_tokenize('Probe one. Probe two.')     # force a real call to surface missing data
        print('Sentence splitter: nltk Punkt')
        return sent_tokenize
    except Exception as e:
        print(f'Sentence splitter: regex fallback ({type(e).__name__}: {e})')
        pat = re.compile(r'(?<=[.!?])\s+')
        return lambda t: pat.split(t)


def load_long(in_path, limit=None):
    """Wide (doi, human, <model>, …) -> long (base_id, doi, author, text), one row per abstract."""
    wide = pd.read_parquet(in_path)
    if 'doi' not in wide.columns:
        raise SystemExit(f'{in_path.name} has no `doi` column (got {list(wide.columns)})')
    authors = [c for c in wide.columns if c != 'doi']
    if HUMAN not in authors:
        raise SystemExit(f'{in_path.name} has no `{HUMAN}` column — needed as the baseline.')
    if limit:
        wide = wide.head(limit)

    # base_id is positional and stable (abs_0001…), so the human and AI rows of the same paper
    # share a key exactly the way HAP-E's parallel base_ids do.
    wide = wide.reset_index(drop=True)
    wide['base_id'] = [f'abs_{i + 1:04d}' for i in range(len(wide))]

    long = wide.melt(id_vars=['doi', 'base_id'], value_vars=authors,
                     var_name='author', value_name='text')
    long = long[long['text'].notna() & (long['text'].astype(str).str.strip() != '')]
    long['doc_id']     = long['author'] + '_' + long['base_id']
    long['genre']      = GENRE
    long['source_tag'] = long['doi']
    print(f'{in_path.name}: {len(wide)} papers x {len(authors)} authors -> {len(long)} abstracts')
    print(f'  authors: {authors}')
    return long.reset_index(drop=True)


def explode_sentences(long, splitter):
    """One row per sentence, carrying its abstract's metadata + sent_idx."""
    rows = []
    for r in long.itertuples(index=False):
        sents = [s.strip() for s in splitter(str(r.text)) if s and s.strip()]
        for i, s in enumerate(sents):
            rows.append({'doc_id': r.doc_id, 'author': r.author, 'genre': r.genre,
                         'base_id': r.base_id, 'source_tag': r.source_tag,
                         'sent_idx': i, 'sentence': s})
    sent = pd.DataFrame(rows)
    per_doc = sent.groupby('doc_id').size()
    print(f'{len(sent):,} sentences  (mean {per_doc.mean():.1f} per abstract, max {per_doc.max()})')
    return sent


def score(sent, device, batch_size, max_length):
    """Run GoEmotions over sent['sentence'] -> DataFrame of prob_<emotion> columns."""
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    print(f'Loading {MODEL_NAME} on {device}…')
    t = time.time()
    tok = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device).eval()
    emotions = [model.config.id2label[i].lower() for i in range(model.config.num_labels)]
    print(f'  loaded in {time.time() - t:.1f}s — {len(emotions)} labels')

    texts = sent['sentence'].tolist()
    out = np.zeros((len(texts), len(emotions)), dtype=np.float32)
    use_fp16 = (device == 'cuda')
    t = time.time()
    with torch.inference_mode():
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            enc = tok(batch, padding=True, truncation=True, max_length=max_length,
                      return_tensors='pt').to(device)
            with torch.autocast(device_type=device, dtype=torch.float16, enabled=use_fp16):
                logits = model(**enc).logits
            out[i:i + len(batch)] = torch.sigmoid(logits.float()).cpu().numpy()
            if i and i % (batch_size * 50) == 0:
                done = i + len(batch)
                rate = done / (time.time() - t)
                print(f'  {done:,}/{len(texts):,} sentences  ({rate:.0f}/s, '
                      f'eta {(len(texts) - done) / max(rate, 1e-6) / 60:.1f} min)')
    print(f'  scored {len(texts):,} sentences in {(time.time() - t) / 60:.1f} min')
    return pd.DataFrame(out, columns=[f'prob_{e}' for e in emotions])


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--in', dest='in_path', type=Path, default=IN_PATH)
    ap.add_argument('--out', dest='out_path', type=Path, default=OUT_PATH)
    ap.add_argument('--device', default=None, help='cuda | mps | cpu (default: best available)')
    ap.add_argument('--batch-size', type=int, default=BATCH_SIZE)
    ap.add_argument('--max-length', type=int, default=MAX_LENGTH)
    ap.add_argument('--limit', type=int, default=None, help='only score the first N papers')
    ap.add_argument('--force', action='store_true', help='overwrite an existing output parquet')
    args = ap.parse_args()

    if not args.in_path.exists():
        raise SystemExit(f'{args.in_path} not found.')
    if args.out_path.exists() and not args.force:
        raise SystemExit(f'{args.out_path} already exists — pass --force to overwrite.')
    try:
        import torch, transformers  # noqa: F401
    except ImportError:
        raise SystemExit('torch + transformers required: pip install "transformers>=4.48" torch')

    device = pick_device(args.device)
    long = load_long(args.in_path, args.limit)
    sent = explode_sentences(long, build_sentence_splitter())
    probs = score(sent, device, args.batch_size, args.max_length)

    out = pd.concat([sent.reset_index(drop=True), probs], axis=1)
    pv = out[[c for c in out.columns if c.startswith('prob_')]].to_numpy()
    assert np.isfinite(pv).all(), 'NaN/inf in prob_ columns'
    assert pv.min() >= 0.0 and pv.max() <= 1.0, f'prob_ out of [0,1]: [{pv.min()}, {pv.max()}]'

    args.out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(args.out_path, index=False)
    print(f'\nWrote {args.out_path}  shape={out.shape}')
    print(out.groupby('author').agg(abstracts=('base_id', 'nunique'), sentences=('sentence', 'size')))
    print('\nNext: python GoEmotions-Analysis/6c.emotions_abstracts_json.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
