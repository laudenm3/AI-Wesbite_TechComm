# Generic embeddable text field. Meant to be loaded in an <iframe> once per
# text entry on a static exercise page, styled to blend into that page.
#
# Two modes, chosen by query params:
#   ?field=<id>&label=<text>&placeholder=<text>&height=<px>
#       Renders a single text box and broadcasts its value to the parent
#       window (window.parent.parent, since this app itself is one level
#       inside the st.iframe sub-frame) via postMessage on every change,
#       so the host page can collect answers from many such iframes.
#   ?combine=1&data=<json>
#       Receives the collected answers (a JSON array of {label, value}) from
#       the host page's "Save all answers" button and bundles them into one
#       downloadable .docx via python-docx.

import io
import json

import streamlit as st
from docx import Document

st.set_page_config(page_title="Exercise Field", layout="centered")

# Hide Streamlit's chrome and let the field's own background/border (set
# below) be the only visible thing, so it blends into the host page.
st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    html, body, .stApp { background: transparent !important; }
    .block-container { padding: 0 !important; }
    textarea {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.89rem !important;
        line-height: 1.65 !important;
        border: 1.5px solid #d8cfc0 !important;
        border-radius: 3px !important;
        background: #faf8f4 !important;
        color: #1c1c2e !important;
    }
    textarea:focus { border-color: #c4a882 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

params = st.query_params

if params.get("combine") == "1":
    raw = params.get("data", "")
    try:
        entries = json.loads(raw) if raw else []
    except json.JSONDecodeError:
        entries = []

    st.subheader("Combined answers")
    if not entries:
        st.warning('No answers were received. Go back and click "Save all answers" again.')
    else:
        doc = Document()
        doc.add_heading("Exercise Responses", level=1)
        for entry in entries:
            label = entry.get("label") or "Untitled"
            value = (entry.get("value") or "").strip()
            doc.add_heading(label, level=2)
            doc.add_paragraph(value or "(No response provided.)")
        buffer = io.BytesIO()
        doc.save(buffer)

        st.success(f"Combined {len(entries)} answer(s). Click below to download.")
        st.download_button(
            label="⬇️ Download combined answers (.docx)",
            data=buffer.getvalue(),
            file_name="exercise_responses.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

else:
    field_id = params.get("field")
    label = params.get("label", field_id or "Your answer")
    placeholder = params.get("placeholder", "")
    height = int(params.get("height", "100"))

    if not field_id:
        st.info("This app is meant to be embedded with a `field` query parameter.")
    else:
        value = st.text_area(
            label,
            key=f"answer_{field_id}",
            placeholder=placeholder,
            height=height,
            label_visibility="collapsed",
        )

        payload = {"type": "fieldSync", "field": field_id, "label": label, "value": value}
        st.iframe(
            f"<script>window.parent.parent.postMessage({json.dumps(payload)}, '*');</script>",
            height=0,
        )
