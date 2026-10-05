"""Reading Check content, originally copied from Pollak_ReadingCheck_7-13-26.html.

CHANGES

September 2026: split into two checks so each can run as its own in-class assignment.
DELUCA carries the four questions about DeLuca et al.; REINHART carries the six about
Reinhart et al. The quiz questions divided cleanly along that line and are unchanged.

The discussion prompts did not divide as cleanly. Three of the original five concern
DeLuca et al. and one concerns Reinhart et al., so the counts are uneven. The prompt about
audiences noticing synthetic markers belongs to neither reading in particular and now
appears on both pages, as SHARED_PROMPT. One phrase changed: the prompt about hedges and
modals said "these two readings," which is wrong on a page about one of them, and now
names DeLuca et al. The two page introductions are new wording, written for the split.

To edit a question, change the text here. Each question has:
  q    - the question
  opts - four answer options, in order (a) to (d)
  a    - the index of the correct option (0 = a, 1 = b, 2 = c, 3 = d)
  fb   - feedback shown after the student answers
"""

DELUCA_CITATION = (
    "DeLuca, L. S., Reinhart, A., Weinberg, G., Laudenbach, M., Miller, S., & Brown, D. W. (2025). "
    "[Developing students’ statistical expertise through writing in the age of AI]"
    "(https://doi.org/10.1080/26939169.2025.2497547). *Journal of Statistics and Data Science "
    "Education, 33*(3), 266–278."
)

REINHART_CITATION = (
    "Reinhart, A., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., Weinberg, G., & Brown, D. W. (2025). "
    "[Do LLMs write like humans? Variation in grammatical and rhetorical styles]"
    "(https://www.pnas.org/doi/abs/10.1073/pnas.2422455122). *PNAS, 122*(8), e2422455122."
)

# Kept as a list because other pages import it for their own citation blocks.
CITATIONS = [DELUCA_CITATION, REINHART_CITATION]

# Not tied to either study, so it closes both checks.
SHARED_PROMPT = (
    "If audiences (employers, professors, community decisionmakers) are becoming more attuned "
    "to these markers of synthetic text, what are the practical risks of submitting writing "
    "that carries them, even if you wrote it yourself?"
)

DELUCA_QUESTIONS = [
    {
        "q": "DeLuca et al. compared introductions written by ChatGPT, by undergraduate students, and by published researchers. What did the largest source of variation (72%) in their analysis separate?",
        "opts": ["Novice writing from expert writing", "Machine-generated writing from human-generated writing", "Statistics writing from writing in other fields", "Long introductions from short ones"],
        "a": 1,
        "fb": "Correct answer: (b). The first discriminant separates machine-generated from human-generated text, and the second (28%) separates novice from expert. ChatGPT lands in its own region of the plot, which the authors describe as somewhere in between novices and experts, not exactly mimicking either.",
    },
    {
        "q": "In the 100 ChatGPT-generated introductions, what did DeLuca et al. find about modal verbs?",
        "opts": ["A wide range of modals, used much as human writers use them", "'Will' appeared 199 times, 'can' five times, and 'may,' 'might,' 'could,' 'should,' and 'must' not at all", "Only necessity modals like 'must' appeared", "No modal verbs appeared at all"],
        "a": 1,
        "fb": "Correct answer: (b). Rather than hedging claims, 'will' forecasts the research. The authors read this restricted set as monotony in the claim-making: human writers weight the strength of their results and modulate their claims for an audience, and both the students and the experts used a much wider array of modals.",
    },
    {
        "q": "How did the noun phrases in the ChatGPT introductions compare to those written by the students and the published experts?",
        "opts": ["The longest of any group, by far", "Longer than the students' but shorter than the experts', with the least variation in length", "The shortest of any group", "About the same as the experts' in both length and variation"],
        "a": 1,
        "fb": "Correct answer: (b). The published experts wrote the longest noun phrases and also varied their length the most, expanding and contracting them strategically by restating key points, giving examples, and signaling clarification to come. The authors connect that variation to audience awareness, which an LLM does not have.",
    },
    {
        "q": "What did DeLuca et al. find about the statistical content of the ChatGPT-generated introductions?",
        "opts": ["They used precise terminology like 't-test' throughout", "They touched on statistical concepts but gave little detail, and none of them included any numeric values", "They contained more numbers than the expert introductions", "They fabricated citations to statistics papers"],
        "a": 1,
        "fb": "Correct answer: (b). Only seven of the one hundred introductions used the word 'variables,' and none introduced terms like 't-test.' Their claims of importance rested on unmeasurable attributes ('crucial for individual development'), where expert writers assign measurable ones ('the most common,' 'the most predictive'). This is a gap that human readers notice and may respond negatively to.",
    },
]

REINHART_QUESTIONS = [
    {
        "q": "According to Reinhart et al., the single most distinctive grammatical marker of instruction-tuned LLM output is:",
        "opts": ["Semicolon overuse", "The agentless passive voice", "Present participial clauses (e.g., 'a program facilitating the development of…')", "Sentence fragments"],
        "a": 2,
        "fb": "Correct answer: (c). Instruction-tuned models use present participial clauses at 2 to 5 times the human rate; GPT-4o used them at 5.3 times the human rate.",
    },
    {
        "q": "Reinhart et al. found that instruction-tuned models use nominalizations (verbs turned into nouns, like 'implementation') at roughly:",
        "opts": ["The same rate as humans", "Half the human rate", "1.5 to 2 times the human rate", "10 times the human rate"],
        "a": 2,
        "fb": "Correct answer: (c). Nominalizations run about 1.5–2× the human rate (GPT-4o about 2.1×). Combined with dense noun phrases, this produces the noun-heavy style described in both articles.",
    },
    {
        "q": "Which finding about the agentless passive voice ('the samples were measured') is correct?",
        "opts": ["GPT-4o uses it at about half the human rate", "All models use it far more than humans", "Only base models avoid it", "The studies didn't measure passive voice"],
        "a": 0,
        "fb": "Correct answer: (a). This finding may surprise some readers (who associate the passive voice with abstraction). GPT-4o underuses the agentless passive, but it achieves a different kind of impersonality by turning actions into nouns through nominalizations ('the completion of the form').",
    },
    {
        "q": "On clausal co-ordination (linking full clauses with words like 'and' or 'but'), Reinhart et al. found:",
        "opts": ["All models avoid it equally", "Both GPT-4o models avoid it, while all Llama 3 variants use it more than humans", "Only humans use clausal co-ordination", "Llama 3 avoids it and GPT-4o overuses it"],
        "a": 1,
        "fb": "Correct answer: (b). The pattern is model-specific: the GPT-4o models link nouns to nouns (phrasal co-ordination at ~1.9× the human rate) rather than clauses to clauses, while Llama 3 variants co-ordinate clauses more than humans do.",
    },
    {
        "q": "Reinhart et al. compared base models with instruction-tuned models and concluded that the distinctive 'AI style':",
        "opts": ["Comes from the pretraining data and can't be changed", "Appears to be introduced by instruction tuning, since base model-produced text has style features closer to human norms", "Only appears in text produced by models below a certain size", "Disappears when models are given longer prompts"],
        "a": 1,
        "fb": "Correct answer: (b). Base models generated text with style features at rates much closer to human norms. The style seems to be a byproduct of tuning models to be helpful assistants, not an inevitable property of language models.",
    },
    {
        "q": "Which vocabulary finding did Reinhart et al. report?",
        "opts": ["LLMs avoid adjectives almost entirely", "Words like 'tapestry,' 'palpable,' 'intricate,' and 'underscore' appeared at 100 times or more the human rate in text produced by GPT-4o", "LLM-generated writing uses more slang than human writing", "LLM vocabulary varies dramatically by genre, unlike human vocabulary"],
        "a": 1,
        "fb": "Correct answer: (b). A handful of LLM-favorite words recur at extreme rates, and LLMs also fail to vary their style by genre the way humans do, producing text misaligned with its context.",
    },
]

DELUCA_PROMPTS = [
    "DeLuca et al. describe generated noun phrases whose content can range from vague to vapid, "
    "even though the prose is informationally *dense*. How can text be dense and vague at the "
    "same time? Try to explain this using one of the specific features from the reading.",

    "DeLuca et al. place ChatGPT's style somewhere in between novices and experts: denser than "
    "student writing, but without the audience awareness of published researchers, who use many "
    "of the same features (nominalizations, long noun phrases) with measurable, specific content. "
    "So where is the line between \"professional style\" and \"AI slop\"? Is it about the features "
    "themselves, or how they're used?",

    "Hedges and modals of possibility (\"might,\" \"could,\" \"seems to\") are often treated as "
    "weak writing. DeLuca et al. suggest the opposite: they keep prose open to other perspectives "
    "(and show intellectual humility). One complication: the same study finds that students "
    "co-ordinate whole clauses (with \"and\" or \"but\") more than experts do, even though the "
    "generated introductions use such co-ordination least of all. When have you been told to cut "
    "hedging or co-ordination from your writing, and do you now agree or disagree with that advice?",

    SHARED_PROMPT,
]

REINHART_PROMPTS = [
    "Reinhart et al. found that *base* models produce writing with style category rates much "
    "closer to human norms, and that instruction tuning appears to introduce the distinctive "
    "\"AI slop\" style rather than correct it. Why might the process of making models more "
    "\"helpful\" also make their writing less human?",

    SHARED_PROMPT,
]

DELUCA_INTRO = (
    "This is the first of our two studies of LLM-generated writing. DeLuca et al. collected 100 "
    "introductions written by ChatGPT and compared them with introductions written by "
    "undergraduate students and by published researchers, looking for specific, countable "
    "language features that differ among the three. This quiz checks whether you've picked up "
    "the key findings. It's self-graded and you can retry it, but you should do it honestly, "
    "because the activities in Units 1–3 all assume that you know these features."
)

REINHART_INTRO = (
    "This is the second of our two studies, and it widens the comparison. Where DeLuca et al. "
    "examined one genre in one field, Reinhart et al. compare several models against human "
    "writing across many kinds of text, and they separate base models from the instruction-tuned "
    "versions most of us actually use. Do the first reading check before this one: the features "
    "named there come up again here. This quiz is self-graded and you can retry it, but you "
    "should do it honestly, because the activities in Units 1–3 all assume that you know these "
    "features."
)

# Each spec drives one page. utils/reading_check.render() takes it from here.
DELUCA = {
    "key": "rc1",
    "kicker": "Readings · 1 of 2",
    "title": "Reading Check 1: How ChatGPT Writes an Introduction",
    "sub": "A comprehension check on DeLuca et al. (2025), plus discussion prompts for class. "
           "Complete this after you've read the article.",
    "intro": DELUCA_INTRO,
    "citations": [DELUCA_CITATION],
    "questions": DELUCA_QUESTIONS,
    "prompts": DELUCA_PROMPTS,
    "doc_title": "Reading Check 1: DeLuca et al. (2025)",
    "file_name": "ReadingCheck1_DeLuca_notes.docx",
}

REINHART = {
    "key": "rc2",
    "kicker": "Readings · 2 of 2",
    "title": "Reading Check 2: Do LLMs Write Like Humans?",
    "sub": "A comprehension check on Reinhart et al. (2025), plus discussion prompts for class. "
           "Complete this after you've read the article and finished Reading Check 1.",
    "intro": REINHART_INTRO,
    "citations": [REINHART_CITATION],
    "questions": REINHART_QUESTIONS,
    "prompts": REINHART_PROMPTS,
    "doc_title": "Reading Check 2: Reinhart et al. (2025)",
    "file_name": "ReadingCheck2_Reinhart_notes.docx",
}
