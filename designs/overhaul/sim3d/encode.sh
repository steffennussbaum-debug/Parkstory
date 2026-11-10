#!/bin/bash
# encodes rendered frames into mp4 + webm clips and posters
set -e
cd "$(dirname "$0")"; mkdir -p media
enc(){ # name pattern start
  ffmpeg -loglevel error -y -framerate 24 -start_number $3 -i "$2" -vf "format=yuv420p" -c:v libx264 -preset slow -crf 22 -g 12 -movflags +faststart -an media/$1.mp4
  ffmpeg -loglevel error -y -framerate 24 -start_number $3 -i "$2" -c:v libvpx-vp9 -b:v 0 -crf 34 -row-mt 1 -g 12 -an media/$1.webm
}
enc common frames/common/v_apt_%04d.png 0
enc apt frames/v_apt/v_apt_%04d.png 101
enc off frames/v_off/v_off_%04d.png 101
enc ret frames/v_ret/v_ret_%04d.png 101
ffmpeg -loglevel error -y -i frames/common/v_apt_0000.png -q:v 3 media/poster0.jpg
ls -la media
