# Post-build SEO for the built site folder: one H1, head metadata, JSON-LD, sitemap, robots. python seo_post.py <outdir>
import sys, os, re, json, html as H
out = sys.argv[1]; BASE = 'https://www.parkstory.com/'
GUIDES = ['automated-parking-cost','automated-parking-vs-agv','automated-parking-reliability','automated-parking-retrieval-time','ev-charging']
H1TOK = re.compile(r'(?<![\w-])h1(?![\w-])')
def dup_css(css):
    toks = re.split(r'([{}])', css); outp = []
    for k, t in enumerate(toks):
        if k + 1 < len(toks) and toks[k+1] == '{' and t not in '{}' and H1TOK.search(t) and not t.lstrip().startswith('@'):
            parts = t.split(','); t = ','.join(parts + [H1TOK.sub('h2.h1x', q) for q in parts if H1TOK.search(q)])
        outp.append(t)
    return ''.join(outp)
def one_h1(s):
    s = s.replace('<h1 class="bs-word bs-plogo">', '<div class="bs-word bs-plogo">', 1)
    i = s.find('<div class="bs-word bs-plogo">'); j = s.find('</h1>', i); s = s[:j] + '</div>' + s[j+5:]
    s = s.replace('<p class="bs-claim">', '<h1 class="bs-claim">', 1); i = s.find('<h1 class="bs-claim">'); j = s.find('</p>', i); s = s[:j] + '</h1>' + s[j+4:]
    first = s.find('<h1 class="bs-claim">')
    def demote(m):
        if m.start() == first: return m.group(0)
        attrs = m.group(1) or ''
        if 'class="' in attrs: attrs = attrs.replace('class="', 'class="h1x ', 1)
        else: attrs = ' class="h1x"' + attrs
        return '<h2' + attrs + '>'
    s = re.sub(r'<h1(\s[^>]*)?>', demote, s)
    # closing tags: every </h1> except the claim's
    k = s.find('</h1>', first); parts = s[:k+5], s[k+5:]
    s = parts[0].replace('</h1>', '</h2>', parts[0].count('</h1>') - 1) if parts[0].count('</h1>') > 1 else parts[0]
    s = s + parts[1].replace('</h1>', '</h2>')
    bits = re.split(r'(<style[^>]*>|</style>)', s); inside = False; res = []
    for b in bits:
        if b.startswith('<style'): inside = True; res.append(b); continue
        if b == '</style>': inside = False; res.append(b); continue
        res.append(dup_css(b) if inside else b)
    s = ''.join(res)
    s = s.replace('</head>', '<style>h1.bs-claim{margin:0}</style></head>', 1)
    return s
def faq_ld(s):
    f = s.find('id="faq"'); e = s.find('</section>', f); blk = s[f:e]
    qs = re.findall(r'<details class="ov-q"><summary>(.*?)</summary><div><p>(.*?)</p>', blk, re.S)
    return {"@type":"FAQPage","@id":BASE+"#faq","mainEntity":[{"@type":"Question","name":H.unescape(q),"acceptedAnswer":{"@type":"Answer","text":H.unescape(re.sub('<[^>]+>','',a))}} for q, a in qs]}, len(qs)
ORG = {"@type":"Organization","@id":BASE+"#org","name":"Parkstory","url":BASE,"email":"info@parkstory.com",
 "subOrganization":[{"@type":"Organization","name":n,"address":{"@type":"PostalAddress","addressLocality":c,"addressCountry":k}} for n,c,k in (("Parkstory GmbH","Munich","DE"),("Parkstory, Inc.","Gastonia","US"),("Parkstory Manufacturing GmbH","Kehl","DE"),("Parkstory Kft.","Budapest","HU"))]}
PRODUCTS = [("TilePark","Automated parking without ramps or drive aisles: independent conveyors move cars in X and Y on every level, and car elevators move them between levels."),
 ("TilePark Automated Stackers","A TilePark conveyor grid on one level with stackers above selected conveyors, for up to four cars on the footprint of one."),
 ("TilePark Tower","A central lift with TilePark conveyors on every level of a steel rack: from 2 to 24 cars per level, up to 13 levels.")]
DESC = "TilePark automated parking by Parkstory: no ramps or drive aisles, more cars on less floor area, and space you can build, sell or rent. Engineered and built in Germany and the USA."
for fn in sorted(os.listdir(out)):
    if not fn.endswith('.html') or fn.replace('.html','') in GUIDES: continue
    p = os.path.join(out, fn); s = open(p).read()
    if '<h1 class="bs-word bs-plogo">' in s: s = one_h1(s)
    head = '<link rel="canonical" href="%s">' % BASE
    if fn == 'index.html':
        faq, nq = faq_ld(s)
        ld = {"@context":"https://schema.org","@graph":[ORG,{"@type":"WebSite","@id":BASE+"#site","url":BASE,"name":"Parkstory","publisher":{"@id":BASE+"#org"}},
              {"@type":"WebPage","@id":BASE+"#page","url":BASE,"name":"TilePark automated parking","description":DESC,"isPartOf":{"@id":BASE+"#site"}}]
              + [{"@type":"Product","name":n,"description":d,"brand":{"@type":"Brand","name":"Parkstory"},"manufacturer":{"@id":BASE+"#org"}} for n, d in PRODUCTS] + [faq]}
        head += ('<meta name="description" content="%s"><meta property="og:type" content="website"><meta property="og:title" content="TilePark automated parking | Parkstory">'
                 '<meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:site_name" content="Parkstory">'
                 '<script type="application/ld+json">%s</script>') % (H.escape(DESC), H.escape(DESC), BASE, json.dumps(ld, ensure_ascii=False))
        print('index: FAQ questions in JSON-LD', nq)
    else:
        head += '<meta name="robots" content="noindex">'
    s = s.replace('</head>', head + '</head>', 1)
    open(p, 'w').write(s)
    print(fn, 'h1:', len(re.findall(r'<h1[\s>]', s)))
urls = [BASE] + [BASE + g for g in GUIDES]
open(os.path.join(out, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>%s</loc></url>\n' % u for u in urls) + '</urlset>\n')
open(os.path.join(out, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n' % BASE)
print('sitemap + robots written')
