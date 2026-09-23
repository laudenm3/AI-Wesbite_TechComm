import streamlit as st

from common.ui import render_sidebar

st.set_page_config(
    page_title="Writing Against AI Slop — Calvin Pollak",
    page_icon="📝",
    layout="wide",
)

render_sidebar()

st.title("📝 Writing Against AI Slop")
st.caption("Practice exercises and course activities for Technical and Professional Communication")

st.markdown(
    """
Hi, I'm Calvin Pollak, an [Assistant Teaching Professor of Technical and Professional Communication
at the University of Washington](https://english.washington.edu/people/calvin-pollak). This site draws
from recent research on the peculiar language style of AI-generated text (Markey et al., 2024;
Reinhart et al., 2025) — I call this language style "AI slop." It includes practice exercises and
in-class activities organized to follow the course itself: the assigned readings come first, then one
activity page for each of the three major projects.

The materials give you practice recognizing AI slop language features, and writing and editing in ways
that make your language sound more human — particularly in cover letters, instruction manuals, and
proposals. Whenever AI is used in an exercise below, you have the option to refuse it: a
previously-generated example is always provided to analyze instead of generating your own.

*This app replaces the standalone HTML exercise pages with one Streamlit site: fill in the text boxes
as you work through each page, and use the "Download my workbook" button in the sidebar at any time to
save everything you've written so far as a single Word document.*
"""
)

st.divider()

st.markdown("### Start Here · The Readings")
st.caption(
    "All of the exercises here are based on two corpus linguistics studies (cited at the bottom of "
    "this page). Read the articles first, then check your understanding."
)
st.page_link("pages/1_📖_Reading_Check.py", label="**Reading Check** — Quiz & discussion prompts", icon="📖")

st.divider()

st.markdown("### Course Units · In-Class Activities")
st.caption(
    "One activity page per major project. On each, you generate a text with an LLM (or analyze a "
    "previously-generated example), investigate its style, draft your own version, and edit it closely."
)
st.page_link("pages/2_✉️_Unit_1_Cover_Letters.py", label="**Unit 1 — Anti-Slop Cover Letters**", icon="✉️")
st.page_link("pages/3_🛠️_Unit_2_Instructions.py", label="**Unit 2 — More Human Instructions**", icon="🛠️")
st.page_link("pages/4_📋_Unit_3_Proposals.py", label="**Unit 3 — Proposals for De-Slop-ification**", icon="📋")

st.divider()

st.markdown("### Practice Anytime · Exercises & Coach")
st.caption("Sentence- and paragraph-level practice — assign these before or alongside the unit activities.")
st.page_link(
    "pages/5_🎯_Exercise_Set_1_Style_Comparison.py",
    label="**Exercise Set 1 — AI Slop Style vs. a More Human Style**",
    icon="🎯",
)
st.page_link(
    "pages/6_📝_Exercise_Set_2_Genre_Exercises.py",
    label="**Exercise Set 2 — Writing in a More Human Style: Genre Exercises**",
    icon="📝",
)
st.link_button(
    "🤖 AI Style Coach (interactive, requires a free Claude.ai account)",
    "https://claude.ai/public/artifacts/9cb59e90-6438-4ba4-bb86-06147f5811e6",
    use_container_width=True,
)

with open("assets/slides.pdf", "rb") as f:
    st.download_button(
        "⬇️ Slides (PDF) — Less \"Slop\", More Human, IEEE ProComm 2026",
        data=f.read(),
        file_name="Pollak_ProComm2026_slides.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

st.divider()

st.markdown("### Research Background")
st.markdown(
    """
The style contrast underlying these materials is drawn from two corpus linguistics studies.
[Markey et al. (2024)](https://journals.sagepub.com/doi/abs/10.1177/07410883241263528) found that
ChatGPT-generated text is significantly more informationally dense than even professional academic
writing; it relies heavily on nominalizations and noun phrases, and is low on the hedges, modals of
possibility, and co-ordinating conjunctions that keep human prose open and dialogic. They also found it
struggles to generate the kind of pedestrian, concrete examples that help clarify abstract concepts.
[Reinhart et al. (2025)](https://www.pnas.org/doi/abs/10.1073/pnas.2422455122) extended this analysis to
multiple LLMs and found that instruction-tuned models use present participial clauses at 2–5x the human
rate and nominalizations at roughly 1.5–2x the human rate. Some patterns turned out to be
model-specific: GPT-4o models avoid clausal co-ordination (favoring noun-to-noun phrasal co-ordination
instead), while Llama 3 variants use clausal co-ordination more than humans do. Base models wrote much
closer to human norms, suggesting instruction tuning introduces the style.

> Markey, B., Brown, D. W., Laudenbach, M., & Kohler, A. (2024). Dense and disconnected: Analyzing the
> sedimented style of ChatGPT-generated text at scale. *Written Communication, 41*(4), 571–600.
>
> Reinhart, A., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., Weinberg, G., & Brown, D. W. (2025).
> Do LLMs write like humans? Variation in grammatical and rhetorical styles. *Proceedings of the
> National Academy of Sciences, 122*(8), e2422455122.
>
> On students' right to refuse generative AI: Sano-Franchini, J., McIntyre, M., & Fernandes, M.
> [Refusing GenAI in Writing Studies: A Quickstart Guide](https://refusal.blog/).
"""
)

st.divider()
st.caption(
    "Calvin Pollak · University of Washington · These materials may be freely used and adapted for "
    "educational purposes. Please cite: Pollak, 2026. Writing Against AI Slop: Practice exercises for "
    "Technical and Professional Communication."
)
