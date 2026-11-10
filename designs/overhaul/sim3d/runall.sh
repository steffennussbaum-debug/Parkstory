#!/bin/bash
cd "$(dirname "$0")"
PY=../bvenv/bin/python
$PY render.py scene.blend v_apt 0-100 frames/common 75 20 2>&1 | grep -E 'frame |rror'
for v in v_apt v_off v_ret; do $PY render.py scene.blend $v 101-160 frames/$v 75 20 2>&1 | grep -E 'frame |rror'; done
echo ALLDONE
