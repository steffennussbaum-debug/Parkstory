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

## Podium design and nine building sizes

The building is a typical multifamily building on a podium garage: shops at street level, the garage in the podium,
a planted terrace on the podium roof, and residential floors above with punched windows, brick and panel bays and
steel balconies. `sim3d/scene_size.py` builds it for any number of spaces (`NCARS`, `LP` levels, `NCOL` columns).

The case study now has nine sizes: 20, 40, 60, 80, 100, 150, 200, 250 and 300 spaces. The page plays the next size
up from the number entered; above 300 it plays the 300 building.

```bash
for cfg in "20 2 10" "40 2 14" "60 2 21" "80 4 14" "100 4 18" "150 4 26" "200 6 23" "250 8 22" "300 8 26"; do set -- $cfg
  NCARS=$1 LP=$2 NCOL=$3 python designs/overhaul/sim3d/scene_size.py sz9/scene_$1.blend; done
designs/overhaul/sim3d/runsz9.sh 20 40 60          # render + encode to sim3d/media9/<n> (run in batches)
NCARS=68 LP=4 NCOL=13 python designs/overhaul/sim3d/scene_size.py film9/scene_film.blend
designs/overhaul/sim3d/runfilm9.sh                 # landing-page film (apartments, offices, retail) -> film9/media
python3 designs/overhaul/case_compact.py Parkstory-overhaul-rev.html cc9.html '{"20":".../media9/20", ..., "300":".../media9/300"}'
python3 designs/overhaul/swap_film.py cc9.html cc9f.html designs/overhaul/sim3d/media designs/overhaul/sim3d/film9/media
```

Then build from `cc9f.html` with `designs/build.py`, `topics.py` and `seo_post.py` as above.
