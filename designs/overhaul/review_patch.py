# Applies the external review: precise reliability wording, commercial argument, evidence table,
# economics steps, guide links, nature chapter after the products. python review_patch.py in.html out.html
import sys, re, json
src, out = sys.argv[1:3]
s = open(src).read()
i = s.find('var D={'); D, _ = json.JSONDecoder().raw_decode(s[i+6:])
T = {}
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:100], s.count(a)); s = s.replace(a, b)
def retext(old, new, de, fr, es):
    """replace a visible English text and register its translations"""
    global s
    pat = re.compile('>(\\s*)' + re.escape(old) + '(\\s*)<')
    s, c = pat.subn(lambda m: '>' + m.group(1) + new + m.group(2) + '<', s); assert c >= 1, ('missing', old[:80])
    T[new] = [de, fr, es]
# ---------- 1. commercial argument in the hero ----------
rep('<p class="bs-claim">More cars on less space. <em>Your car, ready when you are.</em></p>', '<p class="bs-claim">Parking decides how much building you can create. <em>For decades.</em></p>')
T["Parking decides how much building you can create."] = ["Das Parken entscheidet, wie viel Gebäude Sie bauen können.","Le stationnement décide de la surface que vous pouvez construire.","El aparcamiento decide cuánto edificio puede construir."]
T["For decades."] = ["Über Jahrzehnte.","Pour des décennies.","Durante décadas."]
retext("Drive into a bright transfer cabin and step out: TilePark parks the car for you. Independent conveyors move it in every direction, with no ramps, no drive aisles and no central lift that every car depends on. More cars fit on the same footprint, the garage keeps working if one machine stops, and the performance is agreed with you in the contract.",
 "A garage is built once and shapes the building for its whole life. TilePark parks cars without ramps or drive aisles: you drive into a bright transfer cabin, step out, and independent conveyors move the car to its space. More cars fit on less floor area, and the space you gain can be built, sold or rented.",
 "Eine Garage wird einmal gebaut und prägt das Gebäude über seine gesamte Lebensdauer. TilePark parkt ohne Rampen und Fahrgassen: Sie fahren in eine helle Übergabekabine, steigen aus, und unabhängige Fördermodule bringen das Fahrzeug an seinen Platz. So passen mehr Fahrzeuge auf weniger Fläche – und die gewonnene Fläche lässt sich bebauen, verkaufen oder vermieten.",
 "Un parking se construit une fois et marque le bâtiment pour toute sa durée de vie. TilePark gare les voitures sans rampes ni allées : vous entrez dans une cabine de transfert lumineuse, vous descendez, et des convoyeurs indépendants amènent la voiture à sa place. Plus de voitures sur moins de surface, et l’espace gagné peut être construit, vendu ou loué.",
 "Un aparcamiento se construye una vez y marca el edificio durante toda su vida. TilePark aparca sin rampas ni pasillos: entra en una cabina de transferencia luminosa, se baja y transportadores independientes llevan el coche a su plaza. Caben más coches en menos superficie y el espacio ganado se puede construir, vender o alquilar.")
# ---------- 2. precise reliability wording ----------
retext("Nature doesn’t need a central bottleneck.","Nature spreads the work.","Die Natur verteilt die Arbeit.","La nature répartit le travail.","La naturaleza reparte el trabajo.")
retext("Neither should parking.","So does the TilePark grid.","Das TilePark-Raster auch.","La grille TilePark aussi.","La cuadrícula TilePark también.")
retext("Bees coordinate thousands of movements without a central path, and simply work around a damaged cell. TilePark follows the same principle: independent conveyors, each with its own controller, and no central bottleneck.",
 "Bees coordinate thousands of movements without a central path, and simply work around a damaged cell. TilePark applies the same principle to horizontal movement: independent conveyors, each with its own controller, route cars around a stopped conveyor.",
 "Bienen koordinieren Tausende Bewegungen ohne zentralen Weg und umgehen eine beschädigte Zelle einfach. TilePark überträgt dieses Prinzip auf die horizontale Bewegung: Unabhängige Fördermodule mit eigener Steuerung leiten Fahrzeuge um ein stehendes Fördermodul herum.",
 "Les abeilles coordonnent des milliers de mouvements sans chemin central et contournent simplement une cellule endommagée. TilePark applique ce principe au déplacement horizontal : des convoyeurs indépendants, chacun avec sa propre commande, contournent un convoyeur à l’arrêt.",
 "Las abejas coordinan miles de movimientos sin un camino central y simplemente rodean una celda dañada. TilePark aplica el mismo principio al movimiento horizontal: transportadores independientes, cada uno con su propio control, desvían los coches alrededor de un transportador detenido.")
retext("No central control.","Distributed control.","Verteilte Steuerung.","Une commande répartie.","Control distribuido.")
retext("No central bottleneck.","Local faults stay local.","Lokale Störungen bleiben lokal.","Une panne locale reste locale.","Una avería local se queda en local.")
retext("Just like bees in a hive, each TilePark conveyor has its own controller and acts independently. There is no master computer, shuttle, or lift that every car depends on. This decentralized control is the core of our technology and the source of the system's speed, flexibility, and resilience.",
 "Just like bees in a hive, each TilePark conveyor has its own controller and acts independently. Horizontal movement doesn’t depend on a master computer, a shuttle or a robot fleet: if one conveyor stops, the others route around it. Lifts, stackers and transfer cabins are shared by the cars they serve, so their number and redundancy are planned for each project.",
 "Wie die Bienen in einem Bienenstock hat jedes TilePark-Fördermodul eine eigene Steuerung und arbeitet eigenständig. Die horizontale Bewegung hängt weder von einem Zentralrechner noch von einem Shuttle oder einer Roboterflotte ab: Steht ein Fördermodul, fahren die anderen darum herum. Lifte, Hubmodule und Übergabekabinen teilen sich die Fahrzeuge, die sie bedienen – ihre Anzahl und Redundanz planen wir für jedes Projekt.",
 "Comme les abeilles d’une ruche, chaque convoyeur TilePark a sa propre commande et agit de façon autonome. Le déplacement horizontal ne dépend ni d’un ordinateur central, ni d’une navette, ni d’une flotte de robots : si un convoyeur s’arrête, les autres le contournent. Ascenseurs, gerbeurs et cabines de transfert sont partagés par les voitures qu’ils desservent : leur nombre et leur redondance sont définis pour chaque projet.",
 "Como las abejas en una colmena, cada transportador TilePark tiene su propio control y actúa de forma independiente. El movimiento horizontal no depende de un ordenador central, una lanzadera ni una flota de robots: si un transportador se detiene, los demás lo rodean. Ascensores, apiladores y cabinas de transferencia los comparten los coches a los que sirven, así que su número y redundancia se planifican en cada proyecto.")
retext("A modular structure built from industry-standard components means fewer faults and fast replacement. Remote diagnostics let our team respond to any issue immediately.",
 "A modular structure built from industry-standard components means fewer faults and fast replacement. Remote diagnostics let our team respond quickly.",
 "Ein modularer Aufbau aus Industriestandard-Komponenten bedeutet weniger Störungen und schnellen Austausch. Per Ferndiagnose reagiert unser Team schnell.",
 "Une structure modulaire faite de composants industriels standard signifie moins de pannes et un remplacement rapide. Grâce au télédiagnostic, notre équipe réagit rapidement.",
 "Una estructura modular con componentes industriales estándar significa menos averías y una sustitución rápida. Con el diagnóstico remoto, nuestro equipo responde con rapidez.")
old6 = "In a conventional garage, roughly half of the floor area is taken up by ramps and drive aisles. TilePark needs neither. Each car rests on a pallet, and the conveyors beneath move it lengthwise and sideways, just like the pieces of a sliding puzzle. A single empty space is enough to bring any car to the transfer cabin."
o = D[old6]
def lastswap(t, new): return t.rsplit('. ', 1)[0] + '. ' + new
retext(old6, old6.replace("A single empty space is enough to bring any car to the transfer cabin.", "A few free positions in the grid are enough to bring any car to the transfer cabin; how many a layout needs depends on its size, its shape and the retrieval times you require."),
 lastswap(o[0], "Wenige freie Positionen im Raster genügen, um jedes Fahrzeug zur Übergabekabine zu bringen – wie viele ein Layout braucht, hängt von Größe, Form und den geforderten Abrufzeiten ab."),
 lastswap(o[1], "Quelques positions libres dans la grille suffisent pour amener n’importe quelle voiture à la cabine de transfert ; leur nombre dépend de la taille, de la forme et des temps de restitution exigés."),
 lastswap(o[2], "Unas pocas posiciones libres en la cuadrícula bastan para llevar cualquier coche a la cabina de transferencia; cuántas necesita una distribución depende de su tamaño, su forma y los tiempos de entrega exigidos."))
retext("Any car reaches the cabin, with no drive aisle, even with a conveyor offline.","Cars reach the cabin without a drive aisle and are routed around an offline conveyor.","Fahrzeuge erreichen die Kabine ohne Fahrgasse und werden um ein ausgefallenes Fördermodul herumgeleitet.","Les voitures rejoignent la cabine sans allée de circulation et contournent un convoyeur hors service.","Los coches llegan a la cabina sin pasillo y se desvían alrededor de un transportador fuera de servicio.")
retext("Still no central bottleneck","Each stacker on its own","Jedes Hubmodul für sich","Chaque gerbeur indépendant","Cada apilador por su cuenta")
retext("Each stacker serves only its own conveyor. With no central lift tower that every car depends on, the rest of the garage keeps running.",
 "Each stacker serves only its own conveyor. If one stacker stops, only the cars it holds wait; the rest of the garage keeps running.",
 "Jedes Hubmodul bedient nur sein eigenes Fördermodul. Steht ein Hubmodul, warten nur die Fahrzeuge darin – der Rest der Anlage arbeitet weiter.",
 "Chaque gerbeur ne dessert que son propre convoyeur. Si un gerbeur s’arrête, seules les voitures qu’il porte attendent ; le reste du parking continue de fonctionner.",
 "Cada apilador solo sirve a su propio transportador. Si uno se detiene, solo esperan los coches que contiene; el resto del aparcamiento sigue funcionando.")
retext("No single point of failure","Faults stay local","Störungen bleiben lokal","Les pannes restent locales","Las averías quedan localizadas")
retext("Every conveyor has its own controller and at least four drive motors. Cars are routed around a stopped conveyor.",
 "Every conveyor has its own controller and at least four drive motors, and cars are routed around a stopped one. Shared elements such as lifts and transfer cabins are planned with the redundancy your project needs.",
 "Jedes Fördermodul hat eine eigene Steuerung und mindestens vier Antriebsmotoren; Fahrzeuge werden um ein stehendes Modul herumgeleitet. Gemeinsam genutzte Elemente wie Lifte und Übergabekabinen planen wir mit der Redundanz, die Ihr Projekt braucht.",
 "Chaque convoyeur a sa propre commande et au moins quatre moteurs, et les voitures contournent un convoyeur à l’arrêt. Les éléments partagés, comme les ascenseurs et les cabines de transfert, sont prévus avec la redondance nécessaire à votre projet.",
 "Cada transportador tiene su propio control y al menos cuatro motores, y los coches se desvían alrededor de uno detenido. Los elementos compartidos, como ascensores y cabinas de transferencia, se planifican con la redundancia que necesita su proyecto.")
retext("Yes. The other conveyors route the cars around a stopped one, so every car stays reachable.",
 "On the grid, yes: the other conveyors route cars around a stopped one. Only a car standing on the stopped conveyor itself waits for the repair. Lifts and transfer cabins are shared, so we plan how many your project needs.",
 "Auf dem Raster ja: Die übrigen Fördermodule leiten die Fahrzeuge um ein stehendes herum. Nur ein Fahrzeug, das auf dem stehenden Modul selbst steht, wartet auf die Reparatur. Lifte und Übergabekabinen werden gemeinsam genutzt – wie viele Ihr Projekt braucht, planen wir mit Ihnen.",
 "Sur la grille, oui : les autres convoyeurs contournent celui qui est à l’arrêt. Seule une voiture posée sur ce convoyeur attend la réparation. Ascenseurs et cabines de transfert sont partagés : nous prévoyons avec vous combien votre projet en nécessite.",
 "En la cuadrícula, sí: los demás transportadores rodean al que está detenido. Solo un coche situado sobre ese transportador espera a la reparación. Ascensores y cabinas de transferencia se comparten, así que planificamos con usted cuántos necesita su proyecto.")
retext("Not in TilePark: every position is a conveyor with its own controller.",
 "Not for horizontal movement: every position is a conveyor with its own controller. Between levels, cars use lifts or stackers, and TilePark Tower uses a central lift. Their number and redundancy are part of the design.",
 "Nicht bei der horizontalen Bewegung: Jede Position ist ein Fördermodul mit eigener Steuerung. Zwischen den Ebenen nutzen die Fahrzeuge Lifte oder Hubmodule, der TilePark Tower einen zentralen Lift. Anzahl und Redundanz sind Teil der Planung.",
 "Pas pour le déplacement horizontal : chaque position est un convoyeur doté de sa propre commande. Entre les niveaux, les voitures utilisent des ascenseurs ou des gerbeurs, et la TilePark Tower un ascenseur central. Leur nombre et leur redondance font partie de la conception.",
 "No en el movimiento horizontal: cada posición es un transportador con su propio control. Entre plantas, los coches usan ascensores o apiladores, y TilePark Tower un ascensor central. Su número y redundancia forman parte del diseño.")
retext("Every conveyor has its own controller and at least four drive motors. If one conveyor stops, the others route the cars around it, so every car stays reachable. Our service team monitors the system around the clock and solves 99 % of faults remotely.",
 "Every conveyor has its own controller and at least four drive motors. If one conveyor stops, the others route the cars around it; only a car standing on that conveyor waits for the repair. Lifts, stackers and transfer cabins are shared by the cars they serve, so their number and redundancy are planned for your project, and TilePark Tower depends on its central lift. Our service team monitors the system around the clock, with the goal of solving 99 % of faults remotely.",
 "Jedes Fördermodul hat eine eigene Steuerung und mindestens vier Antriebsmotoren. Steht ein Fördermodul, leiten die anderen die Fahrzeuge darum herum – nur ein Fahrzeug, das auf diesem Modul steht, wartet auf die Reparatur. Lifte, Hubmodule und Übergabekabinen teilen sich die Fahrzeuge, die sie bedienen; ihre Anzahl und Redundanz planen wir für Ihr Projekt, und der TilePark Tower hängt von seinem zentralen Lift ab. Unser Serviceteam überwacht die Anlage rund um die Uhr – mit dem Ziel, 99 % der Störungen per Ferndiagnose zu lösen.",
 "Chaque convoyeur a sa propre commande et au moins quatre moteurs. Si un convoyeur s’arrête, les autres le contournent ; seule une voiture posée sur ce convoyeur attend la réparation. Ascenseurs, gerbeurs et cabines de transfert sont partagés par les voitures qu’ils desservent : leur nombre et leur redondance sont définis pour votre projet, et la TilePark Tower dépend de son ascenseur central. Notre équipe de service surveille le système 24 h/24, avec l’objectif de résoudre 99 % des pannes à distance.",
 "Cada transportador tiene su propio control y al menos cuatro motores. Si uno se detiene, los demás desvían los coches a su alrededor; solo un coche situado sobre ese transportador espera a la reparación. Ascensores, apiladores y cabinas de transferencia los comparten los coches a los que sirven, así que su número y redundancia se planifican para su proyecto, y TilePark Tower depende de su ascensor central. Nuestro equipo de servicio supervisa el sistema las 24 horas, con el objetivo de resolver el 99 % de las averías a distancia.")
retext("AGV robots, rail-guided shuttles and tower systems need at least one drive aisle, rails or a central lift. TilePark needs none: every position is a conveyor, so the whole floor is parking and no single machine stands between a driver and their car.",
 "AGV robots and rail-guided shuttles need drive aisles or rails, and tower systems move every car through a central lift. TilePark needs no drive aisles or rails: every position is a conveyor, so the whole floor is parking, and horizontal movement doesn’t depend on a single machine. Between levels, TilePark uses lifts or stackers sized for your project.",
 "AGV-Roboter und schienengeführte Shuttles brauchen Fahrgassen oder Schienen, Turmsysteme bewegen jedes Fahrzeug über einen zentralen Lift. TilePark braucht weder Fahrgassen noch Schienen: Jede Position ist ein Fördermodul, die gesamte Fläche ist Parkfläche, und die horizontale Bewegung hängt nicht von einer einzelnen Maschine ab. Zwischen den Ebenen nutzt TilePark Lifte oder Hubmodule, ausgelegt für Ihr Projekt.",
 "Les robots AGV et les navettes sur rails ont besoin d’allées ou de rails, et les tours font passer chaque voiture par un ascenseur central. TilePark n’a besoin ni d’allées ni de rails : chaque position est un convoyeur, toute la surface sert au stationnement, et le déplacement horizontal ne dépend d’aucune machine isolée. Entre les niveaux, TilePark utilise des ascenseurs ou des gerbeurs dimensionnés pour votre projet.",
 "Los robots AGV y las lanzaderas sobre raíles necesitan pasillos o raíles, y las torres mueven cada coche por un ascensor central. TilePark no necesita pasillos ni raíles: cada posición es un transportador, toda la superficie es aparcamiento y el movimiento horizontal no depende de una sola máquina. Entre plantas, TilePark usa ascensores o apiladores dimensionados para su proyecto.")
retext("AGV systems, rail-guided shuttles and moving tower systems all need at least one drive aisle, rails or central lifts. TilePark needs none: its patented XY technology turns the entire floor into parking.",
 "AGV systems and rail-guided shuttles need drive aisles or rails, and moving tower systems need central lifts. TilePark needs no drive aisles or rails: its patented XY technology turns the entire floor into parking.",
 "AGV-Systeme und schienengeführte Shuttles brauchen Fahrgassen oder Schienen, bewegliche Turmsysteme zentrale Lifte. TilePark braucht weder Fahrgassen noch Schienen: Seine patentierte XY-Technologie macht die gesamte Fläche zur Parkfläche.",
 "Les systèmes AGV et les navettes sur rails ont besoin d’allées ou de rails, et les tours mobiles d’ascenseurs centraux. TilePark n’a besoin ni d’allées ni de rails : sa technologie XY brevetée transforme toute la surface en stationnement.",
 "Los sistemas AGV y las lanzaderas sobre raíles necesitan pasillos o raíles, y las torres móviles, ascensores centrales. TilePark no necesita pasillos ni raíles: su tecnología XY patentada convierte toda la planta en aparcamiento.")
retext("Hundreds of independent conveyors and no central bottleneck. If one is offline, the others route around it.",
 "Hundreds of independent conveyors instead of a few critical machines. If one is offline, the others route around it.",
 "Hunderte unabhängige Fördermodule statt weniger kritischer Maschinen. Fällt eines aus, fahren die anderen darum herum.",
 "Des centaines de convoyeurs indépendants au lieu de quelques machines critiques. Si l’un est hors service, les autres le contournent.",
 "Cientos de transportadores independientes en lugar de unas pocas máquinas críticas. Si uno está fuera de servicio, los demás lo rodean.")
retext("99 % solved remotely","Goal: 99 % solved remotely","Ziel: 99 % per Ferndiagnose gelöst","Objectif : 99 % résolus à distance","Objetivo: 99 % resuelto a distancia")
g = "Our goal: solve 99 % of all issues remotely, through remote diagnostics, before anyone needs to travel."
assert g in D
c = s.count('>Our after-sales team solves 99 % of all issues remotely, through remote diagnostics.<'); assert c >= 1
s = s.replace('>Our after-sales team solves 99 % of all issues remotely, through remote diagnostics.<', '>'+g+'<')
# ---------- 3. nature chapter after the products ----------
def take(marker, tag):
    global s
    i = s.find(marker); assert i >= 0, marker; d = 0
    for m in re.compile(r'<%s[\s>]|</%s>' % (tag, tag)).finditer(s, i):
        d += -1 if m.group(0).startswith('</') else 1
        if d == 0:
            b = s[i:m.end()]; s = s[:i] + s[m.end():]; return b
nat = take('<div class="natwrap">', 'div')
heart_i = s.find('<!-- ============ THE HEART (drop-in section) ============ -->')
heart = take('<section class="hiw heartsec" id="heart">', 'section')
rep('<section class="part-sub" id="included">', nat + heart + '<section class="part-sub" id="included">')
li = re.search(r'<li><a href="#inspired-by-nature">.*?</li>', s, re.S).group(0); s = s.replace(li, '', 1)
tli = re.search(r'<li><a href="#tower">.*?</li>', s, re.S).group(0); rep(tli, tli + li)
# ---------- 4. evidence in References ----------
EVI = ('<div class="ev-box"><p class="hiw-eyebrow">Operating evidence</p><h3 class="ev-h">Measured, targeted, guaranteed: three different things.</h3>'
 '<div class="ev-leg"><div><b>Measured</b><span>Results from systems in operation, with the measurement period and sample.</span></div>'
 '<div><b>Design target</b><span>What we build to, such as 99.5 % availability and solving 99 % of faults remotely.</span></div>'
 '<div><b>Contractual guarantee</b><span>Values agreed for your project and written into the contract, such as retrieval time and availability.</span></div></div>'
 '<div class="ev-tw"><table class="ev-t"><thead><tr><th>System</th><th>Spaces</th><th>In operation since</th><th>Measured retrieval time</th><th>Measured availability</th></tr></thead><tbody>'
 + ''.join('<tr><td>%s</td><td>%s</td><td class="tbp">To be published</td><td class="tbp">To be published</td><td class="tbp">To be published</td></tr>' % (n, sp) for n, sp in (("TilePark Munich","16"),("Helsinki","63"),("Stockholm","10"))) +
 '</tbody></table></div><p class="ev-note">We publish measured values once the measurement period, the sample and the definitions are documented.</p></div>')
w = s.find('id="working-projects"'); e = s.find('</div></section>', w)
s = s[:e] + EVI + s[e:]
T.update({"Operating evidence":["Betriebsdaten","Données d’exploitation","Datos de funcionamiento"],
 "Measured, targeted, guaranteed: three different things.":["Gemessen, angestrebt, garantiert: drei verschiedene Dinge.","Mesuré, visé, garanti : trois choses différentes.","Medido, objetivo, garantizado: tres cosas distintas."],
 "Measured":["Gemessen","Mesuré","Medido"],"Results from systems in operation, with the measurement period and sample.":["Ergebnisse aus Anlagen in Betrieb, mit Messzeitraum und Stichprobe.","Résultats de systèmes en service, avec la période et l’échantillon de mesure.","Resultados de sistemas en funcionamiento, con el periodo y la muestra de medición."],
 "Design target":["Auslegungsziel","Objectif de conception","Objetivo de diseño"],"What we build to, such as 99.5 % availability and solving 99 % of faults remotely.":["Der Anspruch, auf den wir auslegen – etwa 99,5 % Verfügbarkeit und 99 % per Ferndiagnose gelöste Störungen.","Ce pour quoi nous concevons, par exemple 99,5 % de disponibilité et 99 % des pannes résolues à distance.","Aquello para lo que diseñamos, como un 99,5 % de disponibilidad y el 99 % de las averías resueltas a distancia."],
 "Contractual guarantee":["Vertragliche Zusage","Garantie contractuelle","Garantía contractual"],"Values agreed for your project and written into the contract, such as retrieval time and availability.":["Für Ihr Projekt vereinbarte und vertraglich festgehaltene Werte, etwa Abrufzeit und Verfügbarkeit.","Valeurs convenues pour votre projet et inscrites au contrat, comme le temps de restitution et la disponibilité.","Valores acordados para su proyecto y recogidos en el contrato, como el tiempo de entrega y la disponibilidad."],
 "System":["Anlage","Système","Sistema"],"Spaces":["Stellplätze","Places","Plazas"],"In operation since":["In Betrieb seit","En service depuis","En funcionamiento desde"],"Measured retrieval time":["Gemessene Abrufzeit","Temps de restitution mesuré","Tiempo de entrega medido"],"Measured availability":["Gemessene Verfügbarkeit","Disponibilité mesurée","Disponibilidad medida"],
 "To be published":["Wird veröffentlicht","À publier","Pendiente de publicación"],
 "We publish measured values once the measurement period, the sample and the definitions are documented.":["Messwerte veröffentlichen wir, sobald Messzeitraum, Stichprobe und Definitionen dokumentiert sind.","Nous publions les valeurs mesurées dès que la période, l’échantillon et les définitions sont documentés.","Publicamos los valores medidos en cuanto el periodo, la muestra y las definiciones están documentados."]})
# ---------- 5. economics: three steps in the gain calculator ----------
STEPS = ('<div class="eco3"><p class="eco3-h">From parking area to value: three steps</p><ol>'
 '<li><b>Recovered parking area</b><span>What TilePark frees compared with ramps and drive aisles.</span></li>'
 '<li><b>Permitted building area</b><span>How much of it zoning lets you build and use.</span></li>'
 '<li><b>Realizable value</b><span>What the market pays for it, sold or rented, after fit-out.</span></li></ol>'
 '<a class="eco3-l" href="automated-parking-cost.html">Compare total parking cost →</a></div>')
rep('<p class="opp-note">', STEPS + '<p class="opp-note">')
T.update({"From parking area to value: three steps":["Von der Parkfläche zum Wert: drei Schritte","De la surface de stationnement à la valeur : trois étapes","Del aparcamiento al valor: tres pasos"],
 "Recovered parking area":["Gewonnene Parkfläche","Surface de stationnement libérée","Superficie de aparcamiento recuperada"],"What TilePark frees compared with ramps and drive aisles.":["Was TilePark gegenüber Rampen und Fahrgassen frei macht.","Ce que TilePark libère par rapport aux rampes et aux allées.","Lo que TilePark libera frente a rampas y pasillos."],
 "Permitted building area":["Zulässige Geschossfläche","Surface constructible autorisée","Superficie edificable permitida"],"How much of it zoning lets you build and use.":["Wie viel davon der Bebauungsplan als nutzbare Fläche zulässt.","La part que l’urbanisme vous permet de construire et d’utiliser.","La parte que el planeamiento le permite construir y usar."],
 "Realizable value":["Erzielbarer Wert","Valeur réalisable","Valor realizable"],"What the market pays for it, sold or rented, after fit-out.":["Was der Markt dafür zahlt, verkauft oder vermietet, nach dem Ausbau.","Ce que le marché en paie, en vente ou en location, après aménagement.","Lo que paga el mercado por ella, en venta o alquiler, tras el acondicionamiento."],
 "Compare total parking cost →":["Gesamtkosten des Parkens vergleichen →","Comparer le coût total du stationnement →","Comparar el coste total del aparcamiento →"]})
# case study calculator: buildable share
rep('<div class="rg-fix"><span>Area recovered per space</span>',
    '<label for="rgS"><span>Share of the recovered area you can build and use</span><span class="rg-in" data-noi18n><input id="rgS" type="number" min="0" max="100" step="5" inputmode="numeric"><i>%</i></span></label><div class="rg-fix"><span>Area recovered per space</span>')
rep("inp('C').value=d.c;inp('F').value=d.f}", "inp('C').value=d.c;inp('F').value=d.f;inp('S').value=100}")
rep("add=n*d.per,", "add=n*d.per*Math.min(100,g('S'))/100,")
T["Share of the recovered area you can build and use"] = ["Anteil der gewonnenen Fläche, den Sie bebauen und nutzen dürfen","Part de la surface libérée constructible et utilisable","Parte de la superficie recuperada que puede construir y usar"]
# ---------- 6. guide links ----------
GUIDES = [("automated-parking-cost.html","What automated parking costs","Was automatisches Parken kostet","Ce que coûte le stationnement automatisé","Cuánto cuesta el aparcamiento automatizado"),
 ("automated-parking-vs-agv.html","Automated parking vs AGV and shuttle systems","Automatisches Parken im Vergleich zu AGV- und Shuttle-Systemen","Stationnement automatisé, AGV et navettes comparés","Aparcamiento automatizado frente a AGV y lanzaderas"),
 ("automated-parking-reliability.html","Reliability: what happens when a machine stops","Zuverlässigkeit: Was passiert, wenn eine Maschine steht","Fiabilité : que se passe-t-il quand une machine s’arrête","Fiabilidad: qué pasa cuando una máquina se detiene"),
 ("automated-parking-retrieval-time.html","Retrieval time and throughput","Abrufzeit und Durchsatz","Temps de restitution et débit","Tiempo de entrega y capacidad"),
 ("ev-charging.html","EV charging in an automated garage","Laden von Elektrofahrzeugen in einer automatischen Garage","Recharge électrique dans un parking automatisé","Carga de vehículos eléctricos en un aparcamiento automatizado")]
for g_ in GUIDES: T[g_[1]] = list(g_[2:])
T["In-depth guides"] = ["Ausführliche Leitfäden","Guides détaillés","Guías detalladas"]
T["In English"] = ["Auf Englisch","En anglais","En inglés"]
T["In-depth guide →"] = ["Ausführlicher Leitfaden →","Guide détaillé →","Guía detallada →"]
nav = '<nav class="guides" aria-label="In-depth guides"><p class="guides-h"><span>In-depth guides</span> <small>In English</small></p><ul>' + ''.join('<li><a href="%s">%s</a></li>' % (h, t) for h, t, *_ in GUIDES) + '</ul></nav>'
f0 = s.find('id="faq"'); ce = s.find('<div class="ov-ctas">', f0); s = s[:ce] + nav + s[ce:]
QL = {"What does it cost?":"automated-parking-cost.html","How much space do we gain?":"automated-parking-cost.html","How long does it take to get my car?":"automated-parking-retrieval-time.html",
      "What happens if a machine breaks down?":"automated-parking-reliability.html","Can every space charge an electric car?":"ev-charging.html","How is TilePark different from other automated systems?":"automated-parking-vs-agv.html"}
for q, href in QL.items():
    m = re.search(r'(<details class="ov-q"><summary>%s</summary><div><p>.*?</p>)' % re.escape(q), s[f0:], re.S); assert m, q
    a = f0 + m.end(); s = s[:a] + '<a class="faq-more" href="%s">In-depth guide →</a>' % href + s[a:]
# compare part: link to the full comparison
sq = s.find('id="supplier-questions"'); ce = s.find('<div class="ov-ctas">', sq)
s = s[:ce] + '<p class="guide-l"><a href="automated-parking-vs-agv.html">Automated parking vs AGV and shuttle systems</a> · <a href="automated-parking-reliability.html">Reliability: what happens when a machine stops</a></p>' + s[ce:]
CSS = '''<style id="review-css">
.ev-box{margin-top:clamp(28px,4vw,48px);padding:clamp(18px,3vw,32px);border-radius:var(--r-lg);background:var(--surface);border:1px solid var(--line-soft)}
.ev-h{margin:.2rem 0 1rem;font:700 clamp(1.25rem,2.2vw,1.7rem)/1.15 "Outfit","Inter",sans-serif;color:var(--ink)}
.ev-leg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:1.2rem}.ev-leg div{border-top:2px solid var(--green);padding-top:.6rem;display:flex;flex-direction:column;gap:.2rem}
.ev-leg b{color:var(--ink)}.ev-leg span{color:var(--text);font-size:.92rem;line-height:1.45}
.ev-tw{overflow-x:auto}.ev-t{width:100%;border-collapse:collapse;font-size:.92rem;min-width:560px}.ev-t th,.ev-t td{text-align:left;padding:.6rem .7rem;border-bottom:1px solid var(--line-soft)}
.ev-t th{font-size:.76rem;letter-spacing:.05em;text-transform:uppercase;color:var(--text)}.ev-t td{color:var(--ink)}.ev-t .tbp{color:var(--text);font-style:italic}
.ev-note{margin:.8rem 0 0;font-size:.85rem;color:var(--text)}
.eco3{margin:1.4rem 0;padding:1rem 1.2rem;border-radius:12px;border:1px solid var(--line-soft);background:var(--surface)}
.eco3-h{margin:0 0 .6rem;font-weight:700;color:var(--ink)}.eco3 ol{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;counter-reset:e}
.eco3 li{counter-increment:e;display:flex;flex-direction:column;gap:.2rem;padding-left:2rem;position:relative}.eco3 li:before{content:counter(e);position:absolute;left:0;top:0;width:1.5rem;height:1.5rem;border-radius:50%;background:var(--navy);color:var(--green-bright,#b8f03c);display:grid;place-items:center;font-size:.8rem;font-weight:700}
.eco3 b{color:var(--ink)}.eco3 span{font-size:.9rem;color:var(--text)}.eco3-l{display:inline-block;margin-top:.8rem;font-weight:600;color:var(--green-ink,var(--green))}
.guides{margin:1.5rem 0 0;padding:1rem 1.2rem;border-radius:12px;border:1px solid var(--line-soft);background:var(--bg)}.guides-h{margin:0 0 .5rem;font-weight:700;color:var(--ink)}.guides-h small{font-weight:500;color:var(--text)}
.guides ul{margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:.5rem 1.2rem}.guides a,.guide-l a,.faq-more{color:var(--green-ink,var(--green));font-weight:600}
.faq-more{display:inline-block;margin-top:.5rem;font-size:.9rem}.guide-l{margin:1.2rem 0 0;font-size:.95rem}
@media (width<=800px){.ev-leg,.eco3 ol{grid-template-columns:1fr}}
</style>'''
rep('</head>', CSS + '</head>')
rep('var D={', 'var D=' + json.dumps(T, ensure_ascii=False)[:-1] + ', ')
open(out, 'w').write(s); print('ok', len(T), 'strings')
