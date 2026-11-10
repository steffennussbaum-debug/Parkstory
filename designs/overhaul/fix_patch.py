# Small follow-up fixes after review_patch: primer label and part-1 banner text. python fix_patch.py in.html out.html
import sys, json
src, out = sys.argv[1:3]; s = open(src).read(); T = {}
def rep(a, b):
    global s
    if a not in s and b in s: return
    assert s.count(a) == 1, a[:80]; s = s.replace(a, b)
rep('<p class="hiw-eyebrow">New to automated parking</p><h2 class="ov-h">Automated parking', '<p class="hiw-eyebrow">The 5-minute tour</p><h2 class="ov-h">Automated parking')
T["The 5-minute tour"] = ["Die 5-Minuten-Tour","La visite en 5 minutes","El recorrido de 5 minutos"]
rep('<p>How TilePark works for drivers and owners, what it costs, how a project runs, and straight answers to the questions every buyer asks.</p>',
    '<p>How TilePark works for drivers and owners, what it costs and how a project runs. The answers to the questions buyers ask are in the FAQ.</p>')
T["How TilePark works for drivers and owners, what it costs and how a project runs. The answers to the questions buyers ask are in the FAQ."] = [
 "Wie TilePark für Nutzer und Eigentümer funktioniert, was es kostet und wie ein Projekt abläuft. Die Antworten auf die Fragen von Käufern finden Sie unter „Häufige Fragen“.",
 "Comment TilePark fonctionne pour les conducteurs et les propriétaires, ce qu’il coûte et comment se déroule un projet. Les réponses aux questions des acheteurs se trouvent dans la FAQ.",
 "Cómo funciona TilePark para conductores y propietarios, cuánto cuesta y cómo se desarrolla un proyecto. Las respuestas a las preguntas de los compradores están en las preguntas frecuentes."]
s = s.replace('var D={', 'var D=' + json.dumps(T, ensure_ascii=False)[:-1] + ', ', 1)
open(out, 'w').write(s); print('ok')
