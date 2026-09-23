# Unit 1 — Anti-Slop Cover Letters. Students generate a cover letter from an
# LLM, audit its style, then draft their own "inside-out" from STAR stories.

PAGE_METADATA = {
    "key": "unit1_cover_letters",
    "title": "Anti-Slop Cover Letters",
    "unit_label": "Unit 1 · Job Application Package",
    "icon": "✉️",
    "overview": (
        "Generate a cover letter from your own resume and a real job ad, investigate its "
        "peculiar style, and then draft your own letter \"inside-out\" from STAR stories."
    ),
}

_SAMPLE_LETTER = """
**Fictional resume (summary):** Jordan Reyes, 3rd-year Communication major at UW; 2 years as a
barista/shift lead (trained 6 new hires, scheduled a 12-person team); social media volunteer for a
food-security nonprofit (grew Instagram from 400 to 1,900 followers over two quarters; a donation
drive they helped run collected 800 lbs of food); course projects in technical writing and data
visualization.

**Job ad (excerpt):** *Communications & Outreach Intern — Sound Transit Community Engagement Office.*
Duties: draft social posts and newsletter content, help staff open-house events, summarize public
comments. Values: plain-language writing, comfort with the public, making complex information
understandable.

**LLM-generated cover letter (unedited output — the "slop" example students analyze):**

> Dear Hiring Committee,
>
> I am writing to express my enthusiastic interest in the Communications & Outreach Intern position
> with the Sound Transit Community Engagement Office. My academic background in Communication,
> combined with a robust foundation in strategic content creation, has prepared me to make a
> meaningful contribution to your team's public engagement initiatives.
>
> Throughout my professional experience, I have demonstrated a comprehensive skill set encompassing
> team leadership, training and development, and operational optimization. My involvement in
> nonprofit social media management underscores my capacity for impactful digital storytelling and
> audience growth strategy, while my coursework in technical writing and data visualization has
> equipped me with the analytical and communicative competencies necessary for translating complex
> information into accessible content.
>
> The implementation of effective public outreach strategies requires an individual who possesses
> both creative vision and operational rigor — qualities I have consistently exhibited across my
> academic and professional endeavors. I am confident that my comprehensive background positions me
> as an ideal candidate for this role.
>
> I welcome the opportunity to discuss how my qualifications align with your team's objectives.
>
> Sincerely,
> Jordan Reyes
"""

STEPS = [
    {
        "type": "static",
        "content": (
            "**Why this exercise:** LLM-generated cover letters tend to be dense, generic, unhedged, "
            "and short on concrete stories — and hiring managers are getting better at spotting this. "
            "By the end you should be able to identify at least 4 of 6 AI-style features in a generated "
            "letter, explain why each weakens it, and draft 2–3 STAR stories that build a letter around "
            "the strongest one."
        ),
    },
    {
        "type": "static",
        "content": (
            "### Part 1 · Generate a Letter From Your Materials\n\n"
            "1. Open the university-licensed LLM chatbot (use the tool designated in the syllabus, not "
            "your personal account, so your materials stay within the licensed environment).\n"
            "2. Upload your resume and paste in the full text of a real job ad.\n"
            "3. Use this prompt exactly: *\"Write a one-page cover letter applying to this job based on "
            "my resume.\"* Don't coach it toward better style — we want its default behavior.\n"
            "4. Save the output somewhere you can annotate it (copy it into a doc, or print it).\n\n"
            "**You may opt out of using AI here without justification.** If you opt out, use the "
            "previously-generated example below instead."
        ),
    },
    {
        "type": "sample",
        "title": "Previously-generated example: fictional resume, job ad, and LLM cover letter",
        "content": _SAMPLE_LETTER,
    },
    {
        "type": "fields",
        "name": "Part 2 · Investigate the Letter",
        "intro": (
            "Analyze either the letter you generated in Part 1 or the sample above. For each feature, "
            "quote directly from the letter."
        ),
        "items": [
            {
                "id": "p2_nominalizations",
                "label": "1. Nominalizations",
                "prompt": (
                    "Actions turned into abstract nouns: \"the implementation of,\" \"coordination,\" "
                    "\"optimization.\" Find at least two. For each, what's the buried verb, and who is its "
                    "missing subject?"
                ),
                "placeholder": "Quote the phrases and name the buried verbs…",
                "height": 110,
            },
            {
                "id": "p2_participial_clauses",
                "label": "2. Present participial clauses",
                "prompt": (
                    "\"-ing\" clauses stacked onto noun phrases: \"…possessing a robust foundation,\" "
                    "\"…driving significant audience growth.\" Research finding: instruction-tuned models "
                    "use these at 2–5x the human rate. How many can you find in one sentence?"
                ),
                "placeholder": "Quote a sentence and count its participial clauses…",
                "height": 110,
            },
            {
                "id": "p2_dense_noun_phrases",
                "label": "3. Dense noun phrases",
                "prompt": (
                    "Long modifier chains: \"comprehensive skill set,\" \"strategic content creation.\" "
                    "Pick the densest one. Does the letter ever unpack it with a concrete detail, or does "
                    "it stay abstract?"
                ),
                "placeholder": "Quote the densest noun phrase and say whether it ever gets grounded…",
                "height": 110,
            },
            {
                "id": "p2_missing_hedges",
                "label": "4. Missing hedges and modality",
                "prompt": (
                    "Generated text is \"dialogically closed\": everything in it sounds confident and "
                    "settled. Find the most overstated claim. How would a thoughtful human applicant have "
                    "qualified it?"
                ),
                "placeholder": "Quote the overstatement and rewrite it with moderated confidence…",
                "height": 110,
            },
            {
                "id": "p2_phrasal_coordination",
                "label": "5. Phrasal (not clausal) co-ordination",
                "prompt": (
                    "Nouns linked to nouns (\"training, scheduling coordination, and operational "
                    "optimization\") instead of ideas linked to ideas (\"I trained six new hires, and that "
                    "taught me…\"). Find a list of nouns that hides a story."
                ),
                "placeholder": "Quote the noun list and sketch the story it's hiding…",
                "height": 110,
            },
            {
                "id": "p2_missing_examples",
                "label": "6. Missing concrete examples",
                "prompt": (
                    "The research finds LLMs struggle to generate \"pedestrian examples.\" The resume had "
                    "real numbers (400 → 1,900 followers, 800 lbs of food, a 12-person team). What did the "
                    "letter do with them? What would a specific, human paragraph about the donation drive "
                    "look like?"
                ),
                "placeholder": "Note which concrete details survived and which vanished into abstraction…",
                "height": 110,
            },
        ],
    },
    {
        "type": "static",
        "content": (
            "**Discussion checkpoint:** Before moving on, compare notes with a partner. Which feature "
            "was easiest to spot? Did the letter say anything a hundred other applicants' letters "
            "couldn't also say?"
        ),
    },
    {
        "type": "static",
        "content": (
            "### Part 3 · Draft Inside-Out: STAR Stories First\n\n"
            "The LLM seems to have drafted its content \"outside-in,\" starting from generic professional "
            "qualities and never quite reaching a real story. You'll draft \"inside-out\": start from your "
            "two or three most interesting real experiences, write them as stories, and only then build "
            "the letter's structure around them. Use the STAR frame (Situation, Task, Action, Result)."
        ),
    },
    {
        "type": "fields",
        "name": "Story 1 (required)",
        "items": [
            {
                "id": "story1_situation",
                "label": "Situation",
                "prompt": (
                    "Where were you, and what was going on? Be pedestrian and specific: the workplace / "
                    "course, the academic term, the project, the problem."
                ),
                "placeholder": "",
                "height": 120,
            },
            {
                "id": "story1_task",
                "label": "Task",
                "prompt": "What were you responsible for making happen?",
                "placeholder": "",
                "height": 90,
            },
            {
                "id": "story1_action",
                "label": "Action",
                "prompt": (
                    "What did you actually do? Use concrete action verbs with yourself or your team as "
                    "the subject."
                ),
                "placeholder": "",
                "height": 90,
            },
            {
                "id": "story1_result",
                "label": "Result",
                "prompt": (
                    "What changed or improved as a result of your actions? Numbers help, but so does an "
                    "honest, modest outcome. Consider outcomes both for the organization or place and for "
                    "yourself as a professional."
                ),
                "placeholder": "",
                "height": 120,
            },
        ],
    },
    {
        "type": "fields",
        "name": "Story 2 (required)",
        "items": [
            {"id": "story2_situation", "label": "Situation", "placeholder": "", "height": 90},
            {"id": "story2_task", "label": "Task", "placeholder": "", "height": 90},
            {"id": "story2_action", "label": "Action", "placeholder": "", "height": 90},
            {"id": "story2_result", "label": "Result", "placeholder": "", "height": 90},
        ],
    },
    {
        "type": "fields",
        "name": "Story 3 (optional)",
        "items": [
            {"id": "story3_situation", "label": "Situation", "placeholder": "", "height": 90},
            {"id": "story3_task", "label": "Task", "placeholder": "", "height": 90},
            {"id": "story3_action", "label": "Action", "placeholder": "", "height": 90},
            {"id": "story3_result", "label": "Result", "placeholder": "", "height": 90},
        ],
    },
    {
        "type": "fields",
        "name": "From Stories to Letter",
        "items": [
            {
                "id": "letter_match",
                "label": "Match",
                "prompt": (
                    "Reread the job ad. Which of your stories speaks most directly to what this employer "
                    "says they value, and why?"
                ),
                "placeholder": "",
                "height": 100,
            },
            {
                "id": "letter_topic_sentences",
                "label": "Topic sentences",
                "prompt": (
                    "Draft one topic sentence per body paragraph. Each should make a claim that one of "
                    "your STAR stories can back up."
                ),
                "placeholder": "",
                "height": 100,
            },
            {
                "id": "letter_opening_closing",
                "label": "Opening & closing",
                "prompt": (
                    "Only now draft your intro and conclusion, so they frame the stories instead of "
                    "replacing them."
                ),
                "placeholder": "",
                "height": 100,
            },
        ],
    },
    {
        "type": "checklist",
        "name": "Part 4 · Self-Edit Checklist",
        "intro": "Run this checklist on your full draft before submission.",
        "items": [
            {
                "id": "chk_grounded",
                "label": "Every abstract claim is grounded",
                "detail": (
                    "Each \"skill\" you name is attached to a specific moment, place, or number from one "
                    "of your stories."
                ),
            },
            {
                "id": "chk_verbs",
                "label": "Verbs over nominalizations",
                "detail": (
                    "Where you wrote \"coordination of X,\" you've tried \"I coordinated X\" and kept "
                    "whichever is clearer (usually the verb)."
                ),
            },
            {
                "id": "chk_participials",
                "label": "Participial pile-ups broken apart",
                "detail": (
                    "No sentence carries more than one \"-ing\" modifier clause; ideas get their own "
                    "clauses, joined with \"and,\" \"but,\" or \"so.\""
                ),
            },
            {
                "id": "chk_confidence",
                "label": "Confidence is moderated",
                "detail": (
                    "Make strong claims where you've earned them, and hedge where you haven't. Cut "
                    "\"seamlessly,\" and don't claim a \"proven track record\" unless the proof is on the page."
                ),
            },
            {
                "id": "chk_only_you",
                "label": "It could only be you",
                "detail": (
                    "Could another applicant paste their name onto this letter? If so, it needs more of "
                    "your story."
                ),
            },
        ],
    },
    {
        "type": "fields",
        "name": "Reflection",
        "items": [
            {
                "id": "reflection",
                "label": "Reflection (150–250 words)",
                "prompt": "What could the LLM do that you couldn't, and what could you do that it couldn't?",
                "placeholder": "Your reflection…",
                "height": 160,
            },
        ],
    },
    {
        "type": "static",
        "content": (
            "**Bring to class / submit:** the generated or sample letter with your Part 2 notes; your "
            "2–3 STAR stories; the full cover letter draft with the Part 4 checklist completed; and your "
            "reflection."
        ),
    },
]
