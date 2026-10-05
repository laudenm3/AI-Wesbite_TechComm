import streamlit as st

from utils.style import banner

banner(
    "Teaching Resource",
    "Writing Against<br><em>AI Slop</em>",
    "Practice exercises and course activities for Technical and Professional Communication",
)

st.markdown(
    "I'm Calvin Pollak, an [Assistant Teaching Professor of Technical and Professional "
    "Communication at the University of Washington](https://english.washington.edu/people/calvin-pollak). "
    "In this project, I'm drawing from recent research on the peculiar language style of "
    "AI-generated text ([DeLuca et al., 2025](https://doi.org/10.1080/26939169.2025.2497547); "
    "[Markey et al., 2024](https://journals.sagepub.com/doi/abs/10.1177/07410883241263528); "
    "[Reinhart et al., 2025](https://www.pnas.org/doi/abs/10.1073/pnas.2422455122)). I call this "
    "language style \"AI slop\". When I first read these articles, I immediately wanted to "
    "operationalize their findings about the specific features of slop into teaching resources "
    "for Technical and Professional Communication. This app collects the practice exercises and "
    "in-class activities for my course. It's organized to follow the course itself: the assigned "
    "readings come first, and then there is one activity page for each of the three major projects."
)
st.markdown(
    "The materials are designed to give students practice recognizing AI slop language features, "
    "and writing and editing in ways that make their language sound more human, particularly in "
    "cover letters, instruction manuals, and proposals. Whenever I incorporate AI into the "
    "classroom, I give students options and opportunities to refuse use of the technology; "
    "students who practice refusal are given previously-generated examples to analyze and reflect "
    "upon instead of generating new examples themselves."
)
st.caption(
    "Note: This project is in beta testing, and Autumn 2026 is the first quarter I'm using it in class. "
    "The exercises and research background/summaries included here were developed in a "
    "dialogic, iterative composition process with Claude. All text examples (including \"more "
    "human\" examples) are model-generated with extensive prompt engineering and post-generation "
    "editing by me. The previously-generated \"slop\" examples on the unit pages are the "
    "exception: they're unedited LLM output, and they're labeled as such."
)


def card(page, kicker, title, desc, icon):
    with st.container(border=True):
        st.caption(kicker.upper())
        st.page_link(page, label=f"**{title}**", icon=icon)
        st.write(desc)


st.header("Start here · The readings")
st.caption(
    "All of the exercises and activities here are based on two recent studies of LLM-generated "
    "writing: DeLuca et al. (2025) and Reinhart et al. (2025) (linked above; cited in full at the "
    "bottom of this page). Read the articles first, and then check your understanding in this section."
)
card("app_pages/reading_check_deluca.py", "Reading Check 1",
     "How ChatGPT Writes an Introduction",
     "A self-graded comprehension quiz on DeLuca et al. (2025), with four discussion prompts "
     "for class.", ":material/menu_book:")
card("app_pages/reading_check_reinhart.py", "Reading Check 2",
     "Do LLMs Write Like Humans?",
     "A self-graded comprehension quiz on Reinhart et al. (2025), with two discussion prompts "
     "for class. Do this one after Reading Check 1.", ":material/menu_book:")

st.header("Course units · In-class activities")
st.caption(
    "There is one activity page for each major project. On each page, students generate a text "
    "with an LLM (or analyze a previously-generated example if they prefer not to), investigate "
    "its style, draft their own version, and edit it closely."
)
card("app_pages/unit1_cover_letters.py", "Unit 1 · Job Application Package", "Anti-Slop Cover Letters",
     "Students generate a cover letter from their own resume and a real job ad, investigate its "
     "peculiar style, and then draft their own letters \"inside-out\" from STAR stories.",
     ":material/mail:")
card("app_pages/unit2_instructions.py", "Unit 2 · Instructional Design", "More Human Instructions",
     "In small groups, students use an LLM to generate instructions for a tool they know well, "
     "analyze the output's style, supplementary discussion, and formatting, and then rewrite it "
     "themselves.", ":material/list:")
card("app_pages/unit3_proposals.py", "Unit 3 · Local Change Proposal", "Proposals for De-Slop-ification",
     "Students inspect how a generated proposal overstates and underexplains its case, compose "
     "their own proposals from argument and narrative for a real decisionmaker, and closely edit "
     "their drafts.", ":material/description:")

st.header("Practice anytime · Exercises")
st.caption(
    "These exercises give practice at the sentence and paragraph level, and they can be assigned "
    "before or alongside the unit activities."
)
card("app_pages/exercise_set1_style.py", "Exercise Set 1", "AI Slop Style vs. a More Human Style",
     "Side-by-side paragraph comparisons and identification and transformation exercises across "
     "two writing styles.", ":material/compare:")
card("app_pages/exercise_set2_genre.py", "Exercise Set 2", "Writing in a More Human Style: Genre Exercises",
     "Genre-specific exercises in cover letters, instructional documents, and proposals, with "
     "model answers.", ":material/edit_note:")

st.header("Research background")
with st.expander("Read the research summary and full citations"):
    st.markdown(
        "The style contrast underlying these materials is drawn from two recent corpus-based "
        "studies. [DeLuca et al. (2025)](https://doi.org/10.1080/26939169.2025.2497547) compared "
        "report introductions written by ChatGPT, by undergraduate students, and by published "
        "researchers, and the machine-generated writing separated cleanly from both human groups. "
        "It was far more informationally dense than the student writing, it compressed information "
        "into noun phrases whose content could stay vague, and it barely modulated its confidence: "
        "ChatGPT used the predictive modal \"will\" 199 times while \"may,\" \"might,\" and "
        "\"could\" did not appear at all. None of its introductions included numeric values, and "
        "its claims of importance rested on unmeasurable attributes where expert writers assign "
        "measurable ones. The authors place ChatGPT’s style somewhere in between novices and "
        "experts, not exactly mimicking either. "
        "[Reinhart et al. (2025)](https://www.pnas.org/doi/abs/10.1073/pnas.2422455122), a "
        "companion study from the same research group, examined multiple LLMs and found that "
        "instruction-tuned models use present participial clauses at 2–5× the human rate and "
        "nominalizations at roughly 1.5–2× the human rate. Some patterns turned out to be "
        "model-specific: the GPT-4o models avoid clausal co-ordination (they favor noun-to-noun "
        "phrasal co-ordination instead), while all of the Llama 3 variants use clausal "
        "co-ordination more than humans do. Importantly, base models wrote much closer to human "
        "norms, which suggests that instruction tuning introduces the style."
    )
    st.caption(
        "DeLuca, L. S., Reinhart, A., Weinberg, G., Laudenbach, M., Miller, S., & Brown, D. W. "
        "(2025). Developing students’ statistical expertise through writing in the age of AI. "
        "*Journal of Statistics and Data Science Education, 33*(3), 266–278."
    )
    st.caption(
        "Reinhart, A., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., Weinberg, G., & "
        "Brown, D. W. (2025). Do LLMs write like humans? Variation in grammatical and rhetorical "
        "styles. *Proceedings of the National Academy of Sciences, 122*(8), e2422455122."
    )
    st.caption(
        "Optional further reading: Markey, B., Brown, D. W., Laudenbach, M., & Kohler, A. (2024). "
        "Dense and disconnected: Analyzing the sedimented style of ChatGPT-generated text at "
        "scale. *Written Communication, 41*(4), 571–600. The \"AI slop\" framework on this site "
        "also draws on this study."
    )
    st.caption(
        "On students' right to refuse generative AI: Sano-Franchini, J., McIntyre, M., & "
        "Fernandes, M. [Refusing GenAI in Writing Studies: A Quickstart Guide](https://refusal.blog/)."
    )

st.divider()
st.caption(
    "[Calvin Pollak](https://english.washington.edu/people/calvin-pollak) · University of "
    "Washington · These materials may be freely used and adapted for educational purposes. "
    "Please cite: Pollak, 2026. Writing Against AI Slop: Practice exercises for Technical and "
    "Professional Communication. Available from: https://engl288-pollak.streamlit.app/  \n"
)
