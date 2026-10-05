# Writing Against AI Slop: classroom app (Streamlit)

Classroom version of the Writing Against AI Slop site. The HTML site stays live on GitHub Pages; this app is for in-class use.

## What's in this folder

| File or folder | What it does |
|---|---|
| `streamlit_app.py` | The file Streamlit runs. Sets up the sidebar and the list of pages. |
| `app_pages/` | One file per page. Pages that haven't been ported yet show a "coming soon" note. |
| `content/` | The text of quizzes and exercises. **Edit wording here**, not in the page files. |
| `utils/` | Shared helpers: styling, exercise widgets, and the Word download. |
| `.streamlit/config.toml` | Colors and fonts. See the note in step 3 below. |
| `requirements.txt` | Tells Streamlit Cloud which Python packages to install. |

## Putting it online (no terminal needed)

### Step 1: Make a repository on GitHub

Sign in at github.com, click **New** (or the **+** menu, then **New repository**), name it `anti-slop-app`, and click **Create repository**.

### Step 2: Upload the files

On the new repository's page, click **uploading an existing file** (or **Add file → Upload files**). Open the unzipped `anti-slop-app` folder on your computer, select everything inside it, and drag it into the browser window. Click **Commit changes**.

### Step 3: Check for the settings folder

Look at the list of files on your repository page. You should see a folder called `.streamlit`.

**Why it might be missing:** names that start with a dot are hidden files. Mac and Windows don't show them in a normal folder window, so when you select everything and drag it, the `.streamlit` folder usually gets left behind. The app still runs without it, but it uses Streamlit's default colors and fonts, and it shows a yellow setup note on every page until the file is added.

**If `.streamlit` is missing, add it by hand:**

1. On the repository page, click **Add file → Create new file**.
2. In the file name box, type `.streamlit/config.toml` exactly. When you type the slash, GitHub turns `.streamlit` into a folder automatically.
3. Copy the block below and paste it into the large text box.
4. Click **Commit changes**.

```toml
[theme]
base = "light"
primaryColor = "#6b5030"
backgroundColor = "#f5f0e8"
secondaryBackgroundColor = "#ede8de"
textColor = "#1a1410"
borderColor = "#d5ccc0"
font = "Source Serif 4:https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300..700;1,8..60,300..700&display=swap"
headingFont = "Playfair Display:https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap"

[theme.sidebar]
backgroundColor = "#ede8de"

[client]
toolbarMode = "minimal"
```

### Step 4: Turn it into an app

Go to share.streamlit.io, sign in with your GitHub account, and click **Create app**. Choose your `anti-slop-app` repository, leave the branch as `main`, and set the main file path to `streamlit_app.py`. Click **Deploy**. After a few minutes you'll get a web address, and that's the link to put in Canvas.

When you change a file on GitHub later, the app updates itself within a minute or so.

## Look and feel

The app carries two palettes, one for light mode and one for dark, both defined at the top
of `utils/style.py` as `LIGHT` and `DARK`. It reads the viewer's Streamlit setting through
`st.context.theme` and uses the matching one, so dark mode really goes dark and Streamlit's
own toolbar icons stay visible against the page.

To change a color, edit the dictionary entry rather than the CSS below it. Both palettes are
checked against WCAG AA, so if you change one, check the new value: text needs 4.5:1 against
the surface behind it, and borders and focus rings need 3:1.

Both palettes ship in every page's stylesheet, scoped to a `data-slop-theme` attribute
that `utils/a11y.py` writes onto the page from the viewer's Streamlit setting. Streamlit
does not rerun the script when someone switches theme, so resolving the choice in Python
alone would leave the old palette on screen until the next click.

`.streamlit/config.toml` defines a `[theme]` and a `[theme.dark]` section. Both are needed:
with only a light theme defined, Streamlit removes the light / dark / system switcher from
the app's menu. `toolbarMode` is set to `auto` for the same reason, since `minimal` hides
the menu that holds the switcher.

Typography is IBM Plex Sans for headings, labels, and controls, with Literata for reading
text.

## Keeping the app healthy

The app depends on Streamlit's own markup in one place: `utils/a11y.py` adds the landmarks
and list roles that screen readers need, using Streamlit's internal test IDs. If a future
Streamlit release renames those, the fixes stop applying. Two things guard against that.

**1. The version is pinned.** `requirements.txt` says `streamlit==1.64.0`, so Streamlit
Cloud installs that version every time it rebuilds, and a new release can't arrive on its
own. Nothing changes until you change that line.

**2. The app checks itself.** Add `?check=1` to the end of the app's address, for example
`https://engl288-pollak.streamlit.app/?check=1`, and two reports appear at the top:

- a version report, comparing the Streamlit the app is running against the version it was
  tested with (`TESTED_STREAMLIT` in `streamlit_app.py`);
- an accessibility report, saying whether all three screen reader fixes were applied, and
  naming any it could not apply.

Students never see either one, because they appear only with `?check=1` in the address.

**A routine that takes two minutes.** Once a quarter, before your course starts, open the
app with `?check=1` and confirm both reports are green. That is enough, because the pinned
version means nothing changes in between.

**When you want a newer Streamlit.** Edit the version in `requirements.txt`, wait for the
app to rebuild, then open it with `?check=1`. If the accessibility report is green, update
`TESTED_STREAMLIT` in `streamlit_app.py` to match and you're done. If it's red, it names
the piece it couldn't find, which is what a developer needs in order to fix the selector in
`utils/a11y.py`. Changing the version back restores the working state in the meantime.

## Notes

- Nothing students type is stored. Each page has a download button that gives them a Word file of their answers.
- Community Cloud apps go to sleep after a period with no visitors, and the first person to open a sleeping app may wait a minute while it wakes up. Opening it yourself a few minutes before class avoids this.
- To run it on your own computer instead: `pip install -r requirements.txt`, then `streamlit run streamlit_app.py`.
