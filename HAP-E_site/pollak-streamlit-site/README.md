# Writing Against AI Slop — Streamlit Site

A Streamlit rewrite of `ai-style-exercises-main/` that hosts the whole course site (not just
individual embedded fields) so students can work through the readings, unit activities, and
exercise sets in class or at home, then download everything they've typed as one `.docx`.

## Run it locally

```bash
cd pollak-streamlit-site
pip install -r requirements.txt
streamlit run Home.py
```

## Structure

- `Home.py` — landing page (mirrors the original `index.html`), with links to every page.
- `pages/` — one Streamlit page per unit/exercise set. Streamlit's native multipage nav
  (sidebar page list) replaces the original site's card links.
- `metadata/` — one config module per page (`PAGE_METADATA` + `STEPS`), following the same
  metadata-driven pattern as `llm-chatbot/metadata/*.py`. Editing content/prompts means editing
  data here, not the rendering code.
- `common/ui.py` — the "SideDesk" sidebar (name field, per-page progress, workbook download,
  clear-page button) and the step renderer that turns a `STEPS` list into widgets.
- `common/export.py` — builds the single `.docx` workbook from `st.session_state`, pulling every
  page's answers regardless of which page the student is currently on.

## Design notes / decisions made during the port

- Every free-text field across all six original pages is now captured into the exported
  workbook. In the original HTML, several analysis/diagnostic textareas (Unit 1 Part 2, Unit 2
  Part 2, Unit 3 Part 1) were explicitly excluded from the save flow ("copy those out
  separately") — this rewrite captures them too, since the whole point of the migration is one
  reliable export.
- Unit 3's deliverables list mentions "one paragraph noting the two most important edits you
  made," but the original HTML had no field for it — added as `most_important_edits`.
- Reading Check's five discussion prompts previously had no on-page input at all (just "jot
  notes"); they're now optional text areas so they're captured too.
- Pure multiple-choice/identification/ranking exercises (Exercise Sets 1 & 2) stay interactive
  (radio buttons, instant feedback, a ranking widget) rather than becoming text fields, since
  they aren't "text input exercises" in the original — they don't appear in the exported
  workbook.
- The paragraph-comparison browser in Exercise Set 1 (topic buttons + highlight toggle) became a
  set of expanders, one per topic, since it's reference material rather than an exercise.

## Deploying

Point Streamlit Community Cloud (or wherever `llm-chatbot`/`field-entry-tool` are deployed) at
this repo with `Home.py` as the main file, the same way `field-entry-tool` and `reflection-tool`
are deployed today. Once deployed, `ai-style-exercises-main/index.html` and the unit pages can
either redirect here or be retired in favor of this single app.
