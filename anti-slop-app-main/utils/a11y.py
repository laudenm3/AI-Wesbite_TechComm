"""Accessibility patches for Streamlit's own markup.

Streamlit renders its sidebar in a way that trips three axe-core rules: the sidebar
carries aria-expanded on an element whose role doesn't allow it, the navigation list
holds section headers as direct children of a <ul>, and neither the sidebar nor the
main area is marked as a landmark, so a screen reader can't jump between them.

None of that is reachable from Python or CSS, so this module injects a small script
through a zero-height component. The script runs in an iframe written with srcdoc,
which shares the page's origin, so it can adjust the parent document. It fixes roles
only and never moves or deletes an element, so React keeps control of the DOM.
"""

import streamlit.components.v1 as components

from utils.style import palette

_SCRIPT = """
<script>
let doc = null;
let blocked = false;
try {
  doc = window.parent.document;
  if (!doc) blocked = true;
} catch (e) {
  // If the browser ever refuses access to the page from this frame, the fixes
  // cannot be applied at all, and the status box should say so rather than
  // leaving a blank space.
  blocked = true;
}
let lastReport = null;   // declared before patch() runs, not after

// Each fix records whether it found the element it was looking for. If Streamlit
// renames one of these test IDs in a future release, the count of misses is what
// tells us, rather than the page quietly losing a landmark.
// Which palette to use is read from the page itself: Streamlit colors <body> from its
// active theme, and the app never overrides that element, so the color of <body> says
// which theme is in force however it was chosen (menu, system setting, or default).
// An earlier version read the choice from localStorage instead, which worked locally
// but not on Streamlit Community Cloud, where that read fails and every theme then
// fell back to the system setting.
function themeIsDark() {
  try {
    const bg = window.parent.getComputedStyle(doc.body).backgroundColor;
    const m = bg.match(/rgba?\(([^)]+)\)/);
    if (m) {
      const [r, g, b, a] = m[1].split(',').map(x => parseFloat(x));
      if (a === undefined || a > 0) {
        // Rec. 709 luma, which is enough to tell a dark surface from a light one.
        return (0.2126 * r + 0.7152 * g + 0.0722 * b) < 128;
      }
    }
  } catch (e) { /* fall through to the system setting */ }
  try {
    return window.parent.matchMedia('(prefers-color-scheme: dark)').matches;
  } catch (e) {
    return false;
  }
}

function syncTheme() {
  if (blocked) return;
  const want = themeIsDark() ? 'dark' : 'light';
  if (doc.documentElement.getAttribute('data-slop-theme') !== want) {
    doc.documentElement.setAttribute('data-slop-theme', want);
  }
}

function patch() {
  if (blocked) { report(['the page itself (this browser blocked access to it)']); return; }
  syncTheme();
  const missing = [];

  // 1. The sidebar is a <section> with aria-expanded, which that role does not allow.
  //    Naming it a navigation landmark makes the attribute valid and gives screen
  //    reader users a "navigation" region to jump to.
  const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
  if (sidebar) {
    if (sidebar.getAttribute('role') !== 'navigation') {
      sidebar.setAttribute('role', 'navigation');
      sidebar.setAttribute('aria-label', 'Course pages');
    }
  } else { missing.push('sidebar (section[data-testid=stSidebar])'); }

  // 2. The page list is a <ul> that mixes section headers with <div> wrappers holding
  //    the <li> links. Dropping the list role from the <ul> and giving each wrapper a
  //    list role puts every <li> inside a real list.
  const navLists = doc.querySelectorAll('ul[data-testid="stSidebarNavItems"]');
  if (navLists.length) {
    navLists.forEach(ul => {
      ul.setAttribute('role', 'none');
      [...ul.children].forEach(child => {
        if (child.tagName === 'DIV' && child.querySelector('li')) {
          child.setAttribute('role', 'list');
        }
      });
    });
  } else { missing.push('page list (ul[data-testid=stSidebarNavItems])'); }

  // 3. Without a main landmark a screen reader cannot skip the navigation.
  const main = doc.querySelector('section[data-testid="stMain"]');
  if (main) {
    if (main.getAttribute('role') !== 'main') {
      main.setAttribute('role', 'main');
      main.setAttribute('aria-label', 'Page content');
    }
  } else { missing.push('content area (section[data-testid=stMain])'); }

  // 4. Streamlit's sidebar toggle ships with an empty aria-label, so a screen reader
  //    announces a button with no name. The label is supplied here.
  doc.querySelectorAll('[data-testid="stSidebarCollapseButton"] button, ' +
                       '[data-testid="stExpandSidebarButton"] button').forEach(b => {
    if (!b.getAttribute('aria-label')) b.setAttribute('aria-label', 'Show or hide the page list');
  });

  // 5. This component's own iframe is decorative and should not be announced.
  doc.querySelectorAll('iframe[title="streamlit_component"], .stCustomComponentV1')
     .forEach(f => { f.setAttribute('aria-hidden', 'true'); f.setAttribute('tabindex', '-1'); });

  report(missing);
}

function report(missing) {
  const state = missing.join('; ');
  if (state === lastReport) return;      // nothing changed since the last pass
  lastReport = state;
  if (missing.length) {
    console.warn('Accessibility patch could not find: ' + state +
                 '. Streamlit markup has probably changed.');
  }
  // SHOW_STATUS is filled in from Python: true only when the instructor opens the
  // app with ?check=1 on the end of the address. The box is drawn inside this
  // component's own frame, so it never disturbs the page itself.
  if (!SHOW_STATUS || !document.body) return;
  document.body.style.margin = '0';
  document.body.innerHTML =
    '<div style="padding:12px 16px;border-left:5px solid;border-top:1px solid;' +
    'border-right:1px solid;border-bottom:1px solid;' +
    'font-family:Georgia,serif;font-size:0.95rem;line-height:1.6;' +
    'background:BOX_SURFACE;color:BOX_TEXT;border-top-color:BOX_BORDER;' +
    'border-right-color:BOX_BORDER;border-bottom-color:BOX_BORDER;' +
    (missing.length ? 'border-left-color:BOX_NO;"' : 'border-left-color:BOX_OK;"') + '>' +
    (missing.length
      ? '<strong>Accessibility check: FAILED.</strong> Could not find ' + state +
        '. The screen reader fixes are not being applied, so Streamlit has probably ' +
        'changed its markup. See "Keeping the app healthy" in the README.'
      : '<strong>Accessibility check: passed.</strong> All three screen reader fixes ' +
        'are in place: navigation landmark, page list, and main landmark.') +
    '</div>';
}

// This script runs before its own frame has a <body>, so the first pass waits for it.
function start() {
  lastReport = null;   // make sure the status box is drawn on this pass
  patch();
  if (blocked) return;
  // Streamlit rebuilds parts of the page as students answer questions, so re-apply.
  new MutationObserver(patch).observe(doc.body, {childList: true, subtree: true});
  // A theme change in this tab does not raise a storage event, so poll as well.
  setInterval(syncTheme, 400);
  window.parent.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', syncTheme);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', start);
} else {
  start();
}
</script>
"""


def patch_streamlit_a11y(show_status: bool = False):
    """Apply the fixes. With show_status=True the component reports what it found.

    The status box is what makes this maintainable: rather than reading Streamlit's
    release notes, open the app with ?check=1 on the end of its address and the app
    tells you whether the fixes still apply to the Streamlit it is running on.
    """
    pal = palette()
    script = _SCRIPT.replace("SHOW_STATUS", "true" if show_status else "false")
    # The status box lives inside its own frame, so it cannot inherit the app's CSS
    # and takes the palette's colors directly.
    for token, key in (("BOX_SURFACE", "SURFACE"), ("BOX_TEXT", "TEXT"),
                       ("BOX_BORDER", "BORDER"), ("BOX_OK", "OK"), ("BOX_NO", "NO")):
        script = script.replace(token, pal[key])
    if show_status:
        # Full width, or the box is drawn in a frame nobody can see.
        components.html(script, height=130)
    else:
        components.html(script, height=0, width=0)
