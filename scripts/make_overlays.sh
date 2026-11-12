#!/usr/bin/env bash
# Sinh các overlay cần cho treatment look. Chỉ cần ffmpeg, chạy một lần.
#   ./make_overlays.sh [outdir]       (mặc định: ../assets)
set -euo pipefail

OUT="${1:-$(cd "$(dirname "$0")/.." && pwd)/assets}"
mkdir -p "$OUT"
W=1920; H=1080

command -v ffmpeg >/dev/null || { echo "Cần ffmpeg: brew install ffmpeg" >&2; exit 1; }

# Font cho HUD giả (macOS). Đổi nếu máy khác.
FONT=""
for f in /System/Library/Fonts/Supplemental/Courier\ New\ Bold.ttf \
         /System/Library/Fonts/Menlo.ttc \
         /Library/Fonts/Courier\ New\ Bold.ttf; do
  [ -f "$f" ] && FONT="$f" && break
done

echo "→ scanlines.png"
ffmpeg -y -loglevel error -f lavfi -i "color=c=black:s=${W}x${H}" \
  -vf "format=rgba,geq=r='255':g='255':b='255':a='if(lt(mod(Y\,3),1),110,0)'" \
  -frames:v 1 "$OUT/scanlines.png"

echo "→ vignette.png  (đặt lên trên, blend Normal, opacity 55-80%)"
ffmpeg -y -loglevel error -f lavfi -i "color=c=black:s=${W}x${H}" \
  -vf "format=rgba,geq=r='0':g='0':b='0':a='clip(255*2.1*(hypot(X-W/2\,Y-H/2)/(0.70*hypot(W/2\,H/2))-1)\,0,255)'" \
  -frames:v 1 "$OUT/vignette.png"

echo "→ matte_rounded.png  (dùng với Track Matte Key, Matte = Luma)"
ffmpeg -y -loglevel error -f lavfi -i "color=c=black:s=${W}x${H}" \
  -vf "format=gray,geq=lum='if(gt(pow(max(0\,abs(X-W/2)-(W/2-56))\,2)+pow(max(0\,abs(Y-H/2)-(H/2-56))\,2)\,56*56),0,255)'" \
  -frames:v 1 "$OUT/matte_rounded.png"

echo "→ matte_crt.png  (bo góc mạnh hơn cho treatment C)"
ffmpeg -y -loglevel error -f lavfi -i "color=c=black:s=${W}x${H}" \
  -vf "format=gray,geq=lum='if(gt(pow(max(0\,abs(X-W/2)-(W/2-130))\,2)+pow(max(0\,abs(Y-H/2)-(H/2-130))\,2)\,130*130),0,255)'" \
  -frames:v 1 "$OUT/matte_crt.png"

echo "→ grain.mp4  (6s loop, 960x540 - scale 200% trong Premiere, blend Overlay hoặc Soft Light, opacity 12-25%)"
ffmpeg -y -loglevel error -f lavfi -i "color=c=gray:s=960x540:d=6:r=25" \
  -vf "noise=alls=34:allf=t+u,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 30 "$OUT/grain.mp4"

if [ -n "$FONT" ]; then
  echo "→ hud_overlay.png  (ký hiệu camera giả, blend Normal, opacity 70%)"
  # vẽ chữ trắng trên nền đen rồi lấy chính độ sáng làm alpha -> nền trong suốt
  ffmpeg -y -loglevel error -f lavfi -i "color=c=black:s=${W}x${H}:d=1" \
    -vf "\
drawtext=fontfile='${FONT}':text='F7':x=96:y=64:fontsize=26:fontcolor=white@0.75,\
drawtext=fontfile='${FONT}':text='UNFOLD 2016TX':x=760:y=64:fontsize=26:fontcolor=white@0.75,\
drawtext=fontfile='${FONT}':text='XM':x=1760:y=64:fontsize=26:fontcolor=white@0.75,\
drawtext=fontfile='${FONT}':text='> 20':x=360:y=980:fontsize=24:fontcolor=white@0.65,\
drawtext=fontfile='${FONT}':text='> 22':x=1440:y=980:fontsize=24:fontcolor=white@0.65,\
drawtext=fontfile='${FONT}':text='Replay >|':x=880:y=1012:fontsize=28:fontcolor=white@0.85,\
format=rgb24,split[c][m];[m]format=gray[a];[c][a]alphamerge,format=rgba" \
    -frames:v 1 "$OUT/hud_overlay.png"
else
  echo "! bỏ qua hud_overlay.png — không tìm thấy font monospace, sửa biến FONT trong script"
fi

echo
echo "Xong. Asset ở: $OUT"
ls -la "$OUT"
