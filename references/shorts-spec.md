# Shorts — spec đo từ kênh mẫu

Nguồn đo: 3 Shorts tải về 17/11/2026 (cùng một kênh NBA news, host nói trước mic):

| ID | Tiêu đề | Dài |
|---|---|---|
| `QrE50nPu4sw` | The Warriors have one last star to chase | 1:04 |
| `Rq0pUEKwWac` | What are the odds this deal goes down | 1:16 |
| `c75x3FYP97M` | Who should try and trade for Kyrie Irving | 1:02 |

Cùng 3 ảnh cover (Last Chance / Warriors Trade / Free Agents). Contact sheet, chuỗi frame của
từng hiệu ứng và danh sách điểm cắt nằm trong `shorts-analysis-data/`.

> Đây là style **khác hẳn** long-form. Các quy tắc long-form "không burn-in phụ đề", "footage
> lồng khung 82 %", "giữ footage 10–17 s" **không áp dụng cho Shorts**. Các quy tắc còn giữ:
> fact-check, không lặp asset, ảnh tĩnh phải chuyển động, ảnh cầu thủ thật (tải từ bất kỳ nguồn internet nào),
> loudness −14 LUFS / −1 dBTP.

## Số đo

| Chỉ số | v1 | v2 | v3 | Dùng |
|---|---|---|---|---|
| Thời lượng | 64 s | 76 s | 62 s | **55–75 s** |
| Shot trung vị (scene-detect, gộp < 0,4 s) | 1,67 s | 0,90 s | 1,55 s | **0,9–1,7 s** |
| Shot dài nhất | 8,6 s | 6,4 s | 4,2 s | giữ tối đa ~6 s, chỉ cho cảnh reveal/slow-mo |
| Khoảng lặng ≥ 0,25 s (−40 dB) | 0 | 0 | 0 | **không có lỗ**: nhạc chạy liên tục dưới lời |
| Loudness | −14,7 | −17,2 | −16,5 LUFS | ta giữ **−14 LUFS / −1 dBTP** (họ chạm 0 dBTP) |
| LRA | 3,4 | 3,6 | 2,8 | nén mạnh, giọng sát tai |
| Khung | 1080×1920, 60 fps | | | ta xuất 1080×1920, 30 fps (60 nếu nhiều slow-mo) |
| Footage | **tràn viền 9:16**, crop từ nguồn 16:9 | | | không khung, không HUD |

Scene-detect đếm cả chuyển động mạnh trong shot nên số shot hơi cao hơn thực tế; xu hướng
vẫn rõ: Shorts cắt nhanh gấp ~6–10 lần long-form.

## Cấu trúc (giống nhau ở cả 3)

| Đoạn | Thời điểm | Nội dung |
|---|---|---|
| **Hook bí ẩn** | 0–4 s | Câu hỏi/khẳng định gây tò mò + hình **che danh tính**: cầu thủ bị bôi đen thành bóng (v1), bị pixel hoá (v3), hoặc ảnh ghép nhiều ngôi sao + light leak (v3 3–6 s). Reveal ở giây 3–5, có lens glint |
| **Host vào** | 5–9 s | Host nói trước mic, nền tím xanh: "so let me explain" |
| Thân | 9 s → cuối −5 s | B-roll + ảnh cutout, host quay lại **mỗi 15–20 s** (3 lần/video) như nhịp "reset" |
| **Payoff** | ~70–85 % | Con số / gói trade được dựng lên từng phần |
| **CTA** | 2–3 s cuối | Host: "let me know down in the comments" / "follow for more". Câu cuối dang dở để loop về đầu |

Kênh mình **không có host trên hình** (giọng VoiceStudio, profile NBA Commenter - David). Thay mỗi lần "host vào" bằng một
**nhịp reset** cùng chức năng: shot cutout chân dung chủ thể trên nền mờ, hoặc thẻ số liệu.
Đừng bỏ nhịp reset — nó chia video thành các đoạn 15–20 s, đúng bằng tầm chú ý trên Shorts.

## Captions (auto caption kiểu CapCut)

Đo ở frame 1080×1920:
- **1–2 từ mỗi lần**, đổi theo từng từ nói, không bao giờ cả câu.
- IN HOA, sans hình học rất đậm (**Montserrat ExtraBold**), trắng, cao chữ ~40 px (≈ size 54).
- Nền: hộp tối bán trong suốt (~60 % đen) sát chữ + bóng đổ mềm.
- Vị trí: giữa ngang, tâm ở **~63 % chiều cao** (dưới mặt, trên UI YouTube).
- Hiện ra bằng pop nhẹ, thay thế ngay — không fade, không karaoke tô từng chữ.
- Có mặt 100 % thời lượng có lời, cả lúc host nói.

Tô màu từ khoá (tên, con số) không thấy ở kênh mẫu; `--hl` có sẵn nhưng dùng tiết chế
(≤ 1 từ / 5 giây), mặc định tắt.

Cách làm: TTS bằng VoiceStudio (profile NBA Commenter - David, xem SKILL.md mục Giọng đọc) → `scripts/shorts_words.py vo.mp3 words.json --script script.txt`
(faster-whisper cục bộ; `--script` thay chính tả tên bằng chữ trong kịch bản khi số từ khớp)
→ `scripts/shorts_captions.py words.json caps.ass --burn in.mp4 out.mp4`.
Lấy timestamp từ **file VO đã xuất**, không từ kịch bản: TTS hay đọc lệch số và tên.

## Tách nhân vật + animation xuất hiện

Kỹ thuật chủ đạo của kênh mẫu với ảnh tĩnh. Đo từng frame (xem `seq_*.png`):

**1. Một người** — cutout trên nền là chính ảnh đó làm mờ/tối, cả khối push-in chậm.

**2. Nhóm (v1 12–15 s)** — "LeBron… to Jaylen Brown… to Giannis":
- người chính **trồi lên từ dưới + phóng to** (86 → 100 %, ~0,45 s, ease-out) ở giữa;
- người thứ hai **trượt vào từ trái**, người thứ ba **từ phải**, đứng **phía sau** người chính,
  mỗi người vào đúng lúc lời nhắc tên (cách nhau 0,5–0,8 s);
- nền tối gần đen (khán đài mờ), cả nhóm tiếp tục push-in khi đã đủ người.

**3. Gói trade (v2 50–56 s)** — Butler + Banchero, rồi "the young… Yaxel… Lendeborg" thêm từng
người chen vào giữa, cuối cùng chữ to **"+1ST ROUND PICKS"** pop ở trên. Mỗi tên trong lời = một
người xuất hiện.

**4. Ghép nhiều sao (v3 3–6 s)** — 6 cutout xếp chồng kín khung (2 cột × 3 hàng), light leak
cam + tia lửa quét qua, push-in.

**5. Hook bóng đen (v1 0–5 s)** — cầu thủ ở tiền cảnh bị bôi đen thành bóng, lens glint loé ở
góc trên, rồi **rack focus**: tiền cảnh nhoè đi, cầu thủ ở hậu cảnh (Curry) nét lên.

Dựng bằng `scripts/shorts_reveal.py spec.json out.mp4` (`--example` in spec mẫu). Cutout bằng
`scripts/shorts_cutout.py` (cần `pip install "rembg[cpu]"`). Thứ tự trong `layers` = thứ tự xếp
lớp (đầu = sau cùng): **đặt người chính cuối danh sách** nhưng cho `in` sớm nhất.
Mốc `in` lấy từ timestamp từ trong `words.json` (lúc tên được đọc), không canh tay.

Đã chạy thử (17/11/2026, `media/_shorts_test/spec.json`), kích thước cân cho nhóm 3:
người chính `h 0.60, x 0.50, bottom 1.04`; hai bên `h 0.60–0.62, x 0.22 / 0.80, bottom 1.0`.
Người chính to hơn ~0.70 sẽ che gần hết hai người phụ. Hướng nhìn: người bên trái nên quay mặt
vào giữa (`flip` nếu cần). Tách nền: chọn ảnh cầu thủ không bị người khác che; chân/tay người
khác dính liền vào thân sẽ không tự loại được — crop chặt hơn.

## Tiết tấu nhanh–chậm & slow motion

- Đoạn kể sự kiện / play-by-play: tốc độ **1×**, cắt 0,6–1,5 s, reframe dọc theo bóng.
- Khoảnh khắc cảm xúc (dunk treo vành, ăn mừng, ánh mắt nhìn): **slow-mo ~0,3–0,4×**, giữ 2–4 s
  (v2 44–47 s: Banchero treo vành, gào lên, lời đang nói "nobody else… his size").
- Nhịp đi theo câu: câu ngắn đanh → cắt nhanh; câu hỏi lơ lửng / con số lớn → chậm lại.
- Chuyển giữa hai đoạn: **light leak** cam (v3 4–5 s), **tint đơn sắc** cam (v2 40 s),
  **nhiễu hạt tan** (v2 50 s), punch-in zoom. Không dùng wipe/slide của template.

Dựng bằng `scripts/shorts_speed.py in.mp4 out.mp4 "0-1.8:1, 1.8-3.2:0.35"` (`--smooth` nội suy
khung cho nguồn 30 fps, `--x` chọn tâm crop dọc).

## Đồ hoạ trên hình (ngoài caption)

- **Thẻ số liệu**: số to màu đội + nhãn trắng, căn trái, xếp dọc (22 PPG / 8 REB / 5 AST), đè
  lên ảnh cầu thủ; số đếm lên. Số liệu → fact-check như long-form.
- **Ảnh chụp tin báo**: headline + tác giả + ngày, card tối ở 1/5 trên khung, đè lên ảnh — làm
  bằng chứng cho tin đồn. Chỉ trích headline, ghi nguồn rõ.
- **Chữ pop lớn**: font tiêu đề (Anton), trắng, 1/8 trên khung ("+1ST ROUND PICKS").

## Thumbnail / cover

Đo trên 3 cover (xem cùng ảnh mẫu):
- Nền **một màu đội** đặc, gradient toả (sáng ở giữa trên, tối ở góc). Màu theo **đội trong câu
  chuyện**, không nhất thiết đội cầu thủ đang mặc (Booker áo Suns nhưng nền xanh Warriors).
- Tiêu đề **1–2 từ**, IN HOA, font condensed rất đậm (Anton), trắng, 2 dòng xếp chồng, rộng
  ~85–90 % khung, ở 1/3 trên. Có quầng tối mờ sau chữ.
- **Một** cầu thủ, cắt tới ngực, ở giữa, **đầu đè lên mép dưới dòng chữ thứ hai** (người đứng
  trước chữ). Biểu cảm mạnh (cười, gào, nhìn thẳng).
- Không logo, không mũi tên, không emoji, không viền.
- Kệ Shorts hiển thị crop **2:3 ở giữa** (1080×1607 trong 1080×1920): chữ và mặt phải nằm trong
  y = 156…1763.

Từ khoá tiêu đề đã thấy: LAST CHANCE, WARRIORS TRADE, FREE AGENTS → ngắn, là chủ đề chứ không
là câu. Dựng bằng `scripts/shorts_thumb.py cutout.png "WARRIORS\nTRADE" out.png --team GSW --preview`.
Script tự đặt đỉnh đầu cao hơn mép dưới chữ 4,5 % khung (`--overlap`), nên **ảnh cover phải là
chân dung, đầu là điểm cao nhất**: ảnh giơ tay ném/dunk sẽ để bàn tay đè lên chữ thay cho đầu
(đã gặp khi thử với Curry). Crop cutout tới ngực bằng `shorts_cutout.py --crop`.

## Tiêu đề & mô tả video

Tiêu đề là **câu hỏi hoặc tuyên bố mở** (không phải tên chủ đề như cover): "Who should try and
trade for Kyrie Irving", "What are the odds this deal goes down". Theo sau là hashtag:
`#nba #nbanews #basketball #<tênđội> #<têncầuthủ>`.

## Không copy

- **Ảnh chế áo đấu** (Booker mặc áo Warriors, Butler áo khác…) — kênh mẫu dùng nhiều. Đó là ảnh
  cầu thủ thật bị chỉnh sửa; quy tắc của skill vẫn là không tạo/chỉnh mặt cầu thủ bằng AI. Muốn
  minh hoạ trade thì đặt hai cutout thật cạnh nhau + logo/màu đội đích.
- Footage trận lấy từ highlight của kênh khác — xem `sources.md`; Shorts bị Content ID quét như
  video dài.
- Peak chạm 0 dBTP như kênh mẫu.

## Checklist trước khi xuất Short

1. Hook 0–3 s có hình che danh tính hoặc ảnh ghép, câu đầu là câu hỏi/khẳng định gây tò mò.
2. Có nhịp reset mỗi 15–20 s.
3. Caption phủ toàn bộ lời, 1–2 từ, tâm ở 63 % chiều cao, không bị UI che.
4. Mọi ảnh tĩnh đều có chuyển động (push-in / cutout animation); không shot nào đứng yên > 2 s.
5. Ít nhất một đoạn slow-mo đặt đúng khoảnh khắc cảm xúc; phần còn lại 1×.
6. Nhạc chạy liên tục, không lỗ; −14 LUFS / −1 dBTP.
7. Câu cuối nối về câu đầu (loop) hoặc CTA comment.
8. Cover: 1–2 từ, một cầu thủ, nền màu đội, kiểm tra crop 2:3.
9. Số liệu đã có trong `facts.md`.
