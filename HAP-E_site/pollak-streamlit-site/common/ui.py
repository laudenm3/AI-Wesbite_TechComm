"""Shared SideDesk-style chrome and step renderer.

Every exercise page is data (a metadata/*.py module with a PAGE_METADATA
dict and a STEPS list) plus a single call to render_page(cfg). This mirrors
the metadata-driven design of llm-chatbot/main.py: pages are configuration,
not code, and the sidebar/export behavior lives in one shared place.
"""

import streamlit as st

from common.export import build_workbook, field_key, page_progress


# --- SIDEBAR ("SideDesk") ---------------------------------------------------

def render_sidebar(cfg=None):
    with st.sidebar:
        st.title("📝 SideDesk")
        st.caption("Writing Against AI Slop — Practice Exercises")

        st.text_input(
            "Your name (for your downloaded workbook)",
            key="student_name",
            placeholder="e.g. Jordan Reyes",
        )

        if cfg is not None:
            st.divider()
            answered, total = page_progress(cfg)
            if total:
                st.progress(
                    answered / total,
                    text=f"This page: {answered}/{total} exercise fields answered",
                )

        st.divider()
        st.subheader("📥 Export your work")
        st.caption(
            "Bundles every exercise field you've filled in, on every page, "
            "into one Word document."
        )
        st.download_button(
            "⬇️ Download my workbook (.docx)",
            data=build_workbook(st.session_state.get("student_name", "")),
            file_name="ai_slop_exercise_responses.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

        if cfg is not None:
            st.divider()
            if st.button("🔄 Clear my answers on this page", use_container_width=True):
                _clear_page_fields(cfg)
                st.rerun()


def _clear_page_fields(cfg):
    page_key = cfg.PAGE_METADATA["key"]
    for step in cfg.STEPS:
        if step["type"] == "fields":
            for item in step["items"]:
                st.session_state.pop(field_key(page_key, item["id"]), None)
        elif step["type"] == "transform":
            st.session_state.pop(field_key(page_key, step["id"]), None)


# --- PAGE ENTRYPOINT ---------------------------------------------------------

def render_page(cfg):
    st.set_page_config(
        page_title=cfg.PAGE_METADATA["title"],
        page_icon=cfg.PAGE_METADATA.get("icon", "📝"),
        layout="wide",
    )
    render_sidebar(cfg)

    st.title(f"{cfg.PAGE_METADATA.get('icon', '')} {cfg.PAGE_METADATA['title']}")
    if cfg.PAGE_METADATA.get("unit_label"):
        st.caption(cfg.PAGE_METADATA["unit_label"])
    if cfg.PAGE_METADATA.get("overview"):
        st.markdown(cfg.PAGE_METADATA["overview"])
    st.divider()

    page_key = cfg.PAGE_METADATA["key"]
    for i, step in enumerate(cfg.STEPS):
        _STEP_RENDERERS[step["type"]](page_key, step, i)


# --- STEP RENDERERS ----------------------------------------------------------

def _render_static(page_key, step, i):
    st.markdown(step["content"])


def _render_sample(page_key, step, i):
    with st.expander(step["title"], expanded=step.get("expanded", False)):
        st.markdown(step["content"])


def _render_fields(page_key, step, i):
    st.markdown(f"### {step['name']}")
    if step.get("intro"):
        st.markdown(step["intro"])
    for item in step["items"]:
        st.markdown(f"**{item['label']}**")
        if item.get("prompt"):
            st.caption(item["prompt"])
        st.text_area(
            item["label"],
            key=field_key(page_key, item["id"]),
            placeholder=item.get("placeholder", ""),
            height=item.get("height", 100),
            label_visibility="collapsed",
        )
    st.markdown("")


def _render_checklist(page_key, step, i):
    st.markdown(f"### {step['name']}")
    if step.get("intro"):
        st.markdown(step["intro"])
    checked = 0
    for item in step["items"]:
        is_checked = st.checkbox(item["label"], key=field_key(page_key, item["id"]))
        if item.get("detail"):
            st.caption(item["detail"])
        if is_checked:
            checked += 1
    st.caption(f"{checked}/{len(step['items'])} checked off")


def _render_quiz(page_key, step, i):
    st.markdown(f"### {step['name']}")
    if step.get("intro"):
        st.markdown(step["intro"])
    questions = step["questions"]
    correct_count = 0
    answered_count = 0
    for qi, q in enumerate(questions):
        st.markdown(f"**{qi + 1}. {q['question']}**")
        choice = st.radio(
            f"quiz-{i}-{qi}",
            q["options"],
            key=field_key(page_key, f"quiz{i}_{qi}"),
            index=None,
            label_visibility="collapsed",
        )
        if choice is not None:
            answered_count += 1
            if q["options"].index(choice) == q["answer"]:
                st.success(f"Correct. {q.get('feedback', '')}")
                correct_count += 1
            else:
                st.error(f"Not quite. {q.get('feedback', '')}")
        st.markdown("")
    if answered_count:
        st.caption(f"Score so far: {correct_count} / {answered_count} answered")


def _render_transform(page_key, step, i):
    st.markdown(f"#### {step['name']}")
    st.markdown(step["question"])
    if step.get("passage"):
        st.markdown(f"> {step['passage']}")
    if step.get("tip"):
        st.info(f"💡 Tip: {step['tip']}")
    st.text_area(
        step["name"],
        key=field_key(page_key, step["id"]),
        placeholder=step.get("placeholder", "Type your rewritten version here…"),
        height=step.get("height", 100),
        label_visibility="collapsed",
    )
    if step.get("model_answer"):
        with st.expander("Show a model answer (try it yourself first!)"):
            st.markdown(step["model_answer"])
    st.markdown("")


def _render_choice(page_key, step, i):
    if step.get("name"):
        st.markdown(f"#### {step['name']}")
    st.markdown(step["question"])
    choice = st.radio(
        f"choice-{i}",
        step["options"],
        key=field_key(page_key, step["id"]),
        index=None,
        label_visibility="collapsed",
    )
    if choice is not None:
        if step["options"].index(choice) == step["answer"]:
            st.success(f"Correct. {step.get('explanation', '')}")
        else:
            st.error(f"Not quite. {step.get('explanation', '')}")
    st.markdown("")


def _render_rank(page_key, step, i):
    st.markdown(f"#### {step['name']}")
    st.markdown(step["question"])
    versions = step["versions"]
    cols = st.columns(len(versions))
    ranks = {}
    for vi, version in enumerate(versions):
        with cols[vi]:
            st.markdown(f"**{version['label']}**")
            st.caption(version["text"])
            ranks[vi] = st.selectbox(
                f"rank-{i}-{vi}",
                options=[1, 2, 3],
                key=field_key(page_key, f"{step['id']}_rank{vi}"),
                label_visibility="collapsed",
            )
    if st.button("Check my ranking", key=field_key(page_key, f"{step['id']}_check")):
        assigned_order = sorted(range(len(versions)), key=lambda vi: ranks[vi])
        if assigned_order == step["correct_order"]:
            st.success("Correct ranking!")
        else:
            st.error("Not quite yet — here's how to think about it:")
        st.markdown(step.get("explanation", ""))
    st.markdown("")


_STEP_RENDERERS = {
    "static": _render_static,
    "sample": _render_sample,
    "fields": _render_fields,
    "checklist": _render_checklist,
    "quiz": _render_quiz,
    "transform": _render_transform,
    "choice": _render_choice,
    "rank": _render_rank,
}
