"""Exercise Set 2: Writing in a More Human Style (genre exercises).

Ported from Pollak_SlopVsHuman_genre-exercises_3-3-26.html, with the September
2026 carryover fixes applied (see CHANGES at the bottom of this file).

Exercise types:
  choose    - pick one of two options; has "answer" (0 or 1) and "explanation"
  transform - rewrite a passage; has "tip" and "model"
  spotfix   - find features, then rewrite; "features" lists phrases to highlight
  rank      - put three versions in order; "ranking" is the correct order, weakest first
"""

INTRO = (
    "The style comparison framework used in these exercises is drawn from two research articles: "
    "DeLuca et al. (2025) and Reinhart et al. (2025). Together, these studies find that "
    "instruction-tuned LLMs produce a distinctive style: far more informationally dense than "
    "student writing, with nominalizations and present participial clauses used at roughly one and "
    "a half to five times the human rate, and with the hedges, modals of possibility, and clausal "
    "co-ordination that human writers use to qualify and connect their claims largely absent. "
    "Because this style is increasingly present in writing produced with AI assistance (and it can "
    "easily be absorbed into a writer's own habits), these exercises focus on developing the "
    "ability to recognize it, revise it, and write against it across three genres where the "
    "contrast matters most."
)

CITATIONS = [
    "DeLuca, L. S., Reinhart, A., Weinberg, G., Laudenbach, M., Miller, S., & Brown, D. W. (2025). "
    "Developing students’ statistical expertise through writing in the age of AI. *Journal of "
    "Statistics and Data Science Education, 33*(3), 266–278.",
    "Reinhart, A., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., Weinberg, G., & Brown, D. W. "
    "(2025). Do LLMs write like humans? Variation in grammatical and rhetorical styles. "
    "*Proceedings of the National Academy of Sciences, 122*(8), e2422455122.",
]

GENRES = [
    {
        "id": "cover", "label": "Cover Letters", "icon": ":material/mail:",
        "note": {
            "heading": "AI slop style vs. a more human style in cover letters",
            "body": "Many applicants reach for AI slop style because it sounds \"professional\", but it often produces the opposite effect. When verbs are turned into nouns, the person behind the letter disappears: instead of someone who did things, the reader sees a list of abstract qualities. DeLuca et al. (2025) found that ChatGPT-generated text is far more informationally dense than student writing, compressing information into noun phrases whose content can stay vague, and that it barely hedges its claims. In a cover letter, that style also crowds out the first-person voice that makes a letter sound like it came from a person. A more human style restores the writer as an active agent, uses verbs to describe concrete actions, and adds appropriate hedging when describing future fit. The goal is not to sound modest; it is to sound human and specific.",
            "bullets": [
                {"label": "AI slop style risk", "text": "Nominalizations bury the \"I\": \"My demonstrated expertise in stakeholder engagement…\" reads like a CV, not a letter."},
                {"label": "A more human approach", "text": "Keep verbs active and personal: \"I have spent five years managing…\" is warmer and more direct."},
                {"label": "Hedging", "text": "In a more human style, hedging is appropriate for claims about fit and the future: \"I believe I would contribute…\" signals self-awareness, not weakness."},
            ],
        },
        "exercises": [
            {
                "type": "choose", "tag": "Genre awareness",
                "question": "Which opening is written in AI slop style, and why does it create problems in a cover letter?",
                "options": [
                    {"label": "Option 1", "text": "My extensive background in the management of client relationships and the development of strategic communications frameworks, combined with a sustained commitment to the delivery of high-quality outputs, positions me as an ideal candidate for this role."},
                    {"label": "Option 2", "text": "I have spent five years managing client relationships and developing communications strategies, and throughout that time I have tried to deliver consistently high-quality work. I believe these experiences make me a strong candidate for this role."},
                ],
                "answer": 0,
                "explanation": "Option 1 is AI slop style. The nominalizations ('management', 'development', 'delivery', 'commitment') turn actions into abstract nouns and push the writer out of the sentence, so there is no 'I' doing anything. Reinhart et al. (2025) found instruction-tuned LLMs use nominalizations at 1.5–2× the human rate, and DeLuca et al. (2025) found that this nominalization-heavy style compresses information into noun phrases whose content, as they put it, can range from vague to vapid. Option 2 uses verbs ('managing', 'developing', 'deliver') and restores the writer as an active agent with a voice.",
            },
            {
                "type": "transform", "tag": "Transformation",
                "question": "Rewrite this cover letter sentence in a more human style. Restore the 'I', unpack the nominalizations into verbs, and add appropriate hedging where the claim is about the future.",
                "passage": "The completion of a master's degree in Environmental Policy and the undertaking of two internships with government agencies have provided a strong foundation for the pursuit of this role.",
                "tip": "Try turning 'completion', 'undertaking', and 'pursuit' back into verbs. Who completed? Who undertook? Add 'I feel that' or 'I believe' when making a claim about suitability.",
                "model": "I completed a master's degree in Environmental Policy and undertook two internships with government agencies, and I feel that these experiences have given me a strong foundation for this role.",
            },
            {
                "type": "spotfix", "tag": "Spot and fix",
                "question": "The paragraph below is written in AI slop style. Identify the features that make it feel impersonal, then rewrite it in a more human style.",
                "passage": "The demonstrated acquisition of skills in data analysis and the consistent delivery of high-quality outputs throughout my tenure at Meridian Associates have resulted in a deepened understanding of the operational requirements of fast-paced environments. The development of strong collaborative relationships with cross-functional teams has further contributed to my professional growth.",
                "features": ["acquisition of skills", "delivery of high-quality outputs", "tenure", "resulted in a deepened understanding", "development of strong collaborative relationships", "contributed to my professional growth"],
                "tip": "Each nominalization hides a verb. 'Acquisition of skills' = 'I developed skills'. Try starting with 'During my time at…' and convert each noun phrase into a clause.",
                "model": "During my time at Meridian Associates, I developed skills in data analysis and consistently delivered high-quality work, which helped me to understand what fast-paced environments demand. I also built strong working relationships with colleagues across different teams, and I feel that this has shaped how I work and collaborate.",
            },
            {
                "type": "choose", "tag": "Hedging in context",
                "question": "Which sentence uses hedging more appropriately for a cover letter claim about future contribution?",
                "options": [
                    {"label": "Option 1", "text": "A strong alignment between my professional development trajectory and the innovation-focused culture of your organization motivates my application and guarantees a meaningful contribution to your team."},
                    {"label": "Option 2", "text": "I am applying because I feel that the direction my career has taken so far aligns well with the innovative culture your organization seems to foster, and I believe I could contribute meaningfully to your team."},
                ],
                "answer": 1,
                "explanation": "Option 2 hedges appropriately: 'I feel that', 'seems to foster', and 'I believe I could' all signal self-awareness about an uncertain future. DeLuca et al. (2025) found that ChatGPT used the predictive modal will 199 times across 100 introductions, while may, might, and could did not appear at all, producing prose that barely modulates its confidence, and this is the opposite of what a cover letter needs. Hedging is not weakness; it signals the kind of self-aware voice that distinguishes human writing. Option 1's 'guarantees a meaningful contribution' is overconfident (no one can guarantee this), and 'professional development trajectory' is a nominalized, jargon-heavy noun phrase that sounds hollow.",
            },
        ],
    },
    {
        "id": "instructions", "label": "Instructional Documents", "icon": ":material/list:",
        "note": {
            "heading": "AI slop style vs. a more human style in instructional writing",
            "body": "Instruction writing has its own version of the contrast between AI slop style and a more human style. AI slop style tends to produce passive, impersonal, noun-heavy instructions that obscure who does what and when. Reinhart et al. (2025) found that instruction-tuned LLMs use nominalizations at 1.5–2× the human rate; these patterns become serious usability problems in instructions. Interestingly, they also found that GPT-4o actually uses the agentless passive at roughly half the human rate, but pairs this with far more nominalization and participial modification, which creates a different kind of impersonality: actions are hidden inside noun phrases rather than passive constructions. A more human style, with its preference for active verbs and explicit agents, naturally produces clearer, more usable instructions. In this genre, hedging is also important: good instructions acknowledge when steps may vary, when users need to make judgments, or when something might take longer than expected.",
            "bullets": [
                {"label": "Clarity", "text": "AI slop style turns actions into things: 'completion of the registration process requires the submission of…'. A more human style names the agent: 'To register, you will need to submit…'"},
                {"label": "Ambiguity risk", "text": "Agentless passives hide who does what: 'The form should be signed' (signed by whom?). A more human style says: 'You should sign the form before…'"},
                {"label": "Hedging", "text": "In instructions, hedging is practical: 'This typically takes around ten minutes, though it may take longer depending on your connection.'"},
            ],
        },
        "exercises": [
            {
                "type": "choose", "tag": "Clarity comparison",
                "question": "Which instruction is easier to follow, and what specific AI slop style features make the other one harder?",
                "options": [
                    {"label": "Option 1", "text": "Prior to the commencement of the installation procedure, verification of system compatibility requirements and the downloading of the most recent version of the software should be undertaken by the user."},
                    {"label": "Option 2", "text": "Before you start the installation, check that your system meets the requirements and download the most recent version of the software."},
                ],
                "answer": 1,
                "explanation": "Option 2 is far clearer. Option 1 uses three nominalizations ('commencement', 'verification', 'downloading') which turn actions into abstract things. The passive 'should be undertaken by the user' is also roundabout; Option 2 simply says 'check' and 'download', using imperative verbs directed at 'you'. Reinhart et al. (2025) found instruction-tuned LLMs use present participial clauses at 2–5× the human rate and nominalizations at 1.5–2× the rate, and these are especially disorienting in instructions, where clarity of action is paramount. DeLuca et al. (2025) found that generated noun phrases are often dense but vague, and in instructions that vagueness means the reader can't tell what to physically do.",
            },
            {
                "type": "transform", "tag": "Transformation",
                "question": "Rewrite this AI slop style instruction paragraph in a more human style. Use 'you', active verbs, and imperative mood where appropriate. Add a hedged note about timing.",
                "passage": "The successful completion of the application requires the provision of three professional references, the submission of a personal statement not exceeding 500 words, and the payment of the non-refundable processing fee prior to the deadline.",
                "tip": "Start with 'To complete your application…' and list the actions as imperatives or 'you will need to' constructions. Add something like 'Please note that…' for the deadline, and a hedged note about processing time.",
                "model": "To complete your application, you will need to provide three professional references, submit a personal statement of no more than 500 words, and pay the non-refundable processing fee before the deadline. Please note that processing may take up to five working days, so we recommend submitting as early as possible.",
            },
            {
                "type": "spotfix", "tag": "Spot the ambiguity",
                "question": "This AI slop style manual excerpt has several points of ambiguity; it is often unclear who acts, when, or under what conditions. Identify at least three problems, then rewrite it in a more human style.",
                "passage": "Following the completion of initial setup, configuration adjustments may be required. Adjustment of display settings and the modification of notification preferences can be accessed through the Settings menu. In the event of error occurrence, the execution of a system restart is recommended prior to the undertaking of further troubleshooting steps.",
                "features": ["completion of initial setup", "configuration adjustments may be required", "can be accessed", "error occurrence", "execution of a system restart is recommended", "undertaking of further troubleshooting steps"],
                "tip": "For each nominalization, ask: who does this? When? Under what conditions? Try 'Once you have completed…', 'you may need to…', 'If you see an error…'",
                "model": "Once you have completed the initial setup, you may need to adjust some settings. You can change your display settings and notification preferences in the Settings menu. If an error appears, we recommend restarting the system before you try any further troubleshooting steps.",
            },
            {
                "type": "transform", "tag": "Adding appropriate hedges",
                "question": "These instructions already use clear verbs and name the agent, but they make claims that are too absolute. Add hedging to acknowledge variation and help users set realistic expectations.",
                "passage": "Step 3: The verification email arrives in your inbox within two minutes. If you do not see it, check your spam folder. The link in the email expires after 24 hours. Clicking the link activates your account immediately.",
                "tip": "Think about what might vary: email delivery speed, spam filters, activation time. Use hedges like 'typically', 'should', 'usually', 'may', 'in most cases'.",
                "model": "Step 3: The verification email should typically arrive in your inbox within two minutes, though in some cases it may take a little longer. If you do not see it, it is worth checking your spam folder. Please note that the link in the email will expire after 24 hours. Once you click the link, your account should be activated, though it may occasionally take a few minutes to update.",
            },
        ],
    },
    {
        "id": "proposals", "label": "Proposals", "icon": ":material/description:",
        "note": {
            "heading": "AI slop style vs. a more human style in proposals",
            "body": "Proposals are where the tension between AI slop style and a more human style is most educationally interesting. Writers often reach for AI slop style because it sounds authoritative, but proposals make claims about uncertain futures, so appropriate hedging is not weakness. It is intellectual honesty, and it is often more persuasive. DeLuca et al. (2025) found that ChatGPT-generated introductions used almost no modals of possibility (will appeared 199 times; may, might, and could not at all), which produces writing that barely modulates its confidence. Reinhart et al. (2025) further found that base models write much closer to human norms, which suggests that instruction tuning itself introduces the dense, noun-heavy style. That makes the overconfidence of AI slop style a systematic feature of LLM writing rather than a quirk of one prompt. An overconfident AI slop style proposal can seem naive or unaware of complexity. A well-hedged proposal in a more human style shows that the writer has thought carefully about what might happen and under what conditions. The key is calibrated hedging: not so much that the argument collapses, but enough to be credible.",
            "bullets": [
                {"label": "The AI slop style trap", "text": "'Implementation of this scheme will result in a 30% reduction in costs.' No proposal can guarantee this. The overconfidence invites skepticism."},
                {"label": "Hedging in a more human style", "text": "'Evidence suggests this scheme could reduce costs by around 30%, though this would depend on…' This version acknowledges uncertainty while still making a case."},
                {"label": "Calibration", "text": "Too much hedging weakens proposals just as much as too little. A more human style aims for precision about uncertainty, not endless qualification."},
            ],
        },
        "exercises": [
            {
                "type": "choose", "tag": "Identifying overconfidence",
                "question": "Which proposal sentence is problematically overconfident (AI slop style), and which demonstrates appropriately calibrated hedging (a more human style)?",
                "options": [
                    {"label": "Option 1", "text": "The introduction of a four-day working week will result in increased staff retention, the elimination of absenteeism, and measurable improvements in productivity across all departments."},
                    {"label": "Option 2", "text": "Evidence from pilot programs in comparable organizations suggests that introducing a four-day working week might lead to improved staff retention and reduced absenteeism, though the effects on productivity would likely vary across departments."},
                ],
                "answer": 1,
                "explanation": "Option 1 is AI slop style overconfidence: 'will result in', 'elimination of', and 'across all departments' make claims no proposal can guarantee. 'Elimination of absenteeism' is particularly problematic; implausible claims undermine credibility. Option 2 grounds the claim in evidence ('pilot programs'), uses appropriate hedges ('suggests', 'might lead to', 'would likely vary'), and honestly acknowledges variation across departments. DeLuca et al. (2025) found that LLM-generated text uses almost no hedges or modals of possibility, producing writing that barely modulates its confidence, and this is exactly the overconfidence problem in Option 1.",
            },
            {
                "type": "transform", "tag": "Adding calibrated hedges",
                "question": "This proposal sentence makes every claim with complete certainty. Add hedging to make it credible, but do not hedge so much that the argument collapses.",
                "passage": "The redesign of the library study spaces will attract more students to campus, improve academic performance across all year groups, and increase satisfaction scores in the annual student survey.",
                "tip": "Try grounding each claim in evidence or reasoning ('based on feedback…', 'research suggests…'). Use 'could', 'might', 'seems likely to'. Acknowledge that effects may vary. But keep the overall argument positive and clear.",
                "model": "Redesigning the library study spaces could attract more students to campus and might contribute to improved academic performance, particularly for students who currently find the existing spaces difficult to work in. Based on feedback collected during our consultation, we would also expect satisfaction scores in the annual student survey to improve, though the size of any effect would depend on how extensively the spaces are used.",
            },
            {
                "type": "spotfix", "tag": "Spot and fix",
                "question": "This proposal paragraph uses heavy AI slop style nominalization and no hedging. Identify the nominalization chains, then rewrite it in a more human style with appropriate hedges and verbs.",
                "passage": "The implementation of a peer mentoring program represents a strategic response to the identification of high attrition rates among first-year students and would result in the provision of structured social support mechanisms facilitating the development of community belonging and the reduction of social isolation.",
                "features": ["implementation", "identification of high attrition rates", "provision of structured social support mechanisms", "development of community belonging", "reduction of social isolation"],
                "tip": "Start with 'We are proposing to…' and unpack each nominalization: 'implementation' = 'implement', 'provision of support' = 'provide support'. Add hedges when describing expected outcomes.",
                "model": "We are proposing to implement a peer mentoring program in response to the high attrition rates we have identified among first-year students. We believe this program could provide structured social support and might help students to develop a stronger sense of belonging within the university community, which could in turn reduce the social isolation that seems to contribute to early withdrawal.",
            },
            {
                "type": "rank", "tag": "Calibration exercise",
                "question": "Rank these three versions of the same proposal claim from weakest to strongest. Consider: which is overconfident (AI slop style), which is appropriately hedged (a more human style), and which is over-hedged?",
                "options": [
                    {"label": "Version A", "text": "This intervention will dramatically improve student wellbeing across all year groups and will transform the student experience within one academic year."},
                    {"label": "Version B", "text": "This intervention seems likely to improve student wellbeing, particularly for students in their first year, though the extent of the effect may vary depending on uptake and individual circumstances."},
                    {"label": "Version C", "text": "It is perhaps possible that, under certain circumstances, some students might conceivably experience what could tentatively be described as a modest improvement in some aspects of their wellbeing, though this cannot be confirmed at this stage."},
                ],
                "ranking": ["Version C", "Version A", "Version B"],
                "rankLabels": ["Weakest (over-hedged)", "Problematic (overconfident)", "Strongest (calibrated)"],
                "explanation": "Version C (weakest) is over-hedged to the point of paralysis: stacking 'perhaps', 'possible', 'might conceivably', 'tentatively', 'could be described as' signals that the writer has no confidence in their own proposal. Version A (problematic) commits the opposite error: 'will dramatically improve' and 'will transform' are overconfident claims that invite skepticism; as DeLuca et al. (2025) found, this kind of unmodulated confidence, without hedges or modals of possibility, is a defining characteristic of LLM-generated text. Version B (strongest) is calibrated: 'seems likely', 'particularly for', 'may vary depending on' acknowledge uncertainty honestly while still making a positive, coherent case.",
            },
        ],
    },
]

# CHANGES (September 2026), for Calvin's reference:
# - Intro: "significantly more informationally dense than even professional human writing"
#   -> "far more informationally dense than student writing" (DeLuca's experts had the
#   longest noun phrases). "keep human prose open and dialogic" -> "qualify and connect".
# - "a more human style" find-and-replace leftovers fixed (lowercase sentence starts, and
#   uses as a modifier like "a more human style hedging").
# - Markey-era framing ("closed to alternative perspectives", "dialogic") replaced with
#   DeLuca's "barely modulates its confidence".
# - Cover letter note: removed "first-person engagement" from the DeLuca attribution
#   (their study was of report introductions); kept the point as a genre claim.
# - Instructions ex. 1: DeLuca claim reworded so it no longer says they studied instructions.
# - Proposals note: removed "even when prompted to write differently" (not verified in
#   Reinhart et al.); replaced with the base-model finding.
# - British spellings changed to American (organization, program, skepticism, judgments).
