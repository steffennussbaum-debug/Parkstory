#!/bin/bash
cd "$(dirname "$0")"; z=$1; o=media_$z; mkdir -p $o
enc(){ nice -n 10 ffmpeg -loglevel error -y -framerate 24 -start_number $3 -i "$2" -vf format=yuv420p -c:v libx264 -preset slow -crf 22 -g 12 -movflags +faststart -an $o/$1.mp4; nice -n 10 ffmpeg -loglevel error -y -framerate 24 -start_number $3 -i "$2" -c:v libvpx-vp9 -b:v 0 -crf 34 -row-mt 1 -g 12 -an $o/$1.webm; }
enc common fsz/$z/common/v_apt_%04d.png 0
enc apt fsz/$z/apt/v_apt_%04d.png 101
ffmpeg -loglevel error -y -i fsz/$z/common/v_apt_0000.png -q:v 3 $o/poster0.jpg
ffmpeg -loglevel error -y -i fsz/$z/apt/v_apt_0160.png -q:v 3 $o/poster_end.jpg
ls -la $o
