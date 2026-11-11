#!/bin/bash
# renders one building size: ./runsize.sh S|L|XL
cd "$(dirname "$0")"; z=$1; PY=../bvenv/bin/python
mkdir -p fsz/$z/common fsz/$z/apt
$PY render.py scene_$z.blend v_apt 0-100 fsz/$z/common 75 16 2>&1 | grep -E "frame |rror" | tail -1
$PY render.py scene_$z.blend v_apt 101-160 fsz/$z/apt 75 16 2>&1 | grep -E "frame |rror" | tail -1
echo "SIZE $z DONE"
