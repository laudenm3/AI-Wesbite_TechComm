"""HAP-E data analysis: Biber features and sentiment (Streamlit port of
HAP-E_Researcher_website.html). Settings live in content/hape_analysis.py; the data is in
data/*.json."""

import html
import json
import re
from pathlib import Path

import streamlit as st

from content.hape_analysis import (
    AI_FAMILIES, AI_GROUP_LABELS, AI_GROUP_ORDER, AUTHOR_DISPLAY,
    BIBER_LEGEND, DATA_NOTE, PAGE_INTRO, SENTIMENT_INTRO,
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


def render_tokens(tokens: list[dict], group: str | None) -> str:
    """Join tokens into HTML, highlighting tokens that belong to the chosen thematic group."""
    parts = []
    for i, tok in enumerate(tokens):
        body = esc(tok["t"])
        if group and any(FEATURE_TO_THEME.get(f) == group for f in tok.get("f", [])):
            body = f'<span class="hape-hl {group}">{body}</span>'
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


def biber_tab():
    data = load_json("biber_paragraphs.json")
    pairs = data["paragraphsByGenre"]["acad"]  # the Biber view uses academic prose only
    name_a, name_b = display_author(data["authorA"]), display_author(data["authorB"])

    topics = [TOPIC_LABELS[i] if i < len(TOPIC_LABELS) else f"Topic {i + 1}" for i in range(len(pairs))]
    topic = st.selectbox("Topic", topics, key="hape_topic")
    pair = pairs[topics.index(topic)]
    examples = pair["examples"]
    n_ex = 0
    if len(examples) > 1:
        n_ex = st.segmented_control(
            "Example", range(len(examples)), default=0, format_func=lambda i: str(i + 1),
            key=f"hape_example_{topics.index(topic)}",
        ) or 0
    ex = examples[n_ex]

    with st.container(border=True):
        group = st.selectbox(
            "Linguistic Features", [None, *THEMATIC_GROUPS], key="hape_theme",
            format_func=lambda k: "None (no highlighting)" if k is None else THEMATIC_GROUPS[k]["label"],
        )

    left, right = st.columns(2)
    with left:
        para_card("", name_a, render_tokens(ex["aTokens"], group))
    with right:
        para_card("b", name_b, render_tokens(ex["bTokens"], group))

    legend(BIBER_LEGEND)


# ── Sentiment ────────────────────────────────────────────────────────────────
def group_keys(loadings: dict) -> list[str]:
    known = [g for g in AI_GROUP_ORDER if g in loadings]
    return known + [g for g in loadings if g not in AI_GROUP_ORDER]


def group_label(group: str, rates: dict) -> str:
    n = rates.get(group, {}).get("n")
    return AI_GROUP_LABELS.get(group, group) + (f" ({n:,})" if n else "")


def loadings_chart(entries: list, meta: dict, active: set, caption: str,
                   human_rates: dict, group_rates: dict, group_name: str):
    max_abs = max([0.01] + [abs(v) for _, v in entries])
    rows = []
    for emo, val in entries:
        color = VALENCE_COLOR[meta.get(emo, {}).get("valence", "ambiguous")]
        width = abs(val) / max_abs * 50
        if val >= 0:
            bar = f'<div class="hape-bar" style="left:50%;width:{width}%;background:{color}"></div>'
        else:
            bar = f'<div class="hape-bar" style="right:50%;width:{width}%;background:{color};opacity:0.5"></div>'
        tip = (f"{emo}: human {human_rates.get(emo, 0) * 100:.2f}% of sentences, "
               f"{group_name} {group_rates.get(emo, 0) * 100:.2f}% (log2 ratio {val:.2f})")
        rows.append(
            f'<div class="hape-row{" on" if emo in active else ""}" title="{esc(tip)}">'
            f'<div class="hape-name"><span>{esc(emo)}</span><span class="hape-dot" style="background:{color}"></span></div>'
            f'<div class="hape-track">{bar}</div><div class="hape-val">{val:+.2f}</div></div>'
        )
    st.markdown(f'<div class="hape-bars"><div class="cap">{caption}</div>{"".join(rows)}</div>',
                unsafe_allow_html=True)


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
    pairs = data["paragraphs"]
    author_a, author_b = data.get("authorA", "human"), data.get("authorB", "AI")
    scope_label = data.get("scopeLabel", "across all six genres")

    callout("info", SENTIMENT_INTRO)

    # AI model: a family row, then (for a family) a row for its individual models.
    keys = group_keys(all_loadings)
    families = [g for g in keys if g in AI_FAMILIES or not any(
        g.startswith(f + "-") for f in AI_FAMILIES)]
    family = st.segmented_control(
        "AI model", families, default="machine" if "machine" in keys else keys[0],
        format_func=lambda g: group_label(g, rates), key="hape_family",
    ) or "machine"
    models = [g for g in keys if g.startswith(family + "-")]
    group = family
    if models:
        group = st.segmented_control(
            f"{AI_GROUP_LABELS.get(family, family)} models", [family] + models, default=family,
            format_func=lambda g: ("All " if g == family else "") + group_label(g, rates),
            key=f"hape_model_{family}",
        ) or family

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
    loadings_chart(entries, meta, active, caption,
                   rates.get(author_a, {}).get("rates", {}), rates.get(group, {}).get("rates", {}),
                   model_name)

    st.write("")
    def sample_label(i: int) -> str:
        p = pairs[i]
        if "emotion" not in p:
            return p.get("topic") or f"Pair {i + 1}"
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
