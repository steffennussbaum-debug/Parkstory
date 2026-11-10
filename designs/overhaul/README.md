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

## 3D film: "The building that could exist"

`sim3d/` holds the Blender scene that renders the film (Cycles, 960×540, 24 fps), and `sim_patch.py` puts it into the page.

```bash
pip install bpy==5.2.3                      # Blender as a Python module
python designs/overhaul/sim3d/scene.py scene.blend
designs/overhaul/sim3d/runall.sh            # renders all frames (about 1.5 hours on 4 CPU cores)
designs/overhaul/sim3d/encode.sh            # frames -> mp4 + webm clips in sim3d/media
python3 designs/overhaul/sim_patch.py Parkstory-overhaul.html Parkstory-overhaul-sim.html designs/overhaul/sim3d/media
python3 designs/build.py Parkstory-overhaul-sim.html public/overhaul
```
