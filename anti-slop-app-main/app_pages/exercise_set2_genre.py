import streamlit as st

from content.genre_exercises import CITATIONS, GENRES, INTRO
from utils.downloads import PAGE_NOTE, build_docx, save_section
from utils.exercise import locked_choice, model_answer, passage, response_box
from utils.style import banner, callout, label

banner(
    "Exercise Set 2",
    "Writing in a More Human Style",
    "Genre-specific exercises for developing a verbal, hedged, clausal prose style",
)
st.caption(INTRO)
with st.expander("Sources for this exercise set"):
    for c in CITATIONS:
        st.caption(c)
callout("info", PAGE_NOTE)


def rank_exercise(key, ex):
    """Students assign each position a version; checked against ex['ranking']."""
    store = st.session_state.setdefault("rank_checked", {})
    for opt in ex["options"]:
        st.markdown(f"**{opt['label']}.** *{opt['text']}*")
    st.caption("Order the versions from weakest to strongest.")
    labels = [o["label"] for o in ex["options"]]
    positions = ["1 · Weakest", "2 · Middle", "3 · Strongest"]
    cols = st.columns(3)
    picks = [cols[p].selectbox(positions[p], labels, index=None, key=f"{key}_pos{p}",
                               placeholder="Choose…", disabled=key in store)
             for p in range(3)]
    if key not in store:
        ready = all(picks) and len(set(picks)) == 3
        if st.button("Check my ranking", key=f"{key}_check", disabled=not ready):
            store[key] = picks
            st.rerun()
        if all(picks) and not ready:
            callout("note", "Use each version once.")
        return
    picks = store[key]
    if picks == ex["ranking"]:
        callout("correct", "Perfect ranking.", title="Correct", announce=True)
    else:
        callout("wrong", "Here is the intended ranking; see the explanation below.", title="Not quite", announce=True)
    st.markdown("  \n".join(f"**{lbl}:** {v}" for lbl, v in zip(ex["rankLabels"], ex["ranking"])))
    callout("info", ex["explanation"], title="Why")


tabs = st.tabs([g["label"] for g in GENRES])
for g, tab in zip(GENRES, tabs):
    with tab:
        with st.expander(f"Genre notes: {g['note']['heading']}", icon=":material/info:"):
            st.write(g["note"]["body"])
            for b in g["note"]["bullets"]:
                st.markdown(f"**{b['label']}.** {b['text']}")

        for i, ex in enumerate(g["exercises"]):
            key = f"s2_{g['id']}_{i}"
            with st.container(border=True):
                label(f"Exercise {i + 1} · {ex['tag']}")
                st.markdown(f"**{ex['question']}**")
                if ex["type"] == "choose":
                    opts = [f"{o['label']}: {o['text']}" for o in ex["options"]]
                    locked_choice(key, "", opts, ex["answer"], ex["explanation"])
                elif ex["type"] == "transform":
                    passage(ex["passage"])
                    st.caption(f"💡 Hint: {ex['tip']}")
                    response_box(f"{key}_resp")
                    model_answer(ex["model"])
                elif ex["type"] == "spotfix":
                    hl = st.toggle("Highlight AI slop style features", key=f"{key}_hl")
                    passage(ex["passage"], ex["features"] if hl else None)
                    st.caption(f"💡 Hint: {ex['tip']}")
                    response_box(f"{key}_resp")
                    model_answer(ex["model"])
                elif ex["type"] == "rank":
                    rank_exercise(key, ex)

WRITING_KEYS = [f"s2_{g['id']}_{i}_resp"
                for g in GENRES
                for i, ex in enumerate(g["exercises"])
                if ex["type"] in ("transform", "spotfix")]


def build(name):
    sections = []
    for g in GENRES:
        for i, ex in enumerate(g["exercises"]):
            if ex["type"] in ("transform", "spotfix"):
                resp = st.session_state.get(f"s2_{g['id']}_{i}_resp", "") or "(no response)"
                sections.append((f"{g['label']}, Exercise {i + 1}: {ex['question']}",
                                 f"Original: {ex['passage']}\n\nMy version: {resp}"))
    return build_docx("Exercise Set 2: Writing in a More Human Style", name, sections)


save_section(
    key_prefix="s2",
    name_label="Your name (appears on the downloaded file)",
    field_keys=WRITING_KEYS,
    build=build,
    file_name="ExerciseSet2_responses.docx",
    extra_note="The counter covers the writing boxes in all three genre tabs, not only the "
               "tab you have open.",
)
