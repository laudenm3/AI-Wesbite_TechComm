"""Builds the single downloadable .docx workbook from whatever the student
has typed into any page's fields, pulled straight out of st.session_state.

Because this is a native Streamlit multipage app, st.session_state persists
across pages for the length of a browser session, so the sidebar's "Download
my workbook" button (see common/ui.py) can bundle every page's answers no
matter which page the student is currently on.
"""

import io
from datetime import datetime

from docx import Document
from docx.shared import Pt

from metadata import (
    reading_check,
    unit1_cover_letters,
    unit2_instructions,
    unit3_proposals,
    exercise_set1_style_comparison,
    exercise_set2_genre_exercises,
)

# Order here is the order pages appear in the sidebar / the order sections
# appear in the exported workbook.
ALL_PAGES = [
    reading_check,
    unit1_cover_letters,
    unit2_instructions,
    unit3_proposals,
    exercise_set1_style_comparison,
    exercise_set2_genre_exercises,
]

# Step types whose contents are student-written free text that belongs in
# the exported workbook.
_EXPORTABLE_TYPES = {"fields", "transform"}


def field_key(page_key: str, field_id: str) -> str:
    """The st.session_state / widget key for a given page's field."""
    return f"{page_key}__{field_id}"


def page_progress(cfg) -> tuple[int, int]:
    """(answered, total) count of exportable fields filled in on one page."""
    total = 0
    answered = 0
    for step in cfg.STEPS:
        if step["type"] == "fields":
            for item in step["items"]:
                total += 1
                if _session_value(cfg.PAGE_METADATA["key"], item["id"]):
                    answered += 1
        elif step["type"] == "transform":
            total += 1
            if _session_value(cfg.PAGE_METADATA["key"], step["id"]):
                answered += 1
    return answered, total


def _session_value(page_key: str, field_id: str) -> str:
    import streamlit as st

    return (st.session_state.get(field_key(page_key, field_id), "") or "").strip()


def build_workbook(student_name: str = "") -> bytes:
    """Assemble every page's captured fields into one .docx, returned as bytes."""
    doc = Document()

    title = doc.add_heading("Writing Against AI Slop — Exercise Responses", level=0)
    title.runs[0].font.size = Pt(22)

    meta = doc.add_paragraph()
    meta.add_run(f"Student: {student_name.strip() or '(name not entered)'}\n").bold = True
    meta.add_run(f"Downloaded: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    any_content = False

    for cfg in ALL_PAGES:
        page_key = cfg.PAGE_METADATA["key"]
        section_parts = []

        for step in cfg.STEPS:
            if step["type"] not in _EXPORTABLE_TYPES:
                continue

            if step["type"] == "fields":
                for item in step["items"]:
                    value = _session_value(page_key, item["id"])
                    section_parts.append((item["label"], value))
            elif step["type"] == "transform":
                value = _session_value(page_key, step["id"])
                section_parts.append((step["name"], value))

        if not section_parts:
            continue

        doc.add_page_break()
        heading = cfg.PAGE_METADATA.get("unit_label") or cfg.PAGE_METADATA["title"]
        doc.add_heading(f"{cfg.PAGE_METADATA['title']}", level=1)
        if cfg.PAGE_METADATA.get("unit_label"):
            doc.add_paragraph().add_run(heading).italic = True

        for label, value in section_parts:
            doc.add_heading(label, level=2)
            doc.add_paragraph(value if value else "(No response provided.)")
            any_content = True

    if not any_content:
        doc.add_paragraph(
            "No exercise fields have been filled in yet. Complete some steps "
            "on the exercise pages, then download again."
        )

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()
