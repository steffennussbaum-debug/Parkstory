# Replaces the long case study with a compact animated one: film + live result badge + inputs.
# python case_compact.py in.html out.html
import sys, re, json
src, out = sys.argv[1:3]; s = open(src).read(); T = {}
def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:90], s.count(a)); s = s.replace(a, b)
i = s.find('<section class="rg" id="red-to-green">'); assert i > 0; d = 0
for m in re.compile(r'<section[\s>]|</section>').finditer(s, i):
    d += -1 if m.group(0).startswith('</') else 1
    if d == 0: j = m.end(); break
old = s[i:j]
vids = re.findall(r'<video class="rgv"[^>]*>(.*?)</video>', old, re.S); assert len(vids) == 2
poster1 = re.search(r'<article class="rg-ch" data-st="1">.*?<img src="([^"]+)"', old, re.S).group(1)
poster2 = re.search(r'<video class="rgv"[^>]*poster="([^"]+)"', old).group(1)
form = re.search(r'(<form class="rg-form" id="rgForm" novalidate>.*?</form>)', old, re.S).group(1)
def bal(txt, marker):
    k = txt.find(marker); assert k >= 0, marker; dd = 0
    for mm in re.compile(r'<div[\s>]|</div>').finditer(txt, k):
        dd += -1 if mm.group(0).startswith('</') else 1
        if dd == 0: return txt[k:mm.end()]
cmp_ = bal(old, '<div class="rg-cmp">')
diff = bal(old, '<div class="rg-diff">')
NEW = f'''<section class="rg rgc" id="red-to-green"><div class="rg-wrap">
<p class="rg-eye">Case study · fictional example</p><h2 class="rg-h1"><span>The project that didn’t add up.</span> <em>Until parking changed.</em></h2>
<p class="rg-lead">Enter your figures, press play and watch what TilePark changes.</p>
<div class="rgc-grid rg-you" data-mode="sell">
 <div class="rgc-stage">
  <img class="rgc-p" src="{poster1}" alt="Example building with a conventional garage" width="960" height="540">
  <video class="rgc-a" muted playsinline preload="metadata" poster="{poster1}" aria-hidden="true">{vids[0]}</video>
  <video class="rgc-v" muted playsinline preload="metadata" poster="{poster2}" aria-hidden="true">{vids[1]}</video>
  <div class="rgc-step"><span class="on" data-s="1">A conventional garage</span><span data-s="2">Remove the ramps and aisles</span><span data-s="3">TilePark takes over</span><span data-s="4">Build what you want</span></div>
  <div class="rgc-badge" data-tone="red"><span class="k">Project result</span><b data-noi18n>—</b></div>
  <button type="button" class="rgc-play"><span aria-hidden="true">▶</span> <span>Play the case</span></button>
 </div>
 <div class="rgc-in">{form}</div>
</div>
<div class="rg-you rgc-out" data-mode="sell">{cmp_}{diff}
<div class="rgc-act"><a class="btn rg-send" href="#request">Send these numbers with your request →</a></div></div>
<p class="rg-foot">Fictional example. The animation shows an example building with 68 spaces; the recovered area (150 sq ft per space) follows the gain calculator, and the parking itself is assumed to cost about as much as a conventional garage. Your free feasibility study shows the real numbers for your site.</p>
</div></section>'''
s = s[:i] + NEW + s[j:]
T.update({"Enter your figures, press play and watch what TilePark changes.":["Geben Sie Ihre Zahlen ein, starten Sie die Animation und sehen Sie, was TilePark verändert.","Saisissez vos chiffres, lancez l’animation et voyez ce que TilePark change.","Introduzca sus cifras, inicie la animación y vea lo que cambia TilePark."],
 "Play the case":["Fallstudie abspielen","Lancer l’étude de cas","Reproducir el caso"],
 "Example building with a conventional garage":["Beispielgebäude mit konventioneller Garage","Bâtiment exemple avec un parking classique","Edificio de ejemplo con aparcamiento convencional"],
 "Fictional example. The animation shows an example building with 68 spaces; the recovered area (150 sq ft per space) follows the gain calculator, and the parking itself is assumed to cost about as much as a conventional garage. Your free feasibility study shows the real numbers for your site.":
 ["Fiktives Beispiel. Die Animation zeigt ein Beispielgebäude mit 68 Stellplätzen; die gewonnene Fläche (150 sq ft pro Stellplatz) folgt dem Rechner, und für das Parken selbst sind etwa die Kosten einer konventionellen Garage angesetzt. Ihre kostenlose Machbarkeitsstudie zeigt die tatsächlichen Zahlen für Ihr Grundstück.",
  "Exemple fictif. L’animation montre un bâtiment exemple de 68 places ; la surface gagnée (150 sq ft par place) suit le calculateur, et le stationnement lui-même est supposé coûter à peu près autant qu’un parking classique. Votre étude de faisabilité gratuite indique les chiffres réels pour votre site.",
  "Ejemplo ficticio. La animación muestra un edificio de ejemplo con 68 plazas; la superficie recuperada (150 sq ft por plaza) sigue la calculadora y se supone que el aparcamiento en sí cuesta más o menos lo mismo que uno convencional. Su estudio de viabilidad gratuito muestra las cifras reales para su solar."]})
# old script out, new script in
a = s.find('<script id="rg-js">'); b = s.find('</script>', a) + 9; assert a > 0
X = {'en':('million','per year'),'de':('Mio.','pro Jahr'),'fr':('millions','par an'),'es':('millones','al año')}
JS = '''<script id="rgc-js">(()=>{const R=document.getElementById('red-to-green');if(!R)return;const H=document.documentElement,q=c=>R.querySelector(c),qa=c=>[...R.querySelectorAll(c)],X=%s;
const DEF={i:{n:68,a:24000,v:400,r:24,y:6,c:10.6,f:175,per:150,au:'sq ft',cur:'$'},m:{n:68,a:2230,v:4300,r:258,y:6,c:10.6,f:1890,per:14,au:'m²',cur:'€'}};
let sys=null,mode='sell',Y={},stage=0,shown=null,raf=0,run=0;const inp=k=>R.querySelector('#rg'+k),lg=()=>X[H.lang]?H.lang:'en',loc=()=>lg()==='en'?'en-US':lg();
const nf=(v,d=0)=>new Intl.NumberFormat(loc(),{minimumFractionDigits:d,maximumFractionDigits:d}).format(v);
const cm=(m,sg)=>{const c=DEF[sys].cur,s=sg?(m<0?'−':m>0?'+':''):'',v=nf(Math.abs(m),Math.abs(m)<1&&m!==0?2:1);return lg()==='en'?s+c+v+' '+X.en[0]:s+v+' '+X[lg()][0]+' '+c};
function fill(){const d=DEF[sys];inp('N').value=d.n;inp('A').value=d.a;inp('V').value=d.v;inp('Rent').value=d.r;inp('Y').value=d.y;inp('C').value=d.c;inp('F').value=d.f;inp('S').value=100}
function calc(){const ns=H.dataset.units==='m'?'m':'i';if(ns!==sys){sys=ns;fill()}const d=DEF[sys],g=k=>Math.max(0,+inp(k).value||0);
 const n=g('N'),a=g('A'),rent=g('Rent'),yy=Math.max(0.1,g('Y')),v=mode==='rent'?rent/(yy/100):g('V'),c=g('C'),f=g('F'),add=n*d.per*Math.min(100,g('S'))/100,v1=a*v/1e6,r1=v1-c,v2=(a+add)*v/1e6,f2=add*f/1e6,r2=v2-c-f2;Y={n,a,add,au:d.au,r1,r2,mode};
 qa('.rgUa,.rgUa2').forEach(e=>e.textContent=d.au);qa('.rgCur').forEach(e=>e.textContent=d.cur);q('.rgPer').textContent=nf(d.per)+' '+d.au;
 q('.yV1').textContent=cm(v1);q('.yC1').textContent=cm(c);q('.yR1').textContent=cm(r1,true);q('.yR1').className='yR1 '+(r1<0?'neg':'pos');
 q('.yA2').textContent='+ '+nf(add)+' '+d.au;q('.yRent').textContent=(lg()==='en'?d.cur+nf(add*rent):nf(add*rent)+' '+d.cur)+' '+X[lg()][1];
 q('.yV2').textContent=cm(v2);q('.yC2').textContent=cm(c);q('.yF2').textContent=cm(f2);q('.yR2').textContent=cm(r2,true);q('.yR2').className='yR2 '+(r2<0?'neg':'pos');
 q('.yD').textContent=cm(r2-r1,true);q('.yD').className='yD '+(r2-r1<0?'neg':'pos');badge(stage>=4?r2:r1,true)}
function badge(v,inst){const b=q('.rgc-badge'),el=b.querySelector('b');cancelAnimationFrame(raf);const set=x=>{el.textContent=cm(Math.round(x*100)/100,true);b.dataset.tone=x<0?'red':'green'};
 const from=shown==null?v:shown;if(inst||matchMedia('(prefers-reduced-motion: reduce)').matches||from===v){shown=v;set(v);return}
 const t0=performance.now();const st=t=>{const k=Math.min(1,(t-t0)/2400),x=from+(v-from)*(1-Math.pow(1-k,3));shown=x;set(x);if(k<1)raf=requestAnimationFrame(st)};raf=requestAnimationFrame(st)}
function step(n){stage=n;qa('.rgc-step span').forEach(s=>s.classList.toggle('on',+s.dataset.s===n));R.classList.toggle('rgc-done',n>=4)}
const A=q('.rgc-a'),V=q('.rgc-v'),P=q('.rgc-p');
function reset(){run++;A.pause();V.pause();try{A.currentTime=0;V.currentTime=0}catch(e){}V.classList.remove('on');A.classList.remove('on');P.classList.add('on');step(1);badge(Y.r1,true)}
function play(){reset();const tok=run;q('.rgc-play').classList.add('busy');
 setTimeout(()=>{if(tok!==run)return;P.classList.remove('on');A.classList.add('on');A.play().catch(()=>{});
  const chk=()=>{if(tok!==run)return;const t=A.currentTime;if(t>=2.3&&stage<3)step(3);else if(t>=0.6&&stage<2)step(2);
   if(A.ended||t>=(A.duration||4.2)-0.05){step(4);V.classList.add('on');A.classList.remove('on');V.play().catch(()=>{});badge(Y.r2,false);q('.rgc-play').classList.remove('busy');return}requestAnimationFrame(chk)};chk()},900)}
function finish(){reset();P.classList.remove('on');V.classList.add('on');try{V.currentTime=Math.max(0,(V.duration||2.5)-0.05)}catch(e){}step(4);badge(Y.r2,true)}
q('.rgc-play').addEventListener('click',play);
const F=R.querySelector('#rgForm');F.addEventListener('input',calc);F.addEventListener('submit',e=>e.preventDefault());
R.querySelector('.rg-reset').addEventListener('click',()=>{fill();calc()});
qa('.rg-tog button').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.mo;qa('.rg-you').forEach(y=>y.dataset.mode=mode);qa('.rg-tog button').forEach(x=>x.setAttribute('aria-pressed',x===b));calc()}));
R.querySelector('.rg-send').addEventListener('click',()=>{const sp=document.querySelector('[name=spaces]');const f=sp&&sp.form;if(!f)return;sp.value=Y.n;const m=f.querySelector('[name=message]');
 if(m){const line='TilePark case study: '+nf(Y.n)+' spaces, '+nf(Y.a)+' '+Y.au+(Y.mode==='rent'?' rentable':' sellable')+', result '+cm(Y.r1,true)+' → '+cm(Y.r2,true)+' with TilePark.';if(!m.value.includes('TilePark case study'))m.value=(m.value?m.value+'\\n':'')+line}});
new MutationObserver(calc).observe(H,{attributes:true,attributeFilter:['lang','data-units']});calc();step(1);P.classList.add('on');
if(matchMedia('(prefers-reduced-motion: reduce)').matches){finish();return}
if('IntersectionObserver'in window){const io=new IntersectionObserver(e=>{if(e[0].isIntersecting){io.disconnect();A.preload='auto';V.preload='auto';play()}},{threshold:.5});io.observe(q('.rgc-stage'))}})()</script>''' % json.dumps(X, ensure_ascii=False)
s = s[:a] + JS + s[b:]
CSS = '''<style id="rgc-css">
.rgc .rg-lead{margin-bottom:0}
.rgc-grid{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:clamp(16px,2.4vw,28px);align-items:start;margin-top:clamp(20px,3vw,32px)}
.rgc-stage{position:relative;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background:var(--rg-panel);border:1px solid var(--rg-line)}
.rgc-stage>img,.rgc-stage>video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .25s}
.rgc-stage>.on{opacity:1}
.rgc-step{position:absolute;left:12px;top:12px;right:12px;display:flex}.rgc-step span{display:none;padding:.35rem .75rem;border-radius:999px;background:#040d09d9;color:#fff;font:600 .82rem "Inter",sans-serif}
.rgc-step span.on{display:inline-block}.rgc-step span:before{content:attr(data-s) " · ";color:var(--rg-green)}
.rgc-badge{position:absolute;right:12px;bottom:12px;padding:.6rem .9rem;border-radius:12px;background:#040d09e6;display:flex;flex-direction:column;gap:.1rem;min-width:9.5rem;transition:box-shadow .4s}
.rgc-badge .k{font:500 .66rem "IBM Plex Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--rg-muted)}
.rgc-badge b{font:700 clamp(1.2rem,2.4vw,1.8rem)/1.05 "Outfit","Inter",sans-serif;font-variant-numeric:tabular-nums;color:var(--rg-red);transition:color .4s}
.rgc-badge[data-tone=green] b{color:var(--rg-green)}.rgc-badge[data-tone=green]{box-shadow:0 0 0 2px #b8f03c66}
.rgc-play{all:unset;cursor:pointer;position:absolute;left:12px;bottom:12px;padding:.5rem .9rem;border-radius:999px;background:var(--rg-green);color:var(--rg-gink);font:700 .85rem "Inter",sans-serif}
.rgc-play.busy{opacity:.55}.rgc-play:focus-visible{outline:2px solid #fff;outline-offset:2px}
.rgc-in .rg-form{margin:0;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 12px;padding:14px}
.rgc-in .rg-form label{font-size:.8rem}.rgc-in .rg-form input{font-size:.98rem;padding:.45rem .6rem}
.rgc-in .rg-mode>span{font-size:.85rem}
.rgc-out{margin-top:clamp(14px,2vw,22px)}.rgc-out .rg-cmp{margin-top:0}
.rgc-done .rgc-out .rg-col:nth-child(2) .rg-ledger{box-shadow:0 0 0 2px #b8f03c55}
.rgc-act{margin-top:12px}.rgc .rg-foot{margin-top:1rem}
@media (width<=1100px){.rgc-grid{grid-template-columns:minmax(0,1fr)}}
@media (width<=520px){.rgc-in .rg-form{grid-template-columns:minmax(0,1fr)}.rgc-badge{min-width:0}.rgc-badge b{font-size:1.15rem}.rgc-play{bottom:auto;top:52px}}
</style>'''
rep('</head>', CSS + '</head>')
s = s.replace('var D={', 'var D=' + json.dumps(T, ensure_ascii=False)[:-1] + ', ', 1)
open(out, 'w').write(s); print('ok', len(s)//1024, 'KB')
