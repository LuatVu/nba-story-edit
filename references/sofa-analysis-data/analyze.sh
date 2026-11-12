#!/bin/bash
cd "$(dirname "$0")"
while IFS='|' read -r k f; do
  [ -f "$f" ] || continue
  echo "### $k"
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  echo "dur=$D" > "m_$k.txt"
  # 1. cắt cảnh
  ffmpeg -hide_banner -nostats -i "$f" -vf "scale=480:-2,select='gt(scene,0.28)',showinfo" -an -f null - 2>&1 \
    | grep -oE "pts_time:[0-9.]+" | cut -d: -f2 > "cuts_$k.txt"
  # 2. khung đen
  ffmpeg -hide_banner -nostats -i "$f" -vf blackdetect=d=0.06:pic_th=0.98:pix_th=0.10 -an -f null - 2>&1 \
    | grep -oE "black_start:[0-9.]+ black_end:[0-9.]+ black_duration:[0-9.]+" > "black_$k.txt"
  # 3. loudness
  ffmpeg -hide_banner -nostats -i "$f" -filter_complex ebur128=peak=true -f null - 2>&1 \
    | grep -E "^ *(I|LRA|Peak):" >> "m_$k.txt"
  # 4. mật độ lời
  ffmpeg -hide_banner -nostats -i "$f" -af "highpass=f=200,lowpass=f=3400,silencedetect=n=-34dB:d=0.4" -f null - 2>&1 \
    | grep -oE "silence_duration: [0-9.]+" | awk '{s+=$2;n++} END{print "silence_total="s; print "silence_n="n}' >> "m_$k.txt"
  echo "   xong $k"
done < files.txt
echo "ALL DONE"
