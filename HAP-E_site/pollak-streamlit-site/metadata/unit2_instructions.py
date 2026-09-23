# Unit 2 — More Human Instructions. Small groups generate installation
# instructions for a familiar tool, critique them, then rewrite one section.

PAGE_METADATA = {
    "key": "unit2_instructions",
    "title": "More Human Instructions",
    "unit_label": "Unit 2 · Instructional Design",
    "icon": "🛠️",
    "overview": (
        "In small groups, use an LLM to generate instructions for a tool you know well, analyze "
        "the output's style, discussion, and formatting, then rewrite it yourselves."
    ),
}

_SAMPLE_ZOOM = """
**Previously-generated example: LLM instructions for getting started with Zoom (unedited output):**

> **Installation Process**
> The execution of the installer file enables the commencement of the installation process. Upon
> completion of the download, the user should proceed with the execution of the setup file, followed
> by adherence to the on-screen prompts to facilitate proper installation.
>
> **Account Creation and Configuration**
> The establishment of a Zoom account necessitates the provision of a valid email address and the
> completion of subsequent verification procedures. Configuration of account settings, including
> notification preferences and video defaults, is recommended prior to initial usage.
>
> **Joining Your First Meeting**
> Participation in a scheduled meeting is achieved through the utilization of a meeting identifier or
> the selection of an emailed invitation link, followed by the granting of camera and microphone
> permissions as prompted by the application.
"""

STEPS = [
    {
        "type": "static",
        "content": (
            "**Why this exercise:** Instructional writing is where AI style does the most practical "
            "damage — confused readers can't complete the task. The best judge of clarity is a "
            "knowledgeable insider, which is exactly what your group is for this tool."
        ),
    },
    {
        "type": "static",
        "content": (
            "### Part 1 · Generate the Instructions (groups of 3–4, ~10 min)\n\n"
            "1. Agree on a tool, app, or piece of software everyone in the group knows well (a game, a "
            "daily app, a lab tool, a campus system).\n"
            "2. Use this prompt exactly: *\"Write instructions for installing and getting started with "
            "[your tool] for someone who has never used it.\"* Don't add style guidance.\n"
            "3. Read the output together once, silently, before discussing. Note your first reactions "
            "individually.\n\n"
            "**Groups that opt out of AI, or can't agree on a tool, can use the sample below instead.**"
        ),
    },
    {
        "type": "sample",
        "title": "Previously-generated example: LLM instructions for getting started with Zoom",
        "content": _SAMPLE_ZOOM,
    },
    {
        "type": "fields",
        "name": "Part 2 · Analyze by Asking Three Kinds of Questions",
        "intro": "Assign one question set per group member.",
        "items": [
            {
                "id": "q1_language",
                "label": "Question Set 1 — Language style",
                "prompt": (
                    "Is it dense and disconnected to the point of confusing the user? Look for "
                    "nominalizations that bury the user's action (e.g., \"the execution of the installer "
                    "file\" vs. \"double-click the installer\"). Ask who the subject of each step is. Find "
                    "the densest noun phrase and ask if a novice would know what to do. Where would a plain "
                    "imperative verb (\"click,\" \"type,\" \"wait\") be clearer?"
                ),
                "placeholder": "Quote two or three examples and note the plain-language fix for each…",
                "height": 130,
            },
            {
                "id": "q2_discussion",
                "label": "Question Set 2 — Supplementary discussion",
                "prompt": (
                    "Does it explain things the way you would to a friend or family member? What would you "
                    "warn someone about in person, and is it here? Good instructions explain why a step "
                    "matters, flag what can go wrong, and state what success looks like (\"you'll see a "
                    "green checkmark\") — where is this missing? What did the document get wrong, skip, or "
                    "misdescribe, based on your insider knowledge?"
                ),
                "placeholder": "List the tips, warnings, and \"what you'll see\" details a friendly expert would have added…",
                "height": 130,
            },
            {
                "id": "q3_formatting",
                "label": "Question Set 3 — Formatting",
                "prompt": (
                    "Does the layout match the logic of the task? Sequential steps should be numbered, not "
                    "bulleted, since order matters. Is each step one action or several packed together? "
                    "Where would a screenshot, caution box, or \"before you begin\" list help?"
                ),
                "placeholder": "Note specific places where the formatting works against understanding…",
                "height": 130,
            },
        ],
    },
    {
        "type": "static",
        "content": (
            "**Discussion checkpoint:** As a group, decide which set of questions revealed the most "
            "serious problem. Style issues make instructions unpleasant to read — but which failures "
            "make them actually unusable?"
        ),
    },
    {
        "type": "fields",
        "name": "Part 3 · Instructions Rewrite",
        "intro": (
            "Together, rewrite one full section (installation is usually the best candidate) so a "
            "genuine novice could follow it. Requirements: numbered steps; one action per step; the "
            "reader as the subject of every instruction; at least one tip or warning drawn from your "
            "group's real experience with the tool; and a \"what you'll see\" detail confirming success. "
            "Also indicate where you'd add visual elements such as screenshots or caution boxes."
        ),
        "items": [
            {
                "id": "rewrite",
                "label": "Your group's rewrite",
                "placeholder": "Draft your group's rewrite here, or in a shared doc…",
                "height": 220,
            },
        ],
    },
    {
        "type": "fields",
        "name": "Part 4 · Compare and Reflect",
        "intro": (
            "Put the original and the rewrite side by side, then answer: What knowledge did your "
            "rewrite depend on that the LLM couldn't have had? Which differences are style fixes, and "
            "which are content the model simply didn't know to include? The LLM produced its version in "
            "seconds and yours took twenty minutes — for which audiences and situations is the "
            "twenty-minute version worth it, and are there any where it isn't?"
        ),
        "items": [
            {
                "id": "part4_reflection",
                "label": "Your group's reflection",
                "placeholder": "Record your group's answers…",
                "height": 160,
            },
        ],
    },
    {
        "type": "static",
        "content": (
            "**Bring to class / submit (one per group):** the generated instructions or sample with "
            "notes on all three question sets; the rewritten section; your Part 4 reflection."
        ),
    },
]
