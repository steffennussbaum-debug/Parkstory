# Overhaul

Restructured version of the Parkstory page for two readers: first-time buyers and buyers who know other systems.

- `content.py`: all new texts with German, French and Spanish translations.
- `build_ovh.py`: turns the current master page into the overhaul master.

```bash
python3 designs/overhaul/build_ovh.py Parkstory.html Parkstory-overhaul.html designs/overhaul
python3 designs/build.py Parkstory-overhaul.html public/overhaul
```

What changes: new landing text with proof points and two entry buttons (5-minute tour, comparison), new part
"New to automated parking" (primer and FAQ), new part "Comparing systems" (comparison, performance agreed in
the contract, questions to ask every supplier), "News" renamed "References" and moved before "Our DNA", and
merged chapters in Technology and Our DNA. Performance values are not published: they are defined with each
customer and written into the contract.
