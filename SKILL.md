---
name: nba-story-edit
description: Edit long-form NBA documentary, biography, behind-the-scenes and salary-cap videos in Adobe Premiere Pro, using the cinematic style measured from the SOFA Zone channel and adapted for a US audience. Use for scripting chapter structure, cutting, footage look treatment, chapter cards, and generating animated data charts for these videos.
---

# NBA Story Edit — SOFA Zone style, US market

## Style này từ đâu

Hệ thống hình ảnh lấy từ kênh **SOFA Zone** (@sofazonevn, bóng đá, khán giả Việt).

Đã đo **5 video bằng ffmpeg trên từng frame**: `dGlI0rts0AI` (Pep, 13:55) ·
`W7ohHAfYAho` (Haaland, 15:04) · `u6odrTDEMt8` (Real–Barca UCL, 24:03) ·
`NiyEty2yBcc` (PSG, 25:23) · `27RC4-w-dy4` (Zidane, 49:54).
Hai video đo bằng mắt trước đó: `twu12g-DL9A`, `ZxKZ9PwVCv8`.

> **Đọc `references/edit-grammar.md` mục đầu trước khi tin bất kỳ con số nhịp nào.**
> Đo đủ 5 video (14 đến 50 phút) cho thấy phần lớn "quy tắc" rút ra từ một video là sai:
> trung vị shot dao động 2.0–5.9 s, chuyển cảnh có hiệu ứng dao động 1–29%.
> Hằng số thật: mật độ lời **96–98%**, cắt **5.6–7.9 lần/phút**, LRA **3.9–5.2**,
> khung đen trung vị **0.08 s**, luôn kết bằng end card **4–6 giây**.
> Và một cặp đi liền nhau: **cắt nhanh thì nhiều hiệu ứng chuyển, cắt chậm thì cut thẳng.**
>
> **Nhạc nền: hằng số chặt nhất đo được — ~0,4 lần đổi nhạc mỗi phút** (một bản mới mỗi
> 2–2,5 phút), và nhạc chỉ phủ **76–79%** thời lượng. Một phần tư video không có nhạc.

**Quyết định quan trọng:** giữ gần như nguyên bộ nhận diện hình ảnh của SOFA Zone.
Lý do: khảo sát mảng NBA storytelling trên YouTube Mỹ cho thấy không ai xử lý hình ở mức
điện ảnh như vậy — JxmyHighroller (2.66M) dùng clip thô không chỉnh màu + biểu đồ phẳng,
Thinking Basketball (683K) là film-study có telestration, Third Apron (5.35K, chuyên bảng lương)
là podcast talking-head. Look của SOFA Zone vì thế là **điểm khác biệt**, không phải thứ cần giảm.

Chỉ bản địa hoá tầng ngôn ngữ: tiêu đề, thumbnail, mật độ chữ trên hình, giọng narration.
Chi tiết ở `references/visual-spec.md` mục "US adaptation".

## Hỏi trước khi bắt đầu

1. Format nào — `biography` | `what-if` | `cap-explainer` | `behind-the-scenes`?
2. Thời lượng mục tiêu (mặc định 14–20 phút)?
3. Đã có script/VO chưa, hay bắt đầu từ ý tưởng?
4. Footage có những gì, nguồn nào? (quyết định treatment nào dùng được)

## Pipeline

### 1. Script trước, luôn luôn
Edit bám theo chapter. Không có chapter map thì không mở Premiere.
Dùng template trong `references/script-template.md`. Ra được:
- danh sách chapter + thời lượng dự kiến
- câu hook (≤ 2 câu, đặt ở 0:00–0:12)
- mỗi chapter một "asset need": footage / ảnh / chart / quote

### 2. Fact-check — bắt buộc, không bỏ qua
Mọi con số lên hình phải khớp nguồn chốt trong `references/sources.md`.
Khán giả NBA Mỹ cực kỳ thạo số liệu; một con số sai là mất uy tín kênh.
Ghi nguồn + ngày truy xuất vào `facts.md` cạnh project.

### 3. Chuẩn bị asset
- Chart: chạy `scripts/make_chart.py` (xem `--help`) → PNG dọc để scroll, hoặc MP4 đã animate.
  Lần đầu cần `pip install matplotlib`. Chế độ `--video` cần ffmpeg trong PATH.
- Overlay look: chạy `scripts/make_overlays.sh` một lần → `assets/scanlines.png`,
  `assets/grain.mp4`, `assets/vignette.png`
- **Ảnh cầu thủ**: nguồn chính là **Wikimedia Commons** — miễn phí, không mua license.
  Tìm bằng `scripts/commons_search.py "<tên cầu thủ>"` (in kèm license + tác giả).
  Thêm `--by-only` để loại ảnh CC BY-**SA** nếu không muốn dính nghĩa vụ ShareAlike cho cả video.
  Đọc `references/sources.md` trước khi tải — có hai cái bẫy đã gặp thật.

### 4. Dựng trong Premiere
Qua MCP server `premiere-pro`:
- `verify_premiere_connection` trước tiên. Nếu trả về `userActionRequired` → đọc nguyên văn
  `nextStep` cho user rồi DỪNG, không gọi tool khác.
- Catalog 280+ tool không hiện hết trong tools/list. Luôn `search_tools` để tìm đúng tên,
  rồi `invoke_tool`. **Không bịa tên tool.**
- Trình tự: tạo sequence → import → cắt theo chapter → áp treatment → chapter card → chart → audio.

Công thức effect chi tiết: `references/premiere-recipes.md`

### 5. Áp treatment theo niên đại
Footage không bao giờ để thô. Chọn treatment theo tuổi tư liệu, không theo cảm tính.
Bảng tra ở `references/visual-spec.md` mục "Treatment ladder".

### 5b. Telestration / chart reveal — đừng để hình đứng yên
Chữ ký thật sự của style này: **vẽ đè lên hình đang chạy** thay vì cắt sang hình khác để
giải thích. Có footage thì telestration (vùng tô, mũi tên, vòng chân cầu thủ).
Không có footage thì áp cùng nguyên tắc cho chart: **hiện dần khớp lời kể**, không hiện một lúc.

Mốc hiện lấy từ chính file VO, không canh tay:
`ffmpeg -i vo.wav -af silencedetect=n=-45dB:d=0.12 -f null -` → mỗi `silence_end` là một lần
giọng nói bắt đầu lại. Bake animation bằng ffmpeg (`drawbox` + `enable`) đáng tin hơn keyframe
trong Premiere — xem `premiere-recipes.md`.

### 6. Audio
Skill này không xử lý được audio (không nghe được). Ra checklist cho user:
beat nhạc trùng cut chapter, **nhạc đặt thấp hơn giọng ~20 dB trong dải giọng** rồi nâng
4–10 dB ở khoảng lặng (số đo ở `edit-grammar.md`), SFX whoosh ở mỗi chapter card,
khoảng lặng 0.4–0.8s ở black frame giữa các chapter.

### Giọng đọc (ElevenLabs)

- **Voice ID mặc định của kênh:** `2rRUaEOGIGalXrcuLN55` (do người dùng cung cấp).
  Dùng giọng này cho mọi narration trừ khi người dùng chỉ định giọng khác.
- Tạo VO bằng công cụ ElevenLabs (`text_to_speech`) theo từng chapter, rồi căn timing bằng
  `silencedetect` như mục 5b. Nếu đổi giọng, cập nhật lại mục này.

### Nhạc nền (Mixkit)

- **Nguồn nhạc mặc định:** [Mixkit Free Stock Music](https://mixkit.co/free-stock-music/). Tải bằng
  `https://assets.mixkit.co/music/<ID>/<ID>.mp3`, lấy ID từ trang tag (cinematic, dramatic, sport).
- Mixkit cho phép dùng miễn phí trong video, không bắt buộc ghi credit. Kiểm tra lại điều khoản
  trên trang Mixkit trước khi xuất bản.
- Đã dùng trong bản review (xem `music/` trong dự án Curry 2015-16): Silent Descent, Vastness,
  The Journey, Sports Highlights, Epic Games, Echoes, Ode to Loneliness, Epical Drums 01,
  Staring at the Night Sky, Beautiful Dream.
- Mix nhạc dưới giọng đọc bằng sidechaincompress, nhạc ở khoảng −13 dB so với giọng.

## Quy tắc cứng

- **Khung đầu của mỗi chapter phải có nội dung hiển thị, không được trống.** YouTube lấy khung tại mốc
  chapter để làm ảnh xem trước của chapter đó. Nếu khung này là nền trống (thẻ chương đang trượt vào,
  hoặc màn đen/lưới), YouTube sẽ dùng ảnh thumbnail của video thay thế, và tất cả chapter sẽ trông giống nhau.
  Cách làm: thẻ chương phải hiển thị đầy đủ ngay từ giây đầu (không trượt vào), hoặc chapter mở bằng một
  ảnh/clip có nội dung rõ ràng. Mỗi chapter cần một khung đầu khác nhau.
  Kiểm tra trước khi xuất: trích khung ở đúng mốc bắt đầu của từng chapter và xem có phải nền trống không.

- **Không lặp lại cùng một ảnh hoặc clip trong một video long-form.** Mỗi ảnh, clip hay đoạn footage chỉ
  xuất hiện một lần. Nếu cần nhắc lại một khoảnh khắc, hãy dùng khung khác của cùng một trận (crop khác,
  góc khác, hoặc khung đã sắp xếp lại) hoặc dùng chart và thẻ chữ. Trước khi xuất, kiểm tra danh sách asset
  theo chapter và đánh dấu mọi lần lặp. Nếu không đủ asset khác nhau, hãy mở rộng tìm kiếm trước khi lặp lại.
  Một ảnh xuất hiện hai lần sẽ làm người xem chán.

- **Không burn-in phụ đề.** Khán giả Mỹ nghe tiếng Anh native. Bỏ track chữ đi sẽ thấy
  frame trống — lấp bằng chart, ảnh archival, chapter card, chứ không lấp bằng chữ.
- **Không re-upload compilation của kênh khác.** SOFA Zone có làm (thấy watermark
  "MESOPOTAMIA", "TOP FOOTBALL HD" trong frame). Đừng copy phần đó — NBA quét Content ID
  gắt hơn bóng đá nhiều.
- **Số liệu sai = không xuất.** Xem bước 2.
- **Mỗi chapter một ý.** Chapter dài quá 2:20 thì tách.
- **Không để chart hay ảnh đứng yên quá 8 giây** mà không có gì chuyển động. Xem bước 5b.
- **Nhịp lưỡng cực**, không cắt đều tay: montage ngắn xen với shot giữ rất lâu.
  Tỉ lệ cụ thể **chọn theo nội dung**, không có con số cố định — xem bảng phân bố 5 video.
- **Footage không tràn viền.** Mặc định lồng trong khung bo góc **rộng ~82%** trên nền lưới tối,
  có HUD. Full-bleed chỉ dành cho khoảnh khắc lớn. Footage chỉ chiếm ~27% thời lượng.
- **Giữ footage lâu, cắt đồ hoạ nhanh.** Shot footage trung vị 10–17 s; shot đồ hoạ 3,5–4,6 s.
- **Khung lồng KHÔNG phải biện pháp bản quyền.** Thu nhỏ và cắt bỏ logo nguồn không bảo vệ gì,
  riêng việc gỡ logo còn làm xấu đi. Đọc `references/sources.md` trước khi dùng footage của
  bên thứ ba.
- **Không watermark góc, không sting mở đầu.** Nhưng **có bumper logo mờ** giữa video
  (0–7 lần) và **luôn có end card 4–6 giây** ở cuối.
- **Audio: đừng copy SOFA Zone.** Họ xuất ở −21.4 LUFS và peak chạm 0.0 dBFS (đã clip).
  Giữ −14 LUFS / −1.0 dBTP.

## Index reference

| File | Nội dung |
|---|---|
| `references/edit-grammar.md` | Cấu trúc, nhịp, timing — đo từ SOFA Zone |
| `references/visual-spec.md` | Màu, font, treatment ladder, bản địa hoá US |
| `references/script-template.md` | 4 template chapter map theo format |
| `references/premiere-recipes.md` | Stack effect từng treatment · telestration · bake animation · **bảng bẫy đã gặp** |
| `references/sources.md` | Nguồn data, ảnh, footage, nhạc + license |
| `references/sofa-analysis-data/` | Dữ liệu đo gốc 5 video SOFA Zone: nhịp cắt, khung đen, nhạc, stats5.json, DO_DAC.md (số liệu một video), ảnh kiểm tra |
| `scripts/make_chart.py` | Sinh biểu đồ động từ CSV |
| `scripts/make_overlays.sh` | Sinh scanline / grain / vignette bằng ffmpeg |
| `scripts/commons_search.py` | Tìm ảnh Wikimedia Commons, in kèm license + tác giả |
| `scripts/music_analyze.py` | Dò nhạc nền (có/vắng, điểm đổi bản) trong bản mix có cả lời |
| `scripts/duck_analyze.py` | Đo cân bằng giọng/nhạc và độ nâng nhạc ở khoảng lặng |
