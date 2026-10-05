import streamlit as st

from utils.style import callout


def coming_soon(title: str):
    """Placeholder for pages we haven't ported yet."""
    st.title(title)
    callout(
        "info",
        "This page hasn't been moved into the app yet. "
        "For now, please use the version on the course website.",
    )
    st.link_button("Open the course website", "https://cpollak-uw.github.io/ai-style-exercises/")
