"""Unit 1 · Anti-Slop Cover Letters. Ported from Pollak_Unit1_CoverLetters_7-13-26.html.

Two text boxes are new in the app version (marked NEW below): a place to paste the
generated letter, and a place for the short reflection listed under "Bring to class."
They let the Word download hold the whole submission.
"""

UNIT = {
    "key": "u1",
    "kicker": "Course Unit 1 · Job Application Package",
    "title": "Anti-Slop Cover Letters",
    "sub": "Generate a cover letter with an LLM and investigate its peculiar style, and then draft your own letter \"inside-out\" from your best stories (that part, the LLM can't do for you).",
    "doc_title": "Unit 1: Anti-Slop Cover Letters",
    "file_name": "Unit1_CoverLetters.docx",
    "name_label": "Your name (appears on the downloaded file)",
    "goals_intro": "**What you'll do and why.** LLM-generated cover letters tend to be dense, generic, and unhedged, and they almost never tell a concrete story. Hiring managers read hundreds of letters and many are getting good at spotting these patterns. In this activity you'll see the pattern up close in a letter generated from *your own* materials, and then you'll develop content for your own letter based on your actual, lived experiences.",
    "goals_lead": "you should be able to",
    "goals": [
        "identify at least four of the six style features from the readings in an LLM-generated cover letter;",
        "explain why each one weakens the letter for a human reader;",
        "draft two or three STAR stories from your own experience and build a letter outward from the strongest one.",
    ],
    "parts": [
        {
            "num": "Part 1", "title": "Generate a letter from your materials",
            "note": "Work individually. You'll need your current resume and one real job or internship ad you'd plausibly apply to.",
            "blocks": [
                {"type": "steps", "items": [
                    "Open the university-licensed LLM chatbot (use the tool designated in the syllabus, not your personal account, so your materials stay within the licensed environment).",
                    "Upload your resume and paste in the full text of the job ad.",
                    "Prompt it plainly: *\"Write a one-page cover letter applying to this job based on my resume.\"* Don't coach it toward better style; we want its default behavior.",
                    "Paste the output into the box below so it's included in your download (or copy it into a doc, or print it).",
                ]},
                {"type": "refusal", "text": "You can always refuse generative AI use in this course, and you never need to justify this ethical decision. If you're opting out, use the previously-generated example below for Parts 1–2; it was generated in advance from a fictional student resume and a job ad, so you can do the same analysis without prompting anything yourself."},
                {"type": "sample", "label": "Previously-generated example: fictional resume, job ad, and LLM cover letter",
                 "sections": [
                     {"label": "The fictional applicant (resume summary)",
                      "text": "**Jordan Reyes**, a third-year Communication major at UW. Experience: two years as a barista and shift lead at a campus café (trained 6 new hires, handled scheduling for a 12-person team); social media volunteer for a campus food-security nonprofit (grew Instagram from 400 to 1,900 followers over two quarters; ran a donation drive that collected 800 lbs of food); course projects in technical writing and data visualization."},
                     {"label": "The job ad (excerpt)",
                      "text": "**Communications & Outreach Intern — Sound Transit Community Engagement Office.** Support public outreach for transit expansion projects. Duties: draft social posts and newsletter content for non-expert audiences, help staff community open-house events, summarize public comments for project teams. We value clear plain-language writing, comfort talking with the public, and the ability to make complex project information understandable."},
                     {"label": "The LLM-generated cover letter (unedited)",
                      "text": "*Dear Hiring Committee,*\n\n*I am writing to express my enthusiastic interest in the Communications & Outreach Intern position at Sound Transit. As a dedicated Communication major possessing a robust foundation in strategic content creation and community engagement, I am confident that my comprehensive skill set aligns seamlessly with the requirements of this dynamic role.*\n\n*Throughout my academic and professional journey, I have consistently demonstrated a commitment to excellence in stakeholder communication. My experience managing social media operations for a campus nonprofit organization, driving significant audience growth and fostering meaningful community connections, underscores my capacity for impactful digital storytelling. Additionally, my leadership experience in a fast-paced customer service environment, encompassing team training, scheduling coordination, and operational optimization, has equipped me with exceptional interpersonal and organizational capabilities.*\n\n*The implementation of effective public outreach strategies requires a multifaceted approach integrating clear communication, audience awareness, and collaborative problem-solving. I am eager to leverage my proven abilities in content development and community engagement to support Sound Transit's mission of delivering transformative transit solutions to the region.*\n\n*Thank you for considering my application. I look forward to the opportunity to contribute to your team's continued success.*\n\n*Sincerely,*  \n*Jordan Reyes*"},
                 ],
                 "note": "This letter was generated with a general-purpose LLM chatbot from the materials above, and it has not been edited. It's included here so that students practicing AI refusal can complete the analysis without generating text themselves."},
                # NEW in the app version
                {"type": "prompt", "id": "letter", "title": "The letter you're analyzing",
                 "text": "Paste the generated letter here. If you're using the previously-generated example, you can leave this blank.",
                 "placeholder": "Paste the generated letter…", "height": 160},
            ],
        },
        {
            "num": "Part 2", "title": "Investigate the letter",
            "note": "Work through the six features from DeLuca et al. (2025) and Reinhart et al. (2025). For each one, check it off once you've searched the letter, and note down what you found (a quoted phrase, or \"none found\").",
            "blocks": [
                {"type": "audit", "id": "f1", "title": "1 · Nominalizations",
                 "text": "Actions turned into abstract nouns: \"the implementation of,\" \"coordination,\" \"optimization.\" Find at least two. For each, what's the buried verb, and who is its missing subject?",
                 "placeholder": "Quote the phrases and name the buried verbs…"},
                {"type": "audit", "id": "f2", "title": "2 · Present participial clauses",
                 "text": "\"-ing\" clauses stacked onto noun phrases: \"…possessing a robust foundation,\" \"…driving significant audience growth.\" Research finding: instruction-tuned models use these at 2–5× the human rate. How many can you find in one sentence?",
                 "placeholder": "Quote a sentence and count its participial clauses…"},
                {"type": "audit", "id": "f3", "title": "3 · Dense noun phrases",
                 "text": "Long modifier chains: \"comprehensive skill set,\" \"strategic content creation.\" Pick the densest one. Does the letter ever unpack it with a concrete detail, or does it stay abstract?",
                 "placeholder": "Quote the densest noun phrase and say whether it ever gets grounded…"},
                {"type": "audit", "id": "f4", "title": "4 · Missing hedges and modality",
                 "text": "Generated text barely modulates its confidence: in DeLuca et al.’s samples, ChatGPT used \"will\" 199 times across 100 introductions, while \"may,\" \"might,\" and \"could\" did not appear at all. Find the most overstated claim in the letter. How would a thoughtful human applicant have qualified it?",
                 "placeholder": "Quote the overstatement and rewrite it with moderated confidence…"},
                {"type": "audit", "id": "f5", "title": "5 · Phrasal (not clausal) co-ordination",
                 "text": "Nouns linked to nouns (\"training, scheduling coordination, and operational optimization\") instead of ideas linked to ideas (\"I trained six new hires, and that taught me…\"). Find a list of nouns that hides a story.",
                 "placeholder": "Quote the noun list and sketch the story it's hiding…"},
                {"type": "audit", "id": "f6", "title": "6 · Missing concrete examples",
                 "text": "DeLuca et al. found that the ChatGPT-generated introductions in their study included no numeric values at all, with claims of importance resting on vague, unmeasurable attributes. The resume had real numbers (400→1,900 followers, 800 lbs of food, 12-person team). What did the letter do with them? What would a specific, human paragraph about the donation drive look like?",
                 "placeholder": "Note which concrete details survived and which vanished into abstraction…"},
                {"type": "hint", "text": "before moving on, compare notes with a partner. Which feature was easiest to spot? Did the letter say anything a hundred other applicants' letters couldn't also say?"},
            ],
        },
        {
            "num": "Part 3", "title": "Draft inside-out: STAR stories first",
            "note": "The LLM seems to have drafted its content \"outside-in\": it started from cover-letter conventions and filled them with abstractions. You'll draft \"inside-out\": start from your two or three most interesting real experiences, write them as stories, and only then build the letter's structure around them. Use the STAR frame (Situation, Task, Action, Result) for each story.",
            "blocks": [
                {"type": "star", "id": "s1", "title": "Story 1", "fields": [
                    {"id": "s", "label": "Situation", "placeholder": "Where were you, and what was going on? Be pedestrian and specific: the workplace / course, the academic term, the project, the problem.", "hint": "e.g., \"Spring quarter, the café lost two closers in the same week and the schedule fell apart.\""},
                    {"id": "t", "label": "Task", "placeholder": "What were you responsible for making happen?"},
                    {"id": "a", "label": "Action", "placeholder": "What did you actually do? Use concrete action verbs with yourself or your team as the subject."},
                    {"id": "r", "label": "Result", "placeholder": "What changed or improved as a result of your actions? Numbers help, but so does an honest, modest outcome. Consider outcomes both for the organization or place and for yourself as a professional.", "hint": "Hedged results are fine and often more credible: \"the new schedule mostly held, and turnover slowed.\""},
                ]},
                {"type": "star", "id": "s2", "title": "Story 2", "fields": [
                    {"id": "s", "label": "Situation"}, {"id": "t", "label": "Task"},
                    {"id": "a", "label": "Action"}, {"id": "r", "label": "Result"},
                ]},
                {"type": "star", "id": "s3", "title": "Story 3 (optional)", "fields": [
                    {"id": "s", "label": "Situation"}, {"id": "t", "label": "Task"},
                    {"id": "a", "label": "Action"}, {"id": "r", "label": "Result"},
                ]},
                {"type": "star", "id": "letter_plan", "title": "From stories to letter", "fields": [
                    {"id": "match", "label": "Match", "placeholder": "Reread the job ad. Which of your stories speaks most directly to what this employer says they value, and why?"},
                    {"id": "topics", "label": "Topic sentences", "placeholder": "Draft one topic sentence per body paragraph. Each should make a claim that one of your STAR stories can back up."},
                    {"id": "frame", "label": "Opening & closing", "placeholder": "Only now draft your intro and conclusion, so they frame the stories instead of replacing them."},
                ]},
            ],
        },
        {
            "num": "Part 4", "title": "Self-edit checklist",
            "note": "Run this pass on your own full draft before submitting. It's the mirror image of the analysis you did in Part 2.",
            "blocks": [
                {"type": "check", "id": "c1", "title": "Every abstract claim is grounded", "text": "Each \"skill\" you name is attached to a specific moment, place, or number from one of your stories."},
                {"type": "check", "id": "c2", "title": "Verbs over nominalizations", "text": "Where you wrote \"coordination of X,\" you've tried \"I coordinated X\" and kept whichever is clearer (usually the verb)."},
                {"type": "check", "id": "c3", "title": "Participial pile-ups broken apart", "text": "No sentence carries more than one \"-ing\" modifier clause; ideas get their own clauses, joined with \"and,\" \"but,\" or \"so.\""},
                {"type": "check", "id": "c4", "title": "Confidence is moderated", "text": "Make strong claims where you've earned them, and hedge where you haven't. Cut \"seamlessly,\" and don't claim a \"proven track record\" unless the proof is on the page."},
                {"type": "check", "id": "c5", "title": "It could only be you", "text": "Could another applicant paste their name onto this letter? If so, it needs more of your story."},
                # NEW in the app version
                {"type": "prompt", "id": "reflection", "title": "Reflection (150–250 words)",
                 "text": "What could the LLM do that you couldn't, and what could you do that it couldn't?",
                 "placeholder": "Your reflection…", "height": 160},
            ],
        },
    ],
    "deliver_label": "Bring to class / submit",
    "deliver": [
        "The generated letter (or the previously-generated example) with your notes on the six features.",
        "Your two or three STAR stories.",
        "Your full cover letter draft with the Part 4 checklist completed.",
        "A short reflection (150–250 words): what could the LLM do that you couldn't, and what could you do that it couldn't?",
    ],
    "footer": "Part of Writing Against AI Slop · Calvin Pollak · University of Washington. The style framework is drawn from DeLuca et al. (2025) and Reinhart et al. (2025); the refusal option follows Sano-Franchini, McIntyre, & Fernandes, \"Refusing GenAI in Writing Studies.\" The previously-generated example uses a fictional applicant.",
}
