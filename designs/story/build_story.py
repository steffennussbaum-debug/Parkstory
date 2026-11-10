import json, base64, sys, os
S = sys.argv[1]
def b64(p, mime): return 'data:%s;base64,%s' % (mime, base64.b64encode(open(p,'rb').read()).decode())
L = {}
def add(k, en, de, fr, es):
    for lg, v in zip(('en','de','fr','es'), (en, de, fr, es)): L.setdefault(lg, {})[k] = v
add('eye','A project story · fictional example','Eine Projektgeschichte · fiktives Beispiel','Une histoire de projet · exemple fictif','Una historia de proyecto · ejemplo ficticio')
add('h1a','The project that didn’t add up.','Das Projekt, das sich nicht rechnete.','Le projet qui n’était pas rentable.','El proyecto que no salía a cuenta.')
add('h1b','Until parking changed.','Bis sich das Parken änderte.','Jusqu’à ce que le stationnement change.','Hasta que cambió el aparcamiento.')
add('lead','A developer, a tight city plot and a parking requirement that takes half the building. This is how the same building goes from a loss to a profit, with nothing changed but the parking.',
 'Ein Projektentwickler, ein enges Grundstück in der Stadt und eine Stellplatzpflicht, die das halbe Gebäude belegt. So wird aus demselben Gebäude ein rentables Projekt – geändert hat sich nur das Parken.',
 'Un promoteur, une parcelle urbaine étroite et une obligation de stationnement qui occupe la moitié du bâtiment. Voici comment le même bâtiment passe de la perte au bénéfice, sans rien changer d’autre que le stationnement.',
 'Un promotor, un solar urbano estrecho y una exigencia de aparcamiento que ocupa medio edificio. Así pasa el mismo edificio de las pérdidas a los beneficios, sin cambiar nada más que el aparcamiento.')
add('hint','Scroll down and follow the numbers','Scrollen Sie und verfolgen Sie die Zahlen','Faites défiler et suivez les chiffres','Desplácese y siga las cifras')
add('k1','1 · The site','1 · Das Grundstück','1 · La parcelle','1 · El solar')
add('h_1','A corner plot with a lot of potential.','Ein Eckgrundstück mit viel Potenzial.','Une parcelle d’angle pleine de potentiel.','Un solar en esquina con mucho potencial.')
add('p1','The plan: a building with a lobby on the ground floor and eight floors above it. The zoning sets the height and requires 68 parking spaces on site.',
 'Der Plan: ein Gebäude mit Lobby im Erdgeschoss und acht Geschossen darüber. Der Bebauungsplan begrenzt die Höhe und verlangt 68 Stellplätze auf dem Grundstück.',
 'Le projet : un bâtiment avec un hall au rez-de-chaussée et huit étages au-dessus. Le plan d’urbanisme fixe la hauteur et impose 68 places de stationnement sur la parcelle.',
 'El plan: un edificio con vestíbulo en planta baja y ocho plantas encima. El planeamiento fija la altura y exige 68 plazas de aparcamiento en el solar.')
add('cap1','Illustration of the example building with a conventional garage','Illustration des Beispielgebäudes mit konventioneller Garage','Illustration du bâtiment exemple avec un parking classique','Ilustración del edificio de ejemplo con un aparcamiento convencional')
add('k2','2 · The parking problem','2 · Das Parkproblem','2 · Le problème du stationnement','2 · El problema del aparcamiento')
add('h_2','Parking takes half the building.','Das Parken belegt das halbe Gebäude.','Le stationnement occupe la moitié du bâtiment.','El aparcamiento ocupa medio edificio.')
add('p2','A conventional garage needs ramps and drive aisles, and they take about half of every parking floor. To fit 68 cars, the garage needs four of the eight upper floors. Only four floors are left for apartments.',
 'Eine konventionelle Garage braucht Rampen und Fahrgassen – und die belegen rund die Hälfte jeder Parkebene. Für 68 Fahrzeuge braucht die Garage vier der acht Obergeschosse. Für Wohnungen bleiben nur vier.',
 'Un parking classique a besoin de rampes et d’allées de circulation, qui occupent environ la moitié de chaque niveau. Pour 68 voitures, il lui faut quatre des huit étages. Il n’en reste que quatre pour les logements.',
 'Un aparcamiento convencional necesita rampas y pasillos de circulación, que ocupan cerca de la mitad de cada planta. Para 68 coches hacen falta cuatro de las ocho plantas superiores. Para viviendas solo quedan cuatro.')
add('cap2','Orange: floor area that only serves driving','Orange: Fläche, die nur dem Fahren dient','En orange : la surface qui ne sert qu’à circuler','En naranja: superficie que solo sirve para circular')
add('k3','3 · In the red','3 · Rote Zahlen','3 · Dans le rouge','3 · En números rojos')
add('h_3','The bank says no.','Die Bank sagt Nein.','La banque dit non.','El banco dice que no.')
add('p3','Four floors of apartments don’t carry the cost of the land, the building and the garage. The project shows a loss before the first shovel goes into the ground.',
 'Vier Wohngeschosse tragen die Kosten für Grundstück, Gebäude und Garage nicht. Das Projekt schreibt rote Zahlen, bevor der erste Spatenstich erfolgt.',
 'Quatre étages de logements ne couvrent pas le coût du terrain, du bâtiment et du parking. Le projet est déficitaire avant même le premier coup de pelle.',
 'Cuatro plantas de viviendas no cubren el coste del solar, del edificio y del aparcamiento. El proyecto da pérdidas antes de la primera palada.')
add('lv','Value of the sellable area','Wert der verkaufbaren Fläche','Valeur de la surface vendable','Valor de la superficie vendible')
add('at','{a} sq ft at {v} per sq ft','{a} sq ft zu je {v} pro sq ft','{a} sq ft à {v} le sq ft','{a} sq ft a {v} por sq ft')
add('lc','Land, building and garage','Grundstück, Gebäude und Garage','Terrain, bâtiment et parking','Solar, edificio y aparcamiento')
add('lc2','Land, building and parking','Grundstück, Gebäude und Parken','Terrain, bâtiment et stationnement','Solar, edificio y aparcamiento')
add('lf','Fit-out of the two freed floors','Ausbau der beiden frei gewordenen Ebenen','Aménagement des deux étages libérés','Acondicionamiento de las dos plantas liberadas')
add('lr','Result','Ergebnis','Résultat','Resultado')
add('wh','The usual ways out make it worse:','Die üblichen Auswege machen es schlimmer:','Les solutions habituelles aggravent la situation :','Las salidas habituales lo empeoran:')
add('w1','Dig a basement: more excavation, shoring and construction time.','Eine Tiefgarage bauen: mehr Aushub, Verbau und Bauzeit.','Creuser un sous-sol : plus de terrassement, de soutènement et de délais.','Excavar un sótano: más excavación, contención y plazo de obra.')
add('w2','Build fewer spaces: the zoning doesn’t allow it.','Weniger Stellplätze bauen: Das lässt der Bebauungsplan nicht zu.','Construire moins de places : l’urbanisme ne l’autorise pas.','Construir menos plazas: el planeamiento no lo permite.')
add('w3','Sell the plot: the opportunity is gone.','Das Grundstück verkaufen: Die Chance ist vertan.','Vendre la parcelle : l’opportunité est perdue.','Vender el solar: la oportunidad se pierde.')
add('k4','4 · The turn','4 · Die Wende','4 · Le tournant','4 · El giro')
add('h_4','TilePark parks the same 68 cars on two floors.','TilePark parkt dieselben 68 Fahrzeuge auf zwei Ebenen.','TilePark gare les mêmes 68 voitures sur deux niveaux.','TilePark aparca los mismos 68 coches en dos plantas.')
add('p4','No ramps, no drive aisles. Conveyors move every car lengthways and sideways to its space, so the whole floor is parking. Drivers only use the bright transfer cabin at ground level.',
 'Keine Rampen, keine Fahrgassen. Fördermodule bewegen jedes Fahrzeug längs und quer zu seinem Stellplatz – die gesamte Fläche ist Parkfläche. Nutzer betreten nur die helle Übergabekabine im Erdgeschoss.',
 'Ni rampes ni allées. Des convoyeurs déplacent chaque voiture en long et en large jusqu’à sa place : toute la surface sert au stationnement. Les conducteurs n’utilisent que la cabine de transfert lumineuse au rez-de-chaussée.',
 'Sin rampas ni pasillos. Los transportadores mueven cada coche a lo largo y a lo ancho hasta su plaza, así que toda la planta es aparcamiento. Los conductores solo usan la cabina de transferencia luminosa en planta baja.')
add('n4','And it costs about as much as the conventional garage: most TilePark systems from 25 spaces cost around $30,000 per space.',
 'Und es kostet etwa so viel wie die konventionelle Garage: Die meisten TilePark-Anlagen ab 25 Stellplätzen kosten rund 30.000 $ pro Stellplatz.',
 'Et cela coûte à peu près autant que le parking classique : la plupart des systèmes TilePark à partir de 25 places coûtent environ 30 000 $ par place.',
 'Y cuesta más o menos lo mismo que el aparcamiento convencional: la mayoría de los sistemas TilePark a partir de 25 plazas cuestan unos 30.000 $ por plaza.')
add('rp','↻ Replay','↻ Wiederholen','↻ Rejouer','↻ Repetir')
add('cap4','3D animation: TilePark takes over','3D-Animation: TilePark übernimmt','Animation 3D : TilePark prend le relais','Animación 3D: TilePark toma el relevo')
add('k5','5 · Into the green','5 · Schwarze Zahlen','5 · Dans le vert','5 · En positivo')
add('h_5','Two more floors that earn.','Zwei Ebenen mehr, die Ertrag bringen.','Deux étages de plus qui rapportent.','Dos plantas más que generan ingresos.')
add('p5','The freed floors become apartments. Counted conservatively, with 150 sq ft per space, that is 10,200 sq ft of new sellable area. After fitting out the two floors, the same building makes a profit.',
 'Die frei gewordenen Ebenen werden zu Wohnungen. Vorsichtig gerechnet mit 150 sq ft pro Stellplatz sind das 10.200 sq ft neue verkaufbare Fläche. Nach dem Ausbau der beiden Ebenen schreibt dasselbe Gebäude schwarze Zahlen.',
 'Les étages libérés deviennent des logements. Calculé prudemment, avec 150 sq ft par place, cela fait 10 200 sq ft de surface vendable en plus. Après l’aménagement des deux étages, le même bâtiment devient rentable.',
 'Las plantas liberadas se convierten en viviendas. Con un cálculo prudente de 150 sq ft por plaza, son 10.200 sq ft de nueva superficie vendible. Tras acondicionar las dos plantas, el mismo edificio da beneficios.')
add('cap5','3D animation: the freed floors become apartments','3D-Animation: Die frei gewordenen Ebenen werden zu Wohnungen','Animation 3D : les étages libérés deviennent des logements','Animación 3D: las plantas liberadas se convierten en viviendas')
add('k6','6 · Long after opening','6 · Lange nach der Eröffnung','6 · Bien après l’ouverture','6 · Mucho después de la inauguración')
add('h_6','In the green on day one, and for decades.','Schwarze Zahlen vom ersten Tag an – und über Jahrzehnte.','Dans le vert dès le premier jour, et pour des décennies.','En positivo desde el primer día y durante décadas.')
add('t1','Every space can charge an electric car, so fewer chargers serve more cars.','Jeder Stellplatz kann ein Elektrofahrzeug laden – so versorgen weniger Ladepunkte mehr Fahrzeuge.','Chaque place peut recharger une voiture électrique : moins de bornes servent plus de voitures.','Cada plaza puede cargar un coche eléctrico, así que menos cargadores sirven a más coches.')
add('t2','Residents call their car with the app, and it waits for them in the transfer cabin.','Bewohner rufen ihr Fahrzeug per App ab, und es wartet in der Übergabekabine.','Les résidents appellent leur voiture avec l’application, et elle les attend dans la cabine de transfert.','Los residentes piden su coche con la app y les espera en la cabina de transferencia.')
add('t3','Retrieval times, availability and service are agreed in the contract, and you can hold us to them.','Abrufzeiten, Verfügbarkeit und Service sind vertraglich vereinbart – Sie können uns daran messen.','Temps de restitution, disponibilité et service sont convenus par contrat, et vous pouvez nous en tenir responsables.','Tiempos de entrega, disponibilidad y servicio se acuerdan en el contrato y puede exigirnos su cumplimiento.')
add('t4','Our own team services the system, with spare parts for at least 30 years.','Unser eigenes Team betreut die Anlage, mit Ersatzteilen für mindestens 30 Jahre.','Notre propre équipe entretient le système, avec des pièces détachées pendant au moins 30 ans.','Nuestro propio equipo mantiene el sistema, con repuestos durante al menos 30 años.')
add('mk','Project result','Projektergebnis','Résultat du projet','Resultado del proyecto')
add('c0','Planning','In Planung','En projet','En proyecto')
add('c1','In the red','Rote Zahlen','Dans le rouge','Números rojos')
add('c2','Turning','Die Wende','Le tournant','El giro')
add('c3','In the green','Schwarze Zahlen','Dans le vert','En positivo')
add('r1','Parking spaces','Stellplätze','Places de stationnement','Plazas de aparcamiento')
add('r2','Parking floors','Parkebenen','Niveaux de stationnement','Plantas de aparcamiento')
add('r3','Floors that earn','Ebenen mit Ertrag','Niveaux qui rapportent','Plantas que generan ingresos')
add('r4','Sellable area','Verkaufbare Fläche','Surface vendable','Superficie vendible')
add('mf','Fictional example, rounded figures.','Fiktives Beispiel, gerundete Zahlen.','Exemple fictif, chiffres arrondis.','Ejemplo ficticio, cifras redondeadas.')
add('ch','Is your project in the red?','Steckt Ihr Projekt in den roten Zahlen?','Votre projet est-il dans le rouge ?','¿Está su proyecto en números rojos?')
add('cp','Send us your site or floor plan. Our engineers lay out TilePark on your site free of charge and show you what it changes in your numbers.',
 'Senden Sie uns Lageplan oder Grundriss. Unsere Ingenieure planen TilePark kostenlos auf Ihrem Grundstück und zeigen Ihnen, was sich an Ihren Zahlen ändert.',
 'Envoyez-nous votre plan de masse ou d’étage. Nos ingénieurs implantent gratuitement TilePark sur votre site et vous montrent ce que cela change dans vos chiffres.',
 'Envíenos el plano del solar o de planta. Nuestros ingenieros distribuyen TilePark en su solar sin coste y le muestran qué cambia en sus cifras.')
add('cb','Request a free feasibility study','Kostenlose Machbarkeitsstudie anfordern','Demander une étude de faisabilité gratuite','Solicitar un estudio de viabilidad gratuito')
add('ft','Fictional example with rounded figures. The area recovered (150 sq ft per space) and the value of sellable area ($400 per sq ft) are the example values of the Parkstory gain calculator; land, construction and fit-out costs are example values. Your free feasibility study shows the real numbers for your site.',
 'Fiktives Beispiel mit gerundeten Zahlen. Gewonnene Fläche (150 sq ft pro Stellplatz) und Flächenwert (400 $ pro sq ft) sind die Beispielwerte des Parkstory-Rechners; Grundstücks-, Bau- und Ausbaukosten sind Beispielwerte. Ihre kostenlose Machbarkeitsstudie zeigt die tatsächlichen Zahlen für Ihr Grundstück.',
 'Exemple fictif aux chiffres arrondis. La surface gagnée (150 sq ft par place) et la valeur de la surface vendable (400 $ par sq ft) sont les valeurs d’exemple du calculateur Parkstory ; les coûts de terrain, de construction et d’aménagement sont des valeurs d’exemple. Votre étude de faisabilité gratuite indique les chiffres réels pour votre site.',
 'Ejemplo ficticio con cifras redondeadas. La superficie recuperada (150 sq ft por plaza) y el valor de la superficie vendible (400 $ por sq ft) son los valores de ejemplo de la calculadora de Parkstory; los costes de solar, construcción y acondicionamiento son valores de ejemplo. Su estudio de viabilidad gratuito muestra las cifras reales para su solar.')
add('mio','million','Mio.','M','M')
t = open(os.path.join(S,'template.html')).read()
M = os.path.join(S,'..','sim3d','media')
def vid(n): return '<source src="%s" type="video/webm"><source src="%s" type="video/mp4">' % (b64(os.path.join(M,n+'.webm'),'video/webm'), b64(os.path.join(M,n+'.mp4'),'video/mp4'))
t = t.replace('__L__', json.dumps(L, ensure_ascii=False))
t = t.replace("$('lA1').textContent=D.at(nf(24000),'$400')", "$('lA1').textContent=D.at.replace('{a}',nf(24000)).replace('{v}',lang==='en'?'$400':'400 $')")
t = t.replace("$('lA2').textContent=D.at(nf(34200),'$400')", "$('lA2').textContent=D.at.replace('{a}',nf(34200)).replace('{v}',lang==='en'?'$400':'400 $')")
for k,f in (('__C1__','c1'),('__C2__','c2'),('__C5__','c5')): t = t.replace(k, b64(os.path.join(S,'img',f+'.jpg'),'image/jpeg'))
t = t.replace('__V4__', vid('common')).replace('__V5__', vid('apt'))
assert '__' not in t.replace('__proto__',''), [x for x in ('__L__','__C1__','__V4__') if x in t]
open(os.path.join(S,'from-red-to-green.html'),'w').write(t); print('ok', len(t)//1024, 'KB')
