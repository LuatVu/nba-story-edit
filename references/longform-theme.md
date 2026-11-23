# Theme long-form chuẩn: "Vice neon" (hồng × xanh ngọc)

**Áp dụng cho MỌI video long-form của kênh Turn On Hoops** (biography, what-if, cap-explainer,
behind-the-scenes). Rút từ video "How GTA 6 Took Over the NBA" (21/11/2026), được chủ kênh chọn làm
chuẩn ngày 23/11/2026. Khi tài liệu cũ (`visual-spec.md`, bảng màu đen/cam, chapter card serif
nghiêng, vòng chân `#E8912A`) mâu thuẫn với file này, **file này thắng**.

Code dùng lại: `scripts/lf_theme.py` (token màu, font, khung footage, 8 mẫu đồ hoạ động, thẻ chương,
thẻ tiêu đề, end card). Đừng viết lại mẫu từ đầu cho từng video. Import module hoặc gọi CLI, chỉ viết
spec số liệu của video đó.

Phạm vi: chỉ long-form 16:9. **Shorts giữ style riêng** (`shorts-spec.md`, màu đội, caption 1–2 từ).

---

## 1. Màu

| Token | Mã | RGB | Dùng cho |
|---|---|---|---|
| `PINK` (chính) | **#FF40A0** | 255, 64, 160 | Ô nhãn (kicker) mọi đồ hoạ, nhãn "CHAPTER N", thanh/cột chính, chấm mốc thời gian, đường cung bản đồ, chữ tô sáng trong trích dẫn, viền avatar, **viền mảnh quanh khung footage** |
| `TEAL` (phụ) | **#28E1D7** | 40, 225, 215 | **Bóng lệch dưới mọi con số lớn và tiêu đề**, mốc quan trọng nhất, hệ số nhân (`~4.7×`), vạch khoảng cách (`$25K UNDER`), vạch dưới trích dẫn, vòng Subscribe |
| `INK` | #FFFFFF | | Con số, tiêu đề |
| `INK2` | #E1DCE8 | | Nhãn dưới số |
| `INK3` | #AAA4B4 | | Dòng nguồn, số của bên thua / phụ |
| `STROKE` | #0A0610 | | Viền chữ lớn (5–10 px) |
| `CONTEXT` | #BEB8C8 | | Cột/thanh so sánh (đối thủ, năm cũ) |
| `PANEL` | #120A1A | | Nền hộp, vòng tròn (alpha 82–85 %) |
| `CARD_SHADE` | #080414 | | Gradient tối bên trái thẻ chương |
| `FRAME_BG` / `FRAME_GRID` | #0A090E / #16141E | | Nền và lưới quanh khung footage |

Quy tắc dùng màu:
- **Một nhân vật chính = hồng, phần còn lại = xám `CONTEXT`.** Không tô hồng hai thứ đang so sánh.
- **Xanh ngọc chỉ là điểm nhấn thứ hai**: bóng chữ, mốc cuối, kết luận ("UNDER", "×4.7"). Không dùng làm màu cột chính.
- Không thêm màu đội vào đồ hoạ long-form, trừ khi cần phân biệt hai đội trên telestration
  (lúc đó: hồng = đội/cầu thủ chính, xanh ngọc = đồng đội/đối chiếu, trắng = còn lại).
- Logo kênh (vàng/navy) chỉ xuất hiện ở bumper và end card, không trộn vào chart.

## 2. Chữ

| Font | File | Dùng cho |
|---|---|---|
| **Anton** | `assets/fonts/Anton-Regular.ttf` | Con số lớn (96–260 px), tiêu đề thẻ chương (170–190 px), tên người trong trích dẫn, tiêu đề end card |
| **Montserrat ExtraBold** | `assets/fonts/Montserrat-ExtraBold.ttf` | Kicker (40 px), nhãn IN HOA (30–40 px), trích dẫn (68–96 px), dòng nguồn (24 px) |

Hai kiểu chữ chữ ký:
- **Số lớn:** Anton trắng, viền `STROKE` 5–6 px, **bóng xanh ngọc lệch +7/+7 px**. Nhãn Montserrat `INK2` ngay dưới.
- **Tiêu đề kiểu poster GTA:** Anton trắng viền đen 10 px, **lớp xanh ngọc lệch +8/+8 px** phía sau.
- **Kicker:** khối hồng đặc, chữ Montserrat trắng IN HOA, góc trên trái (x 120, y 96).
- **Dòng nguồn:** Montserrat 24 px `INK3`, góc dưới trái (x 120, y H−70). Mọi đồ hoạ số liệu đều phải có.

## 3. Footage và ảnh

| Loại | Cách trình bày |
|---|---|
| Footage thường | **Khung 82 %**: cửa sổ 1574×886 tại (173, 97), bo góc 22 px, trên nền `#0A090E` có lưới ô 48 px `#16141E`, **viền hồng mảnh** (alpha ~60 %). `lf_theme.frame_overlay()` + `lf_theme.footage_filter()` |
| Grade thường | `eq=contrast=1.06:saturation=0.96` |
| Tư liệu cũ ("arch") | `eq=contrast=1.08:saturation=0.62,noise=alls=16:allf=t` |
| Slow-mo | 0,5× (`setpts=2*PTS`), vẫn trong khung |
| Full-bleed | Chỉ khoảnh khắc lớn |
| Ảnh tĩnh | Luôn full-bleed + Ken Burns; ảnh không đủ khổ thì lót chính nó làm mờ, không viền đen |

## 4. Nền đồ hoạ

Mọi đồ hoạ số liệu nằm trên **ảnh thật liên quan**: blur 30 px, sáng 45 %, màu +15 %, vignette,
zoom chậm 100→106 % (xen kẽ chiều in/out) + trôi ngang 2 %. Không bao giờ nền đen phẳng. Không dùng lại
một ảnh nền ở hai đồ hoạ.

## 5. Tám mẫu đồ hoạ (`kind` trong spec)

| kind | Khi nào | Cấu tạo |
|---|---|---|
| `stat` | 1–3 con số của một trận / một sự kiện | Cột số Anton + nhãn, vạch chia mờ, có thể `sep` ("–") cho tỉ số |
| `bars` | So sánh 2–4 giá trị | Cột chính hồng, cột khác `CONTEXT`, đầu cột bo 4 px, số trên đỉnh; `mult` xanh ngọc; `notes` số phụ bên trái |
| `timeline` | 3–5 mốc năm | Chấm hồng nối bằng đường vẽ dần; mốc chốt xanh ngọc, to hơn |
| `org` | Quan hệ cha–con (công ty, front office, cây trade) | Hộp trên viền xanh ngọc → 2–3 hộp dưới viền hồng, đường nối vẽ dần |
| `map` | Lan toả địa lý | Bản đồ chấm, điểm gốc hồng nhấp nháy, cung hồng tới chấm xanh ngọc, 1–2 số lớn bên trái |
| `threshold` | Giá trị so với ngưỡng (cap, apron, hạn mức) | Thanh hồng, vạch đứt ở ngưỡng, khoảng cách bằng ngoặc xanh ngọc |
| `flywheel` | Hai bên cùng hưởng lợi | Hai vòng tròn viền hồng / xanh ngọc, hai mũi tên cong, hàng "ai được gì" ở dưới |
| `quote` | Trích dẫn | Avatar tròn viền hồng (hoặc dấu “ hồng lớn), chữ hiện từng từ, từ khoá tô hồng, vạch xanh ngọc, tên Anton |

Mẫu `bars`, `threshold` hợp với **cap-explainer** (lương, apron, luxury tax); `timeline`, `quote`
hợp với **biography**; `org`, `flywheel`, `map` hợp với **behind-the-scenes**.

## 6. Chuyển động

- **Neo vào lời đọc:** mỗi phần tử hiện đúng từ nhắc tới nó (timestamp từng từ của VO,
  `scripts/shorts_words.py` hoặc whisper). Clip đồ hoạ bắt đầu sớm **0,5 s** trước từ khoá đầu tiên.
- **Hiện chuẩn:** ease-out cubic **0,45 s**, trồi lên 50 px + fade in.
- **Số đếm lên** 0 → giá trị trong **0,8 s**, giữ định dạng (`$975,000`, `32.5M`, `~$3.79B`).
- **Cột** mọc từ đáy **0,9 s**; số trên đỉnh chạy theo.
- **Đường nối / cung / mũi tên** tự vẽ dần (path draw), mũi tên có đầu nhọn; chấm nở 50→100 %.
- **Trích dẫn:** mỗi từ 0,22 s, đúng lúc được đọc; avatar phóng 85→100 %.
- **Kicker** hiện ở 0,1 s, **dòng nguồn** ở 0,3 s.
- Không để đồ hoạ đứng yên quá 8 s (nền vẫn Ken Burns, nhưng nếu đoạn dài hãy tách đồ hoạ).

## 7. Thẻ chương, thẻ tiêu đề, end card

- **Thẻ chương** (`chapter_card`): ảnh full khung (ưu tiên ảnh AI kiểu poster minh hoạ hợp chủ đề, sinh
  bằng `openai-image`, hoặc ảnh thật), gradient `CARD_SHADE` tối dần từ trái, khối hồng "CHAPTER N",
  tiêu đề Anton 170 px kiểu poster (trắng, viền đen, bóng xanh ngọc). Thẻ hiện đủ ngay frame đầu
  (quy tắc khung đầu chapter trong SKILL.md).
- **Thẻ tiêu đề** (`title_card`): như thẻ chương, không kicker, chữ 190 px.
- **End card** (`end_card`): ảnh mờ 6 px, tối 55 %; câu hỏi Anton 84 px (bóng xanh ngọc) + dòng
  "TELL ME IN THE COMMENTS"; hai ô video 760×428 viền hồng cho end screen; vòng Subscribe viền xanh ngọc.
- **SFX:** whoosh ở thẻ tiêu đề và mỗi thẻ chương. Nhạc sidechain dưới giọng.

## 8. Thumbnail long-form

Theo cùng theme: ảnh nền nhiều màu hồng/xanh ngọc, một nhân vật chính, 2–3 từ Anton trắng viền đen
với bóng xanh ngọc. Quy tắc thumbnail chung (0–3 từ, không badge, không viền khung) ở `visual-spec.md`
vẫn áp dụng.

## 9. Cách dùng `scripts/lf_theme.py`

```
python lf_theme.py --example > graphics.json         # mẫu spec
python lf_theme.py graphics.json gfx/out --still     # kiểm tra bố cục nhanh (chỉ frame cuối)
python lf_theme.py graphics.json gfx/out             # render MP4 1920x1080 30fps
python lf_theme.py --card "CHAPTER 3" "THE\nTEST RUNS" bg.png card_03.png
python lf_theme.py --title "HOW GTA 6\nTOOK OVER\nTHE NBA" bg.png card_00.png
python lf_theme.py --frame frame_overlay.png
```

Trong Python: `import lf_theme as T` → `T.render(g, outdir)`, `T.chapter_card(...)`,
`T.end_card(bg, out, headline=..., right=...)`, `T.frame_overlay(path)`, `T.footage_filter(opt, slow)`,
`T.PINK`, `T.TEAL`...

Spec mỗi đồ hoạ: `id, kind, bg, dur, kicker, source` + trường riêng của mẫu (xem docstring từng
`draw_*` trong script). Mọi `t` tính bằng giây **từ đầu clip đó**. Đường dẫn `bg`/`avatar` tương đối
được tính từ thư mục của file spec.

Bản gốc tham khảo (dùng cue tự động từ words.json, 22 đồ hoạ thật):
`D:\TuLieuLamNoiDung\kich ban\How GTA 6 Took Over the NBA\gfx\charts.py`, `chapter_cards.py`,
`edit\build.py`, `edit\finishing.py`.
