"""
Builds Parkstory's one-page site in every homepage design.

    python3 designs/build.py <source.html> <out-dir>

The source is Parkstory's own single-file page (for example Parkstory_13.html,
with images and videos embedded). Its content, structure and interactive
simulators stay exactly as they are. For each design this script

  1. moves embedded images and videos into <out-dir>/assets (shared by all),
  2. self-hosts the fonts and maps the page's font names ("Outfit", "Inter")
     onto the design's typefaces,
  3. recolours the page: CSS variables, plus the hard-coded colours in the
     page's CSS and scripts (inline SVG artwork such as the logo is untouched),
  4. adds the design's finishing rules (radii, weights, labels, cards),
  5. adds a small bar to switch between the designs.

Output: index.html (the page cleaned up), as-sent.html (untouched, for comparison)
and design-a.html ... design-f.html (each design, with the same clean-up).
"""

import base64
import hashlib
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, 'node_modules')

# ---------------------------------------------------------------- designs --
DESIGNS = [
    ('index', '0', 'Clean', 'The page as sent, cleaned up: one type family, calmer labels and panels'),
    ('as-sent', 'S', 'As sent', 'The page exactly as sent, for comparison'),
    ('design-a', 'A', 'Architectural Future', 'Minimal and bright, warm paper and oxide'),
    ('design-b', 'B', 'Technological Disruption', 'Cinematic dark, lime as signal'),
    ('design-c', 'C', 'Industrial Intelligence', 'Graphite, orange, engineering type'),
    ('design-d', 'D', 'Engineering Heritage', 'Light chronicle in the Parkstory CI'),
    ('design-e', 'E', 'Built by Parkstory', 'Shop-floor dark, bold type'),
    ('design-f', 'F', 'Proven Disruption', 'Dark CI with proven-mint accents'),
]

# Colours used by the source page, mapped per design (6-digit hex, lower case;
# an alpha suffix such as #07150fd9 is kept).
GREYS_WARM = {
    'c8dccf': 'd3cec5', 'a2beb0': '9b968e', 'c5d9cf': 'd3cec5', 'e6f0ea': 'ece8e1', 'a9c3b5': 'aaa49b',
    '8fb3a0': '8f8a82', '8fb8a2': '8f8a82', 'cfe0d6': 'd6d1c8', 'ddeae3': 'e2ddd5', '8fae9e': '8f8a82',
    'cbdbd3': 'd3cec5', '93b4a3': '938e86', 'aabeb4': 'aaa49b', '608774': '6f6a63', 'd9e1dd': 'dcd8d0',
    '7f9f8f': '838078', 'bbcdc4': 'c2bdb4',
}
GREYS_STEEL = {
    'c8dccf': 'cfd1d3', 'a2beb0': '8d9297', 'c5d9cf': 'c9cbcd', 'e6f0ea': 'e9e8e4', 'a9c3b5': '9da2a7',
    '8fb3a0': '8d9297', '8fb8a2': '8d9297', 'cfe0d6': 'd3d5d7', 'ddeae3': 'e1e2e3', '8fae9e': '8d9297',
    'cbdbd3': 'cfd1d3', '93b4a3': '8d9297', 'aabeb4': 'a3a8ad', '608774': '6b7075', 'd9e1dd': 'dcdddf',
    '7f9f8f': '7d8287', 'bbcdc4': 'bfc2c5',
}
HEX = {
    'design-a': {
        '07150f': '161615', '040d09': '0e0e0d', '0f261b': '22211f', '0b1f16': '161615', '0d1e16': '1b1a18',
        '0d2219': '1d1c1a', '2e4f3f': '3a3835', '23784a': 'a8442b', '1f6b3f': '8f3720', '267d45': 'b5502f',
        '2f9452': 'a8442b', 'b8f03c': 'e3a58f', 'a6e36b': 'e9b8a6', '5ee3a1': 'e3a58f', 'f6f3ea': 'f3f1ec',
        'eef0e6': 'e9e5dc', 'e4ede8': 'ebe7df', '284637': '2d2b28', '4b6558': '6b6862', '5f7a6c': '77736c',
        '2c3e35': '2d2b28', '3a4c43': '45423d', **GREYS_WARM,
    },
    'design-c': {
        '07150f': '0e1012', '040d09': '0a0b0c', '0f261b': '22262a', '0b1f16': '0e1012', '0d1e16': '16191c',
        '0d2219': '181b1e', '2e4f3f': '3a3f44', '23784a': 'ff5b1f', '1f6b3f': 'd9461a', '267d45': 'ff7a45',
        '2f9452': 'ff5b1f', 'b8f03c': 'ff5b1f', 'a6e36b': 'ff8a5c', '5ee3a1': 'ff8a5c', **GREYS_STEEL,
    },
    'design-d': {'f6f3ea': 'f2f0e9', 'eef0e6': 'e8e5db', '23784a': '3f6b1a', '1f6b3f': '3f6b1a', '267d45': '4a7a20'},
    'design-e': {'07150f': '0c120e', '040d09': '090e0b', '0f261b': '16211a', '0b1f16': '0c120e'},
    'design-f': {},
    'design-b': {},
}
DARK = {'design-b', 'design-c', 'design-e', 'design-f'}

# --------------------------------------------------------------- tokens ----
TOKENS = {
    'design-a': """
  --navy:#161615; --navy-deep:#0e0e0d; --navy-lift:#22211f;
  --green:#a8442b; --green-bright:#e3a58f; --green-ink:#8f3720; --green-hover:#b5502f;
  --green-wash:#a8442b14; --green-edge:#a8442b40;
  --bg:#f3f1ec; --surface:#fbfaf7; --surface-2:#e9e5dc;
  --ink:#121212; --text:#2d2b28; --muted:#6b6862; --line:#1212121f; --line-soft:#12121212;
  --r:2px; --r-lg:2px; --r-sm:2px; --card-sh:none;""",
    'design-b': """
  --navy:#07150f; --navy-deep:#040d09; --navy-lift:#0f261b;
  --green:#b8f03c; --green-bright:#b8f03c; --green-ink:#b8f03c;
  --green-wash:#b8f03c14; --green-edge:#b8f03c4d;
  --bg:#040d09; --surface:#07150f; --surface-2:#0f261b;
  --ink:#ffffff; --text:#c5d9cf; --muted:#a2beb0; --line:#ffffff1a; --line-soft:#ffffff12;
  --r:4px; --r-lg:4px; --r-sm:3px; --card-sh:none;""",
    'design-c': """
  --navy:#0e1012; --navy-deep:#0a0b0c; --navy-lift:#22262a;
  --green:#ff5b1f; --green-bright:#ff5b1f; --green-ink:#ff5b1f; --green-hover:#ff7a45;
  --green-wash:#ff5b1f14; --green-edge:#ff5b1f55; --amber:#ffb020;
  --bg:#141618; --surface:#1b1e21; --surface-2:#202428;
  --ink:#e9e8e4; --text:#c9c8c3; --muted:#8d9297; --line:#ffffff1f; --line-soft:#ffffff12;
  --r:0px; --r-lg:0px; --r-sm:0px; --card-sh:none;""",
    'design-d': """
  --green:#3f6b1a; --green-ink:#3f6b1a; --green-hover:#4a7a20;
  --green-wash:#3f6b1a12; --green-edge:#3f6b1a3d;
  --bg:#f2f0e9; --surface:#ffffff; --surface-2:#e8e5db;
  --ink:#0b1a13; --text:#2a3b32; --muted:#4e5f57; --line:#0b1a1324; --line-soft:#0b1a1314;
  --r:4px; --r-lg:6px; --r-sm:3px; --card-sh:none;""",
    'design-e': """
  --navy:#0c120e; --navy-deep:#090e0b; --navy-lift:#16211a;
  --green:#b8f03c; --green-bright:#b8f03c; --green-ink:#b8f03c;
  --green-wash:#b8f03c12; --green-edge:#b8f03c55;
  --bg:#090e0b; --surface:#101813; --surface-2:#16211a;
  --ink:#ffffff; --text:#cddbd3; --muted:#a2b5aa; --line:#ffffff1a; --line-soft:#ffffff10;
  --r:2px; --r-lg:2px; --r-sm:2px; --card-sh:none;""",
    'design-f': """
  --navy:#07150f; --navy-deep:#040d09; --navy-lift:#0f261b;
  --green:#5ee3a1; --green-bright:#b8f03c; --green-ink:#5ee3a1;
  --green-wash:#5ee3a112; --green-edge:#5ee3a14d;
  --bg:#040d09; --surface:#040d09; --surface-2:#07150f;
  --ink:#ffffff; --text:#c5d9cf; --muted:#a2beb0; --line:#ffffff24; --line-soft:#ffffff14;
  --r:4px; --r-lg:4px; --r-sm:3px; --card-sh:none;""",
}
# the DNA part of the page (.gx) has its own colour variables
GX_DARK = """
.gx{--paper:var(--bg);--paper-2:var(--surface-2);--ink:var(--ink);--mid:var(--muted);--rule:var(--line);
  --green:var(--green);--text:var(--text)}"""
GX_A = """
.gx{--paper:#f3f1ec;--paper-2:#e9e5dc;--ink:#121212;--mid:#6b6862;--rule:#1212121f;--green:#a8442b}"""

# The page's headings and small labels, as its own typography layer lists them.
# Wrapped in :is() with html body so these rules win over that layer.
H = ('html body :is(main h1,main h2,main h3,.bs-claim,.opp-h,.loc-h,.opp-feas-h,.part-open h2,.cd-h2,.fab-h,.motto,'
     '.opp-qh,.fut-sub,.fut-qh,.cd-ledger-n,.cd-uptime-n,.nat-tag,.loc-c h3,.opp-q b,.nat-eng b,.fut-cards b,.fut-cmp h3,'
     '.pl-offer h3,.sg-steps b,.pb figcaption b,.cmp-h,.eng-h)')
E = ('html body :is(.hiw-eyebrow,.opp-eye,.opp-k,.loc-eye,.sg-eye,.pl-eye,.part-k,.tour-eye,.cd-label,.bs-eye,.nat-eye,'
     '.pf .pl-eye,.fut-st,.nw-evid-h,.cmp-eye,.eng-k,.nw-track-k)')

# Clean-up, applied to every version except "As sent": one type family (Outfit for headings, Inter for
# text and labels), one label style, flat cards, plain dark panels and a comfortable line length.
CLEAN = f"""
{H}{{font-family:"Outfit","Inter",Arial,sans-serif!important;font-stretch:100%!important;font-weight:600!important;letter-spacing:-.025em!important}}
{E}{{font-family:"Inter",Arial,sans-serif!important;text-transform:uppercase!important;letter-spacing:.12em!important;font-weight:600!important;font-size:.74rem!important}}
html body :is(.part-open,.sg,.nat,.pf,.loc-box,.fut-urg){{background-image:none!important}}
html body :is(.card,.pc,.opp-note,.gx .cd-rail,.gx .cd-plant){{box-shadow:none!important}}
main section p{{max-width:72ch}}
"""

# design finishing rules, applied after the page's own CSS
EXTRA_RAW = {
    'design-a': """
{H}{font-weight:600!important;letter-spacing:-.03em}
{HE}{font-family:"PS Serif",Georgia,serif!important;font-style:italic!important;font-weight:400!important;letter-spacing:-.01em}
{E}{color:var(--muted)!important;letter-spacing:.16em}
.card,.pc,.opp-q>div,.fut-cmp>div,.gx .cd-rail,.gx .cd-plant{box-shadow:none!important;border:1px solid var(--line)!important}
.btn,.btn-primary,.cta-b1,.opp-cta a{border-radius:0!important}""",
    'design-b': """
{H}{font-weight:500!important;letter-spacing:-.035em}
{E}{color:var(--muted)!important;letter-spacing:.14em}
.card,.pc,.opp-q>div,.fut-cmp>div,.opp-note,.gx .cd-rail,.gx .cd-plant{box-shadow:none!important;border:1px solid var(--line)!important}
section{border-color:var(--line)}""",
    'design-c': """
{H}{font-weight:600!important;letter-spacing:-.02em}
.hiw-eyebrow,.who,.lbl,.cd-label,.cd-kicker{font-family:"PS Mono",ui-monospace,monospace!important;color:var(--green)!important;letter-spacing:.08em}
.card,.pc,.opp-q>div,.fut-cmp>div,.opp-note,.gx .cd-rail,.gx .cd-plant{box-shadow:none!important;border:1px solid var(--line)!important}
.btn,.btn-primary,.cta-b1,.opp-cta a{border-radius:0!important}""",
    'design-d': """
{H}{font-weight:500!important;letter-spacing:-.03em}
{E}{display:flex;align-items:center;gap:.7rem;color:var(--muted)!important}
{EB}{content:"";flex:none;width:10px;height:10px;border-radius:50%;background:#b8f03c;box-shadow:0 0 0 1px #0b1a13}
.card,.pc,.opp-q>div,.fut-cmp>div,.gx .cd-rail,.gx .cd-plant{box-shadow:none!important;border:1px solid var(--line)!important}""",
    'design-e': """
{H}{font-weight:700!important;letter-spacing:-.04em}
{E}{display:inline-block;border:1px solid #b8f03c73;padding:.35rem .7rem;border-radius:2px;color:#b8f03c!important}
.card,.pc,.opp-q>div,.fut-cmp>div,.opp-note,.gx .cd-rail,.gx .cd-plant{box-shadow:none!important;border:1px solid var(--line)!important}
.btn,.btn-primary,.cta-b1,.opp-cta a{border-radius:2px!important}""",
    'design-f': """
{H}{font-weight:500!important;letter-spacing:-.035em}
{HE}{color:#b8f03c!important}
{E}{color:#5ee3a1!important;letter-spacing:.14em}
.card,.pc,.opp-q>div,.fut-cmp>div,.opp-note,.gx .cd-rail,.gx .cd-plant{box-shadow:none!important;background:transparent!important;border:1px solid var(--line)!important}""",
}

HE = 'html body :is(main h1,main h2,main h3) em'
EXTRA = {k: v.replace('{H}', H).replace('{HE}', HE).replace('{EB}', E[:-1] + ')::before').replace('{E}', E)
         for k, v in EXTRA_RAW.items()}

# ---------------------------------------------------------------- fonts ----
FONT_FILES = {
    'outfit.woff2': '@fontsource-variable/outfit/files/outfit-latin-wght-normal.woff2',
    'outfit-ext.woff2': '@fontsource-variable/outfit/files/outfit-latin-ext-wght-normal.woff2',
    'inter.woff2': '@fontsource-variable/inter/files/inter-latin-wght-normal.woff2',
    'inter-ext.woff2': '@fontsource-variable/inter/files/inter-latin-ext-wght-normal.woff2',
    'inter-tight.woff2': '@fontsource-variable/inter-tight/files/inter-tight-latin-wght-normal.woff2',
    'newsreader-italic.woff2': '@fontsource-variable/newsreader/files/newsreader-latin-wght-italic.woff2',
    **{
        f'plex-sans-{w}.woff2': f'@fontsource/ibm-plex-sans/files/ibm-plex-sans-latin-{w}-normal.woff2'
        for w in (400, 500, 600)
    },
    **{
        f'plex-mono-{w}.woff2': f'@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-{w}-normal.woff2'
        for w in (400, 500)
    },
}
LATIN_EXT = 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1EFF,U+20A0-20C0,U+2113,U+2C60-2C7F'


def face(names, file, weight='100 900', style='normal', ext=None):
    out = []
    for n in names:
        out.append(f'@font-face{{font-family:"{n}";src:url(fonts/{file}) format("woff2");font-weight:{weight};'
                   f'font-style:{style};font-display:swap}}')
        if ext:
            out.append(f'@font-face{{font-family:"{n}";src:url(fonts/{ext}) format("woff2");font-weight:{weight};'
                       f'font-style:{style};font-display:swap;unicode-range:{LATIN_EXT}}}')
    return '\n'.join(out)


DISPLAY = ['Outfit', 'Outfit Variable', 'Archivo']
TEXT = ['Inter', 'Inter Variable', 'IBM Plex Mono']


def fonts_for(slug):
    if slug == 'as-sent':
        return face(DISPLAY, 'outfit.woff2', ext='outfit-ext.woff2') + '\n' + face(TEXT, 'inter.woff2', ext='inter-ext.woff2')
    if slug == 'design-a':
        return face(DISPLAY + TEXT, 'inter-tight.woff2') + '\n' + face(['PS Serif'], 'newsreader-italic.woff2', style='italic')
    if slug == 'design-c':
        sans = DISPLAY + TEXT[:2]
        rows = [face(sans, f'plex-sans-{w}.woff2', weight=str(w)) for w in (400, 500, 600)]
        rows.append(face(sans, 'plex-sans-600.woff2', weight='700 900'))
        rows += [face(['PS Mono', 'IBM Plex Mono'], f'plex-mono-{w}.woff2', weight=str(w)) for w in (400, 500)]
        return '\n'.join(rows)
    return face(DISPLAY, 'outfit.woff2', ext='outfit-ext.woff2') + '\n' + face(TEXT, 'inter.woff2', ext='inter-ext.woff2')


# ------------------------------------------------------------ transforms ---
def map_hex(text, mapping):
    if not mapping:
        return text

    def sub(m):
        h = m.group(1).lower()
        return '#' + mapping.get(h, h) + (m.group(2) or '')

    return re.sub(r'#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?(?![0-9a-fA-F])', sub, text)


def light(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    # pale and unsaturated (cream, off-white, pale grey-green), not a bright accent such as lime
    return 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.82 and max(r, g, b) - min(r, g, b) < 0.15


# corner radius per design: the page's rounded corners are capped at this value
RADIUS = {'design-a': 2, 'design-b': 6, 'design-c': 0, 'design-d': 8, 'design-e': 2, 'design-f': 6}


def cap_radius(css, cap):
    def one(v):
        n = float(v.group(1))
        return f'{min(n, cap):g}px' if n >= 6 else v.group(0)

    def decl(m):
        return m.group(1) + re.sub(r'(\d+(?:\.\d+)?)px', one, m.group(2))

    return re.sub(r'(border(?:-[a-z]+)*-radius:)([^;{}]*)', decl, css)


KNOBS = ('.zunits button.on', '.tg::after', '.vl-steps div::before')


def darken_light_sections(css):
    """In dark designs, hard-coded light surfaces and dark text become variables."""

    def rule(m):
        sel, body = m.group(1), m.group(2)
        if not any(k in sel for k in KNOBS):
            body = re.sub(r'background(-color)?:#fff(fff)?\b', r'background\1:var(--surface)', body)
            # any other plain light background (cream, pale green ...) becomes the page background
            body = re.sub(r'background(-color)?:#([0-9a-fA-F]{6})\b(?![0-9a-fA-F])',
                          lambda m: f'background{m.group(1) or ""}:var(--bg)' if light(m.group(2)) else m.group(0), body)
        body = re.sub(r'(?<![-\w])color:#(0b1f16|07150f)\b', 'color:var(--ink)', body) if not re.search(
            r'background:#b8f03c|background:var\(--green-bright\)|tour-play|cta-b1|bee-n|skip|tour-ch span|bs-nav a:hover', sel + body) else body
        body = re.sub(r'(?<![-\w])color:#(2c3e35|3a4c43|284637)\b', 'color:var(--text)', body)
        body = re.sub(r'(?<![-\w])color:#5f7a6c\b', 'color:var(--muted)', body)
        body = re.sub(r'(?<![-\w])color:#(23784a|1f6b3f)\b', 'color:var(--green)', body)
        body = re.sub(r'background(-color)?:#f6f3ea\b', r'background\1:var(--bg)', body)
        body = re.sub(r'background(-color)?:#(eef0e6|e4ede8)\b', r'background\1:var(--surface-2)', body)
        return sel + '{' + body + '}'

    return re.sub(r'([^{}]+)\{([^{}]*)\}', rule, css)


def switcher(current):
    links = []
    for slug, letter, name, _ in DESIGNS:
        on = ' class="on" aria-current="page"' if slug == current else ''
        label = name if letter in '0S' else letter
        links.append(f'<a href="{slug}.html"{on} title="{name}"><b>{label}</b><span>{"" if letter in "0S" else name}</span></a>')
    cur = next(d for d in DESIGNS if d[0] == current)
    cur_label = cur[2] if cur[1] in '0S' else f'Design {cur[1]}'
    return f"""
<nav class="dz" aria-label="Designs"><button type="button" class="dz-btn" aria-expanded="false">{cur_label} ▴</button>{''.join(links)}</nav>
<script>
(function(){{var n=document.querySelector('.dz'),b=n&&n.querySelector('.dz-btn');if(!b)return;
b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)}});}})();
</script>
<style>
.dz{{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:2147483000;display:flex;gap:2px;padding:4px;
  border-radius:999px;background:rgb(18 18 18 / 86%);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  box-shadow:0 10px 30px -10px rgb(0 0 0 / 55%);font:500 12px/1 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
  max-width:calc(100vw - 20px)}}
.dz a{{display:inline-flex;align-items:center;gap:6px;padding:8px 11px;border-radius:999px;color:#e8e8e8;text-decoration:none;
  opacity:.75;white-space:nowrap}}
.dz a:hover{{opacity:1}}
.dz a.on{{background:#fff;color:#111;opacity:1}}
.dz a span{{display:none}}
.dz a.on span{{display:inline}}
.dz-btn{{display:none}}
@media (max-width:720px){{
  .dz{{left:auto;right:12px;bottom:12px;transform:none;flex-direction:column;align-items:stretch;border-radius:16px}}
  .dz-btn{{display:block;appearance:none;border:0;background:transparent;color:#fff;font:inherit;font-weight:600;padding:9px 12px;cursor:pointer}}
  .dz a{{display:none;border-radius:10px}}
  .dz.open a{{display:flex}}
  .dz.open a span{{display:inline}}
}}
@media print{{.dz{{display:none}}}}
</style>"""


def build(src, out):
    html = open(src, encoding='utf-8').read()
    os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
    os.makedirs(os.path.join(out, 'fonts'), exist_ok=True)

    # 1. embedded media -> files
    seen = {}

    def media(m):
        mime, data = m.group(1), m.group(2)
        key = hashlib.sha1(data.encode()).hexdigest()[:12]
        if key not in seen:
            name = f'assets/{key}.{mime.split("/")[1]}'
            with open(os.path.join(out, name), 'wb') as f:
                f.write(base64.b64decode(data))
            seen[key] = name
        return seen[key]

    html = re.sub(r'data:(image/webp|image/png|image/jpeg|video/mp4);base64,([A-Za-z0-9+/=]+)', media, html)

    # 2. fonts: self-hosted, no Google Fonts request
    for name, rel in FONT_FILES.items():
        shutil.copyfile(os.path.join(FONTS, rel), os.path.join(out, 'fonts', name))
    html = re.sub(r'<link[^>]+fonts\.(googleapis|gstatic)\.com[^>]*>\s*', '', html)

    for slug, letter, name, _ in DESIGNS:
        page = html

        def recolour(m, slug=slug):
            open_tag, body, close = m.group(1), m.group(2), m.group(3)
            is_css = open_tag.startswith('<style')
            if is_css and slug in DARK:
                body = darken_light_sections(body)
            if is_css and slug in RADIUS:
                body = cap_radius(body, RADIUS[slug])
            body = map_hex(body, HEX.get(slug, {}))
            return open_tag + body + close

        if slug not in ('index', 'as-sent'):
            page = re.sub(r'(<style[^>]*>)([\s\S]*?)(</style>)', recolour, page)
            page = re.sub(r'(<script(?![^>]*\bsrc=)[^>]*>)([\s\S]*?)(</script>)', recolour, page)

        theme = '<style id="design-fonts">\n' + fonts_for(slug) + '\n</style>\n'
        if slug != 'as-sent':
            theme += f'<style id="design-clean">{CLEAN}</style>\n'
        if slug not in ('index', 'as-sent'):
            gx = GX_A if slug == 'design-a' else (GX_DARK if slug in DARK else '')
            theme += f'<style id="design-theme">\nhtml:root{{{TOKENS[slug]}\n}}{gx}\n{EXTRA[slug]}\n</style>\n'
        page = page.replace('</head>', theme + '</head>', 1)
        if letter != '0':
            suffix = 'As sent' if letter == 'S' else f'Design {letter}'
            page = re.sub(r'<title>(.*?)</title>', rf'<title>\1 · {suffix}</title>', page, count=1)
        page = page.replace('</body>', switcher(slug) + '\n</body>', 1)
        with open(os.path.join(out, f'{slug}.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        print(f'{slug}.html', round(len(page) / 1e6, 2), 'MB')
    print(len(seen), 'media files')


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
