# Replaces the schematic "building that could exist" graphic with the 3D film player.
# python sim_patch.py <master.html> <out.html> <media_dir>
import sys, re, json, base64, os
src, out, md = sys.argv[1:4]
s = open(src).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:90], s.count(a)); s = s.replace(a, b)
def uri(name, mime):
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(os.path.join(md, name), 'rb').read()).decode())

def srcs(n):
    return '<source src="%s" type="video/webm"><source src="%s" type="video/mp4">' % (uri(n+'.webm','video/webm'), uri(n+'.mp4','video/mp4'))
# --- figure ---
i = s.find('<figure class="sg-fig" data-step="0" data-use="apt">'); j = s.find('</figure>', i) + len('</figure>')
assert i > 0
FIG = ('<figure class="sg-fig sg-vid" data-step="0" data-use="apt"><div class="sgv-stage">'
 '<video class="sgv sgv-a" muted playsinline preload="auto" poster="%s" aria-label="3D animation: a conventional garage becomes TilePark and the freed floors become usable space">%s</video>'
 '<video class="sgv sgv-v" data-u="apt" muted playsinline preload="metadata" aria-hidden="true">%s</video>'
 '<video class="sgv sgv-v" data-u="off" muted playsinline preload="metadata" aria-hidden="true">%s</video>'
 '<video class="sgv sgv-v" data-u="ret" muted playsinline preload="metadata" aria-hidden="true">%s</video>'
 '</div><div class="sgv-meter" data-noi18n aria-live="polite">'
 '<div><span class="k" data-m="pk"></span><b class="v" id="sgvPk">4</b></div>'
 '<div><span class="k" data-m="earn"></span><b class="v" id="sgvEarn">4</b><span class="sgu" data-m="of8"></span></div>'
 '<div><span class="k" data-m="area"></span><b class="v" id="sgvArea">–</b><span class="sgu" id="sgvAreaN"></span></div>'
 '<div class="hi"><span class="k" data-m="val"></span><b class="v" id="sgvVal">–</b><a class="sgu" href="#sim-opp" data-m="own"></a></div>'
 '</div><figcaption>Illustrative 3D animation of an example building with 68 parking spaces. What it means for your site depends on zoning and design.</figcaption></figure>') % (
  uri('poster0.jpg','image/jpeg'), srcs('common'), srcs('apt'), srcs('off'), srcs('ret'))
s = s[:i] + FIG + s[j:]

# --- step texts and use buttons ---
rep('<b>TilePark takes over</b><span>Conveyors and stackers park the same cars in half the floors.</span>',
    '<b>TilePark takes over</b><span>Conveyors park the same cars on half the floors.</span>')
rep('<b>Build what you want</b><span>The freed floors become apartments, offices or green space.</span>',
    '<b>Build what you want</b><span>The freed floors become apartments, offices or retail.</span>')
rep('<button type="button" data-u="grn">Green space</button>', '<button type="button" data-u="ret">Retail</button>')

# --- old script out, new player in ---
a = s.find("(()=>{const S=document.getElementById('could-build');if(!S)return;const fig=S.querySelector('.sg-fig')")
b = s.find('</script>', a)
assert a > 0
PLAYER = r'''(()=>{const S=document.getElementById('could-build');if(!S)return;const H=document.documentElement,$=i=>document.getElementById(i);
const fig=S.querySelector('.sg-fig'),steps=[...S.querySelectorAll('.sg-steps li')],A=S.querySelector('.sgv-a'),V={};S.querySelectorAll('.sgv-v').forEach(v=>V[v.dataset.u]=v);
const L={en:{pk:'Parking floors',earn:'Floors that earn',of8:'of 8 upper floors',area:'Floor area gained',val:'Illustrative value',own:'Use your own numbers →',n:(a,b)=>'68 spaces × '+a+' each, at '+b,mio:'million'},
de:{pk:'Parkebenen',earn:'Ebenen mit Ertrag',of8:'von 8 Obergeschossen',area:'Gewonnene Fläche',val:'Beispielwert',own:'Mit eigenen Zahlen rechnen →',n:(a,b)=>'68 Stellplätze × je '+a+', bei '+b,mio:'Mio.'},
fr:{pk:'Niveaux de stationnement',earn:'Niveaux qui rapportent',of8:'sur 8 étages',area:'Surface gagnée',val:'Valeur indicative',own:'Calculer avec vos chiffres →',n:(a,b)=>'68 places × '+a+' chacune, à '+b,mio:'millions'},
es:{pk:'Plantas de aparcamiento',earn:'Plantas que generan ingresos',of8:'de 8 plantas superiores',area:'Superficie ganada',val:'Valor orientativo',own:'Calcule con sus cifras →',n:(a,b)=>'68 plazas × '+a+' cada una, a '+b,mio:'millones'}};
const T1=26/24;let cur=-1,use='apt',seq=0,raf=0,shown=0,run=0;
const lg=()=>L[H.lang]?H.lang:'en',met=()=>H.dataset.units==='m';
function calc(){const m=met(),per=m?14:150,v=+(($('oppVal')||{}).value)||(m?4000:400),au=m?'m²':'sq ft',cur=m?'€':'$';return{per,v,au,cur,A:68*per,M:68*per*v}}
function fmtMoney(M,c){const l=lg(),f1=new Intl.NumberFormat(l==='en'?'en-US':l,{maximumFractionDigits:1}),nf=new Intl.NumberFormat(l==='en'?'en-US':l,{maximumFractionDigits:0});
 const t=M>=1e6?f1.format(M/1e6)+' '+L[l].mio:nf.format(M);return l==='en'?c+t:t+' '+c}
function texts(){const l=L[lg()];S.querySelectorAll('.sgv-meter [data-m]').forEach(e=>e.textContent=l[e.dataset.m]);const c=calc(),nf=new Intl.NumberFormat(lg()==='en'?'en-US':lg());
 $('sgvAreaN').textContent=l.n(nf.format(c.per)+' '+c.au,(lg()==='en'?c.cur+nf.format(c.v):nf.format(c.v)+' '+c.cur)+'/'+c.au);paint(shown)}
function paint(p){shown=p;const c=calc(),nf=new Intl.NumberFormat(lg()==='en'?'en-US':lg());
 $('sgvArea').textContent=p>0?nf.format(Math.round(c.A*p/10)*10)+' '+c.au:'–';$('sgvVal').textContent=p>0?fmtMoney(c.M*p,c.cur):'–'}
function count(){cancelAnimationFrame(raf);const t0=performance.now(),d=2600;const st=t=>{const k=Math.min(1,(t-t0)/d);paint(1-Math.pow(1-k,3));if(k<1)raf=requestAnimationFrame(st)};raf=requestAnimationFrame(st)}
function mark(n){cur=n;fig.dataset.step=n;S.classList.toggle('s3',n===3);steps.forEach((li,i)=>{li.classList.toggle('on',i===n);li.classList.toggle('done',i<n)});
 $('sgvPk').textContent=n>=2?'4 → 2':'4';$('sgvEarn').textContent=n>=3?'4 → 6':'4';fig.classList.toggle('m2',n>=2);fig.classList.toggle('m3',n>=3);
 if(n===3)count();else{cancelAnimationFrame(raf);paint(0)}}
const end=()=>Math.max(0,(A.duration||4.2)-0.02);
function stopV(){Object.values(V).forEach(v=>{v.pause();v.classList.remove('on')})}
function playTo(t,cb){const my=++seq;A.play().catch(()=>{});const chk=()=>{if(my!==seq)return;if(A.currentTime>=t-0.03||A.ended){A.pause();cb&&setTimeout(()=>{if(my===seq)cb()},0)}else requestAnimationFrame(chk)};chk();return my}
function seek(t){seq++;A.pause();try{A.currentTime=t}catch(e){}}
function set(n,anim,cb){stopV();
 if(n===0){seek(0);mark(0)}
 else if(n===1){if(anim){seek(0);mark(1);playTo(T1,cb)}else{seek(T1);mark(1)}}
 else if(n===2){if(anim){if(Math.abs(A.currentTime-T1)>0.08){try{A.currentTime=T1}catch(e){}}mark(2);playTo(end(),cb)}else{seek(end());mark(2)}}
 else{seek(end());mark(3);const v=V[use];if(v){try{v.currentTime=0}catch(e){}v.classList.add('on');v.play().catch(()=>{})}}}
function play(){const tok=++run;set(0);setTimeout(()=>{if(tok!==run)return;set(1,true,()=>setTimeout(()=>{if(tok!==run)return;set(2,true,()=>setTimeout(()=>{if(tok===run)set(3)},900))},1600))},900)}
steps.forEach((li,i)=>li.querySelector('button').addEventListener('click',()=>{run++;set(i,i>0&&i<3&&cur===i-1)}));
S.querySelectorAll('.sg-use button').forEach(b=>b.addEventListener('click',()=>{S.querySelectorAll('.sg-use button').forEach(x=>x.classList.toggle('on',x===b));use=b.dataset.u;fig.dataset.use=use;run++;set(3)}));
S.querySelector('.sg-replay').addEventListener('click',play);
new MutationObserver(texts).observe(H,{attributes:true,attributeFilter:['lang','data-units']});const ov=$('oppVal');if(ov)ov.addEventListener('input',texts);
texts();mark(0);
if(matchMedia('(prefers-reduced-motion: reduce)').matches){set(3);return}
if('IntersectionObserver'in window){const pre=new IntersectionObserver(e=>{if(e[0].isIntersecting){pre.disconnect();Object.values(V).forEach(v=>v.preload='auto')}},{rootMargin:'600px'});pre.observe(fig);
 const io=new IntersectionObserver(e=>{if(e[0].isIntersecting){io.disconnect();setTimeout(play,400)}},{threshold:.45});io.observe(fig)}else play()})()'''
s = s[:a] + PLAYER + s[b:]

CSS = '''<style id="sgv-css">
.sg-vid{margin:0}
.sgv-stage{position:relative;aspect-ratio:16/9;border-radius:6px;overflow:hidden;border:1px solid #ffffff14;background:#0b1a13}
.sgv{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.sgv-v{opacity:0;transition:opacity .2s}.sgv-v.on{opacity:1}
.sgv-meter{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;margin-top:10px;border-radius:6px;overflow:hidden;background:#ffffff14}
.sgv-meter>div{background:#0b1a13;padding:.7rem .85rem;display:flex;flex-direction:column;gap:.15rem;min-width:0}
.sgv-meter .k{font:600 .72rem "Inter",sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#8fa497}
.sgv-meter .v{font:700 clamp(1.15rem,2vw,1.6rem)/1.1 "Outfit","Inter",sans-serif;color:#e6f0ea;transition:color .4s}
.sgv-meter .sgu{font-size:.74rem;color:#8fa497;line-height:1.35}
.sgv-meter a.sgu{color:#b8f03c;text-decoration:none;font-weight:600}
.sg-vid.m2 #sgvPk,.sg-vid.m3 #sgvEarn,.sg-vid.m3 #sgvArea{color:#b8f03c}
.sgv-meter .hi{background:#10261b}.sg-vid.m3 #sgvVal{color:#b8f03c}
@media (width<=900px){.sgv-meter{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>'''
rep('</head>', CSS + '</head>')
T = {
 "Conveyors park the same cars on half the floors.":["Fördermodule parken dieselben Fahrzeuge auf der Hälfte der Ebenen.","Les convoyeurs garent les mêmes voitures sur la moitié des niveaux.","Los transportadores aparcan los mismos coches en la mitad de las plantas."],
 "The freed floors become apartments, offices or retail.":["Die frei gewordenen Ebenen werden zu Wohnungen, Büros oder Läden.","Les niveaux libérés deviennent logements, bureaux ou commerces.","Las plantas liberadas se convierten en viviendas, oficinas o comercios."],
 "Retail":["Läden","Commerces","Comercio"],
 "Illustrative 3D animation of an example building with 68 parking spaces. What it means for your site depends on zoning and design.":["Beispielhafte 3D-Animation eines Gebäudes mit 68 Stellplätzen. Was das für Ihr Grundstück bedeutet, hängt von Bebauungsplan und Entwurf ab.","Animation 3D indicative d’un bâtiment exemple de 68 places. Ce que cela signifie pour votre site dépend de l’urbanisme et de la conception.","Animación 3D orientativa de un edificio de ejemplo con 68 plazas. Lo que significa para su solar depende del planeamiento y del diseño."],
}
rep('var D={', 'var D=' + json.dumps(T, ensure_ascii=False)[:-1] + ', ')
open(out, 'w').write(s); print('ok', len(s)//1024, 'KB')
