#!/bin/bash
# renders and encodes building sizes: ./runsz9.sh 20 40 60
cd "$(dirname "$0")"; PY=../bvenv/bin/python
for n in "$@"; do
  mkdir -p fsz9/$n/common fsz9/$n/apt
  [ $(ls fsz9/$n/common | wc -l) -ge 101 ] || $PY render.py sz9/scene_$n.blend v_apt 0-100 fsz9/$n/common 75 16 2>&1 | grep -E "frame |rror" | tail -1
  [ $(ls fsz9/$n/apt | wc -l) -ge 60 ] || $PY render.py sz9/scene_$n.blend v_apt 101-160 fsz9/$n/apt 75 16 2>&1 | grep -E "frame |rror" | tail -1
  o=media9/$n; mkdir -p $o
  ffmpeg -loglevel error -y -framerate 24 -i fsz9/$n/common/v_apt_%04d.png -vf format=yuv420p -c:v libx264 -preset slow -crf 22 -g 12 -movflags +faststart -an $o/common.mp4
  ffmpeg -loglevel error -y -framerate 24 -i fsz9/$n/common/v_apt_%04d.png -c:v libvpx-vp9 -b:v 0 -crf 34 -row-mt 1 -g 12 -an $o/common.webm
  ffmpeg -loglevel error -y -framerate 24 -start_number 101 -i fsz9/$n/apt/v_apt_%04d.png -vf format=yuv420p -c:v libx264 -preset slow -crf 22 -g 12 -movflags +faststart -an $o/apt.mp4
  ffmpeg -loglevel error -y -framerate 24 -start_number 101 -i fsz9/$n/apt/v_apt_%04d.png -c:v libvpx-vp9 -b:v 0 -crf 34 -row-mt 1 -g 12 -an $o/apt.webm
  ffmpeg -loglevel error -y -i fsz9/$n/common/v_apt_0000.png -q:v 3 $o/poster0.jpg; ffmpeg -loglevel error -y -i fsz9/$n/apt/v_apt_0160.png -q:v 3 $o/poster_end.jpg
  echo "SIZE $n DONE $(date +%T)"
done
