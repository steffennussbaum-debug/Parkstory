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

## Case study "From red to green"

`case_patch.py` adds the story page (`designs/story`) as a chapter of "Your opportunity", after "What you gain":

```bash
python3 designs/overhaul/case_patch.py Parkstory-overhaul-sim.html Parkstory-overhaul-case.html public/story/from-red-to-green.html <story img dir> designs/overhaul/sim3d/media
python3 designs/build.py Parkstory-overhaul-case.html public/overhaul
```

## FAQ

`faq_patch.py` moves the buyer questions into their own menu part "FAQ" (before "Plan your TilePark"), grouped into
five topics with 20 questions:

```bash
python3 designs/overhaul/faq_patch.py Parkstory-overhaul-case.html Parkstory-overhaul-faq.html
python3 designs/build.py Parkstory-overhaul-faq.html public/overhaul
```

## Review round: precision, guides and SEO

```bash
python3 designs/overhaul/review_patch.py Parkstory-overhaul-faq.html Parkstory-overhaul-rev.html   # wording, evidence, economics, guide links
python3 designs/overhaul/fix_patch.py Parkstory-overhaul-rev.html Parkstory-overhaul-rev.html     # primer label, part-1 banner text
python3 designs/overhaul/case_compact.py Parkstory-overhaul-rev.html Parkstory-overhaul-cc.html    # compact animated case study (build from -cc.html)
python3 designs/build.py Parkstory-overhaul-rev.html public/overhaul
python3 designs/overhaul/topics.py public/overhaul <story img dir>                                 # five guide pages + guides.css
python3 designs/overhaul/seo_post.py public/overhaul                                               # one H1, metadata, JSON-LD, sitemap, robots
```

The canonical domain is assumed to be https://www.parkstory.com/ (change `BASE` in topics.py and seo_post.py).
The guide pages use flat files (`automated-parking-cost.html`); with "clean URLs" on the host they are served as `/automated-parking-cost`.

## Case study: building size follows the customer's numbers

The case study film exists in four building sizes: 34, 68, 136 and 272 spaces. `sim3d/scene_size.py` builds them
(`NCOL=12 LP=2` → 34, `12 4` → 68, `24 4` → 136, `24 8` → 272); `runsize.sh S|L|XL` renders, `encsize.sh` encodes to
`sim3d/media_S|L|XL`. The page plays the size closest to the number of spaces entered.

```bash
python3 designs/overhaul/case_compact.py Parkstory-overhaul-rev.html Parkstory-overhaul-cc.html \
  '{"34":"designs/overhaul/sim3d/media_S","68":"designs/overhaul/sim3d/media","136":"designs/overhaul/sim3d/media_L","272":"designs/overhaul/sim3d/media_XL"}'
```
