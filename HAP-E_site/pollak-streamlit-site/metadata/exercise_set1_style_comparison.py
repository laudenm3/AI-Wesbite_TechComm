# Exercise Set 1 — AI Slop Style vs. a More Human Style. Side-by-side
# paragraph comparisons, then identification and transformation exercises.

PAGE_METADATA = {
    "key": "exercise_set1_style_comparison",
    "title": "AI Slop Style vs. a More Human Style",
    "unit_label": "Practice Anytime · Exercise Set 1",
    "icon": "🎯",
    "overview": (
        "Side-by-side paragraph comparisons and identification/transformation exercises across two "
        "writing styles: dense, nominal AI slop style vs. a hedged, clausal, more human style."
    ),
}

STEPS = [
    {
        "type": "static",
        "content": (
            "Grounded in Markey et al. (2024) and Reinhart et al. (2025): LLMs use nominalizations at "
            "1.5–2x the human rate and present participial clauses at 2–5x the human rate; GPT-4o avoids "
            "clausal co-ordination relative to humans; and ChatGPT text is more informationally dense "
            "than professional academic writing and \"dialogically closed\" (heavy on nouns, light on "
            "hedges and modals)."
        ),
    },
    {
        "type": "static",
        "content": "### Paragraph Examples\n\nThree topics, each with an AI-slop version (A) and a more-human version (B).",
    },
    {
        "type": "sample",
        "title": "Climate Change — A (AI slop style) vs. B (more human style)",
        "content": (
            "**A (AI slop style):** The accelerating deterioration of polar ice sheets under conditions "
            "of sustained atmospheric warming presents significant challenges, with the compounding "
            "effects of thermal expansion contributing to projected sea-level rise across coastal regions.\n\n"
            "**B (more human style):** Polar ice sheets are deteriorating at an accelerating rate because "
            "the atmosphere is warming in a sustained way, and this creates significant challenges — "
            "though it is worth noting that thermal expansion might gradually be compounding sea-level "
            "rise in coastal regions.\n\n"
            "*Notice:* A leans on nominalizations and dense noun phrases (\"deterioration,\" \"thermal "
            "expansion,\" \"compounding effects\"); B uses hedges and co-ordinating conjunctions (\"because,\" "
            "\"and so,\" \"might,\" \"though it is worth noting\")."
        ),
    },
    {
        "type": "sample",
        "title": "Medical Research — A (AI slop style) vs. B (more human style)",
        "content": (
            "**A (AI slop style):** The targeted inhibition of inflammatory cytokine pathways represents "
            "a promising avenue for the treatment of autoimmune disorders, with preliminary data "
            "suggesting therapeutic efficacy across multiple patient populations.\n\n"
            "**B (more human style):** It appears to be promising to inhibit inflammatory cytokine "
            "pathways in a targeted way, and this could be used to treat autoimmune disorders — early "
            "data suggests it might work for a range of patients, though more research is needed.\n\n"
            "*Notice:* the same nominalization-vs-hedge contrast as above."
        ),
    },
    {
        "type": "sample",
        "title": "Urban Development — A (AI slop style) vs. B (more human style)",
        "content": (
            "**A (AI slop style):** The rapid densification of metropolitan cores, driven by sustained "
            "inward migration and constrained land availability, has intensified pressure on existing "
            "housing infrastructure.\n\n"
            "**B (more human style):** Metropolitan cores are densifying rapidly because people are "
            "consistently migrating inward and land is constrained, and this seems to be putting more "
            "pressure on existing housing.\n\n"
            "*Notice:* the same nominalization-vs-hedge contrast as above."
        ),
    },
    {
        "type": "static",
        "content": (
            "### Exercises: Identification and Transformation\n\n"
            "The identification exercises focus on nominalization, hedging, and clausal co-ordination; "
            "the transformation exercises ask you to convert between the two styles in both directions."
        ),
    },
    {
        "type": "choice",
        "id": "ex1",
        "name": "Exercise 1 · Identification",
        "question": (
            "Which style is this passage written in?\n\n"
            "> The systematic exclusion of low-income populations from quality educational provision "
            "perpetuates intergenerational cycles of economic disadvantage, limiting social mobility "
            "across successive cohorts."
        ),
        "options": ["AI slop style", "A more human style"],
        "answer": 0,
        "explanation": "Dense nominalizations (\"exclusion,\" \"provision\") with no hedging.",
    },
    {
        "type": "choice",
        "id": "ex2",
        "name": "Exercise 2 · Identification",
        "question": (
            "Which style is this passage written in?\n\n"
            "> It seems that when low-income populations are excluded from quality education in a "
            "systematic way, cycles of economic disadvantage might be perpetuated, and this could mean "
            "that social mobility is limited for people across successive cohorts."
        ),
        "options": ["AI slop style", "A more human style"],
        "answer": 1,
        "explanation": "Hedges (\"it seems,\" \"might,\" \"could\") and clausal co-ordination (\"and this could mean\").",
    },
    {
        "type": "transform",
        "id": "ex3",
        "name": "Exercise 3 · Transformation (human → AI slop style)",
        "question": "Rewrite this human-style sentence in AI slop style by nominalizing the underlined verbs and removing hedges.",
        "passage": (
            "Researchers have suggested that biodiversity might decline rapidly if habitats are "
            "destroyed, and this could affect how ecosystems function."
        ),
        "tip": "Try turning \"decline,\" \"destruction,\" and \"functioning\" into nouns, and remove \"might,\" \"could,\" and the co-ordinating \"and\".",
        "placeholder": "Type your rewritten sentence here…",
        "model_answer": (
            "Research suggests rapid biodiversity decline under conditions of habitat destruction poses "
            "significant risks to ecosystem functioning."
        ),
        "height": 90,
    },
    {
        "type": "transform",
        "id": "ex4",
        "name": "Exercise 4 · Transformation (AI slop style → human)",
        "question": "Rewrite this AI-slop-style sentence in a more human style by unpacking noun phrases into clauses and adding appropriate hedges.",
        "passage": (
            "The progressive commodification of urban housing stock, driven by speculative investment "
            "pressure, has produced severe affordability constraints for low-income renters."
        ),
        "tip": "Try unpacking \"commodification\" back into a verb (\"is being commodified\"), and add hedges like \"seems to be\" and \"might mean\".",
        "placeholder": "Type your rewritten sentence here…",
        "model_answer": (
            "Urban housing stock seems to be becoming increasingly commodified, possibly because "
            "speculative investors are putting pressure on the market, and this might mean that "
            "low-income renters are finding it harder and harder to afford housing."
        ),
        "height": 100,
    },
    {
        "type": "choice",
        "id": "ex5",
        "name": "Exercise 5 · Identification",
        "question": (
            "Which style is this passage written in?\n\n"
            "> Mounting evidence linking prolonged screen exposure to disrupted circadian rhythms "
            "underscores the need for evidence-based guidelines governing adolescent device use in the "
            "hours preceding sleep onset."
        ),
        "options": ["AI slop style", "A more human style"],
        "answer": 0,
        "explanation": "Dense noun phrases stacked with no hedging (\"mounting evidence linking… underscores the need for…\").",
    },
    {
        "type": "choice",
        "id": "ex6",
        "name": "Exercise 6 · Identification",
        "question": (
            "Which style is this passage written in?\n\n"
            "> Some studies have suggested that if adolescents are exposed to screens for prolonged "
            "periods, their circadian rhythms might be disrupted, and so it could be argued that "
            "guidelines which are based on evidence should perhaps be developed to govern how adolescents "
            "use devices in the hours before they go to sleep."
        ),
        "options": ["AI slop style", "A more human style"],
        "answer": 1,
        "explanation": "Heavily hedged (\"might,\" \"could,\" \"perhaps\") and clausally co-ordinated.",
    },
]
