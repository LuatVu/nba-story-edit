---
name: nba-story-edit
description: Edit long-form NBA documentary, biography, behind-the-scenes and salary-cap videos in Adobe Premiere Pro, using the cinematic style measured from the SOFA Zone channel and adapted for a US audience, in the channel's standard "Vice neon" long-form theme (pink #FF40A0 × teal #28E1D7, Anton/Montserrat, 8 animated data-graphic templates, GTA-poster chapter cards), and make 9:16 NBA YouTube Shorts (trade rumors, news, story clips) in a fast news-short style with word-by-word auto captions, player cutout reveal animations, speed-ramped slow motion and team-colour cover thumbnails. Use for scripting chapter structure, cutting, footage look treatment, chapter cards, animated data charts, and for any NBA Short, Reel or vertical video and its cover. Also makes and publishes Facebook photo posts for the Turn On Hoops page: hot NBA news turned into one branded meme image (troll-page humor modelled on Troll Bóng Đá, English captions), with a searchable library of 1,897 imgflip meme templates sorted by meaning (used unedited, no face swaps), an ESPN hot-topic radar, and posting/scheduling through the Facebook MCP. Use for any NBA meme, troll post, Facebook post, photo post or "chế ảnh".
---

> **Làm bài đăng Facebook / meme / chế ảnh cho trang Turn On Hoops?** Đi thẳng tới mục
> **"Facebook meme posts"** ở cuối file và đọc `references/facebook-post.md`. Không áp dụng quy tắc video.

> **Làm Shorts (9:16, < 3 phút)?** Đi thẳng tới mục **"Shorts"** ở cuối file. Phần lớn quy tắc
> long-form bên dưới (không phụ đề, footage lồng khung, giữ shot lâu) **không áp dụng** cho Shorts.

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

## Theme long-form chuẩn: "Vice neon" (bắt buộc từ 23/11/2026)

**Mọi video long-form dùng một bộ nhận diện duy nhất**, rút từ video "How GTA 6 Took Over the NBA".
**Đọc `references/longform-theme.md` trước khi làm đồ hoạ.** Code dùng lại: `scripts/lf_theme.py`.
Khi `visual-spec.md` (bảng màu đen/cam, chapter card serif nghiêng, vòng chân `#E8912A`) mâu thuẫn
với theme này, **theme thắng**. Nhịp cắt, cấu trúc chapter, khung footage 82 %, end card vẫn theo
phần đo SOFA Zone bên dưới. Shorts không dùng theme này.

Tóm tắt:
- **Màu:** hồng `#FF40A0` (chính: kicker, cột chính, mốc, cung, viền khung footage) ·
  xanh ngọc `#28E1D7` (bóng lệch dưới số lớn và tiêu đề, mốc chốt, hệ số, khoảng cách) ·
  chữ `#FFFFFF` / `#E1DCE8` / `#AAA4B4` · so sánh `#BEB8C8`.
- **Chữ:** Anton cho số và tiêu đề (trắng, viền đen, bóng xanh ngọc +7 px) · Montserrat ExtraBold
  cho kicker, nhãn IN HOA, trích dẫn, dòng nguồn.
- **Footage:** khung 82 % bo 22 px trên nền lưới tối 48 px, viền hồng mảnh; grade
  `eq=contrast=1.06:saturation=0.96`, tư liệu cũ thêm desaturate + grain.
- **Đồ hoạ số liệu:** 8 mẫu `stat · bars · timeline · org · map · threshold · flywheel · quote`,
  nền ảnh thật mờ 30 px + tối 45 % + Ken Burns, kicker hồng góc trên trái, dòng nguồn góc dưới trái.
- **Chuyển động:** neo từng phần tử vào từ được đọc (clip sớm 0,5 s); ease-out 0,45 s trồi 50 px;
  số đếm lên 0,8 s; cột mọc 0,9 s; đường/cung tự vẽ; trích dẫn hiện từng từ.
- **Thẻ chương:** ảnh full khung (AI kiểu poster hoặc ảnh thật) + gradient tối bên trái + khối hồng
  "CHAPTER N" + tiêu đề Anton kiểu poster GTA (trắng, viền đen, lớp xanh ngọc lệch).

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
- **Đồ hoạ số liệu, thẻ chương, thẻ tiêu đề, end card, khung footage: `scripts/lf_theme.py`**
  (theme chuẩn, xem `references/longform-theme.md`). Viết `graphics.json` cho video
  (`python scripts/lf_theme.py --example` in mẫu), lấy mốc `t` từ timestamp từng từ của VO, chạy
  `--still` để soát bố cục rồi render MP4. `scripts/make_chart.py` chỉ còn dùng cho chart dọc dạng
  scroll đặc biệt; khi dùng, đổi màu về token của theme.
- Overlay look: chạy `scripts/make_overlays.sh` một lần → `assets/scanlines.png`,
  `assets/grain.mp4`, `assets/vignette.png`
- **Ảnh, video, media: tải từ bất kỳ nguồn nào trên internet** — báo (ESPN, NBA.com, CBS,
  Yahoo, SI, AP...), trang đội, NBA CDN (headshot), og:image của bài báo, thumbnail và clip
  YouTube (yt-dlp), mạng xã hội của đội/giải. **Không giới hạn ở Wikimedia Commons**, không
  mặc định đi Commons trước; chọn ảnh/clip đúng ngữ cảnh nhất, mới nhất, nét nhất.
  Commons chỉ là một nguồn trong số đó (`scripts/commons_search.py` vẫn dùng được khi muốn ảnh CC).
  Cách tải và kiểm tra file: `references/sources.md` mục "Tải media từ internet".
  Người dùng chấp nhận rủi ro Content ID / bản quyền; nhắc một lần, ghi nguồn từng file vào
  `facts.md` / catalog, không cần hỏi lại trước mỗi lần tải.
- **Ảnh/footage minh hoạ và thumbnail do AI tạo: dùng OpenAI** qua MCP server `openai-image`,
  tool `generate_image`. Mặc định: `model: "gpt-image-2"`, `quality: "low"`, `size: "1024x1024"`
  (hoặc `"1536x1024"` cho ngang 16:9, `"1024x1536"` cho dọc Shorts). Chỉ đổi sang `"medium"` hoặc
  `"high"` khi user yêu cầu rõ hoặc khi là thumbnail cần chất lượng cao để lên hình cuối.
  Ảnh lưu trong `D:\TuLieuLamNoiDung\images\`. Ghi prompt đã dùng vào `facts.md` cạnh project,
  và ảnh AI tạo ra không thay thế được fact-check ở bước 2 (không dùng AI để tạo số liệu hay gương mặt
  cầu thủ thật; dùng ảnh thật tải từ internet cho cầu thủ).

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

### Giọng đọc (VoiceStudio) — mặc định, không dùng ElevenLabs

- **TTS mặc định: VoiceStudio** (chạy cục bộ trên GPU, MCP server `voicestudio`,
  `http://127.0.0.1:3900/mcp`). **Không dùng ElevenLabs** cho VO nữa (quy định từ 11.2026),
  trừ khi người dùng yêu cầu rõ.
- **Profile người nói mặc định:** **NBA Commenter - David** — `profile_id: "75881d2a"`
  (giọng clone). Dùng cho mọi narration (long-form và Shorts) trừ khi người dùng chỉ định giọng khác.
  Nếu id không còn, gọi `list_voices` và tìm theo tên "NBA Commenter - David".
- Cách tạo: `generate_speech` với `text`, `profile_id: "75881d2a"`, `language: "en"`,
  `steps: 32` cho bản xuất (16 cho nháp), `speed` 1.0 (Shorts có thể 1.05–1.1).
  Long-form: tạo theo từng chapter rồi căn timing bằng `silencedetect` như mục 5b.
  Shorts: tạo một lần cả kịch bản → `vo.wav`.
- Lấy file: kết quả trả về `audio_id`; tải bằng
  `curl -o vo.mp3 http://127.0.0.1:3900/audio/<audio_id>.mp3` (hoặc `.ogg`) vào thư mục project.
  Nếu kết quả trả về base64 thay vì URL/file, đừng in nó ra — chỉ lấy `audio_id` rồi tải qua URL trên.
- Trước khi tạo: `check_health` — nếu lỗi kết nối thì app VoiceStudio chưa mở; nhờ người dùng mở app.
- Nghe lại và soát tên riêng/số (Sengun, Jokic, 20.4...). Đọc sai thì viết lại theo cách đọc
  (vd "twenty point four") và tạo lại câu đó.

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

- **Nền đồ hoạ KHÔNG được là màu đen/đặc.** Mọi thẻ đồ hoạ (số liệu, honors, quote, timeline, chart, thẻ chữ)
  phải dùng nền là **ảnh footage/ảnh cầu thủ phóng to, làm mờ (blur ~25–40 px) và tối đi (~35–50% sáng)**,
  chọn ảnh liên quan đúng nội dung thẻ, có phủ gradient tối phía chữ để đọc rõ. Thông số chuẩn của theme:
  blur 30 px, sáng 45 %, màu +15 %, vignette, Ken Burns 100→106 % (`lf_theme.Background`).
  Ví dụ chuẩn: `gfx/out/charts/*_final.png` của dự án GTA 6. Không dùng ảnh đã dùng ở chỗ khác (xem quy tắc không lặp):
  chọn khung khác hoặc crop khác. Chỉ chapter card và end card được dùng nền thiết kế riêng.
  Áp dụng cả cho Shorts (nền 9:16 cũng là footage mờ, không đen).
  Kiểm tra trước khi xuất: mở từng thẻ đồ hoạ, nếu thấy nền đen phẳng thì làm lại.

- **Cảnh chỉ có ảnh tĩnh phải có chuyển động (Ken Burns), bắt buộc.** Không để ảnh đứng yên toàn màn hình.
  Mỗi ảnh áp zoom-in hoặc zoom-out chậm liên tục suốt thời lượng (scale 100→112% hoặc 112→100%, ~3–5%/giây
  tuỳ độ dài), kèm trôi nhẹ (pan 2–4% theo hướng đối diện với hướng nhìn của chủ thể). Luân phiên
  zoom-in / zoom-out / pan giữa các ảnh liền kề để không đơn điệu. Làm bằng keyframe Scale+Position trong
  Premiere (`set_clip_properties_batch` chỉ đặt giá trị tĩnh, nên bake bằng ffmpeg `zoompan` hoặc
  `scale+crop` theo thời gian rồi import clip) và nhớ giữ ảnh ở chất lượng đủ để không vỡ khi zoom.
  Kiểm tra trước khi xuất: xem preview từng cảnh ảnh, không được có cảnh nào đứng yên.

- **Không burn-in phụ đề (long-form; Shorts thì BẮT BUỘC có caption).** Khán giả Mỹ nghe tiếng Anh native. Bỏ track chữ đi sẽ thấy
  frame trống — lấp bằng chart, ảnh archival, chapter card, chứ không lấp bằng chữ.
- **Không re-upload compilation của kênh khác.** SOFA Zone có làm (thấy watermark
  "MESOPOTAMIA", "TOP FOOTBALL HD" trong frame). Đừng copy phần đó — NBA quét Content ID
  gắt hơn bóng đá nhiều.
- **Số liệu sai = không xuất.** Xem bước 2.
- **Mỗi chapter một ý.** Chapter dài quá 2:20 thì tách.
- **Không để chart hay ảnh đứng yên quá 8 giây** mà không có gì chuyển động. Xem bước 5b.
- **Nhịp lưỡng cực**, không cắt đều tay: montage ngắn xen với shot giữ rất lâu.
  Tỉ lệ cụ thể **chọn theo nội dung**, không có con số cố định — xem bảng phân bố 5 video.
- **Footage không tràn viền (long-form; Shorts tràn viền 9:16).** Mặc định lồng trong khung bo góc **rộng ~82%** trên nền lưới tối,
  có HUD. Full-bleed chỉ dành cho khoảnh khắc lớn. Footage chỉ chiếm ~27% thời lượng.
  Khung chuẩn của theme: 1574×886 tại (173, 97), bo 22 px, lưới `#16141E` ô 48 px trên `#0A090E`,
  viền hồng `#FF40A0` mảnh (`lf_theme.frame_overlay()` + `lf_theme.footage_filter()`).
- **Giữ footage lâu, cắt đồ hoạ nhanh (long-form).** Shot footage trung vị 10–17 s; shot đồ hoạ 3,5–4,6 s.
- **Khung lồng KHÔNG phải biện pháp bản quyền.** Thu nhỏ và cắt bỏ logo nguồn không bảo vệ gì,
  riêng việc gỡ logo còn làm xấu đi. Đọc `references/sources.md` trước khi dùng footage của
  bên thứ ba.
- **Không watermark góc, không sting mở đầu.** Nhưng **có bumper logo mờ** giữa video
  (0–7 lần) và **luôn có end card 4–6 giây** ở cuối.
- **Audio: đừng copy SOFA Zone.** Họ xuất ở −21.4 LUFS và peak chạm 0.0 dBFS (đã clip).
  Giữ −14 LUFS / −1.0 dBTP.

## Shorts

Style khác hẳn long-form: đo từ 3 Shorts của một kênh NBA news (trade rumor, ~1 phút).
**Đọc `references/shorts-spec.md` trước** — số đo, cấu trúc, từng hiệu ứng, cover, checklist.

Tóm tắt những gì phải có:
- **55–75 s**, 1080×1920 tràn viền, shot trung vị **0,9–1,7 s**, nhạc liên tục không lỗ.
- **Hook 0–4 s che danh tính** (bóng đen / pixel / ảnh ghép nhiều sao) rồi reveal có lens glint.
- **Nhịp reset mỗi 15–20 s** (kênh mẫu dùng host; kênh mình không có host → shot cutout chân dung
  hoặc thẻ số liệu).
- **Caption tự động 1–2 từ**, IN HOA, Montserrat ExtraBold trắng trên hộp tối, tâm ở 63 % chiều cao.
- **Ảnh cầu thủ luôn tách nền**; nhiều người thì người chính trồi lên trước, người sau trượt vào
  từ hai bên, mỗi người đúng lúc tên được đọc.
- **Nhanh–chậm theo cảm xúc**: play-by-play 1×, khoảnh khắc lớn slow-mo 0,3–0,4× trong 2–4 s.
- **Cover**: nền màu đội, 1–2 từ Anton trắng, một cầu thủ đè lên mép dưới chữ.

### Pipeline Shorts

Hỏi trước: chủ đề/tin gì, cầu thủ nào, độ dài, có VO chưa, footage nào.

1. **Kịch bản 130–190 từ** (≈ 55–75 s ở tốc độ đọc VoiceStudio 1.0). Câu 1 là hook dạng câu hỏi hoặc
   khẳng định lơ lửng; đánh dấu chỗ reset ~15–20 s; câu cuối nối ngược về câu đầu hoặc là CTA
   "let me know in the comments". Mọi con số vào `facts.md` như long-form.
2. **VO**: VoiceStudio, profile **NBA Commenter - David** (xem mục Giọng đọc) → `vo.mp3`.
   Rồi `scripts/shorts_words.py vo.mp3 words.json --script script.txt` → timestamp từng từ
   (faster-whisper chạy cục bộ). Đây là cách chuẩn để lấy mốc từng từ; không dùng
   `speech_to_text` của ElevenLabs (không có timestamp, kênh đã bỏ ElevenLabs).
3. **Asset**: ảnh cầu thủ (nguồn bất kỳ) → `scripts/shorts_cutout.py photo.jpg out.png --crop l,t,r,b --check`
   → PNG trong suốt. Luôn `--crop` về đúng một cầu thủ; ảnh gốc cắt ra phải cao ≥ 1000 px (script
   cảnh báo). Footage → `scripts/shorts_speed.py` cắt dọc và ramp tốc độ.
4. **Shot cutout**: viết spec JSON cho từng cảnh ảnh (`scripts/shorts_reveal.py --example`), lấy
   mốc `in` của mỗi người từ `words.json` → render MP4.
5. **Ghép** (ffmpeg concat hoặc Premiere sequence 1080×1920) theo thứ tự lời; thêm light leak /
   tint / grain ở chỗ chuyển đoạn; nhạc Mixkit sidechain dưới giọng.
6. **Caption**: `scripts/shorts_captions.py words.json caps.ass --burn ghep.mp4 short.mp4`.
7. **Loudness** −14 LUFS / −1 dBTP (cách làm như `export/_loudnorm.sh`).
8. **Cover**: `scripts/shorts_thumb.py cutout.png "TỪ1\nTỪ2" cover.png --team XXX --preview`,
   xem file `_shelf.png` (crop 2:3 trên kệ Shorts).
9. Chạy checklist cuối `shorts-spec.md`. Tiêu đề = câu hỏi + `#nba #nbanews #basketball #<đội> #<cầu thủ>`.

Cài một lần (đã cài trên máy này 17/11/2026): `pip install "rembg[cpu]" faster-whisper`.
ffmpeg lấy từ PATH hoặc `imageio_ffmpeg`. Font đã có trong `assets/fonts/`
(`Montserrat-ExtraBold.ttf` tách tĩnh từ bản variable — libass không chọn được độ đậm của font
variable; `Anton-Regular.ttf`); thiếu thì script tự dùng Segoe UI Black / Impact.
Bản chạy thử đầy đủ (VO 6 s, nhóm 3 người, caption, cover): `D:\TuLieuLamNoiDung\media\_shorts_test\`.

## Facebook meme posts

Bài ảnh cho trang **Turn On Hoops** (fb.com/turnonhoops). Mỗi bài là 1 ảnh 1200×1200, tin NBA nóng kèm cú lật hài hước,
tiếng Anh, giọng mỉa mai tỉnh bơ học từ Troll Bóng Đá.
**Đọc `references/facebook-post.md` trước.** File này gồm 6 nguyên tắc hài, 10 công thức có số reaction,
cách chọn tin nóng, thư viện meme, giới hạn, quy trình và checklist.

Tóm tắt:
- **Tin phải nóng (< 24 giờ) và có tên tuổi.** Chạy `scripts/nba_hot_topics.py`, dùng WebSearch, xem r/nba qua trình duyệt, rồi chấm điểm.
  **Xác nhận đội hình hôm nay**: mùa 2026-27 nhiều sao đã đổi đội, đừng tin trí nhớ.
- **Sự thật trước, cú lật sau.** Tầng 1 là tin/chỉ số có nguồn, tầng 2 là câu đá xoáy.
  Ảnh thật là chính, meme là gia vị.
- **Thư viện meme** nằm trong skill: `assets/memes/` (1.897 template imgflip đã nén, 103 MB,
  64 nhóm nghĩa). Tìm bằng prompt:
  `python scripts/meme_search.py "<ý muốn, tiếng Việt hoặc Anh>" --sheet pick.jpg`.
  **Meme giữ nguyên ảnh gốc, không ghép mặt cầu thủ**; ai là ai thì ghi bằng nhãn chữ.
- **Dựng ảnh**: `scripts/fb_post.py spec.json post.jpg`, với 7 layout. Khung vàng, logo góc trên phải,
  footer FB + YouTube đã có sẵn trong script.
- **Caption 2–8 từ**, không link. Lời thoại đùa phải đóng khung "PROBABLY:". Đá xoáy màn trình diễn, không đá xoáy con người.
- **Đăng**: `mcp__facebook__post_photos(alias="turn_on_hoops", …)`, **chỉ sau khi người dùng duyệt ảnh + caption**.
  Có thể đặt lịch theo giờ vàng ET.

## Index reference

| File | Nội dung |
|---|---|
| `references/longform-theme.md` | **Theme long-form chuẩn "Vice neon"**: màu, font, khung footage, 8 mẫu đồ hoạ, chuyển động, thẻ chương, end card |
| `scripts/lf_theme.py` | Module theme: token màu/font, `frame_overlay`, `footage_filter`, 8 mẫu đồ hoạ động từ JSON, `chapter_card`, `title_card`, `end_card` |
| `references/shorts-spec.md` | **Shorts**: số đo 3 video mẫu, cấu trúc, caption, cutout animation, slow-mo, cover, checklist |
| `references/shorts-analysis-data/` | Contact sheet, chuỗi frame từng hiệu ứng, điểm cắt của 3 Shorts mẫu |
| `scripts/shorts_cutout.py` | Tách cầu thủ khỏi nền ảnh (rembg) → PNG trong suốt |
| `scripts/shorts_reveal.py` | Render cảnh cutout: trồi lên / trượt vào lần lượt, bóng đen + glint, light leak, chữ pop |
| `scripts/shorts_speed.py` | Cắt dọc 9:16 + ramp tốc độ (slow-mo / 1× / nhanh) cho footage |
| `scripts/shorts_words.py` | Timestamp từng từ của file VO (faster-whisper cục bộ), sửa chính tả tên theo kịch bản |
| `scripts/shorts_captions.py` | Caption 1–2 từ từ `words.json` → ASS, burn vào video |
| `scripts/shorts_thumb.py` | Cover Shorts: nền màu đội, tiêu đề 2 dòng, cutout đè chữ, xem crop 2:3 |
| `references/edit-grammar.md` | Cấu trúc, nhịp, timing — đo từ SOFA Zone |
| `references/visual-spec.md` | Màu, font, treatment ladder, bản địa hoá US |
| `references/script-template.md` | 4 template chapter map theo format |
| `references/premiere-recipes.md` | Stack effect từng treatment · telestration · bake animation · **bảng bẫy đã gặp** |
| `references/sources.md` | Nguồn data, ảnh, footage, nhạc + license |
| `references/sofa-analysis-data/` | Dữ liệu đo gốc 5 video SOFA Zone: nhịp cắt, khung đen, nhạc, stats5.json, DO_DAC.md (số liệu một video), ảnh kiểm tra |
| `scripts/make_chart.py` | Sinh biểu đồ động từ CSV |
| `scripts/make_overlays.sh` | Sinh scanline / grain / vignette bằng ffmpeg |
| `scripts/commons_search.py` | Tìm ảnh Wikimedia Commons, in kèm license + tác giả |
| `references/facebook-post.md` | **Facebook meme posts**: văn phong Troll Bóng Đá → NBA, 10 công thức, chọn tin nóng, thư viện meme, giới hạn, quy trình đăng |
| `scripts/fb_post.py` | Render ảnh bài Facebook 1200×1200 (7 layout, chữ vàng/trắng, logo, footer FB/YT, nhãn trên meme) |
| `assets/memes/` | 1.897 meme imgflip đã nén (`templates/`) + `meme_index.json` (nhóm nghĩa) + `catalog_raw.json` |
| `scripts/meme_search.py` | Tìm meme theo nghĩa từ prompt Việt/Anh, xuất contact sheet |
| `scripts/meme_build_index.py`, `meme_semantics.py`, `meme_extra_tags*.py` | Nhóm nghĩa, nhãn tay, danh sách nhạy cảm → dựng lại `meme_index.json` |
| `scripts/nba_hot_topics.py` | Radar tin nóng NBA từ ESPN (tỉ số, top scorer, tin mới, chấm điểm độ nóng) |
| `scripts/music_analyze.py` | Dò nhạc nền (có/vắng, điểm đổi bản) trong bản mix có cả lời |
| `scripts/duck_analyze.py` | Đo cân bằng giọng/nhạc và độ nâng nhạc ở khoảng lặng |
