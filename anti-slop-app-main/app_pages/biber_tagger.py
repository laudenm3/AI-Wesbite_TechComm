"""Biber Tagger: paste a text, tag it with PyBiber, and highlight the thematic groups.

Modeled on the DocuScope Tag Explorer (Corpus-site/app.py). The thematic groups come from
content/hape_analysis.py, the same ones used on the HAP-E analysis page. The tagging itself
is in utils/biber_tagger.py.
"""

import hashlib
import html

import streamlit as st

from content.hape_analysis import THEMATIC_GROUPS
from utils.style import banner, callout, palette

MAX_CHARS = 20_000
SPACY_MODEL = "en_core_web_sm"

banner(
    "Data analysis",
    "Biber <em>Tagger</em>",
    "Paste a text to see where its Biber features fall, grouped by theme.",
)


@st.cache_resource(show_spinner="Loading the language model (first run only)...")
def load_model():
    import spacy

    return spacy.load(SPACY_MODEL)


def esc(text: str) -> str:
    """Escape for raw HTML inside st.markdown, which would otherwise read $ as math and
    * _ ` as markdown."""
    out = html.escape(text)
    for ch in "$*_`~":
        out = out.replace(ch, f"&#{ord(ch)};")
    return out


def feature_label(feature: str) -> str:
    """'f_14_nominalizations' -> 'nominalizations'."""
    return feature.split("_", 2)[2].replace("_", " ")


FEATURE_TO_GROUP = {f: key for key, g in THEMATIC_GROUPS.items() for f in g["features"]}


def tag_pasted_text(text: str):
    """Tag the text and keep the result in this browser session only.

    Deliberately not st.cache_data: that cache is process-wide and outlives the session, which
    would keep pasted text in server memory after the tab is gone."""
    from utils.biber_tagger import tag_text

    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if st.session_state.get("_biber_key") != key:
        nlp = load_model()
        with st.spinner("Tagging the text..."):
            tokens, words = tag_text(text, nlp)
        st.session_state["_biber_key"] = key
        st.session_state["_biber_result"] = (tokens, words)
    return st.session_state["_biber_result"]


def render_html(tokens: list[dict], selected: set[str]) -> str:
    parts = []
    for tok in tokens:
        parts.append(esc(tok["gap"]))
        body = esc(tok["t"])
        hit = next((f for f in tok["f"] if FEATURE_TO_GROUP.get(f) in selected), None)
        if hit:
            group = THEMATIC_GROUPS[FEATURE_TO_GROUP[hit]]
            names = ", ".join(feature_label(f) for f in tok["f"] if FEATURE_TO_GROUP.get(f) in selected)
            body = (f'<mark title="{esc(group["label"])}: {esc(names)}" style="background:{group["color"]}40;'
                    f'color:inherit;border-bottom:2px solid {group["color"]};border-radius:3px;'
                    f'padding:0 1px;">{body}</mark>')
        parts.append(body)
    return "".join(parts)


with st.form("biber_form", border=False):
    text = st.text_area(
        "Text to tag", height=220, key="biber_text",
        placeholder="Paste or type your text here, then press Ctrl+Enter (⌘+Enter on a Mac).",
    )
    st.form_submit_button("Tag text", type="primary")
st.caption(
    "Your text is processed in memory for this browser session only. It is never written to "
    "disk, and it is discarded when you refresh or close this tab."
)

if not text.strip():
    st.session_state.pop("_biber_key", None)
    st.session_state.pop("_biber_result", None)
elif len(text) > MAX_CHARS:
    callout("wrong", f"That text is {len(text):,} characters long. Please keep it under {MAX_CHARS:,}.")
else:
    try:
        tokens, words = tag_pasted_text(text)
    except OSError:
        callout("wrong", f"**The language model is missing.** This page needs the spaCy model "
                         f"`{SPACY_MODEL}`; see requirements.txt.")
        st.stop()

    group_keys = list(THEMATIC_GROUPS)
    st.write("**Linguistic Features** (click to highlight):")
    selected = set(st.pills(
        "Linguistic Features", group_keys, selection_mode="multi", default=group_keys,
        format_func=lambda k: THEMATIC_GROUPS[k]["label"],
        label_visibility="collapsed", key="biber_groups",
    ) or [])

    counts = {key: 0 for key in group_keys}
    by_feature: dict[str, int] = {}
    for tok in tokens:
        for key in {FEATURE_TO_GROUP[f] for f in tok["f"] if f in FEATURE_TO_GROUP}:
            counts[key] += 1
        for f in tok["f"]:
            if f in FEATURE_TO_GROUP:
                by_feature[f] = by_feature.get(f, 0) + 1

    p = palette()
    cols = st.columns(len(group_keys))
    for col, key in zip(cols, group_keys):
        group = THEMATIC_GROUPS[key]
        per100 = counts[key] / words * 100 if words else 0
        col.markdown(
            f'<div style="border-left:4px solid {group["color"]};padding:2px 10px;color:{p["TEXT"]}">'
            f'<div style="font-size:0.8rem;color:{p["MUTED"]}">{esc(group["label"])}</div>'
            f'<div style="font-size:1.4rem;font-weight:600">{counts[key]}</div>'
            f'<div style="font-size:0.8rem;color:{p["MUTED"]}">{per100:.1f} per 100 words</div></div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown(
        f'<div style="white-space:pre-wrap;line-height:1.8;color:{p["TEXT"]}">'
        f"{render_html(tokens, selected)}</div>",
        unsafe_allow_html=True,
    )

