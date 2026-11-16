# prodtabs_patch.py in.html out.html
# "TilePark products" becomes one chapter with three options: the product cards work as tabs and the full content
# of each product (TilePark with its simulator and the Munich video, Automated Stackers, Tower) opens below them.
# The menu lists "TilePark products" once instead of separate entries for TilePark, Video, Stackers and Tower.
import re, sys
src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()

def one(pat, s=None, flags=0):
    m = list(re.finditer(pat, h if s is None else s, flags)); assert len(m) == 1, (pat, len(m)); return m[0]

# 1. menu: drop the TilePark / Video / Stackers / Tower entries, keep the "pick a car" simulator under products
m = one(r'<li><a href="#how-it-works"><span class="t">TilePark</span></a>(<a class="hr-sim" href="#sim-puzzle">.*?</a>)</li>')
sim = m.group(1); h = h[:m.start()] + h[m.end():]
for pat in (r'<li><a href="#video"><span class="t">Video</span>.*?</li>',
            r'<li><a href="#third-dimension"><span class="t">TilePark Automated Stackers</span></a></li>',
            r'<li><a href="#tower"><span class="t">TilePark Tower</span></a></li>'):
    m = one(pat); h = h[:m.start()] + h[m.end():]
m = one(r'<li><a href="#products"><span class="t">TilePark products</span></a>')
h = h[:m.end()] + sim + h[m.end():]

# 2. page: wrap the three product sections in panels below the cards
a = one(r'<section class="pg" id="products">').start()
a_end = h.index('</section>', a) + len('</section>')
hiw = one(r'<section class="hiw after-bio" id="how-it-works">').start()
pb = one(r'<section class="zsec" id="third-dimension">').start()   # the conveyor photo before it stays with TilePark
tw = one(r'<section class="pg pg-tower" id="tower">').start()
nat = h.rfind('<div class="natwrap">', 0, one(r'id="inspired-by-nature"').start())
assert a_end <= hiw < pb < tw < nat
P = lambda k, body: '<div class="pg-panel" data-prod="%s" role="tabpanel">%s</div>' % (k, body)
panels = ('<div class="pg-panels">' + P('tilepark', h[hiw:pb]) + P('stackers', h[pb:tw]) + P('tower', h[tw:nat]) + '</div>\n')
h = h[:a_end] + h[a_end:hiw] + panels + h[nat:]

CSS = '''<style id="prodtabs-css">
.pg-panel[hidden]{display:none!important}
#products .pg-card{position:relative;transition:transform .2s,box-shadow .25s,border-color .25s}
#products .pg-card.on{border-color:var(--green)!important;box-shadow:0 0 0 2px var(--green-edge)!important}
#products .pg-card.on .pg-link{visibility:hidden}
#products .pg-card.on:after{content:"";position:absolute;left:50%;bottom:-9px;width:16px;height:16px;transform:translateX(-50%) rotate(45deg);background:inherit;border-right:2px solid var(--green);border-bottom:2px solid var(--green)}
#products{padding-bottom:clamp(8px,1.5vw,16px)}
@media (max-width:960px){#products .pg-card.on:after{display:none}}
</style>'''
JS = r'''<script id="prodtabs-js">(function(){
 var cards=[].slice.call(document.querySelectorAll('#products .pg-card')),panels=[].slice.call(document.querySelectorAll('.pg-panel'));if(!cards.length||!panels.length)return;
 function show(k,scroll){var changed=false;panels.forEach(function(p){var on=p.dataset.prod===k;if(p.hidden===on){changed=true}p.hidden=!on});
  cards.forEach(function(c){var on=c.dataset.prod===k;c.classList.toggle('on',on);c.setAttribute('aria-selected',on)});
  if(changed)setTimeout(function(){dispatchEvent(new Event('resize'))},30);
  if(scroll){var p=panels.filter(function(p){return p.dataset.prod===k})[0];if(p)scrollTo({top:p.getBoundingClientRect().top+scrollY-8,behavior:'instant'})}}
 cards.forEach(function(c){c.setAttribute('role','tab');c.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();show(c.dataset.prod,true)},true)});
 function reveal(id){var t=id&&document.getElementById(id);if(!t)return;var p=t.closest('.pg-panel');if(p&&p.hidden)show(p.dataset.prod,false)}
 // any link to content inside a closed panel opens that panel first, before the page's own navigation runs
 document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(a)reveal(a.getAttribute('href').slice(1))},true);
 addEventListener('hashchange',function(){reveal(location.hash.slice(1))});
 show('tilepark',false);reveal(location.hash.slice(1));
})();</script>'''
h = h.replace('</head>', CSS + '</head>', 1)
i = h.rindex('</body>'); h = h[:i] + JS + h[i:]
open(dst, 'w', encoding='utf-8').write(h)
print('ok')
