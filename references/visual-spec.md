## Khung hình chủ đạo — footage KHÔNG full-bleed

Đo 4 video (685 mẫu, 1 khung/10 s): **footage sân cỏ chỉ chiếm 27% thời lượng**
(haaland 51% · psg 38% · ucl 24% · zidane 16%). Phần còn lại là đồ hoạ, chân dung, khung thiết kế.

**Đây không phải kênh dùng footage.** Hai phần ba thời lượng là hình do họ dựng ra. Rất hợp với
format bảng lương / tiểu sử NBA vốn không được dùng nhiều footage.

Và quan trọng hơn: **khi có footage, nó gần như luôn nằm trong khung, không tràn viền.**
Mẫu lặp đi lặp lại ở cả 4 video:

- Footage đặt trong **hình chữ nhật bo góc**. Đo pixel trên 9 frame: **69–95% chiều ngang,
  trung bình 82%** → footage thật còn ~1571×900 px (69% số pixel của 1080p)
- Nền quanh khung là **lưới ô vuông rất tối** (không phải đen tuyệt đối — có texture kẻ ô mờ)
- **HUD giả** ở đáy khung: `▶ 20`, `Replay ▶|`, đôi khi có **timecode** kiểu `00:21:30:00`
- Thỉnh thoảng có caption một dòng dưới khung

Tài liệu cũ xếp "frame-within-frame" là một trong nhiều thủ pháp. **Sai — nó là mặc định.**
Full-bleed mới là ngoại lệ, dành cho khoảnh khắc lớn.

**Shot footage được giữ rất lâu** — trung vị 10–17 giây, trong khi shot đồ hoạ chỉ 3,5–4,6 giây.
Đừng băm footage nhỏ. Chi tiết và phần cảnh báo về bản quyền ở `sources.md` mục "Cách SOFA Zone
trình bày footage" — **khung lồng là lựa chọn thẩm mỹ, không phải biện pháp bản quyền.**

## Bumper logo — logo CÓ xuất hiện giữa video

Tài liệu cũ viết "không có logo trong phần thân". **Sai.** Có, nhưng không phải watermark góc:

- **Khung toàn màn hình gần như đen, logo SOFA ZONE ở giữa, màu xám rất tối**, độ tương phản
  thấp đến mức gần chìm vào nền
- Dùng làm **nhịp nghỉ giữa các đoạn**, không phải để quảng bá
- Tần suất: **0–7 lần mỗi video** (haaland 0 · zidane 1 · ucl 4 · psg 7), tổng ~1.8% thời lượng

Vẫn đúng: **không có watermark ở góc** (0% pixel đứng yên trên toàn video).

Sang Turn On Hoops: dùng logo bóng rổ vàng ở giữa khung đen, **giảm opacity xuống ~15–20%**
để nó chìm chứ không chói. Đặt ở 2–4 điểm chuyển chương lớn.

## Mở đầu — 3/5 video mở bằng ĐỒ HOẠ, không phải footage

Tài liệu cũ (rút từ một video) viết "mở lạnh vào footage". **Không phải quy tắc.** Đo 5 video:

| Video | Mở đầu |
|---|---|
| haaland | Đồ hoạ: số **"100"** cỡ lớn + ảnh cầu thủ cắt nền, nền tối ánh vàng |
| psg | Đồ hoạ: nền sao trời, bóng người đổ bóng, dấu **"??"** đỏ |
| zidane | Đồ hoạ: **dòng thời gian** gồm các thẻ ảnh bo góc trôi trên nền sao trời, mốc năm |
| pep | Footage có telestration |
| ucl | Footage ăn mừng, grade bloom mạnh |

Hai motif lặp lại đáng học:

- **Nền sao trời / không gian tối** làm nền cho đồ hoạ mở đầu (psg, zidane)
- **Thẻ ảnh bo góc trôi trên nền tối**, xếp theo dòng thời gian hoặc so sánh (zidane)

Vẫn đúng ở cả 5 video: **không có sting logo mở đầu.** Mở đầu là nội dung, không phải thương hiệu.

## Chapter card — có biến thể trên nền ảnh

Ngoài kiểu nền đen + serif nghiêng đã ghi, còn một kiểu nữa đo được ở `ucl`:

- Nền là **ảnh liên quan, làm tối mạnh** (không phải đen trơn)
- Chữ **hai dòng**: dòng trên trắng cỡ nhỏ hơn, dòng dưới **vàng, nghiêng, cỡ lớn**
- Canh giữa khung

Dùng kiểu nền ảnh cho chapter có nhân vật cụ thể; kiểu nền đen cho chapter về khái niệm/số liệu.

## Telestration — thủ pháp chủ đạo, đo từ `dGlI0rts0AI`

Đây là mảng lớn nhất mà tài liệu cũ bỏ sót. Trong video Pep Guardiola, **telestration xuất
hiện liên tục từ frame 0** và là lý do video "nhiều hình minh hoạ" mà vẫn mạch lạc: nó không
cắt sang hình khác để giải thích, nó **vẽ thẳng lên hình đang chạy**.

Bốn loại, đo được trong video:

| Loại | Mô tả | Dùng khi |
|---|---|---|
| **Vùng tô** | Mảng màu bán trong suốt phủ một khu vực sân, có viền trắng mảnh, bên trong kẻ sọc | Chỉ không gian bị chiếm / bỏ trống |
| **Mũi tên** | Nét đứt hoặc nét liền, màu tương phản với sân, có đầu mũi tên | Hướng di chuyển, đường chuyền |
| **Vòng chân cầu thủ** | Ellipse dẹt ôm chân cầu thủ, màu phân biệt hai đội | Chỉ đích danh người |
| **Bảng chiến thuật** | Nền tối, sơ đồ sân trắng mảnh, chấm số theo đội hình | Khi cần sơ đồ sạch, không có footage phù hợp |

**Telestration có animation, không đứng yên.** Đo ở 0.0 → 2.0 s: vùng tô lớn dần và đổi hình
theo pha bóng. Vẽ tĩnh rồi để yên là mất hẳn hiệu quả.

**Ghép ảnh cắt nền lên đồ hoạ:** ở 0:12 có chân dung Guardiola cắt nền đặt đè lên bảng chiến
thuật. Rẻ mà hiệu quả — nối người với sơ đồ trong cùng một khung.

### Sang NBA

| Bóng đá | NBA tương đương |
|---|---|
| Vùng tô khoảng trống giữa tuyến | Tô vùng paint / corner three bị bỏ trống |
| Mũi tên đường chuyền | Đường chuyền, đường cắt, hướng drive |
| Vòng chân cầu thủ | Vòng chân, `#E8912A` cho nhân vật chính, trắng cho đồng đội, `#555555` cho đối thủ |
| Bảng chiến thuật cả sân | Sơ đồ **nửa sân**, half-court set |

⚠️ Telestration vẽ đè lên footage NBA **vẫn là footage NBA** — rủi ro Content ID không giảm.
Xem `sources.md`. Với format bảng lương / tiểu sử không có footage, chuyển nguyên tắc này sang
**chart**: đừng để chart đứng yên, cho nó hiện dần khớp lời kể (xem mục "Chart reveal" dưới).

## Chart reveal — áp nguyên tắc telestration cho đồ hoạ

Chart tĩnh đứng yên 20–40 giây là điểm chết của format không có footage. Cách chữa:

- **Bar chart**: từng thanh hiện dần theo thứ tự câu chuyện, không hiện cùng lúc
- **Chart nhiều tầng**: hiện từng tầng khớp lúc narration nhắc tới
- **Khi narration đọc một danh sách tên**: gắn mỗi mục vào **đúng mốc giọng đọc**, đừng chia đều

Cách lấy mốc giọng đọc mà không phải nghe thủ công:

```
ffmpeg -i vo.wav -af silencedetect=n=-45dB:d=0.12 -f null - 2>&1 | grep silence_end
```

Mỗi `silence_end` là một lần giọng bắt đầu nói lại. Với câu liệt kê "Tên, con số." thì mỗi mục
cho hai onset (tên, rồi con số) — lấy onset tên làm mốc hiện.

Bake animation vào media bằng ffmpeg đáng tin hơn keyframe trong Premiere: che bằng `drawbox`
rồi gỡ che bằng `enable='lt(t,T)'`. Xem `premiere-recipes.md`.

## End card — đo trên 5 video, có 3 biến thể

**Luôn có**, luôn ở cuối, luôn **4–6 giây**, luôn chiếm toàn khung. Nhưng nội dung khác nhau:

| Kiểu | Thấy ở | Nội dung |
|---|---|---|
| **A — Cảm ơn** | pep, haaland | Nền xanh ngọc, chấm bi halftone, chữ display đậm nén "THANKS FOR WATCHING", avatar kênh tròn |
| **B — Bằng chứng xã hội** | psg, zidane | Ảnh nhân vật bên trái, panel logo xanh bên phải, dòng chữ mời đăng ký, thanh credit ở đáy |
| **C — Cộng đồng** | ucl | Ảnh chụp màn hình group/community, panel logo xanh bên phải |

**Cấu trúc chung ở cả ba:** nền xanh thương hiệu · hoạ tiết chấm halftone · ký hiệu `»` ·
panel logo · **thanh CTA ở đáy** (`LIKE | COMMENT | SHARE | SUBSCRIBE`).

Kiểu B và C nhồi nhiều chữ tiếng Việt và bằng chứng xã hội — **đó là đặc thù thị trường Việt,
không mang sang Mỹ**. Lấy kiểu A.

### Khuyến nghị cho Turn On Hoops

Giữ cấu trúc "thương hiệu chỉ ở cuối", nhưng **đổi bảng màu**: logo Turn On Hoops là
vàng `#FFC629` trên navy. Dùng vàng làm nền end card sẽ chói và phá hệ màu đen/cam của chart.
Hai cách an toàn hơn:

1. **Nền đen, logo lớn giữa khung, chữ trắng** — liền mạch với chapter card, an toàn nhất
2. **Nền navy đậm của logo**, chữ trắng, một vạch vàng mảnh — có thương hiệu mà không chói

Dòng CTA: viết thường, một dòng, `Like · Comment · Subscribe`. Khán giả Mỹ dị ứng CTA to và
nhiều. **Không đọc CTA bằng lời** — để chữ làm việc đó.

## US adaptation — chỉ đổi những thứ này

### Tiêu đề
SOFA Zone: `Why FLICK-BALL Makes Barcelona The Most SCARIEST TEAM Now? | SOFA Zone`

Chuẩn Mỹ (đo từ JxmyHighroller, 2.66M subs, ~1M views/video):
`There May Never Be Another GOAT` · `This Trade Would Break The NBA` ·
`How A 5 Year Old Beef Destroyed The Greatest Season In NBA History`

Quy tắc:
- Viết hoa đầu từ, **không ALL CAPS** trừ tối đa một từ
- **Không hậu tố tên kênh**
- Tạo khoảng trống tò mò, không nhồi từ khoá
- 4–11 từ
- Ưu tiên câu khẳng định gây tranh cãi hơn câu hỏi

### Thumbnail
SOFA Zone: viền màu quanh ảnh + badge series góc trái + chữ gradient vàng cỡ lớn +
dải chữ phụ dưới đáy + 3–5 nhân vật cắt ghép.

JxmyHighroller: ảnh game thô hoặc ghép đơn giản, **gần như không chữ**, không viền, không badge.

Khuyến nghị (lai, giữ chất lượng SOFA nhưng theo chuẩn thị trường):
- 1 nhân vật chính cắt nền, chiếm 40–60% khung
- **0–3 từ**, sans đậm trắng, không gradient, không stroke nhiều lớp
- Không viền khung, không badge
- Nền tối, có độ sâu, một nguồn sáng

### Mật độ chữ trên hình
Bỏ phụ đề burn-in. Ngân sách chữ: tối đa **một khối text đang hiện tại một thời điểm**,
và không quá 7 từ mỗi khối. Chỗ trống do bỏ phụ đề lấp bằng chart / ảnh archival / chapter card.

### Telestration, end card, chuyển cảnh
- **Telestration**: giữ nguyên, thậm chí tăng. Thị trường NBA Mỹ đã quen (Thinking Basketball).
- **End card**: giữ cấu trúc, đổi màu (xem trên). Giữ ở 5–7 giây, đừng dài hơn.
- **Chuyển cảnh có hiệu ứng**: giữ ~30% như đo được, nhưng chọn loại trầm (whip, zoom blur nhẹ),
  tránh flash trắng — khán giả Mỹ gắn flash trắng với nội dung giật gân.

### Giọng narration
SOFA Zone nghiêng kịch tính. Khán giả NBA Mỹ dị ứng giọng "documentary thổi phồng" khi
số liệu không đỡ nổi. Giữ nhịp dồn của SOFA, hạ tính từ xuống, để con số làm phần kịch tính.
