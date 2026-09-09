#!/usr/bin/env python3
"""Build step: inline the two data files into the website HTML.

The site is opened straight from disk (file://), where a browser refuses to fetch()
local .json files (cross-origin). So the two canonical data files —

    biber_paragraphs.json     -> the `const paragraphsJson = {...}` the Biber tab reads
    emotions_paragraphs.json  -> the `const emotionsJson   = {...}` the Emotional Tone tab reads

— are embedded directly into HAP-E_Researcher_website.html. This script replaces each inline
`const <var> = {...};` blob in place with the current contents of its .json file, so the page
stays a single portable file you can double-click. Re-run it whenever either .json changes
(the website notebook's last cell calls this automatically).

Usage:  python inject_json.py
Authored by Claude.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
HTML = HERE / 'HAP-E_Researcher_website.html'

# (inline JS variable name) -> (data file to embed)
TARGETS = {
    'paragraphsJson': HERE / 'biber_paragraphs.json',
    'emotionsJson':   HERE / 'emotions_paragraphs.json',
}


def _matching_brace_end(s, i):
    """Index of the `}` that closes the `{` at s[i], skipping braces inside JSON strings."""
    assert s[i] == '{', f'expected {{ at {i}, got {s[i]!r}'
    depth, in_str, esc = 0, False, False
    for j in range(i, len(s)):
        c = s[j]
        if in_str:
            if esc:
                esc = False          # this char is escaped; consume it literally
            elif c == '\\':
                esc = True            # next char is escaped
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return j
    raise ValueError('unbalanced braces')


def replace_const(html, varname, blob):
    """Replace the object literal in `const <varname> = {...};` with `blob` (pretty JSON)."""
    anchor = f'const {varname} = '
    n = html.count(anchor)
    if n != 1:
        raise SystemExit(f'expected exactly one `{anchor}` in HTML, found {n}')
    open_i = html.index(anchor) + len(anchor)
    if html[open_i] != '{':
        raise SystemExit(f'`{anchor}` is not followed by an object literal '
                         f'(saw {html[open_i:open_i + 20]!r})')
    end_i = _matching_brace_end(html, open_i)
    return html[:open_i] + json.dumps(blob, indent=2) + html[end_i + 1:]


def main():
    html = HTML.read_text()
    for var, path in TARGETS.items():
        if not path.exists():
            raise SystemExit(f'{path.name} not found — generate it first (website notebook / 6b).')
        blob = json.loads(path.read_text())
        html = replace_const(html, var, blob)
        print(f'  inlined {path.name}  ->  const {var}  ({len(json.dumps(blob)):} chars)')
    HTML.write_text(html)
    print(f'Updated {HTML.name}')


if __name__ == '__main__':
    main()
