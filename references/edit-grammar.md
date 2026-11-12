# Edit grammar — đo từ SOFA Zone

Nguồn đo: `twu12g-DL9A` "Champions League Has Become IMPOSSIBLE To Win?" (19:31, 375K views,
video có view cao nhất kênh tại thời điểm đo), `ZxKZ9PwVCv8` (22:14), và `dGlI0rts0AI`
(Pep Guardiola, 13:55, 1080p60) — video thứ ba đo bằng máy, chi tiết ở mục cuối file.

**Hai video đầu đo bằng mắt, video thứ ba đo bằng ffmpeg trên từng frame.** Chỗ nào mâu thuẫn
thì tin số đo máy; đã sửa trực tiếp trong file này và ghi rõ chỗ sửa.

## Cấu trúc tổng

Chapter map thật của video 19:31, kèm thời lượng tính ra:

| Vào | Chapter | Dài |
|---|---|---|
| 00:00 | The Champions League of the Past | 2:47 |
| 02:47 | Where Are the Underdogs Today? | 1:36 |
| 04:23 | The Rich-Poor Divide | 1:57 |
| 06:20 | The Wall No One Can Break | 1:52 |
| 08:12 | The Managerial Advantage | 1:42 |
| 09:54 | Already Beaten Before Kick-Off? | 2:19 |
| 12:13 | No More Home Advantage? | 1:15 |
| 13:28 | The Game of Probability | 1:14 |
| 14:42 | The Human Factor | 1:38 |
| 16:20 | Big-Game Experience | 1:02 |
| 17:22 | Is It Impossible? | 2:09 |

**Công thức rút ra:**

- Cold open dài: **2:30–3:00**, chiếm ~14% thời lượng. Hoài niệm, dựng cảm xúc,
  kết bằng câu hỏi trung tâm. Không vội vào luận điểm.
- Thân bài: **8–10 chapter, trung bình 1:37** (đo được 97 giây). Mỗi chapter đúng một nguyên nhân.
- Payoff: **~2:00**, chiếm ~11%. Trả lời câu hỏi ở cold open.
- Tổng **10–25 phút** cho video thường. Flagship 36–65 phút (có, nhưng hiếm, thường là collab).

Áp cho NBA: giữ nguyên tỉ lệ. Video 16 phút = cold open 2:15 + 8 chapter × 1:35 + payoff 1:45.

## Nhịp trong chapter

- Mở chapter: black frame → chapter card (typewriter) → vào footage.
  ⚠️ **ĐÃ SỬA, xác nhận trên 5 video:** black frame **luôn rất ngắn, 0.08–0.30 s**, không bao
  giờ 0.4–0.8 s. Số lần thì tuỳ video (4 đến 29 lần). Dùng 0.15–0.25 s.
- Trong chapter: shot trung bình ngắn, cắt theo câu narration, không theo nhịp nhạc.
  Một câu VO = 1–3 shot.
- Footage luôn có treatment (xem visual-spec). Không bao giờ cắt vào clip thô.
- ⚠️ **ĐÃ SỬA hai lần.** Chuyển cảnh có hiệu ứng dao động **1%–29%** tuỳ video
  (haaland 1%, ucl 7%, pep 29%). **Mặc định là cut thẳng**; hiệu ứng chỉ dùng ở điểm nhấn.
  Công thức ở `premiere-recipes.md` mục "Chuyển cảnh".
- Chart xuất hiện ngay khi narration nói ra con số, không trễ.

## Thủ pháp đặc trưng (giữ nguyên khi sang NBA)

1. **Frame-within-frame** — footage lồng trong khung đen bo góc, có HUD giả
   ("F7 UNFOLD 2016TX", "▶ 20", "Replay ▶|" ở đáy). Tạo cảm giác đang xem lại băng tư liệu.
2. **CRT archive** — tư liệu cũ bo góc mạnh kiểu màn hình lồi, scanline, nhiễu màu, vignette nặng.
3. **Cinema plate** — footage chiếu trên màn hình trong rạp chiếu phim trống.
   Dùng tiết chế: 1–2 lần/video, cho khoảnh khắc lớn nhất.
4. **Tactical board** — sơ đồ sân nền đen, chấm tròn có ảnh cầu thủ bên trong, chấm vàng
   đánh dấu nhân vật chính. Sang NBA = sơ đồ nửa sân, half-court set.
5. **Chapter card** — nền đen + grain, chữ serif nghiêng trắng, canh trái ~15% chiều ngang,
   ~45% chiều cao, hiện kiểu máy đánh chữ.
6. **Chart scroll** — biểu đồ dựng dọc rất dài, camera trôi xuống chậm thay vì cắt từng phần.

## Những thứ KHÔNG mang sang

- Tiêu đề ALL CAPS + hậu tố "| SOFA Zone". Khán giả Mỹ đọc là spam.
- Thumbnail viền màu + badge series + chữ gradient to. Xem visual-spec.
- Track phụ đề burn-in.
- Dùng lại compilation của kênh khác (có watermark người khác trong frame).


---

## Số đo nhiều video — ĐỌC MỤC NÀY TRƯỚC KHI TIN BẤT KỲ CON SỐ NÀO

Đã đo bằng máy 5 video. **Kết quả: phần lớn "quy tắc" rút ra từ một video là sai.**
Dưới đây ghi rõ cái gì là hằng số của kênh, cái gì chỉ là đặc điểm của một video.

| | pep | haaland | ucl | psg | zidane | biên độ |
|---|---|---|---|---|---|---|
| Dài | 13:55 | 15:04 | 24:03 | 25:23 | 49:54 | |
| **Cắt/phút** | 7.9 | 5.6 | 7.0 | 6.9 | 5.6 | **5.6–7.9** ổn định |
| Trung vị shot | 2.00 s | 5.52 s | 4.83 s | 2.55 s | 5.87 s | ⚠️ 2.0–5.9 s |
| Shot < 1 s | 33% | 9% | 14% | 30% | 11% | ⚠️ 9–33% |
| Shot > 8 s | 21% | 44% | 34% | 31% | 39% | ⚠️ 21–44% |
| Chuyển có hiệu ứng | 29% | 1% | 7% | 23% | 5% | ⚠️ **1–29%** |
| Khung đen (số lần) | 6 | 4 | 29 | 40 | 28 | ⚠️ 4–40 |
| Khung đen dài nhất | 0.25 s | 0.08 s | 0.30 s | **1.48 s** | 0.32 s | |
| **Integrated** | −21.4 | −19.6 | −20.4 | −19.5 | −20.1 | **−21.4…−19.5** ổn định |
| **LRA** | 4.2 | 3.9 | 5.2 | 4.1 | 4.7 | **3.9–5.2** ổn định |
| **True peak** | +0.0 | +0.1 | +0.3 | +0.0 | +0.1 | **đều clip** |
| **Mật độ lời** | 96% | 98% | 97% | 96% | 97% | **96–98%** ổn định |

Bộ mẫu trải từ 14 đến 50 phút, đủ để tách quy tắc khỏi ngẫu nhiên.

### Hằng số thật của kênh (tin được)

1. **Giọng kể gần như không ngừng: 96–98% thời lượng.** Đây là quy tắc chắc chắn nhất.
   Khoảng lặng không phải công cụ của họ. Viết script đủ chữ để lấp gần hết thời lượng.
2. **Nén rất chặt: LRA 3.9–5.2 LU.** Không có đoạn to đoạn nhỏ.
3. **Khung đen gần như luôn là một cái chớp.** Gộp 101 khung đen đo được:
   **trung vị 0.08 s, 95% dưới 0.35 s**. Nhưng có ngoại lệ — psg có 5 lần dài tới **1.48 s**.
   Nên quy tắc là: **mặc định 0.08–0.15 s** (chớp giữa hai shot), và **chỉ 3–5 lần mỗi video
   mới dùng 1–1.5 s** cho khoảng nghỉ thật sự. Quy tắc cũ "mỗi chapter một black frame
   0.4–0.8 s" sai ở cả 5 video — không video nào làm vậy.
4. **Luôn kết bằng end card thương hiệu toàn khung, 4–6 giây**, có thanh CTA ở đáy.

### Những thứ KHÔNG phải quy tắc — đừng cố định trong preset

- **Nhịp cắt.** Trung vị dao động **2.0–5.9 s**. Chọn theo nội dung: video phân tích một cầu thủ
  (haaland 5.5 s · zidane 5.9 s, shot >8 s chiếm 39–44%) cắt chậm hơn hẳn video so sánh
  nhiều đội (pep 2.0 s · psg 2.6 s). **Số cắt mỗi phút thì ổn định: 5.6–7.9.**
- **Chuyển cảnh có hiệu ứng.** Từ **1% đến 29%** — không có giá trị chuẩn.
  haaland 1% · zidane 5% · ucl 7% · psg 23% · pep 29%.
  Có tương quan rõ với nhịp: video cắt nhanh (trung vị ~2–2.5 s) dùng nhiều hiệu ứng (23–29%),
  video cắt chậm (trung vị ~5–6 s) gần như chỉ cut thẳng (1–7%).
  **Chọn cặp đi với nhau**: cắt nhanh + nhiều hiệu ứng, hoặc cắt chậm + cut thẳng.
- **Mở đầu.** Xem `visual-spec.md` — 3/5 video mở bằng đồ hoạ thiết kế, 2/5 bằng footage.

### Nhạc nền — KHÔNG phải một bed chạy suốt

Đo dải 20–70 Hz (nằm dưới tần số cơ bản của giọng nam nên gần như chỉ còn nhạc), 4 video:

| | haaland | ucl | psg | zidane |
|---|---|---|---|---|
| Dài | 15,1′ | 24,0′ | 25,4′ | 49,9′ |
| **Có nhạc** | 79% | 76% | 76% | 76% |
| **Vắng nhạc** | 21% | 24% | 24% | 24% |
| Số đoạn có nhạc | 15 | 25 | 25 | 35 |
| Trung vị đoạn nhạc | 40 s | 36 s | 28 s | 46 s |
| Đoạn nhạc dài nhất | 154 s | 146 s | 164 s | 306 s |
| Số đoạn vắng nhạc | 19 | 26 | 24 | 35 |
| Trung vị đoạn vắng | 7 s | 11 s | 12 s | 10 s |
| Vắng dài nhất | 22 s | 44 s | 64 s | 106 s |
| Điểm đổi nhạc | 6 | 9 | 11 | 20 |
| **Đổi nhạc / phút** | **0,40** | **0,38** | **0,43** | **0,40** |

**Hằng số chặt nhất đo được trong cả bộ mẫu: ~0,4 lần đổi nhạc mỗi phút**, tức
**một bản nhạc mới khoảng mỗi 2 đến 2,5 phút**. Giữ nguyên từ video 15 phút đến video 50 phút.

Ba quy tắc rút ra:

1. **Nhạc chỉ phủ ~76–79% thời lượng.** Một phần tư video **không có nhạc** —
   để giọng kể đứng một mình. Đây là công cụ nhấn mạnh chính của kênh.
2. **Nhạc vào theo đoạn 28–46 giây** (trung vị), không phải một bed dài.
   Có đoạn dài tới 2,5–5 phút nhưng là ngoại lệ.
3. **Khoảng vắng nhạc dài 7–12 giây** (trung vị), đủ để người xem cảm nhận sự im ắng
   mà không thấy trống. Thỉnh thoảng có khoảng vắng rất dài (44–106 giây) ở đoạn cao trào lý lẽ.

### Áp cho video 8 phút

| | |
|---|---|
| Số bản nhạc khác nhau | **3–4** (0,4 × 8 ≈ 3,2 điểm đổi) |
| Tổng thời lượng có nhạc | **~370 s** (77% của 480 s) |
| Tổng thời lượng vắng nhạc | **~110 s** |
| Số khoảng vắng | **8–13 khoảng**, mỗi khoảng 7–12 s |

Đặt khoảng vắng ở: câu hook mở đầu, ngay trước một con số lớn, quote card,
và câu chốt của payoff. **Đừng rải đều** — vắng nhạc phải trùng chỗ muốn người xem tập trung.

*Giới hạn của phép đo: ngưỡng dựa trên dải trầm, nên nhạc ambient rất nhẹ không có bass
có thể bị tính nhầm là "vắng". Con số 76–79% nên hiểu là "có nhạc mang bass".*

Script dò lại: `scripts/music_analyze.py <file.wav 16kHz mono>`

### Cân bằng giọng với nhạc — đo thật

Tách bằng tần số: dải **20–70 Hz** (dưới giọng nam) đại diện mức **nhạc**;
dải **200–3400 Hz** đại diện mức **giọng**. So hai trạng thái: đang nói liên tục
so với im giọng liên tục ≥1,5 s (đủ để ducker nhả hết).

| | zidane | psg | độ tin cậy |
|---|---|---|---|
| Mẫu "đang nói" | 1434 s | 651 s | lớn |
| Mẫu "im giọng ≥1,5 s" | 12 s | 10 s | **nhỏ** |
| Nhạc bị hạ khi có giọng | 10,6 dB | 4,2 dB | ⚠️ mẫu nhỏ, chênh nhau nhiều |
| **Giọng nổi trên nhạc (dải giọng)** | **24,9 dB** | **23,1 dB** | **vững** |

**Con số đáng tin và đáng dùng: giọng nằm trên nhạc khoảng 23–25 dB trong dải giọng.**
Đo trên 651–1434 giây lời nói nên rất vững. Đây mới là thứ tạo ra cảm giác
"nghe rõ giọng nhưng vẫn nghe được nhạc một cách dễ chịu" — **cân bằng tĩnh**,
đặt nhạc đủ thấp ngay từ đầu.

**Phần duck động thì KHÔNG kết luận được.** Vì kênh này có mật độ lời 96–98%, cả video
50 phút chỉ còn 12 giây im giọng liên tục để lấy mẫu. Hai video cho 4,2 và 10,6 dB —
chênh quá nhiều để coi là một con số. Và ở những khoảng im hiếm hoi đó, người dựng
rất có thể **chủ động đẩy nhạc lên** cho hiệu quả kịch tính, chứ không phải compressor
tự nhả. Phương pháp này không phân biệt được hai thứ đó.

### Cách làm cho Turn On Hoops

1. **Đặt cân bằng tĩnh trước.** Nhạc phải thấp hơn giọng khoảng **20 dB trở lên**
   trong dải giọng. Nghe thử: nhạc phải cảm nhận được nhưng không bao giờ tranh chỗ.
2. **Rồi mới đẩy nhạc lên ở khoảng lặng.** Ở các khoảng vắng lời (xem mục nhạc nền),
   nâng nhạc **4–10 dB** — khớp với biên độ đo được, và đây là lúc nhạc được phép nổi.
3. **Đừng dựa vào một con số duck cố định.** Tài liệu cũ ghi "VO duck −12 dB dưới nhạc" —
   vừa là số chưa đo, vừa **viết ngược** (nhạc mới là thứ phải lùi xuống dưới giọng).

Script đo lại: `scripts/duck_analyze.py <file.wav 16 kHz mono>`

### ⚠️ Audio: đo được nhưng ĐỪNG COPY

Cả 5 video đều ở **−19.6 đến −21.4 LUFS** (quá nhỏ so với chuẩn YouTube −14) và
**true peak 0.0 đến +0.3 dBFS** — tức **đều đã clip**. Nhất quán nhưng là lỗi kỹ thuật
nhất quán, không phải phong cách. Giữ −14 LUFS / −1.0 dBTP.

---

## Số đo chi tiết video `dGlI0rts0AI` — `dGlI0rts0AI` (Pep Guardiola, 13:55, 1920×1080 @ 60fps)

Đo bằng ffmpeg: scene detect, blackdetect, ebur128, silencedetect, bản đồ phương sai pixel.

### Nhịp cắt

| Chỉ số | Giá trị |
|---|---|
| Điểm chuyển cảnh | 110 (sau khi gộp burst), **7.9 lần/phút** |
| Shot trung bình | 7.5 s · **trung vị 2.0 s** |
| Shot < 1 s | 33% |
| Shot 1–4 s | 30% |
| Shot 4–8 s | 15% |
| Shot > 8 s | 21% (dài nhất **103 s không cắt**) |

**Đây là nhịp lưỡng cực, không phải nhịp đều.** Hoặc montage dồn dập dưới 1 giây, hoặc giữ
rất lâu trên một hình. Phút 4 và phút 6 có cụm cắt cực dày; phút 9 và 12 không cắt lần nào.
Chính sự đối lập này tạo cảm giác "mạch lạc có cao trào", không phải cắt đều tay.

Áp cho NBA: đừng rải shot đều 2–3 giây. Gom montage nhanh ở chỗ liệt kê/dẫn chứng, rồi giữ
một hình thật lâu (20–60 s) ở chỗ phân tích sâu — lúc đó để telestration và giọng kể gánh.

### Khung đen

Chỉ **6 lần / 13:55**, mỗi lần **0.08–0.25 s**: 01:55 · 02:53 · 03:08 · 05:04 · 06:36 · 10:47.
Hiếm và rất ngắn. Không dùng làm nhịp mở chapter.

### Logo & CTA

- **Không có logo watermark ở góc.** Bản đồ phương sai cho thấy 0% pixel đứng yên suốt video
  ở mọi vùng — không có bug cố định nào.
- **Không có sting logo mở đầu.** Frame 0.0 đã là footage có telestration.
- **Chỉ có end card ở cuối**: khoảng **829 s → 834.8 s (~6 s)**. Nền xanh ngọc bão hoà,
  hoạ tiết chấm bi halftone, chữ display đậm nén "THANKS FOR WATCHING", avatar kênh hình tròn
  bên phải, thanh dưới cùng ghi `LIKE | COMMENT | SHARE | SUBSCRIBE`.
- Không có CTA chèn giữa video.

### Audio

| Chỉ số | Đo được | Nhận xét |
|---|---|---|
| Integrated | **−21.4 LUFS** | ⚠️ **quá nhỏ.** YouTube chỉ hạ chứ không nâng, nên video này phát nhỏ hơn mặt bằng. **Đừng copy.** Vẫn dùng −14 LUFS. |
| True peak | **0.0 dBFS** | ⚠️ **đã clip.** Lỗi kỹ thuật, không phải phong cách. Giữ −1.0 dBTP. |
| LRA | 4.2 LU | Nén rất chặt, nhất quán — cái này thì đáng học cho video kể chuyện |
| Mật độ lời | **96% thời lượng có giọng** | 46 khoảng lặng, trung bình 0.68 s, tổng chỉ 31 s |

**Giọng kể gần như không ngừng.** Đây là điểm khác lớn nhất so với tài liệu cũ: khoảng lặng
không phải công cụ chính, nhịp đến từ hình và nhạc chứ không từ việc ngừng nói. Khi viết
script, đừng chừa nhiều khoảng trống — viết đủ chữ để lấp gần hết thời lượng.
