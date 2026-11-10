# Adds the "From red to green" case study to the overhaul as a chapter of "Your opportunity".
# python case_patch.py <in.html> <out.html> <story.html> <img_dir> <media_dir>
import sys, re, json, base64, os
src, out, story, imgd, md = sys.argv[1:6]
s = open(src).read()
L = json.loads(re.search(r'const L=(\{.*?\});\nconst ST=', open(story).read(), re.S).group(1))
def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:90], s.count(a)); s = s.replace(a, b)
def b64(p, mime): return 'data:%s;base64,%s' % (mime, base64.b64encode(open(p,'rb').read()).decode())
def vid(n): return '<source src="%s" type="video/webm"><source src="%s" type="video/mp4">' % (b64(os.path.join(md,n+'.webm'),'video/webm'), b64(os.path.join(md,n+'.mp4'),'video/mp4'))
E = L['en']
# English text of the section; the site's translator handles DE/FR/ES through D
EXTRA = {'eye2': ('Case study · fictional example','Fallstudie · fiktives Beispiel','Étude de cas · exemple fictif','Caso práctico · ejemplo ficticio'),
         'menu': ('Case study: from red to green','Fallstudie: von Rot zu Grün','Étude de cas : du rouge au vert','Caso práctico: de rojo a verde')}
D = {}
for k, en in E.items():
    if k in ('at','mio','c0','c1','c2','c3','eye','cb','rp'): continue
    D[en] = [L['de'][k], L['fr'][k], L['es'][k]]
for k,(en,de,fr,es) in EXTRA.items(): D[en] = [de,fr,es]
def t(k): return E[k]
HTML = f'''<section class="rg" id="red-to-green"><div class="rg-wrap">
<div class="rg-hero"><p class="rg-eye">{EXTRA['eye2'][0]}</p><h2 class="rg-h1"><span>{t('h1a')}</span> <em>{t('h1b')}</em></h2><p class="rg-lead">{t('lead')}</p><p class="rg-hint">{t('hint')}</p></div>
<div class="rg-grid"><div class="rg-story">
<article class="rg-ch" data-st="1"><p class="rg-k">{t('k1')}</p><h3>{t('h_1')}</h3><p>{t('p1')}</p><figure><img src="{b64(os.path.join(imgd,'c1.jpg'),'image/jpeg')}" alt="{t('cap1')}" width="960" height="540" loading="lazy"><figcaption>{t('cap1')}</figcaption></figure></article>
<article class="rg-ch" data-st="2"><p class="rg-k">{t('k2')}</p><h3>{t('h_2')}</h3><p>{t('p2')}</p><figure><img src="{b64(os.path.join(imgd,'c2.jpg'),'image/jpeg')}" alt="{t('cap2')}" width="960" height="540" loading="lazy"><figcaption>{t('cap2')}</figcaption></figure></article>
<article class="rg-ch red" data-st="3"><p class="rg-k">{t('k3')}</p><h3>{t('h_3')}</h3><p>{t('p3')}</p>
<div class="rg-ledger"><div><span><span>{t('lv')}</span><small data-noi18n class="rgA1"></small></span><b data-noi18n class="rgV1"></b></div><div><span>{t('lc')}</span><b data-noi18n class="rgC1"></b></div><div class="res"><span>{t('lr')}</span><b data-noi18n class="rgR1 neg"></b></div></div>
<p class="rg-wh">{t('wh')}</p><ul class="rg-ways"><li>{t('w1')}</li><li>{t('w2')}</li><li>{t('w3')}</li></ul></article>
<article class="rg-ch" data-st="4"><p class="rg-k">{t('k4')}</p><h3>{t('h_4')}</h3><p>{t('p4')}</p><p class="rg-note">{t('n4')}</p>
<figure><video class="rgv" muted playsinline preload="none" poster="{b64(os.path.join(imgd,'c2.jpg'),'image/jpeg')}">{vid('common')}</video><button type="button" class="rg-replay"><span aria-hidden="true">↻</span> Replay</button><figcaption>{t('cap4')}</figcaption></figure></article>
<article class="rg-ch grn" data-st="5"><p class="rg-k">{t('k5')}</p><h3>{t('h_5')}</h3><p>{t('p5')}</p>
<figure><video class="rgv" muted playsinline preload="none" poster="{b64(os.path.join(imgd,'c5.jpg'),'image/jpeg')}">{vid('apt')}</video><button type="button" class="rg-replay"><span aria-hidden="true">↻</span> Replay</button><figcaption>{t('cap5')}</figcaption></figure>
<div class="rg-ledger"><div><span><span>{t('lv')}</span><small data-noi18n class="rgA2"></small></span><b data-noi18n class="rgV2"></b></div><div><span>{t('lc2')}</span><b data-noi18n class="rgC2"></b></div><div><span>{t('lf')}</span><b data-noi18n class="rgF2"></b></div><div class="res"><span>{t('lr')}</span><b data-noi18n class="rgR2 pos"></b></div></div></article>
<article class="rg-ch grn" data-st="6"><p class="rg-k">{t('k6')}</p><h3>{t('h_6')}</h3><ul class="rg-ticks"><li>{t('t1')}</li><li>{t('t2')}</li><li>{t('t3')}</li><li>{t('t4')}</li></ul></article>
</div>
<aside class="rg-meter" data-tone="none" aria-live="polite"><div class="rg-mh"><span class="rg-mk">{t('mk')}</span><span class="rg-chip" data-noi18n></span></div><div class="rg-big" data-noi18n>—</div><div class="rg-bar" aria-hidden="true"><i></i></div><div class="rg-barl" data-noi18n aria-hidden="true"><span class="rgb1"></span><span>0</span><span class="rgb2"></span></div>
<div class="rg-rows"><div><span>{t('r1')}</span><b data-noi18n>68</b></div><div><span>{t('r2')}</span><b data-noi18n class="rgPk">—</b></div><div><span>{t('r3')}</span><b data-noi18n class="rgEa">—</b></div><div><span>{t('r4')}</span><b data-noi18n class="rgAr">—</b></div></div><p class="rg-mf">{t('mf')}</p></aside></div>
<div class="rg-cta"><h3>{t('ch')}</h3><p>{t('cp')}</p><a class="btn rg-btn" href="#request">Request a free feasibility study →</a></div>
<p class="rg-foot">{t('ft')}</p></div></section>'''
# insert after the "What you gain" section
i = s.find('<section class="opp" id="opportunity"'); depth = 0
for m in re.compile(r'<section[\s>]|</section>').finditer(s, i):
    depth += -1 if m.group(0).startswith('</') else 1
    if depth == 0: j = m.end(); break
s = s[:j] + HTML + s[j:]
# menu + chapter-view names
li_opp = re.search(r'<li><a href="#opportunity">.*?</li>', s, re.S).group(0)
rep(li_opp, li_opp + '<li><a href="#red-to-green"><span class="t">%s</span></a></li>' % EXTRA['menu'][0])
k = s.find('const FXN='); e = s.find(';\nconst vis=', k); names = json.loads(s[k+len('const FXN='):e]); names['c']['red-to-green'] = EXTRA['menu'][0]
s = s[:k] + 'const FXN=' + json.dumps(names, ensure_ascii=False) + s[e:]
X = {lg: {'mio': L[lg]['mio'], 'at': L[lg]['at'], 'c0': L[lg]['c0'], 'c1': L[lg]['c1'], 'c2': L[lg]['c2'], 'c3': L[lg]['c3']} for lg in L}
JS = '''<script id="rg-js">(()=>{const R=document.getElementById('red-to-green');if(!R)return;const H=document.documentElement,q=c=>R.querySelector(c),X=%s;
const ST={0:{t:'none'},1:{t:'none'},2:{t:'none',pk:4,ea:4,ar:24000},3:{t:'red',c:'c1',pk:4,ea:4,ar:24000,res:-1.0},4:{t:'red',c:'c2',pk:2,ea:4,ar:24000,res:-1.0},5:{t:'green',c:'c3',pk:2,ea:6,ar:34200,res:1.3},6:{t:'green',c:'c3',pk:2,ea:6,ar:34200,res:1.3}};
let cur=0,shown=null,raf=0;const lg=()=>X[H.lang]?H.lang:'en',loc=()=>lg()==='en'?'en-US':lg();
const nf=(v,d=0)=>new Intl.NumberFormat(loc(),{minimumFractionDigits:d,maximumFractionDigits:d}).format(v);
const money=(m,sg)=>{const s=sg?(m<0?'−':m>0?'+':''):'',v=nf(Math.abs(m),1);return lg()==='en'?s+'$'+v+' '+X.en.mio:s+v+' '+X[lg()].mio+' $'};
const at=a=>X[lg()].at.replace('{a}',nf(a)).replace('{v}',lg()==='en'?'$400':'400 $');
function texts(){q('.rgA1').textContent=at(24000);q('.rgV1').textContent=money(9.6);q('.rgC1').textContent=money(10.6);q('.rgR1').textContent=money(-1,true);
 q('.rgA2').textContent=at(34200);q('.rgV2').textContent=money(13.7);q('.rgC2').textContent=money(10.6);q('.rgF2').textContent=money(1.8);q('.rgR2').textContent=money(1.3,true);
 q('.rgb1').textContent=money(-2,true);q('.rgb2').textContent=money(2,true);paint(true)}
function paint(inst){const s=ST[cur],m=q('.rg-meter'),big=q('.rg-big'),bar=q('.rg-bar i');m.dataset.tone=s.t;q('.rg-chip').textContent=X[lg()][s.c||'c0'];
 q('.rgPk').textContent=s.pk?(cur>=4?'4 → 2':nf(s.pk)):'—';q('.rgPk').classList.toggle('up',cur>=4);
 q('.rgEa').textContent=s.ea?(s.ea===6?'4 → 6':nf(s.ea)+' / 8'):'—';q('.rgEa').classList.toggle('up',s.ea===6);
 q('.rgAr').textContent=s.ar?nf(s.ar)+' sq ft':'—';q('.rgAr').classList.toggle('up',s.ar>24000);
 if(s.res==null){big.textContent='—';bar.style.width='0';bar.style.left='50%%';shown=null;return}
 const T=s.res,p=Math.min(1,Math.abs(T)/2)*50;bar.style.background=T<0?'var(--rg-red)':'var(--rg-green)';bar.style.width=p+'%%';bar.style.left=T<0?(50-p)+'%%':'50%%';
 const from=shown==null?T:shown;cancelAnimationFrame(raf);
 if(inst||from===T||matchMedia('(prefers-reduced-motion: reduce)').matches){shown=T;big.textContent=money(T,true);return}
 const t0=performance.now();const st=t=>{const k=Math.min(1,(t-t0)/1200),v=from+(T-from)*(1-Math.pow(1-k,3));shown=v;big.textContent=money(Math.round(v*10)/10,true);if(k<1)raf=requestAnimationFrame(st)};raf=requestAnimationFrame(st)}
const chs=[...R.querySelectorAll('.rg-ch')];
function onScroll(){const r=R.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;const line=innerHeight*.45;let n=0;chs.forEach(c=>{if(c.getClientRects().length&&c.getBoundingClientRect().top<line)n=+c.dataset.st});if(n!==cur){cur=n;paint(false)}}
addEventListener('scroll',()=>requestAnimationFrame(onScroll),{passive:true});addEventListener('resize',onScroll);
const tb=document.querySelector('.hr-tab'),setTop=()=>R.style.setProperty('--rg-top',(tb&&tb.offsetHeight&&getComputedStyle(tb).display!=='none'?tb.offsetHeight:0)+'px');setTop();addEventListener('resize',setTop);new MutationObserver(texts).observe(H,{attributes:true,attributeFilter:['lang']});texts();onScroll();
R.querySelectorAll('.rgv').forEach(v=>{v.closest('figure').querySelector('.rg-replay').addEventListener('click',()=>{try{v.currentTime=0}catch(e){}v.play().catch(()=>{})});
 if('IntersectionObserver'in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){const io=new IntersectionObserver(e=>{if(e[0].isIntersecting){v.preload='auto';v.play().catch(()=>{});io.disconnect()}},{threshold:.6});io.observe(v)}})})()</script>''' % json.dumps(X, ensure_ascii=False)
rep('</body>', JS + '</body>') if s.count('</body>') == 1 else None
if 'id="rg-js"' not in s: s += JS
CSS = '''<style id="rg-css">
.rg{--rg-bg:#06120c;--rg-panel:#0c1d15;--rg-panel2:#11281d;--rg-ink:#eef5f0;--rg-muted:#9db4a6;--rg-line:#ffffff1c;--rg-green:#b8f03c;--rg-gink:#07150f;--rg-red:#ff6b5b;
 background:var(--rg-bg);color:var(--rg-ink);padding-block:clamp(56px,8vw,110px)}
.rg-wrap{max-width:var(--wrap-max,1280px);margin:0 auto;padding:0 var(--gutter,24px)}
.rg-eye,.rg-k,.rg-mk,.rg-hint{font:500 .76rem "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase}
.rg-eye{color:var(--rg-green);margin:0 0 1rem}.rg-hint{color:var(--rg-muted);margin:1.2rem 0 0}
.rg-h1{font:700 clamp(2rem,4.6vw,3.6rem)/1.04 "Outfit","Inter",sans-serif;letter-spacing:-.02em;margin:0 0 1.1rem;max-width:18ch;color:var(--rg-ink);text-wrap:balance}
.rg-h1 em{font-style:normal;color:var(--rg-green)}
.rg-lead{font-size:clamp(1.02rem,1.5vw,1.2rem);color:#cfe0d6;max-width:60ch;margin:0}
.rg-grid{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:clamp(24px,4vw,52px);align-items:start;margin-top:clamp(28px,5vw,56px)}
.rg-story{display:grid;gap:clamp(48px,8vw,104px);min-width:0}
.rg-ch{min-width:0}.rg-k{color:var(--rg-muted);margin:0 0 .5rem}.rg-ch.red .rg-k{color:var(--rg-red)}.rg-ch.grn .rg-k{color:var(--rg-green)}
.rg-ch h3{font:700 clamp(1.5rem,3vw,2.3rem)/1.1 "Outfit","Inter",sans-serif;letter-spacing:-.015em;margin:0 0 .8rem;color:var(--rg-ink);max-width:24ch;text-wrap:balance}
.rg-ch p{margin:0 0 1rem;max-width:62ch;color:#d6e4db}
.rg figure{margin:1.1rem 0 0;border-radius:10px;overflow:hidden;background:var(--rg-panel);border:1px solid var(--rg-line);position:relative}
.rg figure img,.rg figure video{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;max-width:100%}
.rg figcaption{font-size:.82rem;color:var(--rg-muted);padding:.55rem .85rem}
.rg-replay{all:unset;cursor:pointer;position:absolute;right:10px;top:10px;font:600 .75rem "Inter",sans-serif;padding:.3rem .65rem;border-radius:999px;background:#040d09cc;color:#fff}
.rg-replay:focus-visible{outline:2px solid var(--rg-green);outline-offset:2px}
.rg-ledger{margin:1.1rem 0 0;border:1px solid var(--rg-line);border-radius:10px;overflow:hidden;font-variant-numeric:tabular-nums}
.rg-ledger>div{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1rem;padding:.65rem .95rem;border-top:1px solid var(--rg-line);align-items:baseline;color:#d6e4db}
.rg-ledger>div:first-child{border-top:0}.rg-ledger small{display:block;color:var(--rg-muted);font-size:.8rem}
.rg-ledger b{font:600 1.05rem "Outfit","Inter",sans-serif;white-space:nowrap;color:var(--rg-ink)}.rg-ledger .res{background:var(--rg-panel2)}.rg-ledger .res b{font-size:1.25rem}
.rg .neg{color:var(--rg-red)}.rg .pos{color:var(--rg-green)}
.rg-wh{margin-top:1.3rem!important}
.rg-ways,.rg-ticks{list-style:none;margin:.6rem 0 0;padding:0;display:grid;gap:.55rem}
.rg-ways li,.rg-ticks li{padding-left:1.5rem;position:relative;color:#d6e4db;max-width:62ch}
.rg-ways li:before{content:"×";position:absolute;left:0;color:var(--rg-red);font-weight:700}
.rg-ticks li:before{content:"✓";position:absolute;left:0;color:var(--rg-green);font-weight:700}
.rg-note{font-size:.92rem;color:var(--rg-muted)!important;border-left:2px solid var(--rg-green);padding-left:.8rem}
.rg-meter{position:sticky;top:20px;background:var(--rg-panel);border:1px solid var(--rg-line);border-radius:14px;padding:18px;display:grid;gap:14px}
.rg-mh{display:flex;justify-content:space-between;align-items:center;gap:.6rem}.rg-mk{color:var(--rg-muted)}
.rg-chip{font:600 .72rem "Inter",sans-serif;padding:.25rem .6rem;border-radius:999px;background:#ffffff14;color:var(--rg-muted);white-space:nowrap}
.rg-meter[data-tone=red] .rg-chip{background:#ff6b5b26;color:var(--rg-red)}.rg-meter[data-tone=green] .rg-chip{background:#b8f03c26;color:var(--rg-green)}
.rg-big{font:700 clamp(1.9rem,3vw,2.5rem)/1 "Outfit","Inter",sans-serif;letter-spacing:-.02em;font-variant-numeric:tabular-nums;color:var(--rg-muted)}
.rg-meter[data-tone=red] .rg-big{color:var(--rg-red)}.rg-meter[data-tone=green] .rg-big{color:var(--rg-green)}
.rg-bar{position:relative;height:10px;border-radius:999px;background:#ffffff12;overflow:hidden}
.rg-bar i{position:absolute;top:0;bottom:0;left:50%;width:0;background:var(--rg-red);transition:left .9s cubic-bezier(.4,0,.2,1),width .9s cubic-bezier(.4,0,.2,1)}
.rg-bar:after{content:"";position:absolute;left:50%;top:-2px;bottom:-2px;width:2px;background:var(--rg-ink);opacity:.6}
.rg-barl{display:flex;justify-content:space-between;font:500 .68rem "IBM Plex Mono",monospace;color:var(--rg-muted);margin-top:-8px}
.rg-rows{display:grid;border-top:1px solid var(--rg-line)}.rg-rows>div{display:flex;justify-content:space-between;gap:.8rem;padding:.5rem 0;border-bottom:1px solid var(--rg-line);font-size:.9rem}
.rg-rows span{color:var(--rg-muted)}.rg-rows b{font-weight:600;font-variant-numeric:tabular-nums;color:var(--rg-ink)}.rg-rows b.up{color:var(--rg-green)}
.rg-mf{font-size:.74rem;color:var(--rg-muted);margin:0}
.rg-cta{margin-top:clamp(40px,6vw,72px);background:var(--rg-green);color:var(--rg-gink);border-radius:16px;padding:clamp(22px,4vw,40px);display:grid;gap:.7rem;justify-items:start}
.rg-cta h3{font:700 clamp(1.6rem,3.2vw,2.5rem)/1.05 "Outfit","Inter",sans-serif;margin:0;color:var(--rg-gink)}.rg-cta p{margin:0;max-width:58ch;color:#173018}
.rg-btn{display:inline-flex;padding:.8rem 1.25rem;border-radius:999px;background:var(--rg-gink)!important;color:#fff!important;text-decoration:none;font-weight:600;border:0}
.rg-foot{font-size:.8rem;color:var(--rg-muted);max-width:80ch;margin:1.6rem 0 0}
@media (width<=900px){.rg-grid{grid-template-columns:minmax(0,1fr)}
 .rg-meter{order:-1;top:var(--rg-top,0px);z-index:5;border-radius:0 0 12px 12px;border-top:0;margin-inline:calc(-1*var(--gutter,24px));padding:10px var(--gutter,24px);grid-template-columns:auto 1fr;gap:4px 12px}
 .rg-mh{grid-column:1/-1}.rg-big{font-size:1.5rem}.rg-bar{align-self:center}.rg-barl,.rg-rows,.rg-mf{display:none}}
@media (prefers-reduced-motion:reduce){.rg-bar i{transition:none}}
</style>'''
rep('</head>', CSS + '</head>')
rep('var D={', 'var D=' + json.dumps(D, ensure_ascii=False)[:-1] + ', ')
open(out, 'w').write(s); print('ok', len(s)//1024, 'KB', len(D), 'strings')
