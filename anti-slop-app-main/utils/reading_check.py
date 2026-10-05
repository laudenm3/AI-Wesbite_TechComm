"""Renders one reading check page from a spec in content/reading_check.py.

Both checks work the same way, so they share this function rather than two copies of the
page that would drift apart. Everything that differs between them (title, intro, citation,
questions, prompts, file name, and the session_state prefix) comes from the spec.

The session_state prefix matters. Both pages exist in the same browser session, so a
student who does check 1 and then check 2 would carry their first quiz's answers into the
second if the keys were shared.
"""

import streamlit as st

from utils.downloads import PAGE_NOTE, build_docx, save_section
from utils.exercise import answer_lines
from utils.style import banner, callout, label

LETTERS = ["a", "b", "c", "d"]


def render(spec: dict):
    key = spec["key"]
    questions = spec["questions"]
    prompts = spec["prompts"]
    n = len(questions)

    banner(spec["kicker"], spec["title"], spec["sub"])

    with st.container(border=True):
        st.write(spec["intro"])
        for citation in spec["citations"]:
            st.caption(citation)
    callout("info", PAGE_NOTE)

    # ── Part A: quiz ─────────────────────────────────────────────────────────
    st.header("Part A · Comprehension questions")
    st.caption(
        "Choose one answer per question. You'll get immediate feedback with a pointer back "
        "to the relevant part of the reading. Your first answer counts; use the retry button "
        "at the bottom to start over."
    )

    # A student's first answer is stored and locked, so the feedback cannot be used to
    # improve the score after the fact.
    answers_key = f"{key}_answers"
    round_key = f"{key}_round"
    if answers_key not in st.session_state:
        st.session_state[answers_key] = {}
    if round_key not in st.session_state:
        st.session_state[round_key] = 0  # bumped on retry so the radios start fresh
    answers = st.session_state[answers_key]

    def lock_answer(i):
        val = st.session_state.get(f"{key}_q{i}_{st.session_state[round_key]}")
        if val is not None and i not in answers:
            answers[i] = val

    def reset_quiz():
        st.session_state[answers_key] = {}
        st.session_state[round_key] += 1

    score = 0
    for i, item in enumerate(questions):
        with st.container(border=True):
            label(f"Question {i + 1} of {n}")
            if i not in answers:
                st.radio(
                    item["q"],
                    options=list(range(len(item["opts"]))),
                    format_func=lambda j, item=item: f"({LETTERS[j]}) {item['opts'][j]}",
                    index=None,
                    key=f"{key}_q{i}_{st.session_state[round_key]}",
                    on_change=lock_answer,
                    args=(i,),
                )
            else:
                # Answered: show the options as a static list with the result marked.
                choice = answers[i]
                st.markdown(item["q"])
                labeled = [f"({LETTERS[j]}) {opt}" for j, opt in enumerate(item["opts"])]
                st.markdown(answer_lines(labeled, item["a"], choice), unsafe_allow_html=True)
                if choice == item["a"]:
                    score += 1
                    callout("correct", "That is the right answer.", title="Correct",
                            announce=True)
                else:
                    callout("wrong", f"You chose ({LETTERS[choice]}).", title="Not quite",
                            announce=True)
                callout("info", item["fb"], title="Why")

    answered_count = len(answers)
    st.progress(answered_count / n, text=f"Answered {answered_count} of {n}")
    col1, col2 = st.columns([3, 1])
    col1.metric("Your score", f"{score} / {n}")
    col2.button("Retry quiz", key=f"{key}_retry", on_click=reset_quiz,
                use_container_width=True)

    # ── Part B: discussion ───────────────────────────────────────────────────
    st.header("Part B · Discussion prompts")
    st.caption("We'll take these up in class. Jot notes for at least two of them.")

    for i, prompt in enumerate(prompts):
        with st.container(border=True):
            label(f"Prompt {i + 1}")
            st.markdown(prompt)
            st.text_area("Your notes", key=f"{key}_note{i}", label_visibility="collapsed",
                         placeholder="Your notes…")

    # ── Download ─────────────────────────────────────────────────────────────
    def build(name):
        sections = [("Quiz score", f"{score} / {n} ({answered_count} of {n} answered)")]
        for i, prompt in enumerate(prompts):
            plain = prompt.replace("*", "")
            sections.append((f"Prompt {i + 1}: {plain}",
                             st.session_state.get(f"{key}_note{i}", "")))
        return build_docx(spec["doc_title"], name, sections)

    save_section(
        key_prefix=key,
        name_label="Your name (appears on the downloaded file)",
        field_keys=[f"{key}_note{i}" for i in range(len(prompts))],
        build=build,
        file_name=spec["file_name"],
        extra_note="Your quiz score goes into the file as well.",
    )

    st.divider()
    st.caption(
        "Part of Writing Against AI Slop · Calvin Pollak · University of Washington. "
        "Quiz content paraphrases findings from the cited study for educational purposes."
    )
