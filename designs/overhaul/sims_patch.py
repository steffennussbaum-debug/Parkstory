# sims_patch.py in.html out.html sims3d.min.js
# The stacker and EV charging simulators are open right away (no "Open the simulation" button) and get a
# photorealistic 3D view on top of their 2D logic (3D/2D switch, like the "pick a car" simulator).
import re, sys
src, dst, bundle = sys.argv[1:4]
h = open(src, encoding='utf-8').read()
n = h.count('<div class="sx-fold"><button type="button" class="sx-open" aria-expanded="false">')
assert n == 2, n
h = h.replace('<div class="sx-fold"><button type="button" class="sx-open" aria-expanded="false">',
              '<div class="sx-fold open"><button type="button" class="sx-open" aria-expanded="true">')
a = 'let mode=1,L=4,S=3,busy=false,cars=[],ground,stacks,dyn,nextId=1,moves=0;'
assert h.count(a) == 1
h = h.replace(a, a + 'window.__zsim={get cars(){return cars},get stacks(){return stacks},get S(){return S},C,R,GC};')
CSS = '''<style id="p3-css">
.p3-host{position:relative;min-width:0}
.p3-host>.p3-canvas{position:absolute;inset:0;width:100%!important;height:100%!important;display:block;border-radius:12px;cursor:grab}
.p3-host:not(.p3-2d)>#zSvg,.p3-host:not(.p3-2d)>.board-wrap{visibility:hidden}
.p3-host.p3-2d>.p3-canvas{display:none}
.p3-stack{aspect-ratio:474/400;align-self:center}
.p3-stack>#zSvg{position:absolute;inset:0;width:100%;height:100%}
.p3-toggle{position:absolute;top:10px;right:10px;z-index:3;display:flex;gap:2px;padding:3px;border-radius:999px;background:#07150fd9}
.p3-toggle button{border:0;background:none;color:#cfe0d6;font:700 .78rem/1 Inter,Arial,sans-serif;padding:.4rem .7rem;border-radius:999px;cursor:pointer}
.p3-toggle button.on{background:#b8f03c;color:#07150f}
</style>'''
h = h.replace('</head>', CSS + '</head>', 1)
js = open(bundle, encoding='utf-8').read()
i = h.rindex('</body>'); h = h[:i] + '<script id="p3-js">try{delete window.__THREE__}catch(e){}' + js + '</script>' + h[i:]
open(dst, 'w', encoding='utf-8').write(h)
print('ok')
