# Exercise Set 2 — Writing in a More Human Style: Genre Exercises.
# Genre-specific exercises in cover letters, instructional documents, and
# proposals, each with a model answer.

PAGE_METADATA = {
    "key": "exercise_set2_genre_exercises",
    "title": "Writing in a More Human Style: Genre Exercises",
    "unit_label": "Practice Anytime · Exercise Set 2",
    "icon": "📝",
    "overview": (
        "Genre-specific exercises for developing a verbal, hedged, clausal prose style, grounded in "
        "Markey et al. (2024) and Reinhart et al. (2025) — recognize AI slop style, revise it, and "
        "write against it across three genres where the contrast matters most: cover letters, "
        "instructional documents, and proposals."
    ),
}

STEPS = [
    # --- COVER LETTERS ---
    {
        "type": "sample",
        "title": "Genre notes: AI slop style vs. a more human style in cover letters",
        "content": (
            "Nominalization erases the \"I\" in cover letters (Markey et al.). The goal is to sound "
            "human and specific.\n\n"
            "- **AI slop style risk:** nominalizations bury the \"I\" (\"the management of client "
            "relationships\" instead of \"I managed client relationships\").\n"
            "- **A more human style approach:** keep verbs active and personal.\n"
            "- **Hedging:** hedging on fit and future claims is appropriate here, not weak — "
            "\"I believe this experience has prepared me\" is more credible than \"I am uniquely qualified.\""
        ),
    },
    {
        "type": "choice",
        "id": "cl_ex1",
        "name": "Cover Letters · Exercise 1 (Genre Awareness)",
        "question": (
            "Which opening is written in AI slop style, and why does it create problems in a cover letter?\n\n"
            "**Option 1:** The management of client relationships and the coordination of "
            "cross-departmental initiatives have constituted primary responsibilities throughout my "
            "professional tenure.\n\n"
            "**Option 2:** I have spent five years managing client relationships and coordinating "
            "projects across departments."
        ),
        "options": ["Option 1", "Option 2"],
        "answer": 0,
        "explanation": "Option 1 nominalizes away the \"I\" (\"the management of,\" \"the coordination of\") and reads as generic; Option 2 keeps the writer as the visible subject.",
    },
    {
        "type": "transform",
        "id": "cl_ex2",
        "name": "Cover Letters · Exercise 2 (Transformation)",
        "question": (
            "Rewrite this cover letter sentence in a more human style. Restore the \"I\", unpack the "
            "nominalizations into verbs, and add appropriate hedging where the claim is about the future."
        ),
        "passage": (
            "The completion of a master's degree in Environmental Policy and the undertaking of two "
            "internships with government agencies have provided a strong foundation for the pursuit of "
            "this role."
        ),
        "tip": "Try turning \"completion,\" \"undertaking,\" and \"pursuit\" back into verbs. Who completed? Who undertook? Add \"I feel that\" or \"I believe\" when making a claim about suitability.",
        "placeholder": "Write your more human version here…",
        "model_answer": (
            "I completed a master's degree in Environmental Policy and undertook two internships with "
            "government agencies, and I feel that these experiences have given me a strong foundation "
            "for this role."
        ),
        "height": 100,
    },
    {
        "type": "transform",
        "id": "cl_ex3",
        "name": "Cover Letters · Exercise 3 (Spot and Fix)",
        "question": (
            "The paragraph below is written in AI slop style. Identify the features that make it feel "
            "impersonal, then rewrite it in a more human style."
        ),
        "passage": (
            "The demonstrated acquisition of skills in data analysis and the consistent delivery of "
            "high-quality outputs throughout my tenure at Meridian Associates have resulted in a "
            "deepened understanding of the operational requirements of fast-paced environments. The "
            "development of strong collaborative relationships with cross-functional teams has further "
            "contributed to my professional growth."
        ),
        "tip": "Look for nominalizations (\"acquisition,\" \"delivery,\" \"development\") and restore the \"I\" as the subject of each action.",
        "placeholder": "Write your more human version here…",
        "model_answer": (
            "At Meridian Associates, I built strong data analysis skills and consistently delivered "
            "high-quality work, which deepened my understanding of what fast-paced environments demand. "
            "I also built strong working relationships across teams, which helped me grow professionally."
        ),
        "height": 130,
    },
    {
        "type": "choice",
        "id": "cl_ex4",
        "name": "Cover Letters · Exercise 4 (Hedging in Context)",
        "question": (
            "Which sentence uses hedging more appropriately for a cover letter claim about future "
            "contribution?\n\n"
            "**Option 1:** My comprehensive skill set guarantees the delivery of exceptional results and "
            "the achievement of all departmental objectives.\n\n"
            "**Option 2:** I believe my background in data analysis and project coordination would let me "
            "contribute meaningfully to your team's goals."
        ),
        "options": ["Option 1", "Option 2"],
        "answer": 1,
        "explanation": "Option 2 hedges an inherently uncertain future claim (\"I believe,\" \"would let me\") rather than guaranteeing outcomes no applicant can actually promise.",
    },
    # --- INSTRUCTIONAL DOCUMENTS ---
    {
        "type": "sample",
        "title": "Genre notes: AI slop style vs. a more human style in instructional writing",
        "content": (
            "AI slop style instructions obscure who does what and when via passive and nominal "
            "constructions. Interestingly, GPT-4o actually uses the agentless passive at about half the "
            "human rate — but compensates with heavy nominalization and participial clauses instead.\n\n"
            "- **Clarity:** turn actions into things (\"the completion of installation\") vs. name the "
            "agent (\"you complete installation\").\n"
            "- **Ambiguity risk:** agentless passives hide the actor (\"the file is downloaded\" — by whom?).\n"
            "- **Hedging:** practical hedging about timing (\"this usually takes a few minutes\") sets "
            "realistic expectations."
        ),
    },
    {
        "type": "choice",
        "id": "instr_ex1",
        "name": "Instructions · Exercise 1 (Clarity Comparison)",
        "question": (
            "Which instruction is easier to follow, and what specific AI slop style features make the "
            "other one harder?\n\n"
            "**Option 1:** Commencement of the installation process requires verification of system "
            "requirements, followed by downloading of the most recent software version.\n\n"
            "**Option 2:** Before you start the installation, check that your system meets the "
            "requirements and download the most recent version of the software."
        ),
        "options": ["Option 1", "Option 2"],
        "answer": 1,
        "explanation": "Option 1 buries three actions in nominalizations (\"commencement,\" \"verification,\" \"downloading\") with no named subject; Option 2 makes \"you\" the actor of each step.",
    },
    {
        "type": "transform",
        "id": "instr_ex2",
        "name": "Instructions · Exercise 2 (Transformation)",
        "question": (
            "Rewrite this AI-slop-style instruction paragraph in a more human style. Use \"you\", active "
            "verbs, and imperative mood where appropriate. Add a hedged note about timing."
        ),
        "passage": (
            "The successful completion of the application requires the provision of three professional "
            "references, the submission of a personal statement not exceeding 500 words, and the payment "
            "of the non-refundable processing fee prior to the deadline."
        ),
        "tip": "Turn \"provision,\" \"submission,\" and \"payment\" into verbs with \"you\" as the subject, and add a realistic, hedged timing note.",
        "placeholder": "Write your more human version here…",
        "model_answer": (
            "To complete your application, you will need to provide three professional references, "
            "submit a personal statement of no more than 500 words, and pay the non-refundable "
            "processing fee before the deadline. Please note that processing may take up to five working "
            "days, so we recommend submitting as early as possible."
        ),
        "height": 130,
    },
    {
        "type": "transform",
        "id": "instr_ex3",
        "name": "Instructions · Exercise 3 (Spot the Ambiguity)",
        "question": (
            "This AI-slop-style manual excerpt has several points of ambiguity; it is often unclear who "
            "acts, when, or under what conditions. Identify at least three problems, then rewrite in a "
            "more human style."
        ),
        "passage": (
            "Initial setup is completed through the selection of preferred configuration options. "
            "Adjustment of settings should be undertaken prior to first use. In cases where errors are "
            "encountered, troubleshooting steps as outlined in section 4 should be followed."
        ),
        "tip": "Ask: who selects the options? who adjusts the settings? who follows the troubleshooting steps, and when exactly?",
        "placeholder": "Write your more human version here…",
        "model_answer": (
            "To finish setup, choose your preferred configuration options. Adjust these settings before "
            "you use the tool for the first time. If you run into an error, follow the troubleshooting "
            "steps in section 4."
        ),
        "height": 130,
    },
    {
        "type": "transform",
        "id": "instr_ex4",
        "name": "Instructions · Exercise 4 (Adding Appropriate Hedges)",
        "question": (
            "These instructions are written with appropriately human-style verbs and agents, but they "
            "make claims that are too absolute. Add hedging to acknowledge variation and help users set "
            "realistic expectations."
        ),
        "passage": (
            "Step 3: The verification email arrives in your inbox within two minutes. If you do not see "
            "it, check your spam folder. The link in the email expires after 24 hours. Clicking the link "
            "activates your account immediately."
        ),
        "tip": "Where might timing actually vary? Add words like \"should typically,\" \"may take a little longer,\" \"it is worth checking,\" or \"may occasionally.\"",
        "placeholder": "Write your more human version here…",
        "model_answer": (
            "Step 3: The verification email should typically arrive in your inbox within two minutes, "
            "though it may occasionally take a little longer. If you do not see it, it is worth checking "
            "your spam folder. The link in the email expires after 24 hours. Clicking the link should "
            "activate your account right away."
        ),
        "height": 130,
    },
    # --- PROPOSALS ---
    {
        "type": "sample",
        "title": "Genre notes: AI slop style vs. a more human style in proposals",
        "content": (
            "Proposals require calibrated hedging as intellectual honesty, not weakness. Overconfident "
            "AI-slop-style claims seem naive to an experienced reader.\n\n"
            "- **The AI slop style trap:** \"This program will eliminate absenteeism across all "
            "departments.\"\n"
            "- **A more human style hedging:** \"This program is likely to meaningfully reduce "
            "absenteeism in most departments.\"\n"
            "- **Calibration:** too much hedging is also bad — a proposal that hedges every clause "
            "stops making an argument at all."
        ),
    },
    {
        "type": "choice",
        "id": "prop_ex1",
        "name": "Proposals · Exercise 1 (Identifying Overconfidence)",
        "question": (
            "Which proposal sentence is problematically overconfident (AI slop style), and which "
            "demonstrates appropriately calibrated hedging (a more human style)?\n\n"
            "**Option 1:** This initiative will result in the complete elimination of absenteeism across "
            "all departments.\n\n"
            "**Option 2:** Based on outcomes at peer institutions, this initiative could meaningfully "
            "reduce absenteeism in most departments within the first year."
        ),
        "options": ["Option 1", "Option 2"],
        "answer": 1,
        "explanation": "Option 1 promises a guaranteed, total outcome no program can honestly deliver; Option 2 ties a calibrated claim to evidence and a timeframe.",
    },
    {
        "type": "transform",
        "id": "prop_ex2",
        "name": "Proposals · Exercise 2 (Adding Calibrated Hedges)",
        "question": (
            "This proposal sentence makes every claim with complete certainty. Add hedging to make it "
            "credible, but do not hedge so much that the argument collapses."
        ),
        "passage": (
            "The redesign of the library study spaces will attract more students to campus, improve "
            "academic performance across all year groups, and increase satisfaction scores in the annual "
            "student survey."
        ),
        "tip": "You don't need to hedge every clause — pick the claims that are genuinely uncertain predictions and calibrate those.",
        "placeholder": "Write your more human version here…",
        "model_answer": (
            "The redesign of the library study spaces is likely to attract more students to campus and "
            "could improve academic performance in some year groups; we also expect it to increase "
            "satisfaction scores in the annual student survey."
        ),
        "height": 130,
    },
    {
        "type": "transform",
        "id": "prop_ex3",
        "name": "Proposals · Exercise 3 (Spot and Fix)",
        "question": (
            "This proposal paragraph uses heavy AI-slop-style nominalization and no hedging. Identify "
            "the nominalization chains, then rewrite in a more human style with appropriate hedges and "
            "verbal style."
        ),
        "passage": (
            "The implementation of a peer mentoring programme, informed by the identification of high "
            "attrition rates among first-year students, will facilitate the achievement of improved "
            "retention outcomes and the fostering of a stronger sense of campus belonging."
        ),
        "tip": "Look for \"implementation,\" \"identification,\" \"achievement,\" and \"fostering\" — each is hiding a verb and an actor.",
        "placeholder": "Write your more human version here…",
        "model_answer": (
            "Because we've identified high attrition rates among first-year students, we propose "
            "implementing a peer mentoring program. We expect this to help improve retention and could "
            "foster a stronger sense of campus belonging."
        ),
        "height": 130,
    },
    {
        "type": "rank",
        "id": "prop_ex4",
        "name": "Proposals · Exercise 4 (Calibration Exercise)",
        "question": (
            "Rank these three versions of the same proposal claim from weakest to strongest. Consider: "
            "which is overconfident (AI slop style), which is appropriately hedged (a more human style; "
            "good), and which is over-hedged (excessively)?"
        ),
        "versions": [
            {
                "label": "Version A",
                "text": "This new advising model will dramatically improve student outcomes and will transform the department.",
            },
            {
                "label": "Version B",
                "text": "This new advising model is likely to improve student outcomes and could meaningfully change how the department operates.",
            },
            {
                "label": "Version C",
                "text": "This new advising model might perhaps possibly improve some student outcomes, and it could conceivably, in some cases, tentatively change how the department operates.",
            },
        ],
        # correct_order lists version indices from weakest to strongest
        "correct_order": [2, 0, 1],
        "explanation": (
            "**Weakest (over-hedged): Version C** — stacking qualifiers (\"might perhaps possibly,\" "
            "\"could conceivably… tentatively\") drains the sentence of any claim at all.\n\n"
            "**Problematic (overconfident): Version A** — \"will dramatically improve… will transform\" "
            "promises certainty no proposal can honestly deliver.\n\n"
            "**Strongest (calibrated): Version B** — \"is likely to… could meaningfully\" makes a real "
            "claim while acknowledging it's a prediction."
        ),
    },
]
