"""Exercise Set 1: AI Slop Style vs. a More Human Style.

Ported from Pollak_SlopVsHuman_style-comparison_3-3-26.html, with the September
2026 carryover fixes applied (see CHANGES at the bottom of this file).

PARAGRAPHS: side-by-side pairs. hlA / hlB list the phrases to highlight; each phrase
must appear in the paragraph exactly as written, or it won't be highlighted.
EXERCISES: "identify" items have answer "A" (AI slop style) or "B" (a more human style);
"transform" items have a tip and a model answer.
"""

PARAGRAPHS_INTRO = (
    "These paragraph pairs illustrate the key grammatical contrasts identified by **DeLuca et al. "
    "(2025)** and **Reinhart et al. (2025)**. Reinhart et al. found that instruction-tuned LLMs use "
    "nominalizations at 1.5–2× the human rate and present participial clauses at 2–5× the human "
    "rate, while GPT-4o models avoid clausal co-ordination relative to humans. DeLuca et al. "
    "compared ChatGPT-generated introductions to ones written by students and by published "
    "researchers, and found the machine-generated text far more informationally dense than the "
    "student writing: heavy on nouns, and nearly empty of the hedges and modals of possibility "
    "that human writers use to modulate their confidence. Use the highlights to see these "
    "features in action."
)

EXERCISES_INTRO = (
    "These exercises are based on the stylistic features documented in **DeLuca et al. (2025)** "
    "and **Reinhart et al. (2025)**. The identification exercises focus on nominalization, "
    "hedging, and clausal co-ordination; the transformation exercises ask you to convert between "
    "the two styles in both directions."
)

PARAGRAPHS = [
    {
        "topic": "Climate Change",
        "a": "The accelerating deterioration of polar ice sheets under conditions of sustained atmospheric warming presents significant challenges for coastal infrastructure planning. Rising ocean temperatures, combined with the thermal expansion of seawater, drive the progressive inundation of low-lying territories, threatening densely populated urban centers. Policymakers addressing this transformation must weigh long-term mitigation strategies against immediate adaptation requirements, recognizing the compounding effects of delayed intervention.",
        "b": "Polar ice sheets are deteriorating at an accelerating rate because the atmosphere is warming in a sustained way, and this creates significant challenges for people who plan coastal infrastructure. Ocean temperatures are rising, and seawater is also expanding thermally, and so low-lying territories might gradually be inundated, which could threaten densely populated urban centers. Policymakers need to address this, and they must weigh up long-term mitigation strategies against what needs to happen immediately, though it is worth noting that if intervention is delayed, the effects could compound.",
        "hlA": ["deterioration", "accelerating", "sustained atmospheric warming", "thermal expansion", "progressive inundation", "compounding effects", "delayed intervention"],
        "hlB": ["are deteriorating", "because", "and this creates", "and so", "might gradually be", "though it is worth noting", "could compound"],
    },
    {
        "topic": "Medical Research",
        "a": "The targeted inhibition of inflammatory cytokine pathways represents a promising avenue for the treatment of autoimmune disorders characterized by chronic joint destruction. Early-stage clinical trials examining the efficacy of novel monoclonal antibody therapies have demonstrated measurable reductions in disease activity markers among trial participants, supporting further investigation into optimal dosing regimens and long-term tolerability profiles.",
        "b": "It appears to be promising to inhibit inflammatory cytokine pathways in a targeted way, and this could be used to treat autoimmune disorders where joints are chronically destroyed. Researchers have been conducting early-stage clinical trials to examine whether novel monoclonal antibody therapies are efficacious, and participants in the trials seem to have experienced reductions in their disease activity markers. This suggests that it would be worthwhile to investigate further what dosing regimens would be optimal and whether the therapies are tolerable over the long term.",
        "hlA": ["targeted inhibition", "inflammatory cytokine pathways", "chronic joint destruction", "measurable reductions", "disease activity markers", "optimal dosing regimens", "long-term tolerability profiles"],
        "hlB": ["It appears to be promising", "and this could be used", "and participants", "seem to have", "suggests", "would be worthwhile"],
    },
    {
        "topic": "Urban Development",
        "a": "The rapid densification of metropolitan cores, driven by sustained inward migration and constrained land availability, has intensified pressure on existing transport networks and public service infrastructure. Mixed-use development strategies integrating residential, commercial, and civic functions within walkable neighborhoods offer a partial mitigation of these pressures, reducing per-capita transport demand while supporting vibrant local economies.",
        "b": "Metropolitan cores are densifying rapidly because people are consistently migrating inward and land is constrained in terms of availability, and this has intensified the pressure on transport networks and public services that already exist. Mixed-use development strategies could offer a partial mitigation of these pressures, as these strategies integrate residential, commercial, and civic functions within neighborhoods that can be walked through. They could help to reduce the amount of transport that each person demands while also supporting local economies, which might become more vibrant as a result.",
        "hlA": ["rapid densification", "sustained inward migration", "constrained land availability", "Mixed-use development strategies", "integrating", "walkable neighborhoods", "per-capita transport demand"],
        "hlB": ["are densifying rapidly", "and this has intensified", "could offer", "as these strategies", "could help", "which might become"],
    },
]

EXERCISES = [
    {"type": "identify", "question": "Which style is this passage written in?",
     "passage": "The systematic exclusion of low-income populations from quality educational provision perpetuates intergenerational cycles of economic disadvantage, limiting social mobility across successive cohorts.",
     "answer": "A",
     "explanation": "AI slop style: dense noun phrases (\"systematic exclusion,\" \"intergenerational cycles\"), nominalizations (\"provision,\" \"disadvantage,\" \"mobility\"), no hedging, no co-ordinating conjunctions. Reinhart et al. (2025) found instruction-tuned LLMs use nominalizations at 1.5–2× the human rate, and DeLuca et al. (2025) found that ChatGPT-generated introductions are far more informationally dense than student writing, with almost no modals of possibility."},
    {"type": "identify", "question": "Which style is this passage written in?",
     "passage": "It seems that when low-income populations are excluded from quality education in a systematic way, cycles of economic disadvantage might be perpetuated, and this could mean that social mobility is limited for people across successive cohorts.",
     "answer": "B",
     "explanation": "A more human style: hedges (\"It seems that,\" \"might be,\" \"could mean\"), agentless passives (\"are excluded,\" \"is limited\"), clausal co-ordination (\"and this could mean\"), verbs preferred over nouns. DeLuca et al. (2025) found that ChatGPT used the predictive modal will 199 times across 100 introductions, while may, might, and could did not appear at all, so its prose barely modulates its confidence. Reinhart et al. (2025) found that GPT-4o models avoid clausal co-ordination relative to human writers."},
    {"type": "transform", "question": "Rewrite this sentence in AI slop style by nominalizing its verbs and removing its hedges.",
     "passage": "Researchers have suggested that biodiversity might decline rapidly if habitats are destroyed, and this could affect how ecosystems function.",
     "tip": "Try turning 'decline', 'destroyed', and 'function' into nouns ('decline', 'destruction', 'functioning'), and remove 'might', 'could', and the co-ordinating 'and'.",
     "model": "Research suggests rapid biodiversity decline under conditions of habitat destruction poses significant risks to ecosystem functioning."},
    {"type": "transform", "question": "Rewrite this AI slop style sentence in a more human style by unpacking noun phrases into clauses and adding appropriate hedges.",
     "passage": "The progressive commodification of urban housing stock, driven by speculative investment pressure, has produced severe affordability constraints for low-income renters.",
     "tip": "Try unpacking 'commodification' back into a verb ('is being commodified'), and add hedges like 'seems to be' and 'might mean'.",
     "model": "Urban housing stock seems to be becoming increasingly commodified, possibly because speculative investors are putting pressure on the market, and this might mean that low-income renters are finding it harder and harder to afford housing."},
    {"type": "identify", "question": "Which style is this passage written in?",
     "passage": "Mounting evidence linking prolonged screen exposure to disrupted circadian rhythms underscores the need for evidence-based guidelines governing adolescent device use in the hours preceding sleep onset.",
     "answer": "A",
     "explanation": "AI slop style: present participial clause (\"linking prolonged screen exposure...\"), heavy nominalization (\"disrupted circadian rhythms,\" \"sleep onset,\" \"device use\"), attributive noun stacking, no hedges or co-ordination. Reinhart et al. (2025) found that instruction-tuned LLMs use present participial clauses at 2–5× the human rate; it is one of the single most distinctive features of LLM-generated text."},
    {"type": "identify", "question": "Which style is this passage written in?",
     "passage": "Some studies have suggested that if adolescents are exposed to screens for prolonged periods, their circadian rhythms might be disrupted, and so it could be argued that guidelines which are based on evidence should perhaps be developed to govern how adolescents use devices in the hours before they go to sleep.",
     "answer": "B",
     "explanation": "A more human style: hedges throughout (\"Some studies have suggested,\" \"might be disrupted,\" \"could be argued,\" \"should perhaps\"), agentless passives (\"are exposed,\" \"might be disrupted\"), extensive clausal co-ordination. DeLuca et al. (2025) found that LLM text uses almost none of the hedges and modals of possibility that keep writing open to other perspectives, which is the opposite of this passage. Note also the agentless passives: Reinhart et al. (2025) found GPT-4o uses the agentless passive at roughly half the rate of human writers."},
]

# CHANGES (September 2026), for Calvin's reference:
# - Exercise 3 asked students to nominalize "the underlined verbs," but nothing was
#   underlined. Reworded, and the tip now names the verbs actually in the passage
#   (the old tip listed "destruction," which is already a noun).
# - Explanations 2 and 6 no longer start with a lowercase "a more human style".
# - Explanation 2: "prose with no room for alternatives" -> "barely modulates its confidence".
# - British spellings changed to American (centers, neighborhoods, characterized, recognizing).
