# Reading Check — self-graded comprehension quiz on Markey et al. (2024) and
# Reinhart et al. (2025), plus discussion prompts for class.

PAGE_METADATA = {
    "key": "reading_check",
    "title": "How LLMs Actually Write: Quiz & Discussion Prompts",
    "unit_label": "Start Here · The Readings",
    "icon": "📖",
    "overview": (
        "A self-graded comprehension quiz on the two studies these exercises are based on, "
        "plus five discussion prompts for class."
    ),
}

STEPS = [
    {
        "type": "static",
        "content": (
            "Both readings compare human writing with LLM-generated writing and identify "
            "specific, countable style differences between the two. Read them before starting "
            "this quiz:\n\n"
            "- Markey, B., Brown, D. W., Laudenbach, M., & Kohler, A. (2024). "
            "[Dense and disconnected: Analyzing the sedimented style of ChatGPT-generated text at scale]"
            "(https://journals.sagepub.com/doi/abs/10.1177/07410883241263528). "
            "*Written Communication, 41*(4), 571–600.\n"
            "- Reinhart, A., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., Weinberg, G., & Brown, D. W. (2025). "
            "[Do LLMs write like humans? Variation in grammatical and rhetorical styles]"
            "(https://www.pnas.org/doi/abs/10.1073/pnas.2422455122). "
            "*Proceedings of the National Academy of Sciences, 122*(8), e2422455122.\n\n"
            "The quiz is self-graded and you can retry it — but Units 1–3 all assume you know this "
            "material, so answer honestly rather than by trial and error."
        ),
    },
    {
        "type": "quiz",
        "name": "Part A · Comprehension Questions",
        "questions": [
            {
                "question": "Markey et al.'s central finding is that ChatGPT-generated academic prose is:",
                "options": [
                    "More informationally dense than even professional academic writing.",
                    "About as dense as first-year student writing.",
                    "Less dense than human writing, but more error-prone.",
                    "Indistinguishable from professional writing on density measures.",
                ],
                "answer": 0,
                "feedback": "Density (the involved-vs-informational dimension) is the headline finding of the study.",
            },
            {
                "question": "Markey et al. call generated text 'dialogically closed.' In terms of specific features, this mostly means the text has:",
                "options": [
                    "Too many rhetorical questions.",
                    "Very few hedges and modals of possibility.",
                    "No citations of other authors.",
                    "Short, choppy sentences.",
                ],
                "answer": 1,
                "feedback": "Hedges and modals signal that a writer is considering alternatives; generated text scores low on both, so it reads as closed rather than open to debate.",
            },
            {
                "question": "The researchers informally called ChatGPT's tendency to slot related vocabulary into rigid syntactic templates:",
                "options": [
                    "Boilerplating.",
                    "Mad libbing.",
                    "Stencil drift.",
                    "Template lock.",
                ],
                "answer": 1,
                "feedback": "\"Mad libbing\" — the same syntactic frames recur with only the vocabulary swapped in, producing the lowest variance of any subcorpus studied.",
            },
            {
                "question": "Markey et al. also found that ChatGPT struggles to generate:",
                "options": [
                    "Grammatically correct sentences.",
                    "Pedestrian, concrete examples that ground abstract concepts.",
                    "Long paragraphs.",
                    "Transitions between sections.",
                ],
                "answer": 1,
                "feedback": "Abstract noun phrases pile up but rarely get grounded in a concrete example — part of why the prose feels \"fluffy\" despite being dense.",
            },
            {
                "question": "According to Reinhart et al., the single most distinctive grammatical marker of instruction-tuned LLM output is:",
                "options": [
                    "Semicolon overuse.",
                    "The agentless passive voice.",
                    "Present participial clauses (e.g., \"a program facilitating the development of…\").",
                    "Sentence fragments.",
                ],
                "answer": 2,
                "feedback": "Present participial clauses appear at 2–5x the human rate across models (GPT-4o as high as 5.3x).",
            },
            {
                "question": "Reinhart et al. found that instruction-tuned models use nominalizations (verbs turned into nouns, like \"implementation\") at roughly:",
                "options": [
                    "The same rate as humans.",
                    "Half the human rate.",
                    "1.5 to 2 times the human rate.",
                    "10 times the human rate.",
                ],
                "answer": 2,
                "feedback": "GPT-4o runs about 2.1x; combined with dense noun phrases, this produces the noun-heavy style the readings describe.",
            },
            {
                "question": "Which finding about the agentless passive voice (\"the samples were measured\") is correct?",
                "options": [
                    "GPT-4o uses it at about half the human rate.",
                    "All models use it far more than humans.",
                    "Only base models avoid it.",
                    "The studies didn't measure passive voice.",
                ],
                "answer": 0,
                "feedback": "GPT-4o actually underuses the agentless passive, but achieves a similar impersonal effect through heavy nominalization instead.",
            },
            {
                "question": "On clausal co-ordination (linking full clauses with words like \"and\" or \"but\"), Reinhart et al. found:",
                "options": [
                    "All models avoid it equally.",
                    "Both GPT-4o models avoid it, while all Llama 3 variants use it more than humans.",
                    "Only humans use clausal co-ordination.",
                    "Llama 3 avoids it and GPT-4o overuses it.",
                ],
                "answer": 1,
                "feedback": "This pattern is model-specific: GPT-4o favors linking nouns to nouns (phrasal co-ordination, ~1.9x) rather than linking whole clauses.",
            },
            {
                "question": "Reinhart et al. compared base models with instruction-tuned models and concluded that the distinctive \"AI style\":",
                "options": [
                    "Comes from the pretraining data and can't be changed.",
                    "Appears to be introduced by instruction tuning, since base-model text is closer to human norms.",
                    "Only appears in text produced by models below a certain size.",
                    "Disappears when models are given longer prompts.",
                ],
                "answer": 1,
                "feedback": "Base models write much closer to human norms — the distinctive style looks like a byproduct of tuning models to be \"helpful.\"",
            },
            {
                "question": "Which vocabulary finding did Reinhart et al. report?",
                "options": [
                    "LLMs avoid adjectives almost entirely.",
                    "Words like \"tapestry,\" \"palpable,\" \"intricate,\" and \"underscore\" appeared at 100 times or more the human rate in GPT-4o output.",
                    "LLM-generated writing uses more slang than human writing.",
                    "LLM vocabulary varies dramatically by genre, unlike human vocabulary.",
                ],
                "answer": 1,
                "feedback": "A handful of LLM-favorite words recur at extreme rates, and — unlike human writers — the models fail to vary their vocabulary and style by genre.",
            },
        ],
    },
    {
        "type": "fields",
        "name": "Part B · Discussion Prompts",
        "intro": (
            "We'll take these up in class, but jot your thinking on at least two of them here first "
            "— they'll be saved into your downloadable workbook."
        ),
        "items": [
            {
                "id": "discussion_1",
                "label": "1. Dense and empty at the same time",
                "prompt": (
                    "Markey et al. describe ChatGPT's prose as \"empty\" and \"fluffy\" even though it is "
                    "informationally dense. How can text be dense and empty at the same time? Try to explain "
                    "this using one of the specific features from the readings."
                ),
                "placeholder": "Your answer…",
                "height": 110,
            },
            {
                "id": "discussion_2",
                "label": "2. Helpful, but less human",
                "prompt": (
                    "Reinhart et al. found that base models produce writing with style category rates much "
                    "closer to human norms, and that instruction tuning appears to introduce the distinctive "
                    "\"AI slop\" style rather than correct it. Why might the process of making models more "
                    "\"helpful\" also make their writing less human?"
                ),
                "placeholder": "Your answer…",
                "height": 110,
            },
            {
                "id": "discussion_3",
                "label": "3. Professional style vs. AI slop",
                "prompt": (
                    "Both studies note that some of these features (nominalizations, density) also appear in "
                    "professional academic writing. So where is the line between \"professional style\" and "
                    "\"AI slop\"? Is it about the features themselves, or how they're used?"
                ),
                "placeholder": "Your answer…",
                "height": 110,
            },
            {
                "id": "discussion_4",
                "label": "4. Hedging isn't always weak writing",
                "prompt": (
                    "Hedges and modals of possibility (\"might,\" \"could,\" \"seems to\") are often treated as "
                    "weak writing. These two readings suggest the opposite: they keep prose dialogically open "
                    "(and show intellectual humility). When have you been told to cut hedging from your writing, "
                    "and do you now agree or disagree with that advice?"
                ),
                "placeholder": "Your answer…",
                "height": 110,
            },
            {
                "id": "discussion_5",
                "label": "5. The risk of sounding synthetic",
                "prompt": (
                    "If audiences (employers, professors, community decisionmakers) are becoming more attuned "
                    "to these markers of synthetic text, what are the practical risks of submitting writing that "
                    "carries them, even if you wrote it yourself?"
                ),
                "placeholder": "Your answer…",
                "height": 110,
            },
        ],
    },
]
