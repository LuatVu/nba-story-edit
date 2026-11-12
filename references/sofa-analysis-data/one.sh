#!/bin/bash
# phân tích 1 video: one.sh <key> <path>
cd "$(dirname "$0")"
k="$1"; f="$2"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" | sed 's/^/dur=/' > "m_$k.txt"
ffmpeg -hide_banner -nostats -i "$f" -vf "scale=320:-2,select='gt(scene,0.28)',showinfo" -an -f null - 2>&1 \
  | grep -oE "pts_time:[0-9.]+" | cut -d: -f2 > "cuts_$k.txt"
ffmpeg -hide_banner -nostats -i "$f" -vf blackdetect=d=0.06:pic_th=0.98:pix_th=0.10 -an -f null - 2>&1 \
  | grep -oE "black_duration:[0-9.]+" > "black_$k.txt"
ffmpeg -hide_banner -nostats -i "$f" -filter_complex ebur128=peak=true -f null - 2>&1 \
  | grep -E "^ *(I|LRA|Peak):" >> "m_$k.txt"
ffmpeg -hide_banner -nostats -i "$f" -af "highpass=f=200,lowpass=f=3400,silencedetect=n=-34dB:d=0.4" -f null - 2>&1 \
  | grep -oE "silence_duration: [0-9.]+" | awk '{s+=$2;n++} END{print "silence_total="s; print "silence_n="n}' >> "m_$k.txt"
echo "DONE $k"
