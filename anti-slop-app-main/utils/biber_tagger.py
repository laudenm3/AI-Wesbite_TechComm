"""Per-token Biber feature tagging for pasted text, using the PyBiber package.

spaCy parses the text (PyBiber's own parser), then each Biber feature's filter picks out the
tokens that feature counts. The filters are copied from HAP-E_site/HAP-E_website_json.ipynb,
which tags the HAP-E samples, so a pasted text is tagged the same way as the corpus samples.
Features f_43 (type-token ratio) and f_44 (mean word length) are corpus-level measures with no
per-token attribution, so they are not tagged.
"""

import re

import polars as pl
from pybiber import CorpusProcessor
from pybiber.biber_dict import FEATURES, WORDLISTS

# ── 1. Add the same lead/lag columns that pybiber builds internally ──────────
def _with_lags(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns([
        *(pl.col("dep_rel").shift(i, fill_value="punct").over("doc_id").alias(f"dep_lag_{i}")
          for i in [*range(-3, 0), *range(1, 2)]),
        *(pl.col("lemma").shift(i).over("doc_id").alias(f"lem_lag_{i}")
          for i in range(1, 3)),
        *(pl.col("pos").shift(i).over("doc_id").alias(f"pos_lag_{i}")
          for i in [*range(-4, 0), *range(1, 3)]),
        *(pl.col("tag").shift(i, fill_value="PUNCT").over("doc_id").alias(f"tag_lag_{i}")
          for i in [*range(-3, 0), *range(1, 3)]),
        *(pl.col("token").shift(i).over("doc_id").alias(f"tok_lag_{i}")
          for i in [*range(-3, 0), *range(1, 2)]),
    ])

# ── 2. Add token_tag column (lowercase token + "_" + lowercase tag) ──────────
def _with_token_tag(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df
        .filter((pl.col("token") != " ") & (pl.col("tag") != "_SP"))
        .with_columns(
            pl.when(pl.col("dep_rel") == "punct").then(pl.lit("_punct")).otherwise(pl.col("token")).alias("_t"),
            pl.when(pl.col("dep_rel") == "punct").then(pl.lit("")).otherwise(pl.col("tag")).alias("_tg"),
        )
        .with_columns(
            pl.concat_str([pl.col("_t").str.to_lowercase(), pl.col("_tg").str.to_lowercase()], separator="_").alias("token_tag")
        )
        .drop("_t", "_tg")
    )

# ── 3. Precompile regex patterns ──────────────────────────────────────────────
_PAT = {k: re.compile("|".join(v)) for k, v in FEATURES.items()}
def _rx(name):
    return lambda df: df.filter(pl.col("token_tag").str.contains(_PAT[name].pattern))

# ── 4. Filter dispatch table (all 67 features) ───────────────────────────────
FEATURE_FILTERS = {
    # — Regex-based (match against "token_tag" = "word_postag") —
    "f_01_past_tense":              _rx("f_01_past_tense"),
    "f_03_present_tense":           _rx("f_03_present_tense"),
    "f_04_place_adverbials":        _rx("f_04_place_adverbials"),
    "f_05_time_adverbials":         _rx("f_05_time_adverbials"),
    "f_06_first_person_pronouns":   _rx("f_06_first_person_pronouns"),
    "f_07_second_person_pronouns":  _rx("f_07_second_person_pronouns"),
    "f_08_third_person_pronouns":   _rx("f_08_third_person_pronouns"),
    "f_09_pronoun_it":              _rx("f_09_pronoun_it"),
    "f_11_indefinite_pronouns":     _rx("f_11_indefinite_pronouns"),
    "f_20_existential_there":       _rx("f_20_existential_there"),
    "f_24_infinitives":             _rx("f_24_infinitives"),
    "f_33_pied_piping":             _rx("f_33_pied_piping"),
    "f_36_though":                  _rx("f_36_though"),
    "f_37_if":                      _rx("f_37_if"),
    "f_42_adverbs":                 _rx("f_42_adverbs"),
    "f_45_conjuncts":               _rx("f_45_conjuncts"),
    "f_46_downtoners":              _rx("f_46_downtoners"),
    "f_47_hedges":                  _rx("f_47_hedges"),
    "f_48_amplifiers":              _rx("f_48_amplifiers"),
    "f_49_emphatics":               _rx("f_49_emphatics"),
    "f_50_discourse_particles":     _rx("f_50_discourse_particles"),
    "f_52_modal_possibility":       _rx("f_52_modal_possibility"),
    "f_53_modal_necessity":         _rx("f_53_modal_necessity"),
    "f_54_modal_predictive":        _rx("f_54_modal_predictive"),
    "f_55_verb_public":             _rx("f_55_verb_public"),
    "f_56_verb_private":            _rx("f_56_verb_private"),
    "f_57_verb_suasive":            _rx("f_57_verb_suasive"),
    "f_58_verb_seem":               _rx("f_58_verb_seem"),
    "f_59_contractions":            _rx("f_59_contractions"),
    "f_66_neg_synthetic":           _rx("f_66_neg_synthetic"),
    "f_67_neg_analytic":            _rx("f_67_neg_analytic"),
    # — Filter-based (explicit Polars conditions) —
    "f_02_perfect_aspect": lambda df: df.filter(
        (pl.col("lemma") == "have") & pl.col("dep_rel").str.contains("aux")
    ),
    "f_10_demonstrative_pronoun": lambda df: df.filter(
        (pl.col("tag") == "DT")
        & ((pl.col("tag_lag_1").is_null()) | (~pl.col("tag_lag_1").str.contains("^N|^CD|DT")))
        & pl.col("dep_rel").str.contains("nsubj|dobj|pobj")
        & pl.col("token").str.to_lowercase().is_in(WORDLISTS["pronoun_matchlist"])
    ),
    "f_12_proverb_do": lambda df: df.filter(
        (pl.col("lemma") == "do") & ~pl.col("dep_rel").str.contains("aux")
    ),
    "f_13_wh_question": lambda df: df.with_columns(
        pl.int_range(pl.len()).over(["doc_id", "sentence_id"]).alias("_si")
    ).filter(
        pl.col("tag").str.contains("^W") & (pl.col("pos") != "DET")
        & (pl.col("dep_lag_-1") == "aux")
        & ((pl.col("pos_lag_1") == "PUNCT") | (pl.col("pos_lag_2") == "PUNCT") | (pl.col("_si") <= 1))
    ).drop("_si"),
    "f_14_nominalizations": lambda df: df.filter(
        (pl.col("pos") == "NOUN")
        & pl.col("token").str.to_lowercase().str.contains("tion$|tions$|ment$|ments$|ness$|nesses$|ity$|ities$")
        & ~pl.col("token").str.to_lowercase().is_in(WORDLISTS["nominalization_stoplist"])
    ),
    "f_15_gerunds": lambda df: df.filter(
        pl.col("token").str.to_lowercase().str.contains("ing$|ings$")
        & pl.col("dep_rel").str.contains("nsub|dobj|pobj")
        & ~pl.col("token").str.to_lowercase().is_in(WORDLISTS["gerund_stoplist"])
    ),
    "f_16_other_nouns": lambda df: df.filter(
        ((pl.col("pos") == "NOUN") | (pl.col("pos") == "PROPN"))
        & ~pl.col("token").str.contains("-")
        & ~(pl.col("token").str.to_lowercase().str.contains("ing$|ings$")
            & pl.col("dep_rel").str.contains("nsub|dobj|pobj")
            & ~pl.col("token").str.to_lowercase().is_in(WORDLISTS["gerund_stoplist"]))
        & ~((pl.col("pos") == "NOUN")
            & pl.col("token").str.to_lowercase().str.contains("tion$|tions$|ment$|ments$|ness$|nesses$|ity$|ities$")
            & ~pl.col("token").str.to_lowercase().is_in(WORDLISTS["nominalization_stoplist"]))
    ),
    "f_17_agentless_passives": lambda df: df.filter(
        (pl.col("dep_rel") == "auxpass")
        & (pl.col("tok_lag_-2").is_null() | (pl.col("tok_lag_-2") != "by"))
        & (pl.col("tok_lag_-3").is_null() | (pl.col("tok_lag_-3") != "by"))
    ),
    "f_18_by_passives": lambda df: df.filter(
        (pl.col("dep_rel") == "auxpass")
        & ((pl.col("tok_lag_-2") == "by") | (pl.col("tok_lag_-3") == "by"))
    ),
    "f_19_be_main_verb": lambda df: df.filter(
        (pl.col("lemma") == "be")
        & pl.col("tag").is_in(["VBD", "VBP", "VBZ"])
        & ~pl.col("dep_rel").str.contains("aux")
    ),
    "f_21_that_verb_comp": lambda df: df.filter(
        (pl.col("token") == "that") & (pl.col("pos") == "SCONJ") & (pl.col("pos_lag_1") == "VERB")
    ),
    "f_22_that_adj_comp": lambda df: df.filter(
        (pl.col("token") == "that") & (pl.col("pos") == "SCONJ") & (pl.col("pos_lag_1") == "ADJ")
    ),
    # Note: raw matches before doc-level adjustment (f_23 -= f_31 + f_32)
    "f_23_wh_clause": lambda df: df.filter(
        pl.col("tag").str.contains("^W") & (pl.col("token") != "which") & (pl.col("pos_lag_1") == "VERB")
    ),
    "f_25_present_participle": lambda df: df.filter(
        (pl.col("tag") == "VBG")
        & ((pl.col("dep_rel") == "advcl") | (pl.col("dep_rel") == "ccomp"))
        & (pl.col("dep_lag_1") == "punct")
    ),
    "f_26_past_participle": lambda df: df.filter(
        (pl.col("tag") == "VBN")
        & ((pl.col("dep_rel") == "advcl") | (pl.col("dep_rel") == "ccomp"))
        & (pl.col("dep_lag_1") == "punct")
    ),
    "f_27_past_participle_whiz": lambda df: df.filter(
        (pl.col("tag") == "VBN") & (pl.col("dep_rel") == "acl") & (pl.col("pos_lag_1") == "NOUN")
    ),
    "f_28_present_participle_whiz": lambda df: df.filter(
        (pl.col("tag") == "VBG") & (pl.col("dep_rel") == "acl") & (pl.col("pos_lag_1") == "NOUN")
    ),
    "f_29_that_subj": lambda df: df.filter(
        (pl.col("token").str.to_lowercase() == "that")
        & pl.col("dep_rel").str.contains("nsubj")
        & pl.col("tag_lag_1").str.contains("^N|^CD|DT")
    ),
    "f_30_that_obj": lambda df: df.filter(
        (pl.col("token").str.to_lowercase() == "that")
        & pl.col("dep_rel").str.contains("dobj")
        & pl.col("tag_lag_1").str.contains("^N|^CD|DT")
    ),
    "f_31_wh_subj": lambda df: df.filter(
        pl.col("tag").str.contains("^W")
        & (pl.col("lem_lag_2") != "ask") & (pl.col("lem_lag_2") != "tell")
        & (pl.col("tag_lag_1").str.contains("^N|^CD|DT")
           | ((pl.col("pos_lag_1") == "PUNCT") & pl.col("tag_lag_2").str.contains("^N|^CD|DT") & (pl.col("token") == "who")))
        & (pl.col("token") != "that")
        & pl.col("dep_rel").str.contains("nsubj")
    ),
    "f_32_wh_obj": lambda df: df.filter(
        pl.col("tag").str.contains("^W")
        & (pl.col("lem_lag_2") != "ask") & (pl.col("lem_lag_2") != "tell")
        & (pl.col("tag_lag_1").str.contains("^N|^CD|DT")
           | ((pl.col("pos_lag_1") == "PUNCT") & pl.col("tag_lag_2").str.contains("^N|^CD|DT") & (pl.col("token") == "who")))
        & (pl.col("token") != "that")
        & pl.col("dep_rel").str.contains("obj")
    ),
    "f_34_sentence_relatives": lambda df: df.filter(
        (pl.col("token").str.to_lowercase() == "which") & (pl.col("pos_lag_1") == "PUNCT")
    ),
    "f_35_because": lambda df: df.filter(
        (pl.col("token").str.to_lowercase() == "because")
        & (pl.col("tok_lag_-1").str.to_lowercase() != "of")
    ),
    "f_38_other_adv_sub": lambda df: df.filter(
        (pl.col("pos") == "SCONJ") & (pl.col("dep_rel") == "mark")
        & ~pl.col("token").str.to_lowercase().is_in(["because", "if", "unless", "though", "although", "tho"])
        & ~((pl.col("token").str.to_lowercase() == "that") & (pl.col("dep_lag_1") != "ADV"))
    ),
    "f_39_prepositions": lambda df: df.filter(pl.col("dep_rel") == "prep"),
    "f_40_adj_attr": lambda df: df.filter(
        (pl.col("pos") == "ADJ")
        & ((pl.col("pos_lag_-1") == "NOUN") | (pl.col("pos_lag_-1") == "ADJ")
           | ((pl.col("tok_lag_-1") == ",") & (pl.col("pos_lag_-2") == "ADJ")))
        & ~pl.col("token").str.contains("-")
    ),
    "f_41_adj_pred": lambda df: df.filter(
        (pl.col("pos") == "ADJ")
        & ((pl.col("pos_lag_1") == "VERB") | (pl.col("pos_lag_1") == "AUX"))
        & pl.col("lem_lag_1").is_in(WORDLISTS["linking_matchlist"])
        & (pl.col("pos_lag_-1") != "NOUN") & (pl.col("pos_lag_-1") != "ADJ") & (pl.col("pos_lag_-1") != "ADV")
        & ~pl.col("token").str.contains("-")
    ),
    "f_51_demonstratives": lambda df: df.filter(
        pl.col("token").str.to_lowercase().is_in(WORDLISTS["pronoun_matchlist"])
        & (pl.col("dep_rel") == "det")
    ),
    "f_60_that_deletion": lambda df: df.filter(
        pl.col("lemma").is_in(WORDLISTS["verb_matchlist"]) & (pl.col("pos") == "VERB")
        & (
            ((pl.col("dep_lag_-1") == "nsubj") & (pl.col("pos_lag_-2") == "VERB")
             & (pl.col("tag_lag_-1") != "WP") & (pl.col("tag_lag_-2") != "VBG"))
            | ((pl.col("tag_lag_-1") == "DT") & (pl.col("dep_lag_-2") == "nsubj") & (pl.col("pos_lag_-3") == "VERB"))
            | ((pl.col("tag_lag_-1") == "DT") & (pl.col("dep_lag_-2") == "amod")
               & (pl.col("dep_lag_-3") == "nsubj") & (pl.col("pos_lag_-4") == "VERB"))
        )
    ),
    "f_61_stranded_preposition": lambda df: df.filter(
        (pl.col("tag") == "IN") & (pl.col("dep_rel") == "prep")
        & pl.col("tag_lag_-1").str.contains("^[[:punct:]]$")
    ),
    "f_62_split_infinitive": lambda df: df.filter(
        (pl.col("tag") == "TO")
        & (
            ((pl.col("tag_lag_-1") == "RB") & (pl.col("tag_lag_-2") == "VB"))
            | ((pl.col("tag_lag_-1") == "RB") & (pl.col("tag_lag_-2") == "RB") & (pl.col("tag_lag_-3") == "VB"))
        )
    ),
    "f_63_split_auxiliary": lambda df: df.filter(
        pl.col("dep_rel").str.contains("aux")
        & (
            ((pl.col("pos_lag_-1") == "ADV") & (pl.col("pos_lag_-2") == "VERB"))
            | ((pl.col("pos_lag_-1") == "ADV") & (pl.col("pos_lag_-2") == "ADV") & (pl.col("pos_lag_-3") == "VERB"))
        )
    ),
    "f_64_phrasal_coordination": lambda df: df.filter(
        (pl.col("tag") == "CC")
        & (
            ((pl.col("pos_lag_-1") == "NOUN") & (pl.col("pos_lag_1") == "NOUN"))
            | ((pl.col("pos_lag_-1") == "VERB") & (pl.col("pos_lag_1") == "VERB"))
            | ((pl.col("pos_lag_-1") == "ADJ")  & (pl.col("pos_lag_1") == "ADJ"))
            | ((pl.col("pos_lag_-1") == "ADV")  & (pl.col("pos_lag_1") == "ADV"))
        )
    ),
    "f_65_clausal_coordination": lambda df: df.filter(
        (pl.col("tag") == "CC") & (pl.col("dep_rel") != "ROOT")
        & (
            (pl.col("dep_lag_-1") == "nsubj")
            | (pl.col("dep_lag_-2") == "nsubj")
            | (pl.col("dep_lag_-3") == "nsubj")
        )
    ),
    # f_43 (type-token ratio) and f_44 (mean word length) are corpus-level
    # metrics with no individual token attribution — excluded intentionally.
}

# Polars' regex engine rejects look-around, so features whose pattern uses it are matched with
# Python's re, one row at a time.
_LOOKAROUND_RE = re.compile(r"\(\?<[=!]|\(\?[=!]")
_PY_FALLBACK = {name: pat for name, pat in _PAT.items() if _LOOKAROUND_RE.search(pat.pattern)}

FEATURE_NAMES = list(FEATURE_FILTERS)


def _feature_rows(feature: str, df: pl.DataFrame) -> pl.DataFrame:
    if feature in _PY_FALLBACK:
        pat = _PY_FALLBACK[feature]
        mask = df["token_tag"].map_elements(
            lambda s: bool(pat.search(s)) if s is not None else False, return_dtype=pl.Boolean)
        return df.filter(mask)
    return FEATURE_FILTERS[feature](df)


def tag_text(text: str, nlp) -> tuple[list[dict], int]:
    """Parse text and tag it with Biber features.

    Returns (tokens, word_count). Each token is {"t": the text as written, "f": [feature, ...],
    "gap": the whitespace or characters between this token and the previous one}, so the original
    layout (paragraph breaks included) can be rebuilt exactly. word_count excludes punctuation.
    """
    corpus = pl.DataFrame({"doc_id": ["doc"], "text": [text]})
    parsed = CorpusProcessor().process_corpus(corpus, nlp, show_progress=False)
    annotated = _with_token_tag(_with_lags(parsed))

    tag_map: dict[tuple[int, int], list[str]] = {}
    for feature in FEATURE_FILTERS:
        for row in _feature_rows(feature, annotated).select(["sentence_id", "token_id"]).iter_rows():
            tag_map.setdefault(row, []).append(feature)

    tokens, cursor, words = [], 0, 0
    rows = parsed.sort(["sentence_id", "token_id"]).iter_rows(named=True)
    for r in rows:
        tok = r["token"]
        if not tok.strip():
            continue  # whitespace tokens: the gap before the next token already carries them
        start = text.find(tok, cursor)
        if start < 0:  # the parser changed the token's spelling; fall back to a single space
            gap, start = " ", cursor
        else:
            gap = text[cursor:start]
            cursor = start + len(tok)
        tokens.append({"t": tok, "gap": gap, "f": tag_map.get((r["sentence_id"], r["token_id"]), [])})
        if r["pos"] not in ("PUNCT", "SPACE", "SYM"):
            words += 1
    return tokens, words
