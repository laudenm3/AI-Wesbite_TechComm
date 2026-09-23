# Unit 3 — Proposals for De-Slop-ification. Teams analyze an LLM-generated
# proposal for overstatement and underspecification, then compose their own.

PAGE_METADATA = {
    "key": "unit3_proposals",
    "title": "Proposals for De-Slop-ification",
    "unit_label": "Unit 3 · Local Change Proposal",
    "icon": "📋",
    "overview": (
        "Inspect how a generated proposal overstates and underexplains its case, compose your own "
        "proposal from argument and narrative for a real decisionmaker, and closely edit your draft."
    ),
}

_SAMPLE_PROPOSAL = """
**Previously-generated example: LLM proposal for extended library hours (excerpt, unedited output):**

> *Proposal: Implementation of Extended Library Operating Hours*
>
> The implementation of extended operating hours will deliver transformative benefits to the campus
> community. This initiative will drive measurable improvements in student academic performance and
> overall satisfaction with university facilities. Diverse student populations, including those facing
> scheduling constraints stemming from employment obligations, will experience significantly enhanced
> access to essential study resources. The proposed extension represents a strategic investment in
> student success that will yield substantial returns across multiple institutional metrics.
"""

STEPS = [
    {
        "type": "static",
        "content": (
            "**Why this exercise:** Markey et al. found proposal-style prose from LLMs to be dense, "
            "disconnected, and dialogically closed. Unhedged claims read as naive or dishonest, and "
            "abstraction gives decisionmakers nothing to picture. You'll practice spotting overstatement "
            "and underexplanation, then grounding your own proposal in a defined problem/solution and a "
            "story about real people."
        ),
    },
    {
        "type": "static",
        "content": (
            "### Part 1 · Analyze a Generated Proposal (work in project teams)\n\n"
            "1. Use this prompt, kept plain: *\"Write a two-page proposal to [a university or local "
            "government office] recommending [a change your team is considering for your project].\"*\n"
            "2. Read the output together, then complete the two diagnostic tasks below.\n\n"
            "**Teams that opt out of AI can use the sample below instead.**"
        ),
    },
    {
        "type": "sample",
        "title": "Previously-generated example: LLM proposal for extended library hours",
        "content": _SAMPLE_PROPOSAL,
    },
    {
        "type": "fields",
        "name": "Diagnostic A · Overstatement: Where Should This Hedge?",
        "items": [
            {
                "id": "diagnostic_overstatement",
                "label": "Overstatement diagnostic",
                "prompt": (
                    "Find three claims stated as certainties that are actually predictions or "
                    "possibilities (\"will deliver transformative benefits,\" \"will drive measurable "
                    "improvements\"). For each, rewrite with hedges and/or modals of possibility "
                    "(\"could,\" \"may,\" \"we expect,\" \"if X, then likely Y\"). Then answer: which "
                    "version would an experienced administrator trust more, and why? Consider that "
                    "unhedged predictions also create accountability problems — what happens when the "
                    "\"measurable improvements\" don't materialize?"
                ),
                "placeholder": "Quote three overstatements and rewrite each with more toned-down modality…",
                "height": 150,
            },
        ],
    },
    {
        "type": "fields",
        "name": "Diagnostic B · Underspecification: Where Are the People?",
        "items": [
            {
                "id": "diagnostic_underspecification",
                "label": "Underspecification diagnostic",
                "prompt": (
                    "Find three abstract phrases that gesture at human experience without any specific "
                    "examples (\"students facing scheduling constraints stemming from employment "
                    "obligations,\" \"diverse student populations\"). For each, sketch a concrete example "
                    "or two-sentence narrative that could be added: a named (or realistically anonymized) "
                    "student, a specific occasion or situation, a plausible or typical problem. What "
                    "evidence would you need to gather to write those sentences honestly?"
                ),
                "placeholder": "Quote three abstractions and draft a human story or anecdote to replace one of them…",
                "height": 150,
            },
        ],
    },
    {
        "type": "static",
        "content": (
            "**Discussion checkpoint:** The two problems — overconfidence about the future and "
            "vagueness about the present — are opposites. Why do human writers tend to do the reverse, "
            "and why might that combination be more persuasive?"
        ),
    },
    {
        "type": "fields",
        "name": "Part 2 · Compose From Argument and Narrative",
        "items": [
            {
                "id": "argument_foundation",
                "label": "Argument Foundation (Problem/Solution)",
                "prompt": (
                    "What problem do you want to define, and what solution do you want to advocate? "
                    "State each part in one sentence that a stranger would understand. If you can't state "
                    "these concisely yet, that's an intellectual gap that cannot be solved by AI."
                ),
                "placeholder": "Problem: … Solution: …",
                "height": 110,
            },
            {
                "id": "narrative_foundation",
                "label": "Narrative Foundation",
                "prompt": (
                    "Whose story are you trying to tell or uplift? Which specific people or groups are "
                    "affected by this problem, what does their experience actually look like, and how "
                    "will you learn about it (interviews, observation, survey, public data, your own "
                    "experience...)?"
                ),
                "placeholder": (
                    "The people at the center of this proposal are… Their experience looks like… "
                    "We'll learn about it by…"
                ),
                "height": 130,
            },
            {
                "id": "audience_analysis",
                "label": "The Actual Human Audience",
                "prompt": (
                    "Name the real decisionmaker (a specific office or person at the university or in "
                    "local government). What do they and their stakeholders value, what pressures are "
                    "they under, and what would make saying yes easy or hard for them? Your hedging and "
                    "your evidence should be tailored to this reader."
                ),
                "placeholder": (
                    "Our decisionmaker is… They care about… Saying yes is hard for them because…"
                ),
                "height": 130,
            },
        ],
    },
    {
        "type": "checklist",
        "name": "Part 3 · The De-Slop Editing Checklist",
        "intro": (
            "Apply this checklist to your full draft before submission. Check each item only after "
            "someone on the team has done a thorough pass, not just when you've agreed that it sounds done."
        ),
        "items": [
            {
                "id": "chk_nominalization",
                "label": "Nominalization sweep",
                "detail": (
                    "Search \"-tion/-ment/-ance\" words, try the verb form with a human subject, keep the "
                    "noun only where the verb version is genuinely worse."
                ),
            },
            {
                "id": "chk_participial",
                "label": "Participial clause sweep",
                "detail": (
                    "Search \"-ing\" clauses on noun phrases; break up stacked ones with and/but/so/because."
                ),
            },
            {
                "id": "chk_dense_np",
                "label": "Dense noun phrase sweep",
                "detail": "Flag noun phrases of 4+ words; unpack, ground with an example, or cut.",
            },
            {
                "id": "chk_modality",
                "label": "Modality check",
                "detail": (
                    "Every future prediction is hedged (\"could,\" \"we expect,\" \"is likely to\"); every "
                    "present-tense claim is backed by something actually observed, read, or analyzed."
                ),
            },
            {
                "id": "chk_examples",
                "label": "Example check",
                "detail": (
                    "Every major abstract claim is followed within a sentence or two by a concrete "
                    "example, number, or event."
                ),
            },
            {
                "id": "chk_coordination",
                "label": "Coordination check",
                "detail": (
                    "Ideas are linked via clause-level connectors (\"and this means,\" \"but it's worth "
                    "noting,\" \"which could suggest\") rather than comma-separated noun lists."
                ),
            },
            {
                "id": "chk_favorite_words",
                "label": "Favorite-word scan",
                "detail": (
                    "Search for \"comprehensive,\" \"robust,\" \"leverage,\" \"underscore,\" "
                    "\"transformative,\" \"seamless,\" \"foster,\" \"ecosystem\"; keep only if the "
                    "persuasive value can be defended."
                ),
            },
            {
                "id": "chk_decisionmaker",
                "label": "The decisionmaker test",
                "detail": (
                    "Read the executive summary aloud in the persona of the named decisionmaker. Can you "
                    "repeat the problem, the solution, and one memorable detail to a colleague after one read?"
                ),
            },
        ],
    },
    {
        "type": "fields",
        "name": "Most Important Edits",
        "items": [
            {
                "id": "most_important_edits",
                "label": "One paragraph noting the two most important edits you made",
                "placeholder": "Your paragraph…",
                "height": 120,
            },
        ],
    },
    {
        "type": "static",
        "content": (
            "**Bring to class / submit (one per team):** the generated proposal or sample with both "
            "diagnostics completed; the Part 2 foundations; your proposal draft with the Part 3 checklist "
            "completed and your paragraph on the two most important edits."
        ),
    },
]
