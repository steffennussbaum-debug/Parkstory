# Generates the in-depth guide pages (English) with metadata and JSON-LD. python topics.py <outdir> <imgdir>
import sys, os, json, shutil, html as H
out, imgd = sys.argv[1:3]
BASE = 'https://www.parkstory.com/'
ORG = {"@type":"Organization","@id":BASE+"#org","name":"Parkstory","url":BASE,"email":"info@parkstory.com",
       "subOrganization":[{"@type":"Organization","name":"Parkstory GmbH","address":{"@type":"PostalAddress","addressLocality":"Munich","addressCountry":"DE"}},
                          {"@type":"Organization","name":"Parkstory, Inc.","address":{"@type":"PostalAddress","addressLocality":"Gastonia","addressRegion":"NC","addressCountry":"US"}},
                          {"@type":"Organization","name":"Parkstory Manufacturing GmbH","address":{"@type":"PostalAddress","addressLocality":"Kehl","addressCountry":"DE"}},
                          {"@type":"Organization","name":"Parkstory Kft.","address":{"@type":"PostalAddress","addressLocality":"Budapest","addressCountry":"HU"}}]}
for n in ('c2','c5','c1'): shutil.copy(os.path.join(imgd, n+'.jpg'), os.path.join(out, 'guide-'+n+'.jpg'))
CSS = '''@font-face{font-family:"Inter";src:url(fonts/inter.woff2) format("woff2");font-weight:100 900;font-display:swap}@font-face{font-family:"Outfit";src:url(fonts/outfit.woff2) format("woff2");font-weight:100 900;font-display:swap}@font-face{font-family:"IBM Plex Mono";src:url(fonts/plex-mono-500.woff2) format("woff2");font-weight:500;font-display:swap}
*{box-sizing:border-box}
:root{--bg:#f6f4ee;--surface:#ffffff;--ink:#0b1a13;--text:#3c4d44;--muted:#66786e;--line:#dfe3dc;--green:#1f7a3a;--lime:#b8f03c;--navy:#07150f;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#06120c;--surface:#0c1d15;--ink:#eef5f0;--text:#c8d8ce;--muted:#9db4a6;--line:#ffffff1f;--green:#b8f03c;color-scheme:dark}}
:root[data-theme=dark]{--bg:#06120c;--surface:#0c1d15;--ink:#eef5f0;--text:#c8d8ce;--muted:#9db4a6;--line:#ffffff1f;--green:#b8f03c;color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--text);font:400 1.02rem/1.65 "Inter",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.w{max-width:880px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
header.top{background:var(--navy);color:#fff}header.top .w{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding-block:14px;max-width:1080px}
.brand{font:700 1.1rem "Outfit","Inter",sans-serif;color:#fff;text-decoration:none}.brand i{display:inline-block;width:12px;height:12px;border-radius:3px 9px 3px 9px;background:var(--lime);margin-right:.45rem}
header.top nav a{color:#cfe0d6;text-decoration:none;font-size:.9rem;margin-left:1rem}header.top nav a:hover{color:#fff}
.crumb{font-size:.82rem;color:var(--muted);padding-block:22px 0}.crumb a{color:var(--muted)}
h1{font:700 clamp(2rem,4.6vw,3.1rem)/1.08 "Outfit","Inter",sans-serif;letter-spacing:-.02em;color:var(--ink);margin:.6rem 0 1rem;text-wrap:balance}
h2{font:700 clamp(1.35rem,2.6vw,1.8rem)/1.2 "Outfit","Inter",sans-serif;color:var(--ink);margin:2.6rem 0 .8rem;text-wrap:balance}
h3{font:600 1.08rem/1.3 "Outfit","Inter",sans-serif;color:var(--ink);margin:1.4rem 0 .4rem}
p,li{max-width:68ch}a{color:var(--green)}
.lead{font-size:1.15rem;color:var(--text)}
.short{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--green);border-radius:10px;padding:1rem 1.2rem;margin:1.4rem 0}
.short b{display:block;font:600 .78rem "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--green);margin-bottom:.3rem}.short p{margin:0;color:var(--ink)}
figure{margin:1.6rem 0;border-radius:12px;overflow:hidden;background:var(--surface);border:1px solid var(--line)}figure img{display:block;width:100%;height:auto;max-width:100%}figcaption{font-size:.82rem;color:var(--muted);padding:.5rem .8rem}
.tw{overflow-x:auto;margin:1rem 0}table{border-collapse:collapse;width:100%;min-width:640px;font-size:.92rem;background:var(--surface);border-radius:10px;overflow:hidden}
th,td{text-align:left;vertical-align:top;padding:.65rem .75rem;border-bottom:1px solid var(--line)}th{font-size:.76rem;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);background:var(--surface)}td{color:var(--ink)}
tr.tp td{background:color-mix(in srgb,var(--lime) 14%,var(--surface))}
.note{font-size:.88rem;color:var(--muted)}
.tbp{font-style:italic;color:var(--muted)}
details{background:var(--surface);border:1px solid var(--line);border-radius:10px;margin:.5rem 0}summary{cursor:pointer;padding:.85rem 1rem;font-weight:600;color:var(--ink)}details>div{padding:0 1rem .9rem}details p{margin:0}
.calc{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:1.1rem;display:grid;gap:1rem}
.calc .in{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem 1rem}.calc label{display:flex;flex-direction:column;gap:.3rem;font-size:.86rem;color:var(--muted);min-width:0}
.calc input{font:600 1rem "Inter",sans-serif;padding:.5rem .6rem;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--ink);width:100%;min-width:0}
.calc input:focus{outline:2px solid var(--green);outline-offset:1px}
.res{display:grid;gap:0;border-top:1px solid var(--line)}.res div{display:flex;justify-content:space-between;gap:1rem;padding:.5rem 0;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}.res b{color:var(--ink);white-space:nowrap}.res .big b{font-size:1.25rem}.pos{color:var(--green)!important}.neg{color:#c2410c!important}
.related{margin:3rem 0 0;padding:1rem 1.2rem;border-radius:12px;border:1px solid var(--line);background:var(--surface)}.related ul{margin:.4rem 0 0;padding-left:1.1rem}
.cta{margin:2.4rem 0;padding:1.4rem;border-radius:14px;background:var(--navy);color:#fff}.cta h2{color:#fff;margin:0 0 .4rem}.cta p{color:#cfe0d6;margin:0 0 1rem}.cta a{display:inline-block;padding:.75rem 1.2rem;border-radius:999px;background:var(--lime);color:#07150f;font-weight:700;text-decoration:none}
footer{padding-block:2rem 3rem;font-size:.82rem;color:var(--muted)}
@media (width<=640px){.calc .in{grid-template-columns:1fr}header.top nav a.hide-s{display:none}}
'''
open(os.path.join(out, 'guides.css'), 'w').write(CSS)
GUIDES = [("automated-parking-cost","What automated parking costs"),("automated-parking-vs-agv","Automated parking vs AGV and shuttle systems"),
          ("automated-parking-reliability","Reliability: what happens when a machine stops"),("automated-parking-retrieval-time","Retrieval time and throughput"),("ev-charging","EV charging in an automated garage")]
def page(slug, title, desc, h1, lead, short, body, faqs, img=None, cap=None, script=''):
    faq_html = ''.join('<details><summary>%s</summary><div><p>%s</p></div></details>' % (q, a) for q, a in faqs)
    rel = ''.join('<li><a href="%s.html">%s</a></li>' % (s_, t) for s_, t in GUIDES if s_ != slug)
    ld = {"@context":"https://schema.org","@graph":[ORG,
          {"@type":"WebPage","@id":BASE+slug+"#page","url":BASE+slug,"name":title,"description":desc,"inLanguage":"en","isPartOf":{"@type":"WebSite","url":BASE,"name":"Parkstory"},"publisher":{"@id":BASE+"#org"},"about":{"@type":"Product","name":"TilePark","brand":"Parkstory"}},
          {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Parkstory","item":BASE},{"@type":"ListItem","position":2,"name":h1,"item":BASE+slug}]},
          {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":H.unescape(__import__('re').sub('<[^>]+>','',a))}} for q, a in faqs]}]}
    fig = '<figure><img src="%s" alt="%s" width="960" height="540" loading="lazy"><figcaption>%s</figcaption></figure>' % (img, cap, cap) if img else ''
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title><meta name="claude:viewport-fit-sides" content="cover"><meta name="description" content="{H.escape(desc)}"><link rel="canonical" href="{BASE+slug}">
<meta property="og:type" content="article"><meta property="og:title" content="{H.escape(title)}"><meta property="og:description" content="{H.escape(desc)}"><meta property="og:url" content="{BASE+slug}"><meta property="og:site_name" content="Parkstory">
<link rel="stylesheet" href="guides.css"><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body>
<header class="top"><div class="w"><a class="brand" href="index.html"><i aria-hidden="true"></i>Parkstory</a><nav><a href="index.html#faq" class="hide-s">FAQ</a><a href="index.html#red-to-green" class="hide-s">Case study</a><a href="index.html#request">Free feasibility study</a></nav></div></header>
<main class="w"><p class="crumb"><a href="index.html">Parkstory</a> › Guides</p><h1>{h1}</h1><p class="lead">{lead}</p>
<div class="short"><b>Short answer</b><p>{short}</p></div>{fig}{body}
<h2>Questions on this topic</h2>{faq_html}
<div class="cta"><h2>Get the figures for your site</h2><p>Send us your site or floor plan. Our engineers lay out TilePark on your site free of charge.</p><a href="index.html#request">Request a free feasibility study →</a></div>
<nav class="related" aria-label="More guides"><b>More guides</b><ul>{rel}</ul></nav></main>
<footer class="w">Parkstory GmbH, Munich · Parkstory, Inc., Gastonia, North Carolina · Parkstory Manufacturing GmbH, Kehl · Parkstory Kft., Budapest · info@parkstory.com</footer>{script}</body></html>'''
    open(os.path.join(out, slug + '.html'), 'w').write(doc)

# ---------------- cost ----------------
page('automated-parking-cost', 'What Automated Parking Costs | TilePark by Parkstory',
 'What a TilePark automated parking system costs per space, what drives the price, what to compare between offers, and how to compare total parking cost with a conventional garage.',
 'What does automated parking cost?',
 'The price per space is only half of the comparison. Automated parking also changes how much of your building earns money, so compare the result for the whole project.',
 'Most TilePark systems from 25 spaces cost around $30,000 per space, and the larger the system, the lower the cost per space. Your offer states exactly what is included. The free feasibility study gives the figure for your site.',
 '''<h2>What the price per space depends on</h2><ul>
<li><b>Number of spaces.</b> Elements such as transfer cabins and controls are shared by more spaces in a larger system.</li>
<li><b>Vertical movement.</b> Car elevators between levels (TilePark), stackers above the conveyor grid (TilePark Automated Stackers) or a central lift (TilePark Tower).</li>
<li><b>Number of transfer cabins.</b> More cabins handle more cars at peak times.</li>
<li><b>Site geometry.</b> Column grid, clear height and the shape of the plot decide how the grid is laid out.</li>
<li><b>EV charging.</b> How many cars charge, and the electrical capacity available on site.</li>
<li><b>Service.</b> The scope and term of the service contract.</li></ul>
<h2>What to compare between offers</h2><p>Ask every supplier to state what the price includes, so that offers can be compared line by line:</p><ul>
<li>Conveyors, lifts or stackers, and transfer cabins</li><li>Controls, software, the operator platform and the app</li><li>Installation and commissioning</li><li>EV charging hardware and load management</li><li>Service contract, response times and spare-parts availability</li></ul>
<p>Building works such as the structure, fire protection, ventilation and the electrical supply belong in the comparison too, whoever provides them.</p>
<h2>From parking area to value: three steps</h2><ol>
<li><b>Recovered parking area.</b> What TilePark frees compared with ramps and drive aisles: more than 150 sq ft per space on our calculator.</li>
<li><b>Permitted building area.</b> How much of it zoning lets you build and use. This can be all of it, part of it or none, depending on the site.</li>
<li><b>Realizable value.</b> What the market pays for that area, sold or rented, after fit-out costs.</li></ol>
<p>The case study on our website follows these three steps for an example building that moves from a loss of $1.0 million to a profit of $1.3 million. Its calculator lets you enter your own figures.</p>
<h2>Compare total parking cost</h2><p>Enter the cost per space of the garage you would otherwise build and of the TilePark offer. The tool adds the value of the area you can build on and shows the net effect. All values are examples until you enter yours.</p>
<form class="calc" id="cc" novalidate><div class="in">
<label for="cN">Parking spaces<input id="cN" type="number" min="1" value="68"></label>
<label for="cG">Conventional garage, cost per space ($)<input id="cG" type="number" min="0" step="500" value="30000"></label>
<label for="cT">TilePark, cost per space ($)<input id="cT" type="number" min="0" step="500" value="30000"></label>
<label for="cS">Share of the recovered area you can build and use (%)<input id="cS" type="number" min="0" max="100" step="5" value="100"></label>
<label for="cV">Value of the built area per sq ft ($)<input id="cV" type="number" min="0" step="10" value="400"></label>
<label for="cF">Fit-out cost per sq ft ($)<input id="cF" type="number" min="0" step="5" value="175"></label></div>
<div class="res" aria-live="polite"><div><span>Conventional garage</span><b id="oG"></b></div><div><span>TilePark</span><b id="oT"></b></div><div><span>Difference in parking cost</span><b id="oD"></b></div>
<div><span>Recovered area (150 sq ft per space)</span><b id="oA"></b></div><div><span>Area you can build and use</span><b id="oB"></b></div><div><span>Value after fit-out</span><b id="oV"></b></div><div class="big"><span>Net effect of TilePark</span><b id="oN"></b></div></div>
<p class="note">Assumptions: 150 sq ft recovered per space, as in our gain calculator. The default cost per space is the same for both systems because most TilePark systems from 25 spaces cost around $30,000 per space, about what a conventional garage costs; replace both with your quotes. Land and the rest of the building are the same in both cases and left out.</p></form>''',
 [("Is TilePark more expensive than a conventional garage?","Per space, most TilePark systems cost about as much as a conventional garage. The difference lies in what you gain: without ramps and drive aisles, floor area becomes available that you can build, sell or rent, where zoning permits."),
  ("Does the price include the building?","The building structure is part of the building budget. Your offer states exactly what TilePark supplies and what the building provides."),
  ("Why is the cost per space lower in larger systems?","Shared elements such as transfer cabins, lifts and controls are spread over more spaces."),
  ("How do I get a price for my site?","Send us your site or floor plan. The free feasibility study shows capacity, layout and a price for your site.")],
 'guide-c5.jpg','3D illustration: the two floors freed by TilePark become apartments',
 '''<script>(()=>{const $=i=>document.getElementById(i),f=new Intl.NumberFormat('en-US',{maximumFractionDigits:0}),m=v=>(v<0?'−':'')+'$'+f.format(Math.abs(Math.round(v)));
function r(){const n=+$('cN').value||0,g=+$('cG').value||0,t=+$('cT').value||0,s=Math.min(100,+$('cS').value||0)/100,v=+$('cV').value||0,fo=+$('cF').value||0;
const G=n*g,Tt=n*t,d=Tt-G,A=n*150,B=A*s,V=B*(v-fo),N=V-d;$('oG').textContent=m(G);$('oT').textContent=m(Tt);$('oD').textContent=(d>0?'+':'')+m(d);
$('oA').textContent=f.format(A)+' sq ft';$('oB').textContent=f.format(B)+' sq ft';$('oV').textContent=m(V);$('oN').textContent=(N>0?'+':'')+m(N);$('oN').className=N<0?'neg':'pos'}
$('cc').addEventListener('input',r);$('cc').addEventListener('submit',e=>e.preventDefault());r()})()</script>''')

# ---------------- vs AGV ----------------
page('automated-parking-vs-agv', 'Automated Parking Compared: TilePark vs AGV, Shuttle and Tower Systems',
 'How the TilePark XY conveyor grid compares with AGV robots, rail-guided shuttles, tower systems and conventional garages: floor used for movement, what a stopped machine affects, and layout flexibility.',
 'Automated parking compared: TilePark, AGV robots, shuttles and tower systems',
 'Automated parking systems differ most in how cars move across a floor and between floors. That decides how much floor is parking and what happens when one machine stops.',
 'AGV robots and rail-guided shuttles need drive aisles or rails, and tower systems move every car through a central lift. The TilePark XY grid needs neither aisles nor rails: every position is a conveyor, so the whole floor is parking, and cars are routed around a stopped conveyor. Between levels, every automated system relies on lifts, stackers or a central lift, so their number and redundancy decide how a failure affects the garage.',
 '''<h2>The architectures side by side</h2><div class="tw"><table><thead><tr><th>System</th><th>How cars move</th><th>Floor used for movement</th><th>When one machine stops</th><th>Layout</th></tr></thead><tbody>
<tr><td>Conventional garage</td><td>Drivers drive and walk</td><td>Ramps and drive aisles, about half of each parking floor</td><td>Not applicable</td><td>Fixed by ramps</td></tr>
<tr><td>AGV robots</td><td>Robots carry cars along drive aisles</td><td>At least one drive aisle</td><td>A stopped robot can block the shared aisle</td><td>Fixed by the aisles</td></tr>
<tr><td>Rail-guided shuttles</td><td>Shuttles on rails, lifts between levels</td><td>Rails, aisles and lifts</td><td>A shuttle or lift failure can block an aisle or a level</td><td>Fixed by the rails</td></tr>
<tr><td>Tower systems</td><td>A central lift serves shelves around it</td><td>The central lift shaft</td><td>A lift failure stops every car it serves</td><td>Fixed by the tower</td></tr>
<tr class="tp"><td>TilePark</td><td>Conveyors move cars in X and Y; car elevators between levels</td><td>No drive aisles or rails</td><td>Cars are routed around a stopped conveyor; a stopped elevator affects the levels it serves</td><td>Follows the site and the column grid</td></tr>
<tr class="tp"><td>TilePark Automated Stackers</td><td>Conveyor grid on one level, a stacker above each selected conveyor</td><td>No drive aisles or rails</td><td>A stopped stacker affects only the cars it holds</td><td>Follows the site; uses clear height</td></tr>
<tr class="tp"><td>TilePark Tower</td><td>A central lift; TilePark conveyors on every level</td><td>The central lift shaft</td><td>A stopped central lift pauses retrieval until it is repaired; on each level, conveyors route around a stopped one</td><td>From 2 to 24 cars per level, up to 13 levels</td></tr>
</tbody></table></div>
<p class="note">General descriptions of system types, not of individual products. Every project differs, which is why we compare layouts on your actual site.</p>
<h2>Floor area</h2><p>Because TilePark needs no drive aisles or rails, more of each floor is parking. How many more spaces fit than with an aisle-based system depends on the site; Parkstory layout studies on identical footprints are the basis, and your free feasibility study shows the figure for your site.</p>
<h2>Questions to ask every supplier</h2><ul>
<li>If one machine stops, which cars can still be retrieved, and which wait for the repair?</li>
<li>Which machines does every car pass through: lifts, shuttles, robots or transfer cabins? How many of each are there?</li>
<li>How much floor is used for aisles, rails or lifts?</li>
<li>Who builds the machines, and who will service them in 20 years? For how long are spare parts guaranteed?</li>
<li>Will the supplier commit to retrieval times, throughput and availability in the contract?</li>
<li>Can the layout follow your columns and the shape of your site?</li></ul>''',
 [("Is TilePark an AGV system?","No. AGV robots drive under cars and carry them along aisles. In TilePark the floor itself moves the cars: each position is a conveyor that passes the pallet with the car to the next position."),
  ("Does TilePark need lifts?","To move between levels, yes: car elevators in TilePark, stackers in TilePark Automated Stackers and a central lift in TilePark Tower. On each level, cars move on conveyors only."),
  ("Which system fits the most cars on a footprint?","That depends on the site. Systems that need no drive aisles or rails use more of each floor for parking; your feasibility study compares the layouts for your site.")],
 'guide-c2.jpg','3D illustration: orange marks the floor area of a conventional garage that only serves driving')

# ---------------- reliability ----------------
page('automated-parking-reliability', 'Automated Parking Reliability: What Happens When a Machine Stops | TilePark',
 'Which failures the TilePark conveyor grid routes around, which elements are shared by many cars, and how measured results, design targets and contractual guarantees differ.',
 'What happens when a machine in an automated garage stops?',
 'Reliability depends on which machines every car passes through. In TilePark the horizontal movement is distributed across many conveyors; the elements shared by many cars are planned and agreed per project.',
 'In the TilePark grid, every conveyor has its own controller and at least four drive motors, and cars are routed around a stopped conveyor. Only a car standing on that conveyor waits for the repair. Lifts, stackers, transfer cabins, the power supply and the control network are shared by the cars they serve, so their number, redundancy and the service response are planned and agreed for each project.',
 '''<h2>What a failure affects</h2><div class="tw"><table><thead><tr><th>Element</th><th>What a stop affects</th><th>How it is handled</th></tr></thead><tbody>
<tr><td>One conveyor</td><td>The car standing on it</td><td>The other conveyors route cars around it; the car on it waits for the repair</td></tr>
<tr><td>Car elevator (TilePark)</td><td>Cars on the levels it serves</td><td>Number of elevators and their redundancy are part of the design</td></tr>
<tr><td>Stacker (TilePark Automated Stackers)</td><td>Only the cars it holds</td><td>The rest of the garage keeps running</td></tr>
<tr><td>Central lift (TilePark Tower)</td><td>Retrieval from the upper levels</td><td>Service response and availability are agreed in the contract</td></tr>
<tr><td>Transfer cabin</td><td>Drop-off and pickup at that cabin</td><td>With several cabins, drivers use another one</td></tr>
<tr><td>Power supply and control network</td><td>The whole system</td><td>Shared by every automated garage; the power concept, including retrieval during an outage, is agreed per project</td></tr>
</tbody></table></div>
<h2>Measured, targeted, guaranteed</h2><p>Three kinds of figures are easy to confuse, so we keep them apart:</p><ul>
<li><b>Measured:</b> results from systems in operation, with the measurement period, the sample and the definitions. We publish these once they are documented: <span class="tbp">to be published</span>.</li>
<li><b>Design targets:</b> what we build to, such as 99.5 % availability and the goal of solving 99 % of faults remotely.</li>
<li><b>Contractual guarantees:</b> values agreed for your project and written into the contract, such as availability, retrieval time and service response time.</li></ul>
<h2>How the system is built to keep running</h2><ul>
<li>Every conveyor runs under load on our test rig before it ships, and every component carries a serial number.</li>
<li>Proven industrial components inside our own design, robust and widely available.</li>
<li>24/7 service, remote diagnostics, a technician on site when needed, and spare parts for at least 30 years.</li></ul>''',
 [("Can every car still be retrieved if a conveyor stops?","On the grid, yes: the other conveyors route cars around a stopped one. Only a car standing on the stopped conveyor itself waits for the repair."),
  ("What happens during a power failure?","The power concept, including how cars are retrieved during an outage, is part of the design we agree with you for your building."),
  ("Does TilePark have a single point of failure?","Horizontal movement does not depend on a single machine. Shared elements, such as lifts, transfer cabins, the power supply and, in TilePark Tower, the central lift, are planned with the redundancy and service response agreed for your project."),
  ("Who services the system?","Our own team: 24/7 service, remote diagnostics, a technician on site when needed, and spare parts for at least 30 years.")])

# ---------------- retrieval time ----------------
page('automated-parking-retrieval-time', 'Retrieval Time and Throughput in Automated Parking | TilePark',
 'What determines how long it takes to get a car back from an automated garage, how retrieval time differs from peak-hour throughput, and how both are specified in a TilePark contract.',
 'How long does it take to get your car back?',
 'Two figures matter: how long one driver waits, and how many cars the system delivers per hour at the busiest time of day.',
 'It depends on the size and layout of the system, the number of free positions, lifts or stackers and transfer cabins, and how many drivers want their car at the same time. We define the retrieval time and the peak-hour throughput with you for your project and write them into the contract. With the app, drivers can call their car ahead so it is waiting when they arrive.',
 '''<h2>What determines retrieval time</h2><ul>
<li><b>Distance on the grid.</b> How far the car travels in X and Y to the cabin or lift.</li>
<li><b>Free positions.</b> A few free positions let the grid move cars aside; how many a layout needs depends on its size, its shape and the required retrieval times.</li>
<li><b>Vertical movement.</b> The number and speed of car elevators, stackers or the central lift.</li>
<li><b>Transfer cabins.</b> More cabins serve more drivers at the same time.</li>
<li><b>Peak demand.</b> How many drivers leave in the same hour, for example in the morning rush.</li>
<li><b>Calling ahead.</b> A request from the app starts the retrieval before the driver arrives.</li></ul>
<h2>Retrieval time and throughput are different</h2><p><b>Retrieval time</b> is the time from a request until the car is ready in the transfer cabin. <b>Throughput</b> is the number of cars the system delivers per hour at peak. A system can be quick for one car and still be too slow in the rush hour, so both belong in the specification, as a typical and a maximum value.</p>
<h2>How we specify them</h2><p>In the feasibility study we lay out the grid, lifts or stackers and transfer cabins for your site and show how fast the system delivers cars. The agreed values go into the contract.</p>
<p>Measured retrieval-time distributions from systems in operation: <span class="tbp">to be published</span> with the measurement period and sample.</p>''',
 [("Is retrieval slower at peak times?","Peak demand is what the system is designed for: the number of lifts and transfer cabins is chosen so that the agreed peak-hour throughput is met."),
  ("Can drivers call their car in advance?","Yes. Drivers tell the app they are leaving, and the car is moved to the transfer cabin so it is waiting when they arrive."),
  ("What retrieval time can we put in the contract?","That depends on your layout and peak demand. We define typical and maximum retrieval times and the peak-hour throughput with you, and write them into the contract.")])

# ---------------- EV charging ----------------
page('ev-charging', 'EV Charging in an Automated Garage | TilePark by Parkstory',
 'How TilePark charges electric cars: EV-ready pallets, charging points that are never blocked by a full car, metering in the app, load management and what is defined per project.',
 'EV charging in an automated garage',
 'In a conventional garage, a fully charged car blocks the charger until its driver returns. An automated garage can move the car away.',
 'Every TilePark pallet is EV-ready: drivers plug their own cable into the socket on the pallet and start charging from the app. TilePark moves the car to a charging point, charges it to the level requested and then moves it away, so the next car can charge. Fewer charging points serve more cars, charging power is managed across the whole system, and capacity can grow with demand.',
 '''<h2>How it works</h2><ol>
<li>The driver parks in the transfer cabin, plugs the cable into the socket on the pallet and chooses the charge level in the app.</li>
<li>The system moves the car to a charging point and charges it.</li>
<li>When the car reaches the requested level, it is moved away and the charging point is free for the next car.</li>
<li>Charging is metered live in the app and paid in the same app; automated re-parking means no idle fees.</li></ol>
<h2>Why fewer charging points serve more cars</h2><p>A fixed charging bay is blocked by a full car until its driver returns. Because TilePark moves charged cars away, its charging points stay in use through the night. The overnight simulation on our website shows the effect for one charging point over a working day.</p>
<h2>What is defined for each project</h2><ul>
<li>Number of charging points and the charging power per point</li><li>Connector type for the market</li><li>Connection to the building’s electrical supply and the load-management limits</li><li>Metering, billing and the operator’s pricing</li><li>Room to add capacity later as demand grows</li></ul>''',
 [("Do drivers need their own cable?","Yes. Drivers plug their own cable into the socket on the pallet."),
  ("How many charging points do we need?","That depends on how many EVs park in the building and how much they need to charge. The feasibility study sizes the charging points and the electrical connection for your project."),
  ("Can charging capacity grow later?","Yes. Charging capacity can grow with demand without rebuilding the garage.")],
 'guide-c1.jpg','3D illustration of an example building with an automated garage')
print('guides written')
