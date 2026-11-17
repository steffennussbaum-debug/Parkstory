# tablet_patch.py in.html out.html
# Touch screens up to tablet size (for example an unfolded foldable) get the phone menu: a top bar that opens
# the contents as a slide-in panel, instead of the narrow side menu that has to be scrolled inside itself.
# Only the menu rules change; the content layout keeps its own breakpoints.
import re, sys
src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()
Q_OLD = '(width<=600px)'
Q_NEW = '(width<=600px),(pointer:coarse) and (width<=1180px)'
MENU = re.compile(r'\.hr-(shell|tab|rail|top|close)\b')

def block_end(s, i):  # i = index of the "{" that opens the @media block
    d = 0
    for k in range(i, len(s)):
        if s[k] == '{': d += 1
        elif s[k] == '}':
            d -= 1
            if d == 0: return k
    raise ValueError

out, pos, n_css = [], 0, 0
for m in re.finditer(r'@media \(width<=600px\)\s*\{', h):
    if m.start() < pos: continue
    i = m.end() - 1; j = block_end(h, i); body = h[i:j + 1]
    in_style = h.rfind('<style', 0, m.start()) > h.rfind('</style>', 0, m.start())
    if in_style and MENU.search(body):
        rules = re.findall(r'([^{}]+)\{([^{}]*)\}', body[1:-1])
        menu = [r for r in rules if MENU.search(r[0]) or re.search(r'\.(lang-sw|cx-pill|un-tog)\b|^\s*main section,main header', r[0])]
        if len(menu) == len(rules):   # a pure menu block: widen its condition
            out.append(h[pos:m.start()]); out.append('@media ' + Q_NEW + body)
        else:                         # mixed: keep it for phones, add the menu rules for tablets after it
            out.append(h[pos:j + 1]); out.append('@media ' + Q_NEW + '{' + ''.join(a + '{' + c + '}' for a, c in menu) + '}')
        pos = j + 1; n_css += 1
out.append(h[pos:]); h = ''.join(out)

n_js = 0
for old in ('const phone=()=>matchMedia("(width<=600px)").matches',
            "off=matchMedia('(width<=600px)').matches&&tab?tab.offsetHeight:0",
            "const off=matchMedia('(width<=600px)').matches?(document.querySelector('.hr-tab')||{}).offsetHeight||0:0"):
    c = h.count(old); assert c == 1, (old, c)
    h = h.replace(old, old.replace(Q_OLD, Q_NEW)); n_js += 1
open(dst, 'w', encoding='utf-8').write(h)
print('menu rules', n_css, 'scripts', n_js)
