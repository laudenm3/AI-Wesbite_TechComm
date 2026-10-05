"""Colors, typography, and the small components the pages share.

The app follows Streamlit's active theme instead of overriding it. Streamlit reports the
viewer's choice through `st.context.theme`, so this module builds its CSS from whichever
of the two palettes below applies. That matters beyond appearance: when the app forced a
light page onto a viewer in dark mode, Streamlit kept drawing its own toolbar icons for a
dark background, and they disappeared against the light page. Following the theme keeps
the framework's chrome and the app's surfaces in agreement.

Rules worth holding to when editing this file:

1. Every color comes from the palette dictionaries. No hex values in the CSS body and
   none in the page files, so changing the palette is a change in one place.
2. Every rule that sets a color covers descendants (`.thing, .thing *`), because
   Streamlit wraps text in spans of its own, and a rule naming only the parent leaves
   those spans to inherit the theme's color.
3. Status is carried by an edge and a label, never by a tinted fill behind running text.
4. Both palettes are checked against WCAG AA: text on every surface at 4.5:1 or better,
   borders and focus rings at 3:1 or better.
5. Nothing here sets a background on <body>. Streamlit colors that element from its
   active theme, and utils/a11y.py reads it to decide which palette applies. Styling it
   would blind that check.
"""

import re

import streamlit as st

LIGHT = {
    "PAGE": "#f5f5f7",      # cool near-white, deliberately not cream
    "SURFACE": "#ffffff",   # cards and callouts
    "INPUT": "#e9eaef",     # text boxes, a shade off the card so the field is visible
    "RAISED": "#ececed",    # sidebar
    "TEXT": "#14151a",
    "MUTED": "#4c4f58",
    "BORDER": "#787e8c",   # 3.7:1 on PAGE, 4.1:1 on SURFACE, 3.4:1 on INPUT
    "ACCENT": "#553a9e",    # violet, a nod to UW purple without claiming the brand
    "ACCENT_SOFT": "#ede9f7",
    "OK": "#1a6b41",
    "NO": "#98292b",
    "CAUTION": "#7d5300",
    "NOTE": "#4b3f8f",
    "MARK_A": "#ffd97a",
    "MARK_B": "#a8cdf5",
    "MARK_TEXT": "#14151a",
}

DARK = {
    "PAGE": "#15161c",
    "SURFACE": "#1e2029",
    "INPUT": "#282b36",
    "RAISED": "#1a1c23",
    "TEXT": "#edeef2",
    "MUTED": "#b2b7c2",
    "BORDER": "#767c88",
    "ACCENT": "#bcaaf5",
    "ACCENT_SOFT": "#2a2540",
    "OK": "#6fd39b",
    "NO": "#f0908f",
    "CAUTION": "#e3b256",
    "NOTE": "#bcaaf5",
    "MARK_A": "#6d5a1c",
    "MARK_B": "#22456e",
    "MARK_TEXT": "#f4f2ea",
}


def palette() -> dict:
    """The palette matching the viewer's Streamlit theme, light unless it says dark."""
    try:
        return DARK if st.context.theme.type == "dark" else LIGHT
    except Exception:
        # Older Streamlit, or a context that does not report a theme.
        return LIGHT


FONT_IMPORT = ("@import url('https://fonts.googleapis.com/css2?"
               "family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&"
               "family=Literata:ital,opsz,wght@0,7..72,300..700;1,7..72,300..700&display=swap');")


def _rules(p: dict) -> str:
    return f"""

/* ── Surfaces ──────────────────────────────────────────────────────────── */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
[data-testid="stMain"], [data-testid="stMainBlockContainer"],
[data-testid="stBottomBlockContainer"] {{ background: {p['PAGE']} !important; }}
[data-testid="stSidebar"], [data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {{ background: {p['RAISED']} !important; }}

.stApp, .stApp *, [data-testid="stSidebar"] * {{ color: {p['TEXT']} !important; }}
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stCaptionContainer"] * {{ color: {p['MUTED']} !important; opacity: 1 !important; }}
.stApp a, .stApp a * {{ color: {p['ACCENT']} !important; }}

/* ── Typography: sans for structure, serif for reading ─────────────────── */
.stApp {{ font-family: 'Literata', Georgia, serif; }}
.stApp textarea, .stApp input, .stApp button, .stApp select {{
  font-family: 'IBM Plex Sans', system-ui, sans-serif;
}}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {{
  font-family: 'IBM Plex Sans', system-ui, sans-serif !important;
  font-weight: 600 !important; letter-spacing: -0.01em;
  color: {p['TEXT']} !important;
}}
[data-testid="stSidebar"] {{ font-family: 'IBM Plex Sans', system-ui, sans-serif; }}
[data-testid="stIconMaterial"] {{ font-family: 'Material Symbols Rounded' !important; }}

/* ── Cards, expanders, form controls ──────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) {{
  border-color: {p['BORDER']} !important;
}}
.stApp [data-testid="stExpander"] details,
.stApp [data-testid="stExpander"] summary {{
  background: {p['SURFACE']} !important; border-color: {p['BORDER']} !important;
}}
/* A text box has to be findable. Cards and inputs both used the same surface, so in
   either mode the field vanished into the card behind it: an empty box with no edge.
   The field now sits a shade off the card and carries a border of its own. */
.stApp textarea, .stApp input, .stApp [data-baseweb="input"],
.stApp [data-baseweb="base-input"], .stApp [data-baseweb="textarea"],
.stApp [data-baseweb="select"] > div,
.stApp [data-testid="stTextAreaRootElement"], .stApp [data-testid="stTextInputRootElement"] {{
  background: {p['INPUT']} !important; color: {p['TEXT']} !important;
  border-color: {p['BORDER']} !important;
}}
.stApp [data-testid="stTextAreaRootElement"], .stApp [data-testid="stTextInputRootElement"],
.stApp [data-baseweb="select"] > div {{
  border: 1.5px solid {p['BORDER']} !important;
}}
.stApp textarea::placeholder, .stApp input::placeholder {{
  color: {p['MUTED']} !important; opacity: 1 !important;
}}
[data-baseweb="popover"] [role="listbox"], [data-baseweb="popover"] li,
[data-baseweb="menu"], [data-baseweb="menu"] li {{
  background: {p['SURFACE']} !important; color: {p['TEXT']} !important;
}}
[data-baseweb="menu"] li:hover, [data-baseweb="popover"] li:hover {{ background: {p['ACCENT_SOFT']} !important; }}
.stApp [disabled], .stApp [aria-disabled="true"], .stApp [disabled] *, .stApp [aria-disabled="true"] * {{
  opacity: 1 !important; color: {p['MUTED']} !important; -webkit-text-fill-color: {p['MUTED']} !important;
}}

[data-testid="stBaseButton-secondary"] {{
  background: {p['SURFACE']} !important; color: {p['TEXT']} !important; border-color: {p['BORDER']} !important;
}}
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primary"] * {{
  background: {p['ACCENT']} !important; color: {p['SURFACE']} !important; border-color: {p['ACCENT']} !important;
}}
.stApp [data-testid="stButtonGroup"] button,
.stApp [data-baseweb="button-group"] button {{
  background-color: {p['SURFACE']} !important; border-color: {p['BORDER']} !important; color: {p['TEXT']} !important;
}}
.stApp [data-testid="stButtonGroup"] button[aria-checked="true"],
.stApp [data-testid="stButtonGroup"] button[aria-pressed="true"],
.stApp [data-baseweb="button-group"] button[aria-checked="true"] {{
  background-color: {p['ACCENT_SOFT']} !important; border-color: {p['ACCENT']} !important;
}}
[data-testid="stRadioOption"] > div > div:first-child {{
  background-color: {p['SURFACE']} !important; border: 1.5px solid {p['ACCENT']} !important;
}}
[data-testid="stRadioOption"] > div > div:first-child > div {{ background-color: transparent !important; }}
[data-testid="stRadioOption"]:has(input:checked) > div > div:first-child > div {{
  background-color: {p['ACCENT']} !important;
}}
[data-testid="stCheckbox"] label > div:not([data-testid]) {{
  background-color: {p['SURFACE']} !important; border: 1.5px solid {p['ACCENT']} !important;
}}
[data-testid="stCheckbox"] label:has(input:checked) > div:not([data-testid]) {{
  background-color: {p['ACCENT']} !important;
}}
[data-testid="stProgressBarTrack"] {{ background-color: {p['BORDER']} !important; }}
[data-testid="stProgressBarTrack"] > div {{ background-color: {p['ACCENT']} !important; }}

.stApp [data-baseweb="textarea"]:focus-within, .stApp [data-baseweb="input"]:focus-within,
.stApp [data-baseweb="base-input"]:focus-within, .stApp textarea:focus, .stApp input:focus {{
  border-color: {p['ACCENT']} !important; box-shadow: none !important;
}}
.stApp :focus-visible {{
  outline: 3px solid {p['ACCENT']} !important; outline-offset: 2px !important; border-radius: 2px;
}}

/* ── Tabs ─────────────────────────────────────────────────────────────── */
[data-baseweb="tab-list"], [data-baseweb="tab"] {{ background: transparent !important; }}
[data-baseweb="tab"] {{ color: {p['MUTED']} !important; font-family: 'IBM Plex Sans', sans-serif; }}
[data-baseweb="tab"][aria-selected="true"], [data-baseweb="tab"][aria-selected="true"] * {{
  color: {p['TEXT']} !important;
}}
[data-baseweb="tab-highlight"] {{ background-color: {p['ACCENT']} !important; }}
[data-baseweb="tab-border"] {{ background-color: {p['BORDER']} !important; }}

/* ── Masthead ─────────────────────────────────────────────────────────
   The page title used to sit in a filled block. That works against a near-white
   page but not against a dark one: no fill dark enough to keep the kicker legible
   is light enough to separate from the page behind it, so in dark mode the block
   turned into a muddy rectangle. The title now sits on the page itself, and a thick
   accent bar carries the emphasis. The bar is the accent color, which is 7.8:1
   against the page in light mode and 8.8:1 in dark, so it reads in both. */
.slop-banner {{
  background: transparent !important;
  padding: 10px 0 20px 22px; margin-bottom: 26px;
  border-left: 6px solid {p['ACCENT']};
  border-bottom: 1px solid {p['BORDER']};
}}
.slop-kicker, .slop-kicker * {{
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.72rem; font-weight: 600; letter-spacing: 0.16em;
  text-transform: uppercase; color: {p['ACCENT']} !important; margin-bottom: 10px;
}}
.slop-banner h1, .slop-banner h1 * {{
  color: {p['TEXT']} !important; font-size: 2.1rem !important;
  line-height: 1.2 !important; padding: 0 !important; margin: 0 0 8px 0 !important;
}}
.slop-banner h1 em, .slop-banner h1 em * {{ color: {p['ACCENT']} !important; font-style: italic; }}
.slop-sub, .slop-sub * {{
  color: {p['MUTED']} !important; font-style: italic; font-size: 0.95rem; line-height: 1.6;
}}
.slop-banner a, .slop-banner a *, .slop-banner svg, .slop-banner path, .slop-banner line {{
  color: {p['ACCENT']} !important; stroke: {p['ACCENT']} !important; fill: {p['ACCENT']} !important;
}}

/* ── Passages and labels ──────────────────────────────────────────────── */
.slop-passage, .slop-passage * {{ color: {p['TEXT']} !important; }}
.slop-passage {{
  background: {p['SURFACE']}; border-left: 4px solid {p['ACCENT']};
  border-top: 1px solid {p['BORDER']}; border-right: 1px solid {p['BORDER']};
  border-bottom: 1px solid {p['BORDER']};
  padding: 14px 18px; line-height: 1.8; margin-bottom: 12px;
}}
.slop-label, .slop-label * {{
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.72rem; font-weight: 600; letter-spacing: 0.14em;
  text-transform: uppercase; color: {p['ACCENT']} !important; margin: 8px 0 4px;
}}

/* ── Callouts ─────────────────────────────────────────────────────────── */
.slop-callout {{
  background: {p['SURFACE']} !important;
  border-left: 5px solid;
  border-top: 1px solid {p['BORDER']}; border-right: 1px solid {p['BORDER']};
  border-bottom: 1px solid {p['BORDER']};
  padding: 13px 17px; margin: 6px 0 14px; line-height: 1.7; font-size: 0.95rem;
}}
.slop-callout, .slop-callout * {{ color: {p['TEXT']} !important; }}
.slop-callout .slop-callout-label {{
  display: block; font-family: 'IBM Plex Sans', sans-serif; font-size: 0.74rem;
  font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 6px;
}}
.slop-callout.info {{ border-left-color: {p['ACCENT']}; }}
.slop-callout.info .slop-callout-label {{ color: {p['ACCENT']} !important; }}
.slop-callout.correct {{ border-left-color: {p['OK']}; }}
.slop-callout.correct .slop-callout-label {{ color: {p['OK']} !important; }}
.slop-callout.wrong {{ border-left-color: {p['NO']}; }}
.slop-callout.wrong .slop-callout-label {{ color: {p['NO']} !important; }}
.slop-callout.note {{ border-left-color: {p['CAUTION']}; }}
.slop-callout.note .slop-callout-label {{ color: {p['CAUTION']} !important; }}
.slop-callout.refusal {{ border-left-color: {p['NOTE']}; }}
.slop-callout.refusal .slop-callout-label {{ color: {p['NOTE']} !important; }}
.slop-callout.deliver {{ border-left-color: {p['OK']}; }}
.slop-callout.deliver .slop-callout-label {{ color: {p['OK']} !important; }}

/* ── Answered quiz options ────────────────────────────────────────────── */
.slop-opt {{
  display: block; padding: 5px 10px; margin: 3px 0; line-height: 1.6;
  border-left: 4px solid transparent;
}}
.slop-opt, .slop-opt * {{ color: {p['TEXT']} !important; }}
.slop-opt.ok {{ border-left-color: {p['OK']}; background: {p['SURFACE']}; font-weight: 600; }}
.slop-opt.no {{ border-left-color: {p['NO']}; background: {p['SURFACE']}; }}
.slop-opt.dim {{ border-left-color: {p['BORDER']}; }}
.slop-opt.dim, .slop-opt.dim * {{ color: {p['MUTED']} !important; }}
.slop-mark {{ font-weight: 700; }}
.slop-opt.ok .slop-mark {{ color: {p['OK']} !important; }}
.slop-opt.no .slop-mark {{ color: {p['NO']} !important; }}

/* ── Model answers ────────────────────────────────────────────────────── */
.slop-model, .slop-model * {{ color: {p['TEXT']} !important; }}
.slop-model {{
  background: {p['SURFACE']}; border-left: 5px solid {p['OK']};
  border-top: 1px solid {p['BORDER']}; border-right: 1px solid {p['BORDER']};
  border-bottom: 1px solid {p['BORDER']};
  padding: 14px 18px; line-height: 1.8; font-style: italic;
}}
.slop-model .slop-model-label {{
  display: block; font-style: normal; font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.74rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;
  margin-bottom: 6px; color: {p['OK']} !important;
}}

/* ── Highlighter marks ────────────────────────────────────────────────── */
mark.hl-a, mark.hl-a * {{ background: {p['MARK_A']} !important; color: {p['MARK_TEXT']} !important; border-radius: 2px; padding: 0 2px; }}
mark.hl-b, mark.hl-b * {{ background: {p['MARK_B']} !important; color: {p['MARK_TEXT']} !important; border-radius: 2px; padding: 0 2px; }}

/* ── Screen-reader-only text ──────────────────────────────────────────── */
.slop-sr-only {{
  position: absolute !important; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;
}}
"""


def _scope(css: str, prefix: str) -> str:
    """Prefix every selector in a block of CSS, so one palette can be nested under
    an attribute on <html> and the other under its absence."""
    out = []
    for chunk in css.split("}"):
        if "{" not in chunk:
            continue
        selectors, body = chunk.split("{", 1)
        comment = ""
        if "*/" in selectors:            # keep the comment above the rule
            comment, selectors = selectors.rsplit("*/", 1)
            comment += "*/"
        parts = [f"{prefix} {sel.strip()}" for sel in selectors.split(",") if sel.strip()]
        out.append(f"{comment}\n{', '.join(parts)} {{{body}}}")
    return "\n".join(out)


def _css(p_light: dict, p_dark: dict) -> str:
    """Both palettes in one stylesheet.

    The viewer can switch theme from Streamlit's menu without the script rerunning,
    so the choice cannot be resolved in Python alone. utils/a11y.py writes the active
    theme onto <html> as data-slop-theme, and the two scoped blocks below respond to
    it immediately.
    """
    light = _scope(_rules(p_light), 'html:not([data-slop-theme="dark"])')
    dark = _scope(_rules(p_dark), 'html[data-slop-theme="dark"]')
    return f"<style>{FONT_IMPORT}{light}{dark}</style>"


def inject_css():
    st.markdown(_css(LIGHT, DARK), unsafe_allow_html=True)


def banner(kicker: str, title_html: str, sub: str = ""):
    """The header block at the top of each page. title_html may contain <em>."""
    sub_html = f'<div class="slop-sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div class="slop-banner"><div class="slop-kicker">{kicker}</div>'
        f"<h1>{title_html}</h1>{sub_html}</div>",
        unsafe_allow_html=True,
    )


def label(text: str):
    st.markdown(f'<div class="slop-label">{text}</div>', unsafe_allow_html=True)


def light_markdown(text: str) -> str:
    """Convert the small amount of markdown used in our content into HTML."""
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    out = re.sub(r"(?<![\*\w])\*([^*]+?)\*(?!\*)", r"<em>\1</em>", out)
    rendered = []
    for line in out.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- "):
            rendered.append(f"&bull;&nbsp;{stripped[2:]}")
        else:
            rendered.append(stripped)
    return "<br>".join(x for x in rendered if x)


def callout(kind: str, body: str, title: str | None = None, icon: str | None = None,
            announce: bool = False):
    """A card with a colored edge, in place of st.info / st.success / st.warning.

    kind: info, correct, wrong, note, refusal, deliver
    """
    head = f'<span class="slop-callout-label">{title}</span>' if title else ""
    lead = f"{icon} " if icon else ""
    role = ' role="status" aria-live="polite"' if announce else ""
    st.markdown(
        f'<div class="slop-callout {kind}"{role}>{head}{lead}{light_markdown(body)}</div>',
        unsafe_allow_html=True,
    )
