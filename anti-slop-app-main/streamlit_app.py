"""Writing Against AI Slop: classroom version (Streamlit).

This is the file Streamlit runs. It sets up the page list and the sidebar
navigation. Each page's content lives in the app_pages/ folder.
"""

from pathlib import Path

import streamlit as st

from utils.a11y import patch_streamlit_a11y
from utils.style import callout, inject_css

# The Streamlit version this app was last tested against. utils/a11y.py depends on
# Streamlit's own markup, so a newer version should be tried on purpose, not by
# surprise. requirements.txt pins the same number.
TESTED_STREAMLIT = "1.64.0"

st.set_page_config(
    page_title="Writing Against AI Slop",
    page_icon="✎",
    layout="centered",
)
inject_css()

# ?check=1 turns on the instructor health check (see the README).
HEALTH_CHECK = st.query_params.get("check") == "1"
patch_streamlit_a11y(show_status=HEALTH_CHECK)

# Health check, shown only with ?check=1 on the end of the address.
if HEALTH_CHECK:
    running = st.__version__
    if running == TESTED_STREAMLIT:
        callout("correct", f"**Version check: fine.** Streamlit {running}, which is the "
                           f"version this app was tested against.")
    else:
        callout("wrong", f"**Version check: Streamlit has changed.** This app is running "
                         f"Streamlit {running} but was tested against {TESTED_STREAMLIT}. "
                         f"Read the accessibility check below, then see 'Keeping the app "
                         f"healthy' in the README.")

# Setup check: look for the settings file itself, next to this script. Checking the
# theme values instead gave a false alarm on Streamlit Community Cloud, which supplies
# its own theme defaults.
if not (Path(__file__).parent / ".streamlit" / "config.toml").is_file():
    callout(
        "note",
        "Setup note for the instructor: the color and font settings file "
        "(.streamlit/config.toml) is missing. The app still looks right, because its colors "
        "are also set in utils/style.py, but see step 4 in the README to add the file back.",
    )


pages = {
    "": [
        st.Page("app_pages/home.py", title="Home", icon=":material/home:", default=True),
    ],
    "Start here": [
        st.Page("app_pages/reading_check_deluca.py", title="Reading Check 1: DeLuca", icon=":material/menu_book:"),
        st.Page("app_pages/reading_check_reinhart.py", title="Reading Check 2: Reinhart", icon=":material/menu_book:"),
    ],
    "Course units": [
        st.Page("app_pages/unit1_cover_letters.py", title="Unit 1: Cover Letters", icon=":material/mail:"),
        st.Page("app_pages/unit2_instructions.py", title="Unit 2: Instructions", icon=":material/list:"),
        st.Page("app_pages/unit3_proposals.py", title="Unit 3: Proposals", icon=":material/description:"),
    ],
    "Practice anytime": [
        st.Page("app_pages/exercise_set1_style.py", title="Exercise Set 1: Style Comparison", icon=":material/compare:"),
        st.Page("app_pages/exercise_set2_genre.py", title="Exercise Set 2: Genre Exercises", icon=":material/edit_note:"),
    ],
    "Data analysis": [
        st.Page("app_pages/hape_analysis.py", title="HAP-E: Biber & Sentiment", icon=":material/analytics:"),
        st.Page("app_pages/biber_tagger.py", title="Biber Tagger", icon=":material/sell:"),
    ],
}

nav =st.navigation(pages)
nav.run()
