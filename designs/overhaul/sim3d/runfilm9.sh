#!/bin/bash
# "building that could exist" film in the podium design: common 0-100 + apt/off/ret 101-160
cd "$(dirname "$0")"; PY=../bvenv/bin/python; F=film9; o=film9/media; mkdir -p $o $F/common
[ $(ls $F/common | wc -l) -ge 101 ] || $PY render.py $F/scene_film.blend v_apt 0-100 $F/common 75 20 2>&1 | grep -E "frame |rror" | tail -1
for v in v_apt v_off v_ret; do mkdir -p $F/$v
  [ $(ls $F/$v | wc -l) -ge 60 ] || $PY render.py $F/scene_film.blend $v 101-160 $F/$v 75 20 2>&1 | grep -E "frame |rror" | tail -1; done
enc(){ ffmpeg -loglevel error -y -framerate 24 -start_number $3 -i "$2" -vf format=yuv420p -c:v libx264 -preset slow -crf 22 -g 12 -movflags +faststart -an $o/$1.mp4
       ffmpeg -loglevel error -y -framerate 24 -start_number $3 -i "$2" -c:v libvpx-vp9 -b:v 0 -crf 34 -row-mt 1 -g 12 -an $o/$1.webm; }
enc common $F/common/v_apt_%04d.png 0; enc apt $F/v_apt/v_apt_%04d.png 101; enc off $F/v_off/v_off_%04d.png 101; enc ret $F/v_ret/v_ret_%04d.png 101
ffmpeg -loglevel error -y -i $F/common/v_apt_0000.png -q:v 3 $o/poster0.jpg; ffmpeg -loglevel error -y -i $F/v_apt/v_apt_0160.png -q:v 3 $o/poster_end.jpg
echo "FILM DONE $(date +%T)"; ls -la $o
