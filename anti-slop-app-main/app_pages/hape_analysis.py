"""HAP-E data analysis: Biber features and sentiment (Streamlit port of
HAP-E_Researcher_website.html). Settings live in content/hape_analysis.py; the data is in
data/*.json."""

import html
import json
import math
import re
from pathlib import Path

import streamlit as st

from content.hape_analysis import (
    AI_FAMILIES, AI_GROUP_LABELS, AI_GROUP_ORDER, AUTHOR_DISPLAY,
    BIBER_CHART_NOTE, BIBER_INTRO, BIBER_LEGEND, BIBER_PASSAGE_NOTE, DATA_NOTE, PAGE_INTRO, SENTIMENT_INTRO,
    THEMATIC_GROUPS, TOP_N_EMOTIONS, TOPIC_LABELS, VALENCE_COLOR,
)
from utils.style import DARK, banner, callout, palette

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@st.cache_data
def load_json(name: str) -> dict:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def display_author(author_id: str) -> str:
    return AUTHOR_DISPLAY.get(author_id) or (author_id[:1].upper() + author_id[1:])


def model_name_of(sample: dict, default_model: str) -> str:
    model = sample.get("model", default_model)
    return AI_GROUP_LABELS.get(model) or display_author(model)


def esc(text: str) -> str:
    """Escape for raw HTML inside st.markdown, which would otherwise read $ as math and
    * _ ` as markdown."""
    out = html.escape(text)
    for ch in "$*_`~":
        out = out.replace(ch, f"&#{ord(ch)};")
    return out


def highlight_css(p: dict) -> str:
    mode = "dark" if p is DARK else "light"
    return "\n".join(
        f".hape-card .hape-hl.{k} {{ background: {g['hl'][mode][0]}; color: {g['hl'][mode][1]}; }}"
        for k, g in THEMATIC_GROUPS.items()
    )


def page_css(p: dict) -> str:
    return f"""<style>
.hape-card, .hape-card * {{ color: {p['TEXT']}; }}
.hape-card {{ background: {p['SURFACE']}; border: 1px solid {p['BORDER']}; border-top: 4px solid {p['ACCENT']};
  padding: 20px 22px; line-height: 1.8; border-radius: 4px; }}
.hape-hl {{ padding: 1px 3px; border-radius: 3px; -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
{highlight_css(p)}
.hape-card.b {{ border-top-color: {p['MUTED']}; }}
.hape-card-title {{ font-weight: 700; font-size: 1.05rem; margin-bottom: 10px; }}
.hape-badge {{ display: inline-block; padding: 2px 10px; font-size: 0.72rem; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase; border-radius: 2px;
  background: {p['ACCENT']}; color: {p['SURFACE']} !important; }}
.hape-card.b .hape-badge {{ background: {p['MUTED']}; }}
.hape-legend, .hape-legend * {{ color: {p['TEXT']}; }}
.hape-legend {{ margin-top: 16px; padding: 12px 16px; background: {p['SURFACE']};
  border-left: 3px solid {p['ACCENT']}; font-size: 0.85rem; line-height: 1.65; }}
.hape-legend em {{ font-style: normal; font-weight: 700; }}
.hape-bars, .hape-bars * {{ color: {p['TEXT']}; }}
.hape-bars {{ background: {p['SURFACE']}; border: 1px solid {p['BORDER']}; border-top: 4px solid {p['ACCENT']};
  padding: 16px 20px; border-radius: 4px; }}
.hape-bars .cap {{ font-size: 0.82rem; line-height: 1.55; margin-bottom: 12px; }}
.hape-row {{ display: grid; grid-template-columns: 145px 1fr 52px; align-items: center; gap: 12px; padding: 3px 6px; }}
.hape-row.on {{ background: {p['ACCENT_SOFT']}; border-radius: 3px; }}
.hape-name {{ font-size: 0.85rem; display: flex; align-items: center; gap: 7px; justify-content: flex-end; text-align: right; }}
.hape-dot {{ width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }}
.hape-track {{ position: relative; height: 16px; background: {p['INPUT']}; border-radius: 2px; }}
.hape-track::before {{ content: ''; position: absolute; left: 50%; top: -3px; bottom: -3px; width: 1px; background: {p['BORDER']}; }}
.hape-bar {{ position: absolute; top: 2px; bottom: 2px; border-radius: 2px; }}
.hape-val {{ font-size: 0.78rem; font-variant-numeric: tabular-nums; }}
.hape-sent, .hape-sent * {{ color: {p['TEXT']}; }}
.hape-sent {{ display: block; padding: 5px 9px; margin: 2px 0; border-radius: 3px; line-height: 1.65;
  border-left: 3px solid transparent; }}
.hape-sent.has {{ border-left-color: {p['BORDER']}; }}
.hape-chip {{ display: inline-block; font-size: 0.66rem; font-weight: 700; letter-spacing: 0.03em;
  text-transform: uppercase; padding: 1px 8px; border-radius: 10px; margin: 0 2px; vertical-align: middle;
  white-space: nowrap; color: #fff !important; }}
.hape-chip.dim {{ opacity: 0.4; }}
.hape-summary, .hape-summary * {{ color: {p['MUTED']}; }}
.hape-summary {{ font-size: 0.8rem; font-style: italic; margin-top: 12px; padding-top: 10px;
  border-top: 1px dotted {p['BORDER']}; }}
</style>"""


def legend(text_html: str):
    st.markdown(f'<div class="hape-legend">{text_html}</div>', unsafe_allow_html=True)


# ── Biber features ───────────────────────────────────────────────────────────
NO_SPACE_BEFORE = re.compile(r"^(?:[.,;:!?)\]}%’”…]|'(?:s|d|m|re|ve|ll)\b|n't\b)", re.I)
NO_SPACE_AFTER = re.compile(r"[(\[{‘“]$")

FEATURE_TO_THEME = {f: k for k, g in THEMATIC_GROUPS.items() for f in g["features"]}


def render_tokens(tokens: list[dict], groups: list[str] | None) -> str:
    """Join tokens into HTML, highlighting tokens that belong to a chosen thematic group
    (the first chosen group, in THEMATIC_GROUPS order, wins when a token matches several)."""
    wanted = [g for g in THEMATIC_GROUPS if g in (groups or [])]
    parts = []
    for i, tok in enumerate(tokens):
        body = esc(tok["t"])
        hit = next((g for g in wanted if any(FEATURE_TO_THEME.get(f) == g for f in tok.get("f", []))), None)
        if hit:
            body = f'<span class="hape-hl {hit}">{body}</span>'
        if i > 0 and not NO_SPACE_BEFORE.match(tok["t"]) and not NO_SPACE_AFTER.search(tokens[i - 1]["t"]):
            parts.append(" ")
        parts.append(body)
    return "".join(parts)


def para_card(css_class: str, badge: str, inner_html: str, summary_html: str = ""):
    st.markdown(
        f'<div class="hape-card {css_class}"><div class="hape-card-title">'
        f'<span class="hape-badge">{esc(badge)}</span></div>{inner_html}{summary_html}</div>',
        unsafe_allow_html=True,
    )


BIBER_SMOOTH = 0.1  # per 1,000 tokens, matches the smoothing in the notebook's feature ratios


def feature_name(feature: str) -> str:
    return re.sub(r"^f_\d+_", "", feature).replace("_", " ")


def group_density(tokens: list[dict], group: str) -> float:
    """Share of tokens carrying any feature of a thematic group, lightly smoothed."""
    hits = sum(any(FEATURE_TO_THEME.get(f) == group for f in t.get("f", [])) for t in tokens)
    return (hits + 0.5) / (len(tokens) + 1)


def pair_contrast(human: list[dict], other: list[dict], other_name: str) -> str:
    """'more nominal density in Human': the thematic group whose density differs most."""
    best, best_val = None, 0.0
    for g in THEMATIC_GROUPS:
        val = math.log2(group_density(other, g) / group_density(human, g))
        if abs(val) >= abs(best_val):
            best, best_val = g, val
    label = THEMATIC_GROUPS[best]["label"]
    return f"more {label.lower()} in {display_author('human') if best_val < 0 else other_name}"


def biber_tab():
    data = load_json("biber_paragraphs.json")
    all_loadings, rates = data["featureLoadings"], data["featureRates"]
    human_tokens, model_pairs = data["humanTokens"], data["modelPairs"]
    author_a = data.get("authorA", "human")
    scope_label = data.get("scopeLabel", "across all six genres")

    callout("info", BIBER_INTRO)

    # High level: which feature groups does a model use more or less than humans? Same groups
    # as the highlighting below; a group's rate is the sum of its features' per-1,000-token rates.
    group = model_picker(all_loadings, rates, "hape_biber")
    model_name = AI_GROUP_LABELS.get(group, group)
    human_rates, group_rates = rates.get(author_a, {}).get("rates", {}), rates.get(group, {}).get("rates", {})
    shown = st.session_state.get("hape_theme") or []
    def group_ratio(rate_map: dict, g: dict) -> tuple[float, float, float]:
        h = sum(human_rates.get(f, 0) for f in g["features"])
        m = sum(rate_map.get(f, 0) for f in g["features"])
        return h, m, math.log2((m + BIBER_SMOOTH) / (h + BIBER_SMOOTH))

    # One scale for every model, so switching models shows relative differences, not a rescale.
    scale = max(abs(group_ratio(r["rates"], g)[2]) for name, r in rates.items() if name != author_a
                for g in THEMATIC_GROUPS.values())
    rows = []
    for key, g in THEMATIC_GROUPS.items():       # fixed order: the order of THEMATIC_GROUPS
        h, m, val = group_ratio(group_rates, g)
        rows.append({
            "name": g["label"], "val": val, "on": key in shown, "color": g["color"],
            "tip": (f"{g['label']}: human {h:.1f}, {model_name} {m:.1f} per 1,000 tokens (log2 ratio "
                    f"{val:.2f}). Features: {', '.join(feature_name(f) for f in g['features'])}"),
        })
    loadings_chart(
        rows,
        BIBER_CHART_NOTE.format(model=esc(model_name), scope=esc(scope_label)),
        max_abs=scale)

    # Low level: one of the chosen model's most divergent topics. Passages exist per individual
    # model, so a family or "All LLMs" selection falls back to its first model with passages.
    st.write("")
    default_model = data.get("authorB", "gemma-2-9b-it")
    if group in model_pairs:
        model = group
    else:
        members = [m for m in AI_GROUP_ORDER if m in model_pairs and (group == "machine" or m.startswith(group + "-"))]
        model = default_model if group == "machine" and default_model in model_pairs else members[0]
        st.caption(f"Passages below are from {AI_GROUP_LABELS.get(model, model)}; choose an individual "
                   f"model above to read another.")
    other_name = AI_GROUP_LABELS.get(model, model)
    pairs = model_pairs[model]
    st.caption(BIBER_PASSAGE_NOTE)

    def topic_label(i: int) -> str:
        base = pairs[i]["baseId"]
        topic = TOPIC_LABELS.get(base, base)
        return f"{topic}: {pair_contrast(human_tokens[base], pairs[i]['tokens'], other_name)}"

    n = st.selectbox("Topic", range(len(pairs)), key=f"hape_topic_{model}", format_func=topic_label)
    pair = pairs[n]

    with st.container(border=True):
        theme = st.multiselect(
            "Linguistic Features", list(THEMATIC_GROUPS), key="hape_theme",
            format_func=lambda k: THEMATIC_GROUPS[k]["label"],
            help="Choose one or more feature groups to highlight in both passages.",
        )

    left, right = st.columns(2)
    with left:
        para_card("", display_author(author_a), render_tokens(human_tokens[pair["baseId"]], theme))
    with right:
        para_card("b", other_name, render_tokens(pair["tokens"], theme))

    legend(BIBER_LEGEND)


# ── Sentiment ────────────────────────────────────────────────────────────────
def group_keys(loadings: dict) -> list[str]:
    known = [g for g in AI_GROUP_ORDER if g in loadings]
    return known + [g for g in loadings if g not in AI_GROUP_ORDER]


def group_label(group: str, rates: dict) -> str:
    n = rates.get(group, {}).get("n")
    return AI_GROUP_LABELS.get(group, group) + (f" ({n:,})" if n else "")


def loadings_chart(rows: list[dict], caption: str, max_abs: float | None = None):
    """Diverging bars of log2 ratios. Each row: name, val, color, tip, on (highlighted).
    Pass max_abs to hold the scale fixed across charts."""
    max_abs = max_abs or max([0.01] + [abs(r["val"]) for r in rows])
    out = []
    for r in rows:
        width = abs(r["val"]) / max_abs * 50
        if r["val"] >= 0:
            bar = f'<div class="hape-bar" style="left:50%;width:{width}%;background:{r["color"]}"></div>'
        else:
            bar = f'<div class="hape-bar" style="right:50%;width:{width}%;background:{r["color"]};opacity:0.5"></div>'
        out.append(
            f'<div class="hape-row{" on" if r["on"] else ""}" title="{esc(r["tip"])}">'
            f'<div class="hape-name"><span>{esc(r["name"])}</span><span class="hape-dot" style="background:{r["color"]}"></span></div>'
            f'<div class="hape-track">{bar}</div><div class="hape-val">{r["val"]:+.2f}</div></div>'
        )
    st.markdown(f'<div class="hape-bars"><div class="cap">{caption}</div>{"".join(out)}</div>',
                unsafe_allow_html=True)


def model_picker(loadings: dict, rates: dict, key: str) -> str:
    """AI model: a family row, then (for a family) a row for its individual models."""
    keys = group_keys(loadings)
    families = [g for g in keys if g in AI_FAMILIES or not any(
        g.startswith(f + "-") for f in AI_FAMILIES)]
    family = st.segmented_control(
        "AI model", families, default="machine" if "machine" in keys else keys[0],
        format_func=lambda g: group_label(g, rates), key=f"{key}_family",
    ) or "machine"
    models = [g for g in keys if g.startswith(family + "-")]
    if not models:
        return family
    return st.segmented_control(
        f"{AI_GROUP_LABELS.get(family, family)} models", [family] + models, default=family,
        format_func=lambda g: ("All " if g == family else "") + group_label(g, rates),
        key=f"{key}_model_{family}",
    ) or family


def sentence_html(sent: dict, meta: dict, active: set) -> str:
    fired = sent.get("e", [])
    hot = [e for e in fired if e in active]
    cls = "hape-sent" + (" has" if fired else "")
    style = ""
    if hot:
        color = VALENCE_COLOR[meta.get(hot[0], {}).get("valence", "ambiguous")]
        style = f' style="background:{color}22;border-left-color:{color}"'
    chips = ""
    if fired:
        chips = " " + "".join(
            f'<span class="hape-chip{" dim" if active and e not in active else ""}" '
            f'style="background:{VALENCE_COLOR[meta.get(e, {}).get("valence", "ambiguous")]}">{esc(e)}</span>'
            for e in fired
        )
    return f'<span class="{cls}"{style}>{esc(sent["s"])}{chips}</span>'


def summary_html(s: dict | None) -> str:
    if not s:
        return ""
    return (f'<div class="hape-summary">{s["nEmo"]} of {s["nSent"]} sentences carry emotion: '
            f'{s["nPos"]} positive, {s["nNeg"]} negative.</div>')


def sentiment_tab():
    data = load_json("emotions_paragraphs.json")
    meta, all_loadings, rates = data["emotionMeta"], data["emotionLoadings"], data["emotionRates"]
    pairs = [p for p in data["paragraphs"] if "emotion" in p]  # drop the generic "Pair 1-3" samples
    author_a, author_b = data.get("authorA", "human"), data.get("authorB", "AI")
    scope_label = data.get("scopeLabel", "across all six genres")

    callout("info", SENTIMENT_INTRO)

    group = model_picker(all_loadings, rates, "hape_emo")

    loads = all_loadings.get(group, {})
    entries = sorted(loads.items(), key=lambda kv: abs(kv[1]), reverse=True)[:TOP_N_EMOTIONS]
    active = set(st.multiselect(
        "Highlight emotions in the passages", sorted(meta), key="hape_emotions",
        help="Choose one or more emotions to tint the sentences where they fire.",
    ))

    model_name = AI_GROUP_LABELS.get(group, group)
    caption = (f"Sentence-level GoEmotions firing rate, <strong>{esc(model_name)}</strong> vs. human, "
               f"{esc(scope_label)}. Top {TOP_N_EMOTIONS} emotions by relative difference; bars "
               f'<strong>right</strong> = AI expresses more.')
    human_rates, group_rates = rates.get(author_a, {}).get("rates", {}), rates.get(group, {}).get("rates", {})
    loadings_chart([{
        "name": emo, "val": val, "on": emo in active,
        "color": VALENCE_COLOR[meta.get(emo, {}).get("valence", "ambiguous")],
        "tip": (f"{emo}: human {human_rates.get(emo, 0) * 100:.2f}% of sentences, "
                f"{model_name} {group_rates.get(emo, 0) * 100:.2f}% (log2 ratio {val:.2f})"),
    } for emo, val in entries], caption)

    st.write("")
    def sample_label(i: int) -> str:
        p = pairs[i]
        return (f"{p['emotion'].capitalize()}: AI {p['direction']} than human "
                f"({p['genre']}, {model_name_of(p, author_b)})")

    def highlight_sample_emotion():
        """Selecting a chart sample turns on the highlight for the emotion it illustrates."""
        emo = pairs[st.session_state["hape_sample"]].get("emotion")
        if emo:
            st.session_state["hape_emotions"] = [emo]

    n = st.selectbox("Sample", range(len(pairs)), key="hape_sample", format_func=sample_label,
                     on_change=highlight_sample_emotion,
                     help="Samples named after an emotion illustrate that bar in the chart: "
                          "the pair where the AI text differs most from the human text, in the "
                          "chart's direction.")
    pair = pairs[n]
    ex = pair["examples"][0]

    left, right = st.columns(2)
    with left:
        para_card("", display_author(author_a),
                  "".join(sentence_html(s, meta, active) for s in ex.get("aSentences", [])),
                  summary_html(ex.get("aSummary")))
    with right:
        para_card("b", model_name_of(pair, author_b),
                  "".join(sentence_html(s, meta, active) for s in ex.get("bSentences", [])),
                  summary_html(ex.get("bSummary")))



# ── Page ─────────────────────────────────────────────────────────────────────
st.markdown(page_css(palette()), unsafe_allow_html=True)
banner("Data analysis", "LLM Research <em>Dashboard</em>", PAGE_INTRO)
st.caption(DATA_NOTE)

tab_biber, tab_sentiment = st.tabs(["Biber features", "Sentiment"])
with tab_biber:
    biber_tab()
with tab_sentiment:
    sentiment_tab()
