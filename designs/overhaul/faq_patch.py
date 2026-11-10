# Moves the FAQ into its own menu part "FAQ" (before Plan your TilePark), grouped by topic.
# python faq_patch.py <in.html> <out.html>
import sys, re, json
src, out = sys.argv[1:3]
s = open(src).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:90], s.count(a)); s = s.replace(a, b)
def cut_section(marker):
    global s
    i = s.find(marker); assert i >= 0, marker; d = 0
    for m in re.compile(r'<section[\s>]|</section>').finditer(s, i):
        d += -1 if m.group(0).startswith('</') else 1
        if d == 0:
            blk = s[i:m.end()]; s = s[:i] + s[m.end():]; return blk
old = cut_section('<section class="ov ov-faq" id="faq">')
QA = dict(re.findall(r'<details class="ov-q"><summary>(.*?)</summary><div><p>(.*?)</p></div></details>', old))
assert len(QA) == 12, len(QA)
NEWQ = [
 ("How do drivers park and pick up their car?","They drive into the bright transfer cabin, step out and confirm at the touchscreen or in the app. To pick it up, they tell the app they’re leaving, and the car is waiting in the transfer cabin when they get there.",
  ["Wie parken Nutzer ein und holen ihr Fahrzeug ab?","Sie fahren in die helle Übergabekabine, steigen aus und bestätigen am Touchscreen oder in der App. Zum Abholen sagen sie der App, dass sie losfahren – das Fahrzeug wartet in der Übergabekabine, wenn sie ankommen."],
  ["Comment les conducteurs garent-ils et récupèrent-ils leur voiture ?","Ils entrent dans la cabine de transfert lumineuse, descendent et confirment sur l’écran tactile ou dans l’application. Pour la récupérer, ils indiquent à l’application qu’ils partent : la voiture les attend dans la cabine de transfert à leur arrivée."],
  ["¿Cómo aparcan y recogen los conductores su coche?","Entran en la cabina de transferencia luminosa, se bajan y confirman en la pantalla táctil o en la app. Para recogerlo, avisan a la app de que se van y el coche les espera en la cabina de transferencia cuando llegan."]),
 ("Can guests and family members use it?","Yes. Residents invite friends and guests with a tap in the app.",
  ["Können Gäste und Familienmitglieder die Anlage nutzen?","Ja. Bewohner laden Freunde und Gäste mit einem Fingertipp in der App ein."],
  ["Les invités et les membres de la famille peuvent-ils l’utiliser ?","Oui. Les résidents invitent amis et visiteurs d’un simple geste dans l’application."],
  ["¿Pueden usarlo invitados y familiares?","Sí. Los residentes invitan a amigos y visitas con un toque en la app."]),
 ("Who handles permits and approvals?","Your architect and engineers lead the approval process. We support them with layouts, BIM models and the technical information the authorities ask for, including for fire protection.",
  ["Wer kümmert sich um die Genehmigungen?","Ihr Architekt und Ihre Fachplaner führen das Genehmigungsverfahren. Wir unterstützen sie mit Layouts, BIM-Modellen und den technischen Angaben, die die Behörden verlangen – auch zum Brandschutz."],
  ["Qui s’occupe des permis et autorisations ?","Votre architecte et vos bureaux d’études pilotent les démarches d’autorisation. Nous les accompagnons avec des implantations, des modèles BIM et les informations techniques demandées par les autorités, y compris pour la protection incendie."],
  ["¿Quién se ocupa de los permisos?","Su arquitecto y sus ingenieros dirigen la tramitación. Les apoyamos con distribuciones, modelos BIM y la información técnica que piden las autoridades, también para la protección contra incendios."]),
 ("How much space do we gain?","Without ramps and drive aisles, more than 150 sq ft per space goes back to the building. Compared with automated systems that need drive aisles, TilePark fits at least 20 % more spaces on the same footprint, based on our layout studies.",
  ["Wie viel Fläche gewinnen wir?","Ohne Rampen und Fahrgassen gehen mehr als 150 sq ft pro Stellplatz an das Gebäude zurück. Im Vergleich zu automatischen Systemen mit Fahrgassen bringt TilePark auf derselben Grundfläche mindestens 20 % mehr Stellplätze unter – auf Basis unserer Layoutstudien."],
  ["Combien d’espace gagnons-nous ?","Sans rampes ni allées, plus de 150 sq ft par place reviennent au bâtiment. Par rapport aux systèmes automatisés avec allées, TilePark loge au moins 20 % de places en plus sur la même emprise, selon nos études d’implantation."],
  ["¿Cuánto espacio ganamos?","Sin rampas ni pasillos, más de 150 sq ft por plaza vuelven al edificio. Frente a los sistemas automatizados con pasillos, TilePark aloja al menos un 20 % más de plazas en la misma superficie, según nuestros estudios de distribución."]),
 ("Can we sell or rent the space we gain?","Both, where zoning permits the extra floor area. The calculator in the case study shows the result for your project, for sellable or rentable area.",
  ["Können wir die gewonnene Fläche verkaufen oder vermieten?","Beides, sofern der Bebauungsplan die zusätzliche Fläche zulässt. Der Rechner in der Fallstudie zeigt das Ergebnis für Ihr Projekt – für verkaufbare oder vermietbare Fläche."],
  ["Peut-on vendre ou louer l’espace gagné ?","Les deux, si l’urbanisme autorise la surface supplémentaire. Le calculateur de l’étude de cas montre le résultat pour votre projet, en surface vendable ou locative."],
  ["¿Podemos vender o alquilar el espacio ganado?","Ambas cosas, si el planeamiento permite la superficie adicional. La calculadora del caso práctico muestra el resultado para su proyecto, con superficie vendible o alquilable."]),
 ("What do banks and investors look at?","A predictable cost per space, more revenue from the same plot and a risk they can assess: our own plants, every conveyor load-tested, operating risk spread across the grid, and service for the life of the financing.",
  ["Worauf achten Banken und Investoren?","Kalkulierbare Kosten pro Stellplatz, mehr Ertrag aus demselben Grundstück und ein Risiko, das sich bewerten lässt: eigene Werke, jedes Fördermodul unter Last geprüft, das Betriebsrisiko auf das Raster verteilt und Service über die gesamte Finanzierungslaufzeit."],
  ["Qu’examinent les banques et les investisseurs ?","Un coût par place prévisible, plus de revenus sur la même parcelle et un risque mesurable : nos propres usines, chaque convoyeur testé en charge, un risque d’exploitation réparti sur la grille et un service pendant toute la durée du financement."],
  ["¿Qué miran los bancos y los inversores?","Un coste por plaza previsible, más ingresos del mismo solar y un riesgo evaluable: plantas propias, cada transportador probado con carga, el riesgo operativo repartido en la cuadrícula y servicio durante toda la financiación."]),
 ("Where is TilePark made?","In our own plants: in Kehl, Germany, for Europe and in Gastonia, North Carolina, for North America.",
  ["Wo wird TilePark gefertigt?","In unseren eigenen Werken: in Kehl für Europa und in Gastonia, North Carolina, für Nordamerika."],
  ["Où TilePark est-il fabriqué ?","Dans nos propres usines : à Kehl, en Allemagne, pour l’Europe, et à Gastonia, en Caroline du Nord, pour l’Amérique du Nord."],
  ["¿Dónde se fabrica TilePark?","En nuestras propias plantas: en Kehl (Alemania) para Europa y en Gastonia (Carolina del Norte) para Norteamérica."]),
]
for q, a, *_ in NEWQ: QA[q] = a
QA["Is the core technology protected?"] = "Yes: a granted core patent on the X-Y conveyor technology (EP 3924576 B1), and three further applications filed in the USA."
CATS = [
 ('faq-drivers','For drivers',["How do drivers park and pick up their car?","How long does it take to get my car?","Can guests and family members use it?","Can every space charge an electric car?","Which cars fit?"]),
 ('faq-tech','Technology and reliability',["What happens if a machine breaks down?","What happens during a power failure?","How is TilePark different from other automated systems?","Is the core technology protected?"]),
 ('faq-safety','Safety and approvals',["Is it safe? Who goes into the garage?","How is fire protection handled?","Who handles permits and approvals?"]),
 ('faq-cost','Cost and value',["What does it cost?","How much space do we gain?","Can we sell or rent the space we gain?","What do banks and investors look at?"]),
 ('faq-project','Project and service',["How do we start?","Who are we buying from?","Where is TilePark made?","How long will the system last, and who services it?"]),
]
used = [q for _,_,qs in CATS for q in qs]; assert len(used) == len(set(used)) == 20 and all(q in QA for q in used), [q for q in used if q not in QA]
nav = ''.join('<a href="#%s">%s</a>' % (cid, name) for cid, name, _ in CATS)
blocks = ''.join('<div class="faq-cat" id="%s"><h3>%s</h3><div class="ov-qa">%s</div></div>' % (cid, name, ''.join('<details class="ov-q"><summary>%s</summary><div><p>%s</p></div></details>' % (q, QA[q]) for q in qs)) for cid, name, qs in CATS)
FAQ = ('<span id="part-faq" class="part-anchor"></span><section class="ov ov-faq" id="faq"><div class="wrap"><p class="hiw-eyebrow">FAQ</p><h2 class="ov-h">Straight answers <em>before you decide.</em></h2>'
       '<p class="ov-lead">The questions buyers ask most, sorted by topic.</p><nav class="faq-nav" aria-label="FAQ topics">' + nav + '</nav>' + blocks +
       '<div class="ov-ctas"><a class="ov-btn" href="#supplier-questions">More answers for experts →</a><a class="ov-btn ov-btn2" href="#request">Request a free feasibility study →</a></div></div></section>')
rep('<div class="plx" id="part-plan">', FAQ + '<div class="plx" id="part-plan">')
# ---- menu ----
rep(re.search(r'<li><a href="#faq"><span class="t">[^<]*</span></a></li>', s).group(0), '')
rep('The essentials in five minutes, and straight answers to the questions every buyer asks.</span>', 'The essentials in five minutes: how TilePark works, what it costs and how a project runs.</span>')
lis = ''.join('<li><a href="#%s"><span class="t">%s</span></a></li>' % (cid, name) for cid, name, _ in CATS)
SEC = ('<div class="hr-sec" data-part="part-faq"><a class="hr-pa" href="#part-faq" data-part="part-faq" aria-expanded="false"><span class="pn">7</span><span class="pt">FAQ</span><span class="go" aria-hidden="true">›</span>'
       '<span class="pd">Straight answers to the questions buyers ask, by topic.</span><span class="pp" aria-hidden="true"></span></a><ol class="hr-ch">' + lis + '</ol></div>')
rep('<div class="hr-sec" data-part="part-plan">', SEC + '<div class="hr-sec" data-part="part-plan">')
rep('data-part="part-plan" aria-expanded="false"><span class="pn">7</span>', 'data-part="part-plan" aria-expanded="false"><span class="pn">8</span>')
k = s.find('const FXN='); e = s.find(';\nconst vis=', k); names = json.loads(s[k+len('const FXN='):e])
names['p']['part-faq'] = 'FAQ'; names['c'].pop('faq', None)
for cid, name, _ in CATS: names['c'][cid] = name
s = s[:k] + 'const FXN=' + json.dumps(names, ensure_ascii=False) + s[e:]
CSS = '''<style id="faq-css">
.faq-nav{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 2rem}
.faq-nav a{padding:.5rem .95rem;border-radius:999px;border:1px solid var(--line-soft);background:var(--bg);color:var(--ink);text-decoration:none;font-weight:600;font-size:.9rem}
.faq-nav a:hover{border-color:var(--green)}
.faq-cat{margin:0 0 2.2rem;scroll-margin-top:80px}.faq-cat h3{margin:0 0 .8rem;font:700 clamp(1.15rem,1.8vw,1.4rem)/1.2 "Outfit","Inter",sans-serif;color:var(--ink)}
</style>'''
rep('</head>', CSS + '</head>')
T = {"FAQ":["Häufige Fragen","Questions fréquentes","Preguntas frecuentes"],
 "The questions buyers ask most, sorted by topic.":["Die häufigsten Fragen von Käufern, nach Themen sortiert.","Les questions les plus fréquentes des acheteurs, classées par thème.","Las preguntas más frecuentes de los compradores, ordenadas por temas."],
 "Straight answers to the questions buyers ask, by topic.":["Klare Antworten auf die Fragen, die Käufer stellen – nach Themen sortiert.","Des réponses claires aux questions des acheteurs, classées par thème.","Respuestas claras a las preguntas de los compradores, ordenadas por temas."],
 "The essentials in five minutes: how TilePark works, what it costs and how a project runs.":["Das Wichtigste in fünf Minuten: wie TilePark funktioniert, was es kostet und wie ein Projekt abläuft.","L’essentiel en cinq minutes : comment fonctionne TilePark, ce qu’il coûte et comment se déroule un projet.","Lo esencial en cinco minutos: cómo funciona TilePark, cuánto cuesta y cómo se desarrolla un proyecto."],
 "Technology and reliability":["Technik und Zuverlässigkeit","Technologie et fiabilité","Tecnología y fiabilidad"],
 "Safety and approvals":["Sicherheit und Genehmigung","Sécurité et autorisations","Seguridad y permisos"],
 "Cost and value":["Kosten und Wert","Coûts et valeur","Costes y valor"],
 "Project and service":["Projekt und Service","Projet et service","Proyecto y servicio"]}
for q, a, de, fr, es in NEWQ:
    T[q] = [de[0], fr[0], es[0]]; T[a] = [de[1], fr[1], es[1]]
rep('var D={', 'var D=' + json.dumps(T, ensure_ascii=False)[:-1] + ', ')
open(out, 'w').write(s); print('ok', len(T), 'strings')
