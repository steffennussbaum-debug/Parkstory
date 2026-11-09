import sys,re,json
sys.path.insert(0,sys.argv[3]);from content import T
src,out=sys.argv[1],sys.argv[2]
s=open(src).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:100],s.count(a)); s=s.replace(a,b)
def block(start_marker,tag):
    """return (i,j) of the balanced element starting at start_marker"""
    i=s.find(start_marker); assert i>=0,start_marker
    pos=i; depth=0; o=re.compile(r'<%s[\s>]|</%s>'%(tag,tag))
    for m in o.finditer(s,i):
        if m.group(0).startswith('</'): depth-=1
        else: depth+=1
        if depth==0: return i,m.end()
    raise Exception('unbalanced')
def cut(start_marker,tag):
    global s
    i,j=block(start_marker,tag); b=s[i:j]; s=s[:i]+s[j:]; return b

# ---------------- menu: collect existing pieces ----------------
acc_i=s.find('<div class="hr-sec"'); last=s.rfind('<div class="hr-sec"'); acc_j=s.find('</ol></div>',last)+len('</ol></div>')
menu=s[acc_i:acc_j]
LI={}
for m in re.finditer(r'<li><a href="#([^"]+)">.*?</li>',menu,re.S): LI[m.group(1)]=m.group(0)
PD={m.group(1):(m.group(2),m.group(3)) for m in re.finditer(r'data-part="([^"]+)" aria-expanded="false"><span class="pn">\d+</span><span class="pt">([^<]+)</span><span class="go"[^>]*>›</span><span class="pd">([^<]*)</span>',menu)}
def li(h,name=None):
    if h in LI and not name: return LI[h]
    if h in LI and name: return re.sub(r'<span class="t">[^<]*</span>','<span class="t">%s</span>'%name,LI[h],1)
    return '<li><a href="#%s"><span class="t">%s</span></a></li>'%(h,name)
PARTS=[
 ('part-start','New to automated parking','The essentials in five minutes, and straight answers to the questions every buyer asks.',
   [li('primer','Automated parking in 5 minutes'),li('faq','Questions buyers ask')]),
 ('part-opp',PD['part-opp'][0],PD['part-opp'][1],[LI[h] for h in ['could-build','opportunity','economics','future-proof']]),
 ('part-how',PD['part-how'][0],PD['part-how'][1],[LI[h] for h in ['products','inspired-by-nature','how-it-works','video','third-dimension','tower','included','app','ev-charging','journey']]),
 ('part-compare','Comparing systems','For readers who know other systems: the architectures compared, and the performance we commit to.',
   [LI['compare'],li('agreed-performance','Performance you can hold us to'),li('supplier-questions','Questions to ask every supplier')]),
 ('part-news','References','TilePark systems and towers in operation, installations in progress, and what comes next.',[LI[h] for h in ['working-projects','follow-installations','ongoing-projects']]),
 ('part-dna',PD['part-dna'][0],PD['part-dna'][1],[LI[h] for h in ['figures','made-locally','service','engineering-ownership','different-approach']]),
 ('part-plan',PD['part-plan'][0],PD['part-plan'][1],[LI[h] for h in ['feasibility','feas-examples','request','bim','courses','contact']]),
]
newmenu=''.join('<div class="hr-sec" data-part="%s"><a class="hr-pa" href="#%s" data-part="%s" aria-expanded="false"><span class="pn">%d</span><span class="pt">%s</span><span class="go" aria-hidden="true">›</span><span class="pd">%s</span><span class="pp" aria-hidden="true"></span></a><ol class="hr-ch">%s</ol></div>'%(pid,pid,pid,k+1,t,d,''.join(ch)) for k,(pid,t,d,ch) in enumerate(PARTS))
s=s[:acc_i]+newmenu+s[acc_j:]
# chapter-view names (English originals)
names={"p":{p[0]:p[1] for p in PARTS},"c":{}}
for p in PARTS:
    for h in p[3]:
        m=re.search(r'<a href="#([^"]+)"><span class="t">([^<]+)</span>',h); names["c"][m.group(1)]=m.group(2)
i=s.find('const FXN=');j=s.find(';\nconst vis=',i);assert i>0 and j>i
s=s[:i]+'const FXN='+json.dumps(names,ensure_ascii=False)+s[j:]

# ---------------- hero ----------------
rep('<p class="bs-eye">TilePark XY</p><p class="bs-claim">What would you build if parking <em>didn’t dictate the design?</em></p>',
    '<p class="bs-eye">TilePark automated parking</p><p class="bs-claim">More cars on less space. <em>Your car, ready when you are.</em></p>'
    '<div class="ov-proof"><div><b>100+</b><span>automated parking projects</span></div><div><b>20,000+</b><span>installed parking spaces</span></div><div><b>DE + US</b><span>our own plants</span></div><p>Including the Nussbaum automated parking legacy.</p></div>')
i=s.find('<p class="bs-lead">');j=s.find('</p>',i)+4
s=s[:i]+'<p class="bs-lead">Drive into a bright transfer cabin and step out: TilePark parks the car for you. Independent conveyors move it in every direction, with no ramps, no drive aisles and no central lift that every car depends on. More cars fit on the same footprint, the garage keeps working if one machine stops, and the performance is agreed with you in the contract.</p>'\
 '<div class="ov-paths"><a class="ov-path" href="#primer" data-tour="primer"><span>New to automated parking?</span><b>Take the 5-minute tour</b><i aria-hidden="true">→</i></a><a class="ov-path ov-path2" href="#compare" data-tour="compare"><span>Comparing systems?</span><b>See how TilePark compares</b><i aria-hidden="true">→</i></a></div>'+s[j:]
rep('<a class="bs-cue" href="#part-opp"><i aria-hidden="true"></i>Discover what you could build</a>','<a class="bs-cue" href="#part-start"><i aria-hidden="true"></i>Start here</a>')

# ---------------- new sections ----------------
cabin_poster=re.search(r'<div class="bs-pop" id="pop-cabin" hidden>.*?poster="([^"]+)"',s,re.S).group(1)
def opener(pid,k,h1,h2,p): return '<section class="part-open" id="%s"><div class="wrap"><p class="part-k">%s</p><h2>%s <em>%s</em></h2><p>%s</p></div></section>'%(pid,k,h1,h2,p)
steps=[("Drive in","Drive into the bright transfer cabin and step out."),("Confirm","Confirm at the touchscreen or in the app. The system takes over."),
       ("Parked for you","Conveyors move the car in every direction to a free space; lifts or stackers take it between levels."),("Call it back","Tell the app you’re leaving, and your car is waiting in the transfer cabin when you get there.")]
proj=[("Free feasibility study","Send us your site or floor plan. We show capacity, layout and the space you gain."),("Design with your architect","BIM models and our engineers support your design team."),
      ("Agreed performance","Retrieval times, capacity and service are defined with you and written into the contract."),("Made in our own plants","Built in Kehl or Gastonia, every conveyor load-tested before it ships."),
      ("Installation and commissioning","Our own team installs the system and hands it over."),("Service for decades","24/7 service, remote diagnostics and spare parts for at least 30 years.")]
PRIMER=('<section class="ov ov-primer" id="primer"><div class="wrap">'
 '<p class="hiw-eyebrow">New to automated parking</p><h2 class="ov-h">Automated parking <em>in five minutes.</em></h2>'
 '<p class="ov-lead">No ramps, no searching for a space, no walking through a dark garage. This is what you need to know before your first conversation with us.</p>'
 '<div class="ov-drv"><div><h3 class="ov-h3">For the driver</h3><ol class="ov-steps">'+''.join('<li><b>%d</b><div><h4>%s</h4><p>%s</p></div></li>'%(n+1,a,b) for n,(a,b) in enumerate(steps))+'</ol></div>'
 '<figure class="ov-fig"><img src="'+cabin_poster+'" alt="Driving into the bright TilePark transfer cabin in Munich" loading="lazy"><figcaption>TilePark Munich: entrance to the transfer cabin</figcaption></figure></div>'
 '<div class="ov-two"><div class="ov-card"><h3 class="ov-h3">For your building</h3><ul class="ov-ticks"><li>More cars on the same footprint: at least 20 % more spaces than automated systems with drive aisles, based on our layout studies.</li><li>No ramps or drive aisles: the space goes back to apartments, offices or green space.</li><li>Fits irregular sites and column grids, because identical conveyors form the grid.</li></ul></div>'
 '<div class="ov-card ov-dark"><h3 class="ov-h3">What it costs</h3><p class="ov-big">≈ $30,000</p><p>Most TilePark systems from 25 spaces cost around $30,000 per space. The larger the system, the lower the cost per space.</p><p class="ov-small">The free feasibility study shows the figure for your site.</p></div></div>'
 '<h3 class="ov-h3">How a project runs</h3><ol class="ov-proj">'+''.join('<li><b>%d</b><h4>%s</h4><p>%s</p></li>'%(n+1,a,b) for n,(a,b) in enumerate(proj))+'</ol>'
 '<div class="ov-ctas"><a class="ov-btn" href="#faq">Questions? See the answers →</a><a class="ov-btn ov-btn2" href="#request">Request a free feasibility study →</a></div>'
 '</div></section>')
FAQ_ITEMS=[
 ("How long does it take to get my car?","That depends on the size and layout of your system and the number of transfer cabins. We define the retrieval time with you for your project and put it in the contract. With the app you can call your car ahead, so it is waiting when you arrive."),
 ("What happens if a machine breaks down?","Every conveyor has its own controller and at least four drive motors. If one conveyor stops, the others route the cars around it, so every car stays reachable. Our service team monitors the system around the clock and solves 99 % of faults remotely."),
 ("What happens during a power failure?","The power concept, including how cars are retrieved during an outage, is part of the design we agree with you for your building."),
 ("Is it safe? Who goes into the garage?","Drivers only enter the bright transfer cabin at ground level. The parking area itself is closed to the public, so there are no dark ramps or stairwells to walk through."),
 ("How is fire protection handled?","Fire protection is planned for each site with your fire protection engineer and the local authorities, and becomes part of the agreed design."),
 ("Which cars fit?","We define the vehicle sizes and weights with you, based on who will park in your building, and design the system for them."),
 ("Can every space charge an electric car?","Every space can be equipped for charging. The system moves cars to and from the chargers, so fewer charging points serve more cars."),
 ("How long will the system last, and who services it?","A parking system is part of your building for decades. Our own team commissions and services every system: 24/7 service, remote diagnostics, a technician on site when needed, and spare parts for at least 30 years."),
 ("What does it cost?","Most TilePark systems from 25 spaces cost around $30,000 per space; the larger the system, the lower the cost per space. The free feasibility study shows the figure for your site."),
 ("How is TilePark different from other automated systems?","AGV robots, rail-guided shuttles and tower systems need at least one drive aisle, rails or a central lift. TilePark needs none: every position is a conveyor, so the whole floor is parking and no single machine stands between a driver and their car."),
 ("Who are we buying from?","Parkstory designs, builds, installs and services TilePark itself: engineering in Germany, the USA and Hungary, our own plants in Kehl and Gastonia, and one team responsible for the system over its lifetime."),
 ("How do we start?","Send us your site or floor plan. Our engineers lay out TilePark on your site free of charge and show you capacity, layout and the space you gain."),
]
FAQ=('<section class="ov ov-faq" id="faq"><div class="wrap"><p class="hiw-eyebrow">Questions buyers ask</p><h2 class="ov-h">Straight answers <em>before you decide.</em></h2><div class="ov-qa">'
 +''.join('<details class="ov-q"><summary>%s</summary><div><p>%s</p></div></details>'%(q,a) for q,a in FAQ_ITEMS)+
 '</div><div class="ov-ctas"><a class="ov-btn" href="#supplier-questions">More answers for experts →</a><a class="ov-btn ov-btn2" href="#request">Request a free feasibility study →</a></div></div></section>')
VALS=[("Retrieval time","How quickly a driver gets their car, at normal times and at peak."),("Throughput","How many cars the system moves per hour in the morning and evening rush."),
      ("Vehicles","The sizes and weights of the cars your users drive, including electric vehicles."),("Availability","How reliably the system is ready to park and retrieve."),
      ("EV charging","How many cars can charge, and how fast they are ready."),("Service","Response times, remote diagnostics and on-site support.")]
WHY=[("One team, one responsibility","We engineer, build, install and service the system ourselves. No subcontractor to point to."),
     ("No single point of failure","Every conveyor has its own controller and at least four drive motors. Cars are routed around a stopped conveyor."),
     ("Tested before it ships","Every conveyor runs under load on our test rig and carries a serial number."),
     ("Proven over decades","Built on more than 100 automated parking projects and 20,000+ installed spaces, including the Nussbaum legacy.")]
AGREED=('<section class="ov ov-agree" id="agreed-performance"><div class="wrap"><p class="hiw-eyebrow">Our commitment</p><h2 class="ov-h">Performance <em>you can hold us to.</em></h2>'
 '<p class="ov-lead">Every building is different, so we don’t sell brochure figures. The values that matter are defined with you for your project, written into the contract, and you can hold us to them.</p>'
 '<div class="ov-vals">'+''.join('<div><span class="ov-chk" aria-hidden="true">✓</span><h4>%s</h4><p>%s</p></div>'%(a,b) for a,b in VALS)+'</div>'
 '<h3 class="ov-h3">Why we can commit to them</h3><div class="ov-why">'+''.join('<div><h4>%s</h4><p>%s</p></div>'%(a,b) for a,b in WHY)+'</div></div></section>')
QS=[("If one machine stops, can every car still be retrieved?","Yes. The other conveyors route the cars around a stopped one, so every car stays reachable."),
    ("Does every car depend on one lift, shuttle or robot?","Not in TilePark: every position is a conveyor with its own controller."),
    ("How much floor is lost to aisles, rails or lifts?","None to aisles or rails: the whole floor is parking."),
    ("Who builds the machines, and who will service them in 20 years?","We do: our own plants in Kehl and Gastonia and our own service team, with spare parts for at least 30 years."),
    ("Will the supplier commit to retrieval times and availability in the contract?","We do. We define them with you, and you can hold us to them."),
    ("Can the layout follow your columns and site shape?","Yes. Identical conveyors form the grid, so it adapts to irregular sites, columns and any size."),
    ("Is the core technology protected?","Yes: a granted core patent on the X-Y conveyor technology (EP 3924576 B1), and three further applications filed in the USA.")]
SUPP=('<section class="ov ov-supp" id="supplier-questions"><div class="wrap"><p class="hiw-eyebrow">For buyers who know other systems</p><h2 class="ov-h">Questions to ask <em>every supplier.</em></h2>'
 '<p class="ov-lead">If you have seen AGV robots, shuttle systems or parking towers, these are the questions that separate the architectures. Here are our answers.</p><ol class="ov-sq">'
 +''.join('<li><b>%d</b><div><h4>%s</h4><p><span class="ov-ans">Our answer</span>%s</p></div></li>'%(n+1,q,a) for n,(q,a) in enumerate(QS))+
 '</ol><div class="ov-ctas"><a class="ov-btn" href="#compare">Compare the architectures →</a><a class="ov-btn ov-btn2" href="#bim">Download BIM models →</a></div></div></section>')

# ---------------- reorder ----------------
compare=cut('<section class="cmp" id="compare">','section')
news_i=s.find('<section class="part-open" id="part-news"'); _,news_j=block('<section class="nw sec-bg" id="ongoing-projects"' if '<section class="nw sec-bg" id="ongoing-projects"' in s else '<section class="nw" id="ongoing-projects"','section')
news=s[news_i:news_j]; s=s[:news_i]+s[news_j:]
P1=opener('part-start','New to automated parking','Start here.','The essentials in five minutes.','How TilePark works for drivers and owners, what it costs, how a project runs, and straight answers to the questions every buyer asks.')
rep('</header><span id="part-opp" class="part-anchor"></span>','</header>'+P1+PRIMER+FAQ+'<span id="part-opp" class="part-anchor"></span>')
P4=opener('part-compare','Comparing systems','Already know other systems?','Here is the difference.','The architectures side by side, the performance we commit to in the contract, and the questions to ask every supplier.')
dna='<div class="dna" id="part-dna"'
assert s.count(dna)==1
s=s.replace(dna,P4+compare+AGREED+SUPP+news+dna)

# ---------------- tour buttons ----------------
TOUR='document.addEventListener("click",e=>{const a=e.target.closest("[data-tour]");if(!a)return;const t=document.getElementById(a.dataset.tour);const c=CH.find(c=>c.el===t);if(!c)return;e.preventDefault();e.stopImmediatePropagation();setOpenPart(c.part.id);fxChapter(c)},true);\n'
rep('// any other in-page link to something outside the chapter',TOUR+'// any other in-page link to something outside the chapter')

# ---------------- css ----------------
CSS='''<style id="overhaul-css">
.ov-proof{display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:.5rem clamp(.9rem,2vw,1.6rem);margin-top:1.1rem;align-items:start}
.ov-proof div{display:flex;flex-direction:column}.ov-proof b{font:700 clamp(1.4rem,2.4vw,2rem)/1 "Outfit","Inter",sans-serif;color:var(--green-bright,#b8f03c)}
.ov-proof span{font-size:.8rem;color:#d7e6dd;margin-top:.2rem}.ov-proof p{grid-column:1/-1;margin:0;font-size:.72rem;color:#b9cbbf}
.ov-paths{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.6rem;margin:1rem 0 .9rem}
.ov-path{position:relative;display:flex;flex-direction:column;gap:.15rem;padding:.75rem 2.2rem .8rem 1rem;border-radius:14px;background:var(--green-bright,#b8f03c);color:#07150f;text-decoration:none}
.ov-path span{font-size:.78rem;font-weight:600;opacity:.8}.ov-path b{font-size:1rem}.ov-path i{position:absolute;right:.9rem;top:50%;transform:translateY(-50%);font-style:normal;font-weight:700}
.ov-path2{background:#ffffff14;color:#fff;border:1px solid #ffffff4d}.ov-path2 span{opacity:.85}
@media (width<=600px){.ov-paths{grid-template-columns:1fr}}
.ov{padding:clamp(56px,7vw,104px) 0;background:var(--bg)}.ov .wrap{max-width:var(--wrap-max,1280px);margin:0 auto;padding:0 var(--gutter,24px)}
.ov-h{margin:.2rem 0 .7rem;font:700 clamp(1.9rem,3.6vw,3rem)/1.06 "Outfit","Inter",sans-serif;color:var(--ink);max-width:22ch}.ov-h em{font-style:normal;color:var(--green)}
.ov-lead{max-width:64ch;color:var(--text);font-size:var(--fs-md,1.08rem);margin:0 0 2rem}
.ov-h3{margin:2.2rem 0 1rem;font:700 clamp(1.2rem,2vw,1.5rem)/1.2 "Outfit","Inter",sans-serif;color:var(--ink)}
.ov-drv{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(20px,3vw,48px);align-items:center}.ov-drv .ov-h3{margin-top:0}
.ov-steps,.ov-proj,.ov-sq{list-style:none;margin:0;padding:0}
.ov-steps{display:grid;gap:1rem}.ov-steps li,.ov-sq li{display:grid;grid-template-columns:38px 1fr;gap:.9rem;align-items:start}
.ov-steps b,.ov-proj b,.ov-sq>li>b{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--navy);color:var(--green-bright,#b8f03c);font-weight:700}
.ov h4{margin:.1rem 0 .25rem;font-size:1.02rem;color:var(--ink)}.ov li p,.ov-card p,.ov-vals p,.ov-why p{margin:0;color:var(--text);line-height:1.5}
.ov-fig{margin:0;border-radius:var(--r-lg);overflow:hidden;position:relative;background:var(--navy)}.ov-fig img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.ov-fig figcaption{position:absolute;left:.8rem;bottom:.8rem;padding:.25rem .65rem;border-radius:999px;background:#040d09cc;color:#fff;font-size:.78rem}
.ov-two{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:clamp(14px,2vw,24px);margin-top:2.4rem}
.ov-card{background:var(--surface);border:1px solid var(--line-soft);border-radius:var(--r-lg);padding:clamp(18px,2.4vw,30px)}.ov-card .ov-h3{margin-top:0}
.ov-ticks{margin:0;padding:0;list-style:none;display:grid;gap:.8rem}.ov-ticks li{position:relative;padding-left:1.7rem;color:var(--text);line-height:1.5}
.ov-ticks li:before{content:"✓";position:absolute;left:0;top:0;font-weight:700;color:var(--green)}
.ov-dark{background:var(--navy);border-color:transparent}.ov-dark .ov-h3,.ov-dark p{color:#e3efe7!important}.ov-big{font:700 clamp(2.2rem,4vw,3.2rem)/1 "Outfit","Inter",sans-serif;color:var(--green-bright,#b8f03c)!important;margin:0 0 .8rem!important}
.ov-small{font-size:.88rem;margin-top:.7rem!important;opacity:.85}
.ov-proj{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(12px,1.6vw,20px)}
.ov-proj li{background:var(--surface);border:1px solid var(--line-soft);border-radius:var(--r-lg);padding:1.1rem 1.2rem}.ov-proj li h4{margin-top:.7rem}
.ov-ctas{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:2rem}
.ov-btn{display:inline-flex;align-items:center;padding:.75rem 1.25rem;border-radius:999px;background:var(--navy);color:#fff;text-decoration:none;font-weight:600}
.ov-btn2{background:var(--green-bright,#b8f03c);color:#07150f}
.ov-faq{background:var(--surface)}.ov-qa{display:grid;gap:.6rem;max-width:900px}
.ov-q{border:1px solid var(--line-soft);border-radius:14px;background:var(--bg)}.ov-q summary{cursor:pointer;list-style:none;padding:1rem 3rem 1rem 1.2rem;font-weight:700;color:var(--ink);position:relative}
.ov-q summary::-webkit-details-marker{display:none}.ov-q summary:after{content:"+";position:absolute;right:1.2rem;top:50%;transform:translateY(-50%);font-size:1.3rem;color:var(--green)}
.ov-q[open] summary:after{content:"–"}.ov-q>div{padding:0 1.2rem 1.1rem}.ov-q p{margin:0;color:var(--text);line-height:1.6}
.ov-agree{background:var(--navy)}.ov-agree .ov-h,.ov-agree .ov-h3,.ov-agree h4{color:#fff}.ov-agree .ov-h em{color:var(--green-bright,#b8f03c)}.ov-agree .ov-lead,.ov-agree p{color:#cfe0d6!important}
.ov-agree .hiw-eyebrow{color:var(--green-bright,#b8f03c)}
.ov-vals{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(12px,1.6vw,20px)}
.ov-vals>div{border:1px solid #ffffff26;border-radius:var(--r-lg);padding:1.1rem 1.2rem;background:#ffffff0a}
.ov-chk{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--green-bright,#b8f03c);color:#07150f;font-weight:700;margin-bottom:.5rem}
.ov-why{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(12px,1.6vw,20px)}.ov-why>div{border-top:2px solid var(--green-bright,#b8f03c);padding-top:.8rem}
.ov-sq{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.1rem 2rem}
.ov-ans{display:block;font-size:.72rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--green-ink,var(--green));margin-bottom:.15rem}
@media (width<=1100px){.ov-proj,.ov-vals{grid-template-columns:repeat(2,minmax(0,1fr))}.ov-why{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (width<=800px){.ov-drv,.ov-two,.ov-sq{grid-template-columns:1fr}}
@media (width<=600px){.ov-proj,.ov-vals,.ov-why{grid-template-columns:1fr}}
</style>'''
rep('</head>',CSS+'</head>')
# translations
rep('var D={','var D='+json.dumps(T,ensure_ascii=False)[:-1]+', ')
open(out,'w').write(s);print('ok',len(s)//1024,'KB')
