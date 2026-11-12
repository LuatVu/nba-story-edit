# Số đo video SOFA Zone `dGlI0rts0AI` (Pep Guardiola)

1920×1080 @ 60fps · 13:55 (834,76 s) · đo bằng ffmpeg trên từng frame, 09–10.11.2026.
Đã đưa vào skill `nba-story-edit`. File này giữ lại số gốc để đối chiếu.

## Nhịp cắt
- 374 lần scene-detect thô → gộp burst <0,35 s → **110 điểm chuyển cảnh** (7,9 lần/phút)
- Shot: TB 7,5 s · **trung vị 2,0 s** · dài nhất **103 s không cắt**
- Phân bố: <1 s **33%** · 1–4 s 30% · 4–8 s 15% · >8 s **21%**
- **29% điểm chuyển là hiệu ứng** (burst 5–10 frame @60fps = 0,08–0,17 s), 71% cut thẳng
- Mật độ cắt rất lệch: phút 4 có 165 phát hiện thô, phút 9 và 12 không có lần nào

## Khung đen
6 lần / 13:55, mỗi lần 0,08–0,25 s — 01:55 · 02:53 · 03:08 · 05:04 · 06:36 · 10:47

## Thương hiệu
- Bản đồ phương sai 104 frame: **0% pixel đứng yên** → không có watermark góc
- Frame 0,0 đã là footage có telestration → **không có sting logo mở đầu**
- End card **829 → 834,8 s (~6 s)**: nền xanh ngọc, hoạ tiết chấm halftone, chữ display đậm nén,
  avatar kênh tròn, thanh đáy `LIKE | COMMENT | SHARE | SUBSCRIBE`
- Không có CTA chèn giữa video

## Audio
| | |
|---|---|
| Integrated | **−21,4 LUFS** (quá nhỏ so với chuẩn YouTube −14) |
| True peak | **0,0 dBFS** (đã clip — lỗi, không phải phong cách) |
| LRA | 4,2 LU (nén chặt) |
| Mật độ lời | **96%** thời lượng có giọng; 46 khoảng lặng, TB 0,68 s, tổng 31 s |

## Telestration (quan sát từ frame mẫu)
Vùng tô bán trong suốt có viền trắng + kẻ sọc · mũi tên nét đứt · vòng ellipse dẹt ôm chân
cầu thủ · bảng chiến thuật nền tối chấm số · chân dung cắt nền ghép đè lên bảng chiến thuật.
Telestration **có animation**, biến đổi theo pha bóng.

---

# Mở rộng: đo thêm 4 video (10.11.2026)

`W7ohHAfYAho` Haaland 15:04 · `u6odrTDEMt8` Real–Barca UCL 24:03 ·
`NiyEty2yBcc` PSG 25:23 · `27RC4-w-dy4` Zidane 49:54. Tất cả 1080p60.

## Bảng đầy đủ n=5

| | pep | haaland | ucl | psg | zidane |
|---|---|---|---|---|---|
| Dài | 13:55 | 15:04 | 24:03 | 25:23 | 49:54 |
| Cắt/phút | 7,9 | 5,6 | 7,0 | 6,9 | 5,6 |
| Trung vị shot | 2,00 s | 5,52 s | 4,83 s | 2,55 s | 5,87 s |
| Shot <1 s | 33% | 9% | 14% | 30% | 11% |
| Shot >8 s | 21% | 44% | 34% | 31% | 39% |
| Chuyển có hiệu ứng | 29% | 1% | 7% | 23% | 5% |
| Khung đen | 6 | 4 | 29 | 40 | 28 |
| Khung đen dài nhất | 0,25 s | 0,08 s | 0,30 s | **1,48 s** | 0,32 s |
| Integrated | −21,4 | −19,6 | −20,4 | −19,5 | −20,1 LUFS |
| LRA | 4,2 | 3,9 | 5,2 | 4,1 | 4,7 LU |
| True peak | +0,0 | +0,1 | +0,3 | +0,0 | +0,1 dBFS |
| Mật độ lời | 96% | 98% | 97% | 96% | 97% |

## Phân bố khung đen (101 khung, không kể pep)
trung vị **0,08 s** · p75 0,13 s · p90 0,22 s · max 1,48 s
**95% dưới 0,35 s**; chỉ 5 lần trên 0,5 s, tất cả nằm trong psg.

## Tương quan đáng chú ý
Video cắt nhanh (trung vị 2,0–2,6 s) dùng nhiều hiệu ứng chuyển (23–29%).
Video cắt chậm (trung vị 4,8–5,9 s) gần như chỉ cut thẳng (1–7%). Hai thứ đi cặp với nhau.

## Tỉ lệ thời lượng theo loại hình (n=4, 685 mẫu 1 khung/10 s)

| | sân cỏ | nền tối | khác |
|---|---|---|---|
| haaland | 51% | 14% | 34% |
| psg | 38% | 24% | 38% |
| ucl | 24% | 27% | 49% |
| zidane | 16% | 36% | 48% |
| **gộp** | **27%** | **29%** | **44%** |

## Bumper logo mờ (khung đen, logo xám tối ở giữa)
haaland 0 lần · zidane 1 · ucl 4 · psg 7 → ~1,8% thời lượng

## Mở đầu (n=5)
Đồ hoạ thiết kế: haaland (số "100" + ảnh cắt nền) · psg (nền sao trời + "??") ·
zidane (dòng thời gian thẻ ảnh trên nền sao trời).
Footage: pep (telestration) · ucl (ăn mừng, bloom mạnh).
**Không video nào có sting logo mở đầu.**

## End card (n=5) — luôn có, 4–6 s, toàn khung
Kiểu A cảm ơn (pep, haaland) · kiểu B bằng chứng xã hội (psg, zidane) ·
kiểu C cộng đồng (ucl). Chung: nền xanh thương hiệu, chấm halftone, ký hiệu `»`,
panel logo, thanh CTA ở đáy.

## Khung hình chủ đạo
Footage **lồng trong hình chữ nhật bo góc** trên **nền lưới ô vuông rất tối**, có HUD giả
ở đáy (`▶ 20`, `Replay ▶|`) và đôi khi timecode. Full-bleed là ngoại lệ.

## Khung lồng footage (9 frame, 4 video)
Bề rộng **69%–95%** chiều ngang, TB **82%**. Footage thật ~**1571×900 px** = 69% pixel của 1080p.
Chi tiết: haaland_490 88% · haaland_90 88% · psg_1400 76% · psg_760 76% · ucl_1290 85% ·
ucl_140 77% · zidane_1200 69% · zidane_1660 95% · haaland_360 98% (full-bleed).

## Độ dài shot: footage so với đồ hoạ
| | footage | đồ hoạ/chân dung |
|---|---|---|
| haaland | trung vị 17,4 s (TB 22,4 · max 58,1) | trung vị 3,5 s |
| ucl | trung vị 10,2 s (TB 17,0 · max 63,0) | trung vị 4,6 s |

Kiểm chứng bằng 3 phương pháp trên một đoạn footage 58 s của haaland:
scene@0,28 → 0 cắt trong · scene@0,10 → 47 (bắt nhầm chuyển động) ·
đột biến frame-to-frame → **3 cắt thật** (mốc 24,4 / 45,3 / 57,9 s).
Kết luận: footage thật sự được giữ lâu, ~12–24 s mỗi shot.

## Nhạc nền (đo dải 20–70 Hz, dưới tần số cơ bản giọng nam)

| | haaland | ucl | psg | zidane |
|---|---|---|---|---|
| Có nhạc | 79% | 76% | 76% | 76% |
| Số đoạn có nhạc | 15 | 25 | 25 | 35 |
| Trung vị đoạn nhạc | 40 s | 36 s | 28 s | 46 s |
| Số đoạn vắng nhạc | 19 | 26 | 24 | 35 |
| Trung vị đoạn vắng | 7 s | 11 s | 12 s | 10 s |
| Vắng dài nhất | 22 s | 44 s | 64 s | 106 s |
| Điểm đổi nhạc | 6 | 9 | 11 | 20 |
| **Đổi nhạc / phút** | **0,40** | **0,38** | **0,43** | **0,40** |

Hằng số chặt nhất cả bộ mẫu: ~0,4 lần đổi nhạc/phút, giữ nguyên từ 15 đến 50 phút.
Giới hạn: ngưỡng dựa dải trầm nên nhạc ambient không bass có thể bị tính nhầm là "vắng".

## Cân bằng giọng / nhạc

Phương pháp: dải 20–70 Hz = mức nhạc, dải 200–3400 Hz = mức giọng.
So "đang nói liên tục" với "im giọng liên tục ≥1,5 s".

| | zidane | psg |
|---|---|---|
| Mẫu đang nói | 1434 s | 651 s |
| Mẫu im giọng ≥1,5 s | 12 s | 10 s |
| Nhạc bị hạ khi có giọng | 10,6 dB | 4,2 dB |
| **Giọng nổi trên nhạc (dải giọng)** | **24,9 dB** | **23,1 dB** |

Kết luận: con số **23–25 dB** vững (mẫu lớn). Phần duck động **không kết luận được** —
mật độ lời 96–98% khiến cả video 50 phút chỉ còn 12 s im giọng liên tục, và ở những
khoảng đó người dựng có thể chủ động đẩy nhạc lên chứ không phải compressor nhả.

Lần đo đầu cho kết quả sai (0,5 và −0,1 dB) vì ngưỡng tương đối bắt nhầm khoảng nghỉ
giữa các từ làm "im giọng"; đã sửa bằng cách yêu cầu im liên tục ≥1,5 s.
