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
NEW_STRINGS = {'7 · Your project': ['7 · Ihr Projekt', '7 · Votre projet', '7 · Su proyecto'], 'Now try it with your numbers.': ['Jetzt mit Ihren Zahlen.', 'Essayez avec vos chiffres.', 'Pruebe con sus cifras.'], 'Enter the figures of your project. The result updates as you type. The example values are filled in to start.': ['Geben Sie die Zahlen Ihres Projekts ein. Das Ergebnis rechnet sich sofort neu. Zum Start sind die Beispielwerte eingetragen.', 'Saisissez les chiffres de votre projet. Le résultat se met à jour pendant la saisie. Les valeurs de l’exemple sont préremplies.', 'Introduzca las cifras de su proyecto. El resultado se actualiza al escribir. Para empezar, están los valores del ejemplo.'], 'Parking spaces required': ['Erforderliche Stellplätze', 'Places de stationnement exigées', 'Plazas de aparcamiento exigidas'], 'Sellable area with a conventional garage': ['Verkaufbare Fläche mit konventioneller Garage', 'Surface vendable avec un parking classique', 'Superficie vendible con aparcamiento convencional'], 'Value of sellable area per': ['Wert der verkaufbaren Fläche pro', 'Valeur de la surface vendable par', 'Valor de la superficie vendible por'], 'Land, building and garage, in millions': ['Grundstück, Gebäude und Garage, in Millionen', 'Terrain, bâtiment et parking, en millions', 'Solar, edificio y aparcamiento, en millones'], 'Fit-out cost of the new area per': ['Ausbaukosten der neuen Fläche pro', 'Coût d’aménagement de la nouvelle surface par', 'Coste de acondicionamiento de la nueva superficie por'], 'Area recovered per space': ['Gewonnene Fläche pro Stellplatz', 'Surface gagnée par place', 'Superficie recuperada por plaza'], 'as in the gain calculator': ['wie im Rechner oben', 'comme dans le calculateur', 'como en la calculadora'], 'Reset to the example': ['Auf das Beispiel zurücksetzen', 'Revenir à l’exemple', 'Volver al ejemplo'], 'With a conventional garage': ['Mit konventioneller Garage', 'Avec un parking classique', 'Con aparcamiento convencional'], 'With TilePark': ['Mit TilePark', 'Avec TilePark', 'Con TilePark'], 'New sellable area': ['Neue verkaufbare Fläche', 'Nouvelle surface vendable', 'Nueva superficie vendible'], 'Fit-out of the new area': ['Ausbau der neuen Fläche', 'Aménagement de la nouvelle surface', 'Acondicionamiento de la nueva superficie'], 'Difference made by TilePark': ['Unterschied durch TilePark', 'Différence grâce à TilePark', 'Diferencia gracias a TilePark'], 'The parking itself is assumed to cost about the same: most TilePark systems from 25 spaces cost around $30,000 per space. This is a first estimate; the free feasibility study shows the real numbers for your site.': ['Für das Parken selbst sind etwa gleiche Kosten angesetzt: Die meisten TilePark-Anlagen ab 25 Stellplätzen kosten rund 30.000 $ pro Stellplatz. Das ist eine erste Schätzung – die kostenlose Machbarkeitsstudie zeigt die tatsächlichen Zahlen für Ihr Grundstück.', 'Le stationnement lui-même est supposé coûter à peu près autant : la plupart des systèmes TilePark à partir de 25 places coûtent environ 30 000 $ par place. C’est une première estimation ; l’étude de faisabilité gratuite indique les chiffres réels pour votre site.', 'Se supone que el aparcamiento en sí cuesta más o menos lo mismo: la mayoría de los sistemas TilePark a partir de 25 plazas cuestan unos 30.000 $ por plaza. Es una primera estimación; el estudio de viabilidad gratuito muestra las cifras reales para su solar.'], 'Send these numbers with your request →': ['Diese Zahlen mit der Anfrage senden →', 'Envoyer ces chiffres avec votre demande →', 'Enviar estas cifras con su solicitud →']}
# English text of the section; the site's translator handles DE/FR/ES through D
EXTRA = {'eye2': ('Case study · fictional example','Fallstudie · fiktives Beispiel','Étude de cas · exemple fictif','Caso práctico · ejemplo ficticio'),
         'menu': ('Case study: from red to green','Fallstudie: von Rot zu Grün','Étude de cas : du rouge au vert','Caso práctico: de rojo a verde')}
D = {}
for k, en in E.items():
    if k in ('at','mio','c0','c1','c2','c3','eye','cb','rp'): continue
    D[en] = [L['de'][k], L['fr'][k], L['es'][k]]
for k,(en,de,fr,es) in EXTRA.items(): D[en] = [de,fr,es]
D.update(NEW_STRINGS)
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
<article class="rg-ch rg-you" data-st="7"><p class="rg-k">7 · Your project</p><h3>Now try it with your numbers.</h3><p>Enter the figures of your project. The result updates as you type. The example values are filled in to start.</p>
<form class="rg-form" id="rgForm" novalidate>
<label for="rgN"><span>Parking spaces required</span><input id="rgN" type="number" min="1" step="1" inputmode="numeric"></label>
<label for="rgA"><span>Sellable area with a conventional garage</span><span class="rg-in" data-noi18n><input id="rgA" type="number" min="0" step="10" inputmode="numeric"><i class="rgUa"></i></span></label>
<label for="rgV"><span><span>Value of sellable area per</span> <span class="rgUa2" data-noi18n></span></span><span class="rg-in" data-noi18n><i class="rgCur"></i><input id="rgV" type="number" min="0" step="10" inputmode="numeric"></span></label>
<label for="rgC"><span>Land, building and garage, in millions</span><span class="rg-in" data-noi18n><i class="rgCur"></i><input id="rgC" type="number" min="0" step="0.1" inputmode="decimal"></span></label>
<label for="rgF"><span><span>Fit-out cost of the new area per</span> <span class="rgUa2" data-noi18n></span></span><span class="rg-in" data-noi18n><i class="rgCur"></i><input id="rgF" type="number" min="0" step="5" inputmode="numeric"></span></label>
<div class="rg-fix"><span>Area recovered per space</span><b data-noi18n class="rgPer"></b><small>as in the gain calculator</small></div>
<button type="button" class="rg-reset">Reset to the example</button>
</form>
<div class="rg-cmp">
<div class="rg-col"><h4>With a conventional garage</h4><div class="rg-ledger"><div><span>Value of the sellable area</span><b data-noi18n class="yV1"></b></div><div><span>Land, building and garage</span><b data-noi18n class="yC1"></b></div><div class="res"><span>Result</span><b data-noi18n class="yR1"></b></div></div></div>
<div class="rg-col"><h4>With TilePark</h4><div class="rg-ledger"><div><span><span>New sellable area</span></span><b data-noi18n class="yA2"></b></div><div><span>Value of the sellable area</span><b data-noi18n class="yV2"></b></div><div><span>Land, building and parking</span><b data-noi18n class="yC2"></b></div><div><span>Fit-out of the new area</span><b data-noi18n class="yF2"></b></div><div class="res"><span>Result</span><b data-noi18n class="yR2"></b></div></div></div>
</div>
<div class="rg-diff"><span>Difference made by TilePark</span><b data-noi18n class="yD"></b></div>
<p class="rg-note">The parking itself is assumed to cost about the same: most TilePark systems from 25 spaces cost around $30,000 per space. This is a first estimate; the free feasibility study shows the real numbers for your site.</p>
<a class="btn rg-send" href="#request">Send these numbers with your request →</a>
</article>
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
const ST={0:{t:'none'},1:{t:'none'},2:{t:'none',pk:4,ea:4,ar:24000},3:{t:'red',c:'c1',pk:4,ea:4,ar:24000,res:-1.0},4:{t:'red',c:'c2',pk:2,ea:4,ar:24000,res:-1.0},5:{t:'green',c:'c3',pk:2,ea:6,ar:34200,res:1.3},6:{t:'green',c:'c3',pk:2,ea:6,ar:34200,res:1.3},7:{t:'none',you:1}};
let cur=0,shown=null,raf=0;const lg=()=>X[H.lang]?H.lang:'en',loc=()=>lg()==='en'?'en-US':lg();
const nf=(v,d=0)=>new Intl.NumberFormat(loc(),{minimumFractionDigits:d,maximumFractionDigits:d}).format(v);
const money=(m,sg)=>{const s=sg?(m<0?'−':m>0?'+':''):'',v=nf(Math.abs(m),1);return lg()==='en'?s+'$'+v+' '+X.en.mio:s+v+' '+X[lg()].mio+' $'};
const at=a=>X[lg()].at.replace('{a}',nf(a)).replace('{v}',lg()==='en'?'$400':'400 $');
function texts(){q('.rgA1').textContent=at(24000);q('.rgV1').textContent=money(9.6);q('.rgC1').textContent=money(10.6);q('.rgR1').textContent=money(-1,true);
 q('.rgA2').textContent=at(34200);q('.rgV2').textContent=money(13.7);q('.rgC2').textContent=money(10.6);q('.rgF2').textContent=money(1.8);q('.rgR2').textContent=money(1.3,true);
 calc();paint(true)}
function paint(inst){const s=cur===7?you():ST[cur],m=q('.rg-meter'),big=q('.rg-big'),bar=q('.rg-bar i');m.dataset.tone=s.t;q('.rg-chip').textContent=X[lg()][s.c||'c0'];
 q('.rgPk').textContent=s.pk?(cur>=4?'4 → 2':nf(s.pk)):'—';q('.rgPk').classList.toggle('up',cur>=4);
 q('.rgEa').textContent=s.ea?(s.ea===6?'4 → 6':nf(s.ea)+' / 8'):'—';q('.rgEa').classList.toggle('up',s.ea===6);
 q('.rgAr').textContent=s.ar?nf(s.ar)+' '+(s.au||'sq ft'):'—';q('.rgAr').classList.toggle('up',s.ar>24000);
 if(s.res==null){big.textContent='—';bar.style.width='0';bar.style.left='50%%';shown=null;return}
 const sc=s.scale||2,mf=cur===7?cm:money;q('.rgb1').textContent=mf(-sc,true);q('.rgb2').textContent=mf(sc,true);const T=s.res,p=Math.min(1,Math.abs(T)/sc)*50;bar.style.background=T<0?'var(--rg-red)':'var(--rg-green)';bar.style.width=p+'%%';bar.style.left=T<0?(50-p)+'%%':'50%%';
 const from=shown==null?T:shown;cancelAnimationFrame(raf);
 const mf2=cur===7?cm:money;if(inst||from===T||matchMedia('(prefers-reduced-motion: reduce)').matches){shown=T;big.textContent=mf2(T,true);return}
 const t0=performance.now();const st=t=>{const k=Math.min(1,(t-t0)/1200),v=from+(T-from)*(1-Math.pow(1-k,3));shown=v;big.textContent=mf2(Math.round(v*100)/100,true);if(k<1)raf=requestAnimationFrame(st)};raf=requestAnimationFrame(st)}

const met=()=>H.dataset.units==='m',DEF={i:{n:68,a:24000,v:400,c:10.6,f:175,per:150,au:'sq ft',cur:'$'},m:{n:68,a:2230,v:4300,c:10.6,f:1890,per:14,au:'m²',cur:'€'}};
const F=R.querySelector('#rgForm'),inp=k=>R.querySelector('#rg'+k);let sys=null,Y={};
const cm=(m,sg)=>{const c=DEF[sys].cur,s=sg?(m<0?'−':m>0?'+':''):'',v=nf(Math.abs(m),Math.abs(m)<1&&m!==0?2:1);return lg()==='en'?s+c+v+' '+X.en.mio:s+v+' '+X[lg()].mio+' '+c};
function fill(){const d=DEF[sys];inp('N').value=d.n;inp('A').value=d.a;inp('V').value=d.v;inp('C').value=d.c;inp('F').value=d.f}
function calc(){const ns=met()?'m':'i';if(ns!==sys){sys=ns;fill()}const d=DEF[sys],g=k=>Math.max(0,+inp(k).value||0);
 const n=g('N'),a=g('A'),v=g('V'),c=g('C'),f=g('F'),add=n*d.per,v1=a*v/1e6,r1=v1-c,v2=(a+add)*v/1e6,f2=add*f/1e6,r2=v2-c-f2;Y={n,a,add,au:d.au,r1,r2,v1,v2,c,f2};
 R.querySelectorAll('.rgUa').forEach(e=>e.textContent=d.au);R.querySelectorAll('.rgUa2').forEach(e=>e.textContent=d.au);R.querySelectorAll('.rgCur').forEach(e=>e.textContent=d.cur);
 q('.rgPer').textContent=nf(d.per)+' '+d.au;
 q('.yV1').textContent=cm(v1);q('.yC1').textContent=cm(c);q('.yR1').textContent=cm(r1,true);q('.yR1').className='yR1 '+(r1<0?'neg':'pos');
 q('.yA2').textContent='+ '+nf(add)+' '+d.au;q('.yV2').textContent=cm(v2);q('.yC2').textContent=cm(c);q('.yF2').textContent=cm(f2);q('.yR2').textContent=cm(r2,true);q('.yR2').className='yR2 '+(r2<0?'neg':'pos');
 q('.yD').textContent=cm(r2-r1,true);q('.yD').className='yD '+(r2-r1<0?'neg':'pos');
 if(cur===7)paint(true)}
function you(){const t=Y.r2<0?'red':'green',sc=Math.max(0.5,Math.abs(Y.r1),Math.abs(Y.r2))*1.25;return {t,c:Y.r2<0?'c1':'c3',res:Y.r2,scale:sc,pk:null,ea:null,ar:Y.a+Y.add,au:Y.au}}
F.addEventListener('input',()=>calc());F.addEventListener('submit',e=>e.preventDefault());
R.querySelector('.rg-reset').addEventListener('click',()=>{fill();calc()});
R.querySelector('.rg-send').addEventListener('click',()=>{const f=document.querySelector('#request form')||document.querySelector('form [name=spaces]')?.form;if(!f)return;
 const sp=f.querySelector('[name=spaces]');if(sp)sp.value=Y.n;const m=f.querySelector('[name=message]');
 if(m){const line='TilePark case study: '+nf(Y.n)+' spaces, '+nf(Y.a)+' '+Y.au+' sellable, result '+cm(Y.r1,true)+' → '+cm(Y.r2,true)+' with TilePark.';if(!m.value.includes('TilePark case study'))m.value=(m.value?m.value+'\\n':'')+line}});
const chs=[...R.querySelectorAll('.rg-ch')];
function onScroll(){const r=R.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;const line=innerHeight*.45;let n=0;chs.forEach(c=>{if(c.getClientRects().length&&c.getBoundingClientRect().top<line)n=+c.dataset.st});if(n!==cur){cur=n;paint(false)}}
addEventListener('scroll',()=>requestAnimationFrame(onScroll),{passive:true});addEventListener('resize',onScroll);
const tb=document.querySelector('.hr-tab'),setTop=()=>R.style.setProperty('--rg-top',(tb&&tb.offsetHeight&&getComputedStyle(tb).display!=='none'?tb.offsetHeight:0)+'px');setTop();addEventListener('resize',setTop);new MutationObserver(texts).observe(H,{attributes:true,attributeFilter:['lang','data-units']});texts();onScroll();
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

.rg-you{border-top:1px solid var(--rg-line);padding-top:clamp(28px,4vw,44px)}
.rg-form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 18px;margin:1.2rem 0 0;padding:clamp(14px,2vw,20px);background:var(--rg-panel);border:1px solid var(--rg-line);border-radius:12px}
.rg-form label{display:flex;flex-direction:column;gap:.35rem;font-size:.86rem;color:var(--rg-muted);min-width:0}
.rg-form input{font:600 1.05rem "Inter",sans-serif;color:var(--rg-ink);background:var(--rg-bg);border:1px solid #ffffff2e;border-radius:8px;padding:.55rem .7rem;width:100%;min-width:0;font-variant-numeric:tabular-nums}
.rg-form input:focus{outline:2px solid var(--rg-green);outline-offset:1px;border-color:transparent}
.rg-in{display:flex;align-items:center;gap:.4rem}.rg-in i{font-style:normal;color:var(--rg-muted);font-weight:600;white-space:nowrap}
.rg-fix{display:flex;flex-direction:column;gap:.2rem;font-size:.86rem;color:var(--rg-muted)}.rg-fix b{font:600 1.05rem "Inter",sans-serif;color:var(--rg-ink)}.rg-fix small{font-size:.75rem}
.rg-reset{grid-column:1/-1;justify-self:start;all:unset;cursor:pointer;font:600 .82rem "Inter",sans-serif;color:var(--rg-green);padding:.3rem 0}
.rg-reset:focus-visible{outline:2px solid var(--rg-green);outline-offset:2px}
.rg-cmp{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:1.1rem}
.rg-col h4{margin:0 0 .4rem;font:600 .95rem "Outfit","Inter",sans-serif;color:var(--rg-ink)}.rg-col .rg-ledger{margin-top:0}
.rg-diff{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;margin-top:14px;padding:.9rem 1.1rem;border-radius:12px;background:var(--rg-panel2);border:1px solid var(--rg-line)}
.rg-diff span{color:#d6e4db}.rg-diff b{font:700 clamp(1.3rem,2.4vw,1.8rem) "Outfit","Inter",sans-serif;white-space:nowrap}
.rg-you .rg-note{margin-top:1rem}
.rg-send{display:inline-flex;margin-top:.4rem;padding:.75rem 1.2rem;border-radius:999px;background:var(--rg-green)!important;color:var(--rg-gink)!important;text-decoration:none;font-weight:700;border:0}
@media (width<=700px){.rg-form,.rg-cmp{grid-template-columns:minmax(0,1fr)}}
@media (width<=900px){.rg-grid{grid-template-columns:minmax(0,1fr)}
 .rg-meter{order:-1;top:var(--rg-top,0px);z-index:5;border-radius:0 0 12px 12px;border-top:0;margin-inline:calc(-1*var(--gutter,24px));padding:10px var(--gutter,24px);grid-template-columns:auto 1fr;gap:4px 12px}
 .rg-mh{grid-column:1/-1}.rg-big{font-size:1.5rem}.rg-bar{align-self:center}.rg-barl,.rg-rows,.rg-mf{display:none}}
@media (prefers-reduced-motion:reduce){.rg-bar i{transition:none}}
</style>'''
rep('</head>', CSS + '</head>')
rep('var D={', 'var D=' + json.dumps(D, ensure_ascii=False)[:-1] + ', ')
open(out, 'w').write(s); print('ok', len(s)//1024, 'KB', len(D), 'strings')
