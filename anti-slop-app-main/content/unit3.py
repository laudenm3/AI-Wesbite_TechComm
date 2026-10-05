"""Unit 3 · Proposals for De-Slop-ification. Ported from Pollak_Unit3_Proposals_7-13-26.html.

Changes in the app version:
  - NEW text box for pasting the generated proposal, and NEW text box for the
    "two most important edits" paragraph listed under "Bring to class."
  - Typo fixed in the Modality check ("Every prediction about the future carries is
    appropriately hedged" -> "Every prediction about the future is appropriately hedged").
"""

UNIT = {
    "key": "u3",
    "kicker": "Course Unit 3 · Local Change Proposal",
    "title": "Proposals for De-Slop-ification",
    "sub": "Analyze how an LLM-generated proposal overstates and underexplains its case, and then compose your team's proposal from argument and narrative, aimed at an actual decisionmaker. Finish with a feature-by-feature editing pass.",
    "doc_title": "Unit 3: Proposals for De-Slop-ification",
    "file_name": "Unit3_Proposals.docx",
    "name_label": "Team members (appears on the downloaded file)",
    "goals_intro": "**What you'll do and why.** The reports studied in DeLuca et al. (2025) were written for a non-expert decisionmaker (a property developer weighing an investment), which is close to the rhetorical situation of a proposal. The pattern they document shows up here with particular force (and significant consequences): the model forecast outcomes with \"will\" while using \"may\" and \"might\" not at all, and it quoted results with minimal interpretation of their meaning, more as a laundry list than as an argument. A proposal that never hedges its claims reads as either naive or dishonest to an experienced decisionmaker, and a proposal built from abstractions gives that decisionmaker nothing to picture, remember, or repeat to their colleagues. It also doesn't clarify the human stakes of the issue enough. This unit works on both problems as it guides you to recognize AI slop style in proposals and write them more effectively.",
    "goals_lead": "your team should be able to",
    "goals": [
        "spot *overstatement* (a lack of hedging and modality) and *underexplanation* (a lack of illustrative examples and narratives) in an LLM-generated proposal;",
        "ground your own proposal in a clearly defined problem and solution, and in a story about real people;",
        "run a systematic de-slop editing pass on your draft.",
    ],
    "parts": [
        {
            "num": "Part 1", "title": "Analyze a generated proposal",
            "note": "Work in your project teams. Either generate a proposal or use the previously-generated example below.",
            "blocks": [
                {"type": "steps", "items": [
                    "If generating: in the university-licensed LLM chatbot, prompt: *\"Write a two-page proposal to [a university or local government office] recommending [a change your team is considering for your project].\"* Keep the prompt plain.",
                    "Read the output together, then complete the two diagnostic tasks below.",
                ]},
                {"type": "refusal", "text": "Teams opting out can complete both diagnostics with the previously-generated example below, which proposes a familiar kind of campus change."},
                {"type": "sample", "label": "Previously-generated example: LLM proposal for extended library hours (excerpt)",
                 "sections": [{"label": "", "text":
                    "**Proposal: Implementation of Extended Library Operating Hours**\n\n"
                    "*The implementation of extended operating hours at the undergraduate library represents a critical enhancement to the institution's academic support infrastructure. Current operational limitations create significant barriers to student success, undermining the university's commitment to fostering an equitable and accessible learning environment.*\n\n"
                    "*Extended hours will deliver transformative benefits across multiple dimensions of the student experience. The provision of additional late-night study space will drive measurable improvements in academic performance, enhancing student wellbeing and strengthening institutional retention outcomes. Students facing scheduling constraints stemming from employment obligations will gain essential access to critical academic resources, ensuring comprehensive support for diverse student populations.*\n\n"
                    "*The proposed initiative requires the allocation of additional staffing resources and the establishment of enhanced security protocols. These operational investments will be offset by substantial gains in student satisfaction, academic achievement, and institutional reputation, positioning the university as a leader in student-centered service delivery.*\n\n"
                    "*The adoption of this proposal underscores the institution's dedication to academic excellence and represents a decisive step toward the realization of a truly comprehensive learning ecosystem.*"}],
                 "note": "This excerpt was generated with a general-purpose LLM chatbot, and it has not been edited. It's included here so that teams practicing AI refusal can complete the analysis without generating text themselves."},
                # NEW in the app version
                {"type": "prompt", "id": "generated", "title": "The proposal you're analyzing",
                 "text": "Paste the generated proposal here. If you're using the previously-generated example, you can leave this blank.",
                 "placeholder": "Paste the generated proposal…", "height": 160},
                {"type": "prompt", "id": "diagA", "title": "Diagnostic A · Overstatement: where should this hedge?",
                 "text": "Find three claims stated as certainties that are actually predictions or possibilities (\"will deliver transformative benefits,\" \"will drive measurable improvements\"). For each, rewrite with hedges and/or modals of possibility (\"could,\" \"may,\" \"we expect,\" \"if X, then likely Y\"). Then answer: which version would an experienced administrator trust more, and why? Consider that unhedged predictions also create accountability problems: what happens when the \"measurable improvements\" don't materialize?",
                 "placeholder": "Quote three overstatements and rewrite each with more toned-down modality…"},
                {"type": "prompt", "id": "diagB", "title": "Diagnostic B · Underspecification: where are the people?",
                 "text": "Find three abstract phrases that gesture at human experience without any specific examples (\"students facing scheduling constraints stemming from employment obligations,\" \"diverse student populations\"). For each, sketch a concrete example or two-sentence narrative that could be added: a named (or realistically anonymized) student, a specific occasion or situation, a plausible or typical problem. What evidence would you need to gather to write those sentences honestly?",
                 "placeholder": "Quote three abstractions and draft a human story or anecdote to replace one of them…"},
                {"type": "hint", "text": "notice that these two problems are opposites: the proposal is too confident about future outcomes, but it's too vague about the present. DeLuca et al. saw the same pairing in a full GPT-4-generated report: flat predictions, and statistics quoted with little interpretation of what they meant for the problem. Human proposal writers tend to do the reverse: they hedge their predictions, and they describe the current problem in concrete detail that they've actually observed. Why might the latter combination be more persuasive?"},
            ],
        },
        {
            "num": "Part 2", "title": "Compose from argument and narrative",
            "note": "Now, build your team's actual proposal from the inside out. Answer these brainstorming questions before drafting any section.",
            "blocks": [
                {"type": "prompt", "id": "argument", "title": "Argument foundation (problem/solution)",
                 "text": "What problem do you want to define, and what solution do you want to advocate? State each part in one sentence that a stranger would understand. If you can't state these concisely yet, that's an intellectual gap that cannot be solved by AI.",
                 "placeholder": "Problem: … Solution: …"},
                {"type": "prompt", "id": "narrative", "title": "Narrative foundation",
                 "text": "Whose story are you trying to tell or uplift? Which specific people or groups of people are affected by this problem, what does their experience actually look like, and how will you learn about it (interviews, observation, survey, public data, your own experience...)?",
                 "placeholder": "The people at the center of this proposal are… Their experience looks like… We'll learn about it by…"},
                {"type": "prompt", "id": "audience", "title": "The actual human audience",
                 "text": "Name the real decisionmaker (a specific office or person at the university or in local government). What do they and their stakeholders value, what pressures are they under, and what would make saying yes easy or hard for them? Your hedging and your evidence should be tailored to this reader.",
                 "placeholder": "Our decisionmaker is… They care about… Saying yes is hard for them because…"},
            ],
        },
        {
            "num": "Part 3", "title": "The de-slop editing checklist",
            "note": "Apply this editing checklist to your full draft before submission. (It works for any document in this course, not only proposals, so bookmark it!) Check each item only after someone on the team has done a thorough pass, not just when you've agreed that it *sounds* done.",
            "blocks": [
                {"type": "check", "id": "c1", "title": "Nominalization sweep", "text": "Search the draft for \"-tion,\" \"-ment,\" and \"-ance\" words. For each, try the verb form with a human subject. Keep the noun only where the verb version is genuinely worse (for instance, if it reduces cohesion between sentences)."},
                {"type": "check", "id": "c2", "title": "Participial clause sweep", "text": "Search for \"-ing\" clauses attached to noun phrases. Where two or more stack in one sentence, break them into separate clauses joined with \"and,\" \"but,\" \"so,\" or \"because.\""},
                {"type": "check", "id": "c3", "title": "Dense noun phrase sweep", "text": "Flag any noun phrase of four or more words. Either unpack it, ground it with an example, or cut it."},
                {"type": "check", "id": "c4", "title": "Modality check", "text": "Every prediction about the future is appropriately hedged through modality (\"could,\" \"we expect,\" \"is likely to\"), and every claim about the present is backed by something you actually observed, read, and/or analyzed."},
                {"type": "check", "id": "c5", "title": "Example check", "text": "Every major abstract claim is followed within a sentence or two by a concrete example, number, or event from a real person's experience."},
                {"type": "check", "id": "c6", "title": "Coordination check", "text": "Ideas connect to ideas: the draft uses clause-level links (\"and this means,\" \"but it's worth noting,\" \"which could suggest\") rather than only comma-separated noun lists."},
                {"type": "check", "id": "c7", "title": "Favorite-word scan", "text": "Search for \"comprehensive,\" \"robust,\" \"leverage,\" \"underscore,\" \"transformative,\" \"seamless,\" \"foster,\" and \"ecosystem.\" Keep an instance of any of these only if you can defend its persuasive value."},
                {"type": "check", "id": "c8", "title": "The decisionmaker test", "text": "Imagine yourself in the persona of your named decisionmaker, and read the executive summary aloud. Can you repeat the problem, solution, and one memorable detail to a colleague after reading it once?"},
                # NEW in the app version
                {"type": "prompt", "id": "edits", "title": "Your two most important edits",
                 "text": "In one paragraph, note the two most important edits you made during this pass.",
                 "placeholder": "The two most important edits we made were…", "height": 140},
            ],
        },
    ],
    "deliver_label": "Bring to class / submit (one per team)",
    "deliver": [
        "The generated proposal (or the previously-generated example) with both diagnostics completed.",
        "Your Part 2 foundations: problem/solution, narrative plan, and decisionmaker analysis.",
        "Your proposal draft with the Part 3 checklist completed and one paragraph noting the two most important edits you made.",
    ],
    "footer": "Part of Writing Against AI Slop · Calvin Pollak · University of Washington. The style framework is drawn from DeLuca et al. (2025) and Reinhart et al. (2025); the refusal option follows Sano-Franchini, McIntyre, & Fernandes, \"Refusing GenAI in Writing Studies.\"",
}
