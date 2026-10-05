"""Unit 2 · More Human Instructions. Ported from Pollak_Unit2_Instructions_7-13-26.html.

One text box is new in the app version (marked NEW below): a place to paste the
generated instructions, so the Word download holds the whole submission.
"""

UNIT = {
    "key": "u2",
    "kicker": "Course Unit 2 · Instructional Design",
    "title": "More Human Instructions",
    "sub": "A small-group activity: have an LLM write instructions for a tool your group knows well, take the instructions apart by asking three kinds of questions, and then rewrite them the way you'd explain the tool to a friend or family member.",
    "doc_title": "Unit 2: More Human Instructions",
    "file_name": "Unit2_Instructions.docx",
    "name_label": "Group members (appears on the downloaded file)",
    "goals_intro": "**What you'll do and why.** Instructional writing is where AI-inflected style can do the most practical damage, because a confused reader is less likely to successfully complete the task. The best test of instructional clarity is a knowledgeable insider: someone who knows the tool or procedure well enough to notice where the document skips things, gets the order wrong, or dresses simple actions up in formal language. That's where your group comes in. You'll pick a tool you all know, prompt an LLM to document it, and evaluate the result the way real users would.",
    "goals_lead": "your group should be able to",
    "goals": [
        "analyze instructions for their language style, supplementary discussion, and formatting;",
        "explain what good instructional writers add beyond a bare list of steps;",
        "rewrite a flawed section so a genuine novice could follow it.",
    ],
    "parts": [
        {
            "num": "Part 1", "title": "Generate the instructions",
            "note": "Groups of 3–4. Budget about 10 minutes for this part.",
            "blocks": [
                {"type": "steps", "items": [
                    "Agree on a piece of software, an app, or a tool that *everyone* in your group knows well: a game you all play, an app you all use daily, a lab tool, a campus system. The more insider knowledge your group has about it, the better.",
                    "In the university-licensed LLM chatbot, prompt: *\"Write instructions for installing and getting started with [your tool] for someone who has never used it.\"* Don't add style guidance.",
                    "Read the output together once, silently, before discussing. Note your first reactions individually.",
                ]},
                {"type": "refusal", "text": "If your group opts out (or can't agree on a shared tool), you can analyze the previously-generated example below instead. It documents an app that most students know, so your insider knowledge still applies."},
                {"type": "sample", "label": "Previously-generated example: LLM instructions for getting started with Zoom",
                 "sections": [{"label": "", "text":
                    "**Getting Started with Zoom: Installation and Initial Configuration**\n\n"
                    "Zoom is a comprehensive video communications platform facilitating seamless virtual collaboration across diverse organizational and educational contexts. The successful utilization of Zoom's robust feature set requires the completion of several foundational configuration processes, encompassing application installation, account creation, and audio-visual optimization.\n\n"
                    "**Installation Process**\n\n"
                    "- Navigate to the official Zoom download center, ensuring the selection of the appropriate client version corresponding to your operating system.\n"
                    "- Initiate the download of the Zoom Workplace desktop client.\n"
                    "- The execution of the installer file enables the commencement of the installation process.\n"
                    "- Upon completion of the installation, the application launch process can be initiated.\n\n"
                    "**Account Creation and Configuration**\n\n"
                    "- The creation of a Zoom account is achievable through multiple authentication pathways, including email-based registration and single sign-on integration leveraging existing institutional credentials.\n"
                    "- Following successful authentication, users gain access to a comprehensive settings interface enabling the customization of meeting preferences, notification parameters, and accessibility configurations.\n\n"
                    "**Joining Your First Meeting**\n\n"
                    "- Meeting participation is facilitated through the utilization of meeting IDs or invitation links distributed by meeting hosts.\n"
                    "- The verification of audio and video functionality prior to meeting entry ensures an optimized participation experience."}],
                 "note": "These instructions were generated with a general-purpose LLM chatbot, and they have not been edited. They're included here so that groups practicing AI refusal can complete the analysis without generating text themselves."},
                # NEW in the app version
                {"type": "prompt", "id": "generated", "title": "The instructions you're analyzing",
                 "text": "Paste the generated instructions here. If you're using the previously-generated example, you can leave this blank.",
                 "placeholder": "Paste the generated instructions…", "height": 160},
            ],
        },
        {
            "num": "Part 2", "title": "Analyze by asking three kinds of questions",
            "note": "Assign one question set per group member (double up in groups of four), discuss together, and record your findings.",
            "blocks": [
                {"type": "prompt", "id": "q1", "title": "Question set 1 · Language style: is it dense and disconnected to the point of confusing the user?",
                 "text": "- Hunt for nominalizations that bury the action the user must take (\"the execution of the installer file\" vs. \"double-click the installer\"). Who is the subject of each step, and is it the reader?\n- Find the densest noun phrase. Would a first-time user know what to physically do after reading it?\n- Where would a plain imperative verb (\"click,\" \"type,\" \"wait\") have been clearer?",
                 "placeholder": "Quote two or three examples and note the plain-language fix for each…"},
                {"type": "prompt", "id": "q2", "title": "Question set 2 · Supplementary discussion: does it explain things the way you would to a friend or family member?",
                 "text": "- When you help someone install this tool in person, what do you warn them about? Is any of that here?\n- Good instructions explain *why* a step matters, flag what can go wrong, and say what success looks like (\"you'll see a green checkmark\"). Where is this missing?\n- Your insider knowledge: what did the document get wrong, skip, or describe in a way no actual user would recognize?",
                 "placeholder": "List the tips, warnings, and 'what you'll see' details a friendly expert would have added…"},
                {"type": "prompt", "id": "q3", "title": "Question set 3 · Formatting: does the layout match the logic of the task?",
                 "text": "- Sequential steps should be *numbered*, because order matters and users need to keep their place. Did the document use bullets where it should have used numbers?\n- Is each step one action, or are several actions packed into one item?\n- Where would a screenshot, a caution box, or a \"before you begin\" list have helped?",
                 "placeholder": "Note specific places where the formatting works against understanding…"},
                {"type": "hint", "text": "as a group, decide which set of questions revealed the most serious problem. Style issues make instructions unpleasant to read, but which failures make them actually unusable?"},
            ],
        },
        {
            "num": "Part 3", "title": "Rewrite it",
            "note": "Together, rewrite one full section (installation is usually the best candidate) so a genuine novice could follow it. Requirements: numbered steps, one action per step, the reader as the subject of every instruction, at least one tip or warning drawn from your group's real experience with the tool, and a \"what you'll see\" detail confirming success. Also, be sure to indicate where you would add visual elements such as screenshots or caution boxes.",
            "blocks": [
                {"type": "prompt", "id": "rewrite", "title": "Your group's rewrite",
                 "text": "Draft your rewrite here, or in a shared doc and paste it in when you're done.",
                 "placeholder": "1. …", "height": 260},
            ],
        },
        {
            "num": "Part 4", "title": "Compare and reflect",
            "note": "Put the original and the rewrite side by side and answer together:",
            "blocks": [
                {"type": "prompt", "id": "reflect", "title": "Reflection",
                 "text": "- What knowledge did your rewrite depend on that the LLM couldn't have had?\n- Which differences are style fixes, and which are content the model simply didn't know to include?\n- The LLM produced its version in seconds and yours took twenty minutes. For which audiences and situations is the twenty-minute version worth it, and are there any where it isn't?",
                 "placeholder": "Record your group's answers…", "height": 160},
            ],
        },
    ],
    "deliver_label": "Bring to class / submit (one per group)",
    "deliver": [
        "The generated instructions (or the previously-generated example) with your notes on all three question sets.",
        "Your rewritten section.",
        "Your Part 4 reflection answers.",
    ],
    "footer": "Part of Writing Against AI Slop · Calvin Pollak · University of Washington. The style framework is drawn from DeLuca et al. (2025) and Reinhart et al. (2025); the refusal option follows Sano-Franchini, McIntyre, & Fernandes, \"Refusing GenAI in Writing Studies.\"",
}
