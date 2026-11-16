# onefile.py built_dir out.html [default_slug]
# One self-contained HTML with every design: media and fonts stored once (base64), each design page stored
# gzip-compressed. On open, the chosen design (?d=slug) is unpacked and written into the page; the design
# switcher links become ?d=slug, so switching reloads the same file with another design.
import base64, gzip, os, re, sys
d, out = sys.argv[1], sys.argv[2]; default = sys.argv[3] if len(sys.argv) > 3 else 'index'
SL = ['index', 'as-sent'] + sorted(f[:-5] for f in os.listdir(d) if re.fullmatch(r'design-[a-z]\.html', f))
MIME = {'webp': 'image/webp', 'png': 'image/png', 'jpeg': 'image/jpeg', 'jpg': 'image/jpeg', 'mp4': 'video/mp4',
        'webm': 'video/webm', 'woff2': 'font/woff2'}
PAT = r'(?:assets|fonts)/[0-9A-Za-z_-]+\.(?:webp|png|jpeg|jpg|mp4|webm|woff2)'
used, pages = set(), {}
for s in SL:
    h = open(os.path.join(d, s + '.html'), encoding='utf-8').read()
    used |= set(re.findall(PAT, h))
    for t in SL:  # switcher links -> same file with ?d=
        h = h.replace('href="%s.html"' % t, 'href="?d=%s"' % t)
    pages[s] = base64.b64encode(gzip.compress(h.encode('utf-8'), 9)).decode()
parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">',
         '<title>Parkstory</title><style>html,body{margin:0;background:#141a24;color:#c9d0d9;font:16px system-ui,sans-serif}'
         '#ld{position:fixed;inset:0;display:grid;place-items:center}</style></head><body><div id="ld">Loading Parkstory…</div>']
for p in sorted(used):
    parts.append('<script type="text/plain" data-m="%s" data-t="%s">%s</script>' % (
        p, MIME[p.rsplit('.', 1)[1]], base64.b64encode(open(os.path.join(d, p), 'rb').read()).decode()))
for s in SL:
    parts.append('<script type="text/plain" data-p="%s">%s</script>' % (s, pages[s]))
parts.append('''<script>
(async function(){
 var q=new URLSearchParams(location.search).get('d'),SL=%s,slug=SL.indexOf(q)>=0?q:'%s';
 function bin(b){var s=atob(b),u=new Uint8Array(s.length);for(var i=0;i<s.length;i++)u[i]=s.charCodeAt(i);return u}
 var map={};document.querySelectorAll('script[data-m]').forEach(function(e){map[e.dataset.m]=URL.createObjectURL(new Blob([bin(e.textContent)],{type:e.dataset.t}))});
 var gz=bin(document.querySelector('script[data-p="'+slug+'"]').textContent);
 var html=await new Response(new Blob([gz]).stream().pipeThrough(new DecompressionStream('gzip'))).text();
 html=html.replace(/%s/g,function(p){return map[p]||p});
 document.open();document.write(html);document.close();
})();
</script></body></html>''' % (str(SL).replace("'", '"'), default, PAT.replace('/', '\\/')))
open(out, 'w', encoding='utf-8').write(''.join(parts))
print(len(used), 'media', round(os.path.getsize(out) / 1e6, 1), 'MB')
