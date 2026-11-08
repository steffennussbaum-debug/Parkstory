# Parkstory page in every design

`public/designs/` holds Parkstory's one-page site (Parkstory_13) in its original
look and in the six homepage designs A–F. Content, structure and simulators are
unchanged; only colours, typefaces and finishing differ. A bar at the bottom
switches between the designs (on phones: the "Design" button).

To rebuild after a new version of the page:

    python3 designs/build.py path/to/Parkstory_NN.html public/designs

Served by the site at `/designs/` (`index.html` is the original look,
`design-a.html` … `design-f.html` the designs).
