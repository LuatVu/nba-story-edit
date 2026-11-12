# Premiere recipes

## Cách gọi tool

MCP server `premiere-pro` chỉ quảng cáo 5 tool, catalog thật hơn 280 tool.

1. `verify_premiere_connection` — luôn gọi đầu tiên.
   Nếu trả `retry:false` + `userActionRequired:true` → đọc nguyên văn `nextStep` cho user, DỪNG.
2. `search_tools` với `query` ngôn ngữ tự nhiên ("apply effect to clip", "create title",
   "import media") hoặc `pattern` regex (`^list_`, `mogrt`). `detail=schema` để lấy tham số.
3. `invoke_tool` với đúng tên tìm được.

**Không bịa tên tool.** Tên dưới đây là **tên effect của Premiere**, không phải tên MCP tool.

## Thứ tự layer — quan trọng

Đã kiểm chứng bằng render thật. Sai thứ tự là hỏng look:

```
V4  hud_overlay.png        ← NGOÀI khung, không bị bo góc
V3  [khung đã bo góc]      ← Track Matte Key với matte_*.png
V2    grain.mp4            ← TRONG khung
V1    footage + scanlines + vignette + Lumetri   ← TRONG khung
V0  nền đen
```

Scanline, grain, vignette nằm **trong** khung. HUD nằm **ngoài**. Nền quanh khung là đen tuyệt đối.

---

## Treatment A — Broadcast (2015–nay)

| Lớp | Effect | Thông số |
|---|---|---|
| 1 | Lumetri Color | Contrast +12, Shadows −8, Shadow Tint ngả teal (hue ~195), Saturation 92 |
| 2 | Lumetri → Vignette | Amount −1.2, Midpoint 55, Roundness 0, Feather 60 |
| 3 | Transform | Scale 100 (full-bleed) hoặc 96 nếu muốn viền mỏng |

Không scanline, không HUD. Đây là treatment mặc định, dùng ~60% thời lượng.

---

## Treatment B — Camcorder (2005–2014)

| Lớp | Effect | Thông số |
|---|---|---|
| 1 | Transform | Scale 92 |
| 2 | Lumetri | Contrast +8, Saturation 85, Highlights −10 |
| 3 | `assets/grain.mp4` trên track trên | Blend **Overlay**, Opacity 14%, Scale 200% |
| 4 | `assets/matte_rounded.png` + **Track Matte Key** | Matte = Luma, áp lên clip đã scale |
| 5 | `assets/hud_overlay.png` track trên cùng | Blend Normal, Opacity 70% |

---

## Treatment C — CRT archive (1990–2004)

| Lớp | Effect | Thông số |
|---|---|---|
| 1 | Transform | Scale 78 |
| 2 | Lumetri | Saturation 55, Contrast +8, Highlights −15, Blacks +6 (bạc màu) |
| 3 | Lens Distortion | Curvature +6, Fill Alpha off |
| 4 | Offset (bản sao clip, blend Screen) | Shift Center +3px trục X, chỉ kênh đỏ → tách màu nhẹ |
| 5 | `assets/scanlines.png` | Blend **Soft Light**, Opacity 45% |
| 6 | `assets/grain.mp4` | Blend Overlay, Opacity 22%, Scale 200% |
| 7 | `assets/vignette.png` | Blend Normal, Opacity 75% |
| 8 | `assets/matte_crt.png` + Track Matte Key | Matte = Luma |
| 9 | `assets/hud_overlay.png` | Opacity 70% |

**C+ (trước 1990):** như C, thêm Lumetri Saturation 35 và keyframe Opacity nhấp nháy
nhẹ (100 → 94 → 100) chu kỳ ~0.5s.

---

## Treatment D — Cinema plate

Dùng tối đa 2 lần/video, cho khoảnh khắc lớn nhất.

1. Ảnh rạp chiếu trống làm nền (tự mua stock hoặc render 3D, **không** lấy từ video gốc).
2. Footage đặt trên, áp **Corner Pin**, kéo 4 góc khớp màn hình trong ảnh.
3. Lumetri trên footage: Exposure −0.3, Contrast +15 (màn chiếu không bao giờ sáng bằng trực tiếp).
4. Gaussian Blur 1.5 lên footage.
5. Thêm một Adjustment Layer phủ toàn khung: Lumetri Vignette −1.8.

---

## Chapter card

1. **Color Matte** đen, dài 2.6s.
2. `assets/grain.mp4` lên trên, blend Overlay, Opacity 12%.
3. **Essential Graphics → Text**: EB Garamond Italic, 68px, trắng,
   Position x=290 y=500 (khung 1920×1080), canh trái.
4. Hiệu ứng máy đánh chữ: áp **Linear Wipe** lên layer text,
   Wipe Angle 270°, keyframe Transition Complete 100 → 0 trong (số ký tự ÷ 22) giây, Feather 0.
5. Giữ 1.2s sau khi chữ xong.
6. Cắt sang footage bằng cut thẳng, không dissolve.

**Black frame 0.4–0.8s trước mỗi chapter card.** Đây là nhịp thở, không phải lỗi.

---

## Chart scroll

1. `scripts/make_chart.py --mode dumbbell ... --tall` → PNG cao (vd 1920×5400).
2. Import, đặt lên sequence, Scale 100.
3. Keyframe **Motion → Position** trục Y: từ `(H_png − 1080)/2` xuống `−(H_png − 1080)/2`.
4. Ease In/Ease Out ở cả hai keyframe. Tốc độ: khoảng **420 px/giây** — đủ đọc kịp.
5. Nếu chỉ cần một phần, dùng `--slice 0:12` để chỉ render 12 dòng đầu.

Chart đã animate sẵn (`--video`) thì import như clip thường, không cần keyframe.

---

## Tactical board (bóng rổ)

Premiere không dựng được sơ đồ động phức tạp. Cách làm:
1. Nền nửa sân (PNG 1920×1080, nền đen, đường kẻ `#2A2A2A`) — tự vẽ một lần rồi tái dùng.
2. Mỗi cầu thủ = một **Ellipse shape** trong Essential Graphics, fill bằng ảnh cầu thủ
   (Appearance → Fill → Image), viền 3px.
3. Chấm `#E8912A` cho nhân vật chính, `#FFFFFF` cho đồng đội, `#555555` cho đối thủ.
4. Di chuyển = keyframe Position của từng shape. Mũi tên = Pen tool + Linear Wipe.

Nếu cần nhiều hơn 8 object chuyển động → làm ở After Effects, xuất `.mogrt`, import vào Premiere.

---

## Chuyển cảnh — đo từ `dGlI0rts0AI`

Trong 110 điểm chuyển cảnh: **71% cut thẳng, 29% có hiệu ứng** dài 5–10 frame @60fps
(0.08–0.17 s). Ở 29.97fps là **3–5 frame**. Rất ngắn — nó là cú hích, không phải transition
kiểu đám cưới.

| Dùng ở | Hiệu ứng | Thông số |
|---|---|---|
| Trong một chuỗi montage | **Whip pan** | Transform → Position trượt ngang 1 chiều rộng khung trong 3 frame + Directional Blur 40 |
| Đổi chủ đề trong cùng chapter | **Zoom blur** | Transform Scale 100→115 trong 4 frame + Gaussian Blur 0→12→0 |
| Vào khoảnh khắc lớn | **Dip to black 3 frame** | Dip to Black, dài 0.10 s |

Không dùng Cross Dissolve dài, không dùng flash trắng (xem ghi chú thị trường Mỹ trong
`visual-spec.md`).

## Telestration

Premiere làm được cả 4 loại mà không cần After Effects:

1. **Vùng tô** — Essential Graphics → Pen tool vẽ đa giác ôm khu vực.
   Fill màu accent **Opacity 28%**, Stroke trắng 3px.
   Animate: keyframe từng điểm neo của Pen theo pha bóng, hoặc đơn giản hơn là
   **Linear Wipe** lên chính shape để nó lớn dần.
2. **Mũi tên** — Pen tool vẽ đường, Stroke 5px, bật **Dashes** cho nét đứt.
   Animate bằng **Linear Wipe**, Wipe Angle theo hướng mũi tên.
3. **Vòng chân cầu thủ** — Ellipse dẹt (Scale Height ~35%), Stroke 4px, Fill 20%.
   Bám theo cầu thủ bằng **Motion → Position** keyframe, hoặc Track Motion nếu cảnh ổn định.
4. **Bảng chiến thuật** — xem mục "Tactical board" bên dưới.

**Luôn animate.** Telestration đứng yên trông như ảnh chụp màn hình.

## Chart reveal — bake bằng ffmpeg, đừng keyframe trong Premiere

Keyframe qua API của Premiere không đáng tin cho ảnh tĩnh (xem "Bẫy đã gặp" cuối file).
Cách chắc ăn: che vùng bằng `drawbox` rồi gỡ che đúng mốc, render ra MP4, import như clip thường.

```bash
# mỗi vùng một drawbox, enable='lt(t,T)' = chỉ che TRƯỚC mốc T
ffmpeg -y -loop 1 -i chart.png \
  -vf "drawbox=x=0:y=123:w=1920:h=85:color=black:t=fill:enable='lt(t,1.0)',\
drawbox=x=0:y=209:w=1920:h=85:color=black:t=fill:enable='lt(t,2.35)',\
format=yuv420p" \
  -t 19.9 -r 30000/1001 -c:v libx264 -preset medium -crf 14 chart_anim.mp4
```

Lấy toạ độ vùng bằng cách dò dải màu accent trong PNG (numpy: tìm hàng pixel có màu `#E8912A`).

### Typewriter cho chapter card — cũng bake

Quét **đúng bề ngang của chữ**, không quét cả khung. Chữ thường chỉ chiếm 40–55% chiều ngang;
quét cả khung thì chữ hiện xong ở 40% thời gian, phần còn lại vệt quét chạy trên nền đen trống.

```bash
# x0,x1 = mép trái/phải của chữ (đo từ PNG); D = số ký tự ÷ 22
ffmpeg -y -f lavfi -i color=black:s=1920x1080:r=30000/1001:d=2.7 \
       -loop 1 -i card.png \
       -f lavfi -i color=black:s=1920x1080:r=30000/1001:d=2.7 \
  -filter_complex "[0:v][1:v]overlay=0:0[b];[b][2:v]overlay=x='X0+(X1-X0)*min(1,t/D)':y=0:shortest=1,format=yuv420p" \
  -t 2.7 -c:v libx264 -crf 14 card_anim.mp4
```

## Grain phủ toàn video

Render sẵn một file grain đúng độ dài và đúng khung hình thay vì lặp clip ngắn 80 lần:

```bash
ffmpeg -y -stream_loop 100 -i assets/grain.mp4 -t 480 \
  -vf "scale=1920:1080:flags=bicubic,fps=30000/1001" -an \
  -c:v libx264 -crf 16 -pix_fmt yuv420p grain_480s.mp4
```

Đặt lên track trên cùng, **Blend Mode Overlay** (trong Premiere là enum, `13`), **Opacity 8%**.

⚠️ **Grain phải tránh mọi vùng mà track dưới trong suốt** — black frame, và chapter card đang
bị wipe. Ở đó không có gì để blend nên grain hiện thành **mảng xám** giữa khung. Cắt grain
thành nhiều đoạn, chừa các khoảng đó ra. Overlay vốn không tác động lên đen tuyệt đối nên
chừa ra cũng không mất gì.

## End card

6 giây cuối. Nền phẳng một màu (xem `visual-spec.md` cho bảng màu Turn On Hoops), logo kênh
hình tròn, chữ display lớn, một dòng CTA chữ thường ở đáy. Không đọc CTA bằng lời.

## Bẫy đã gặp — đọc trước khi debug

| Triệu chứng | Nguyên nhân thật |
|---|---|
| `apply_effect "Linear Wipe"` báo không tạo component | Premiere 2026 đặt tên là **`Linear Wipe (Legacy)`**. Gọi `list_available_effects` để lấy tên đúng. |
| Keyframe thêm xong nhưng render không đổi | `time` của `add_keyframe` tính theo **source time của clip**, không phải timeline. Ảnh tĩnh có inPoint ở **~3600 s** (Premiere đặt gốc ở mốc 1 giờ). Lấy inPoint bằng `list_clip_effects`. |
| `set_keyframe_interpolation` chạy xong thì hiệu ứng mất | Nó **xoá giá trị keyframe về 0**. Phải set interpolation **trước**, rồi mới ghi lại giá trị. Tham số tên là `property`, không phải `paramName`. |
| `set_blend_mode` báo "Illegal Parameter type" | Blend mode là **enum số**, không phải chuỗi. Overlay = `13`. |
| `import_folder` báo `targetBin.importFiles is not a function` | Tool hỏng. Dùng `import_media` từng file. |
| Hở 1 frame đen giữa hai clip liền nhau | Premiere làm tròn theo frame. Đặt clip trước **dài hơn 0.1–0.15 s**, rồi đặt clip sau đè lên — overwrite sẽ cắt khớp. |
| Xuất frame kiểm tra thấy sai mốc | **`export_frame` lệch 0.1%** (29.97 vs 30 fps). Ở phút thứ 6 lệch ~0.4 s. Muốn đúng mốc T thì yêu cầu **T ÷ 0.999**. |
| Nhạc dồn hết về đầu file sau khi dựng bằng ffmpeg | `adelay` nhận **mili giây nguyên**. Ghép chuỗi `"12.05"+"000"` ra 12 ms. Tính `int(round(giây*1000))`. |

## Export

- H.264, VBR 2-pass, Target 16 Mbps / Max 24 Mbps, 1920×1080, khung hình khớp sequence
- Audio AAC 320 kbps 48 kHz
- Bật **Use Maximum Render Quality** (grain và scanline rất nhạy với downscale)
