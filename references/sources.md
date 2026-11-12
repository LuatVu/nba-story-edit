# Nguồn & license

## Dữ liệu — bắt buộc đối chiếu trước khi lên hình

| Loại | Nguồn chốt | Ghi chú |
|---|---|---|
| Lương, hợp đồng, cap | **Spotrac**, **HoopsHype** | Hai nguồn lệch nhau thì ghi rõ "theo Spotrac" |
| Cap / tax / apron, luật CBA | Văn bản CBA của NBA, **CapSheets** (Yossi Gozlan) | Yossi là analyst chuyên cap, kênh @ThirdApron |
| Stats mọi thời kỳ | **Basketball-Reference** | Chuẩn de-facto của cộng đồng |
| Stats chính thức, tracking | **NBA.com/stats** | Số liệu tracking chỉ có từ 2013–14 |
| Giao dịch, tiểu sử | **RealGM**, Basketball-Reference | |

Quy trình: ghi `facts.md` cạnh project, mỗi dòng = con số + nguồn + ngày truy xuất.
In ngày truy xuất lên góc dưới phải mỗi chart, `#9A9A9A`, 18px.

## Ảnh

| Nguồn | Dùng được? |
|---|---|
| **Wikimedia Commons** | **Có — miễn phí, không mua license. Nguồn chính cho kênh này.** Xem mục dưới |
| Getty Images / NBAE via Getty | Có — phải mua license editorial |
| AP Images | Có — mua license |
| Unsplash / Pexels | Có — cho b-roll chung, **không có ảnh cầu thủ NBA** |
| Google Images | **Không** |

## Wikimedia Commons — hướng dẫn dùng thật

https://commons.wikimedia.org/wiki/Main_Page

Miễn phí, không tốn tiền license. Nhưng **không phải "dùng sao cũng được"** — mọi ảnh đều là
Creative Commons và **bắt buộc ghi credit**. Mục này ghi lại những gì đã kiểm chứng khi làm
video top-10 lương 2026-27.

### Tìm ảnh

Dùng `scripts/commons_search.py` (chỉ cần Python, không cần cài gì):

```bash
python3 scripts/commons_search.py "Jimmy Butler basketball" "Devin Booker"
```

Script in ra kích thước, **license**, tác giả, ngày chụp — đủ để chọn mà không phải mở trình duyệt.
Nó tự giãn cách request; gọi API quá nhanh sẽ bị **HTTP 429**.

Tải file gốc (thay `2400` bằng bề ngang mong muốn):

```
https://commons.wikimedia.org/wiki/Special:FilePath/<TÊN%20FILE>?width=2400
```

### Nhiếp ảnh gia đáng nhớ

| Tác giả | License | Ghi chú |
|---|---|---|
| **Erik Drost** | **CC BY 2.0** | Kho NBA lớn nhất trên Commons, ảnh 8256×5504. Có trọn bộ **NBA All-Star Game 2022**. Chỉ cần ghi credit, **không dính ShareAlike** → ưu tiên tuyệt đối |
| **Daiei Onoguchi** | **CC BY 4.0** | Ảnh mới (đã thấy bộ NBA Cup 12.2025). Cũng không dính ShareAlike |
| All-Pro Reels | CC BY-SA 2.0 | ⚠️ ShareAlike |
| Keith Allison | CC BY-SA 2.0 | ⚠️ ShareAlike |
| Cyrus Saatsaz | CC BY-SA 4.0 | ⚠️ ShareAlike |
| Hameltion | CC BY-SA 4.0 | ⚠️ ShareAlike |

### ⚠️ Bẫy 1 — CC BY khác CC BY-**SA**

- `CC BY` → chỉ cần ghi credit. **An toàn, ưu tiên dùng.**
- `CC BY-SA` → thêm nghĩa vụ **ShareAlike**: tác phẩm phái sinh phải phát hành dưới license
  tương thích. Video có chèn ảnh BY-SA đã chỉnh sửa rất có thể bị coi là phái sinh, nghĩa là
  **cả video** phải để CC BY-SA — tức người khác được tái sử dụng video của bạn.

ShareAlike **không cấm kiếm tiền** (nó không phải NonCommercial). Nhưng nếu không muốn video
bị tái sử dụng, **chỉ dùng ảnh CC BY**. Lọc theo cột license trong kết quả script.

Lưu ý: ô "License" trong YouTube Studio chỉ có *Standard* và *Creative Commons – Attribution
(CC BY)*. **CC BY không thoả ShareAlike** — phải ghi dòng license trong phần mô tả.

### ⚠️ Bẫy 2 — thiếu ảnh cầu thủ MỚI ĐỔI ĐỘI

Nói cho chính xác: Commons **không** thiếu ảnh mới nói chung — tìm "Victor Wembanyama" ra ảnh
CC BY 4.0 chụp 12.2025. Chỗ thiếu rất cụ thể: **cầu thủ vừa chuyển nhượng, trong áo đội mới**.
Tổ hợp người + đội mới cần thời gian mới có người chụp và upload.

Vậy nên: cầu thủ ở yên một đội thì thường có ảnh tốt và mới. Cầu thủ vừa trade thì phải
xử lý theo ba cách dưới. Khi làm video 11.2026:

- Giannis → Heat (07.2026): **không có ảnh áo Heat**
- Anthony Davis → Wizards (02.2026): **chỉ có ảnh Lakers và Pelicans**
- Jaylen Brown → 76ers (07.2026): **chỉ có ảnh Celtics**
- Jimmy Butler → Warriors: **không có ảnh áo Warriors**

Đã tìm bằng cả tên người lẫn tên đội mới, không có.

**Ba cách xử lý, theo thứ tự ưu tiên:**

1. **Dùng ảnh All-Star Game** — áo All-Star **trung tính, không mang logo đội nào**, nên
   không bao giờ hiện sai logo. Bộ All-Star 2022 của Erik Drost có gần hết các ngôi sao.
   Đây là cách sạch nhất cho cầu thủ mới đổi đội.
2. **Dùng ảnh áo cũ đúng ngữ cảnh** — nếu lời kể đang nói về đội cũ ("Boston traded him to
   Philadelphia") thì ảnh áo Boston là **đúng**, không phải lỗi. Ghi rõ trong lower-third.
3. **Không dùng ảnh** — thay bằng card số trên nền đen, cùng ngôn ngữ với chart. Dùng khi
   không có ảnh nào đúng ngữ cảnh (ví dụ Davis: Lakers và Pelicans đều sai, không câu nào cứu).

**Luôn bake lower-third ghi đội hiện tại + số liệu.** Đó là chỗ mang thông tin đúng, không
phải cái áo.

### Bắt buộc khi xuất bản

Dán vào mô tả YouTube, kèm **dòng khai đã sửa ảnh** (CC yêu cầu):

```
IMAGE CREDITS
Photos via Wikimedia Commons. Images were cropped and colour-graded.

<Tên cầu thủ...> — © <Tác giả> — CC BY 2.0
  https://creativecommons.org/licenses/by/2.0/
```

Nếu có dùng ảnh BY-SA, thêm:

```
This video contains material licensed under CC BY-SA and is therefore
released under the Creative Commons Attribution-ShareAlike 4.0 licence.
https://creativecommons.org/licenses/by-sa/4.0/
```

*Đây là tóm tắt điều khoản license, không phải tư vấn pháp lý.*

## Footage

NBA quét Content ID rất gắt, gắt hơn phần lớn giải bóng đá. Cả họp báo và nội dung
media day cũng là tài sản NBA.

**Được:**
- Clip ngắn có narration đè lên, phục vụ bình luận/phân tích (fair use — vẫn có rủi ro claim)
- Footage tự quay
- Stock có license (Getty Video, AP Archive)
- Nội dung không cần game footage: chart, ảnh, motion graphic — đây là hướng an toàn nhất
  và đúng với format tiểu sử / bảng lương

**Không được:**
- Upload lại compilation của kênh khác. SOFA Zone có làm việc này — thấy watermark
  "MESOPOTAMIA" và "TOP FOOTBALL HD" trong frame video của họ. Đừng copy phần đó.
- Highlight dài không có bình luận
- Full trận, full hiệp

## Cách SOFA Zone trình bày footage — ĐO ĐƯỢC

### Khung lồng (đo pixel trên 9 frame, 4 video)

| | |
|---|---|
| Bề rộng khung lồng | **69%–95% chiều ngang**, trung bình **82%** |
| Độ phân giải footage thật bên trong | ~**1571×900 px** |
| So với full 1080p | còn ~**69% số pixel** |
| Nền quanh khung | lưới ô vuông rất tối, **không phải đen tuyệt đối** |
| Phụ kiện | HUD giả ở đáy (`▶ 20`, `Replay ▶\|`), đôi khi timecode `00:21:30:00` |
| Full-bleed | có, nhưng là **ngoại lệ** cho khoảnh khắc lớn |

### Độ dài shot footage — ngược với trực giác

Đo riêng shot có footage so với shot đồ hoạ (haaland + ucl):

| | footage sân cỏ | đồ hoạ / chân dung |
|---|---|---|
| haaland | trung vị **17.4 s** | trung vị **3.5 s** |
| ucl | trung vị **10.2 s** | trung vị **4.6 s** |

**Footage được giữ RẤT LÂU, đồ hoạ mới là thứ cắt nhanh.** Đã kiểm chứng bằng ba phương pháp
độc lập (scene detect ngưỡng 0.28, ngưỡng 0.10, và dò đột biến frame-to-frame): trong một
đoạn footage 58 giây chỉ có **3 lần cắt thật**.

Hệ quả cho dựng: **đừng băm footage thành mảnh 2 giây.** Giữ một pha bóng 10–20 giây,
để telestration và giọng kể làm việc trên đó. Băm nhỏ vừa mệt vừa sai phong cách.

### ⚠️ Nhưng ĐỪNG coi cách trình bày này là biện pháp bản quyền

Có ba hiểu lầm phổ biến, cần nói thẳng:

**1. Cắt bỏ logo của kênh nguồn làm tình hình XẤU ĐI, không tốt lên.**
Logo/watermark là thông tin quản lý bản quyền. Ở Mỹ, cố ý gỡ bỏ nó là **một vi phạm riêng
biệt** (DMCA §1202), độc lập với việc dùng clip. Nó biến "có thể tranh luận fair use" thành
"có dấu hiệu cố ý". Nếu buộc phải dùng clip có watermark của bên thứ ba thì vấn đề nằm ở chỗ
**đừng dùng nguồn đó** — đi tìm nguồn gốc hoặc nguồn có license.

**2. Thu nhỏ và giảm độ phân giải không thay đổi tình trạng bản quyền.**
Số đo ở trên cho thấy họ chỉ giảm còn ~69% số pixel — gần như không giảm. Và Content ID
so khớp bằng vân tay nội dung, bền với co giãn, đổi khung, đổi màu, đổi tốc độ. Đây là
**lựa chọn thẩm mỹ** (tạo cảm giác đang xem lại băng tư liệu), không phải lớp bảo vệ.

**3. Thứ thật sự có trọng lượng là tính chất sử dụng, không phải hình thức.**
Cái giúp lập luận fair use: **trích đoạn ngắn**, có **bình luận/phân tích đè lên liên tục**,
clip phục vụ luận điểm đang nói chứ không phải để người xem thưởng thức trận đấu,
và **không thay thế** việc xem nguồn gốc. Khung lồng + HUD có hỗ trợ gián tiếp vì nó trình bày
clip như tư liệu đang được mổ xẻ — nhưng chỉ khi phần bình luận thật sự tồn tại.

*Đây là tóm tắt cách các yếu tố thường được cân nhắc, không phải tư vấn pháp lý.
Nếu kênh bắt đầu có doanh thu đáng kể, hỏi luật sư.*

### Quy trình khi có asset footage

Khi người dùng đưa file cảnh quay / highlight để cắt minh hoạ:

1. **Hỏi nguồn trước khi cắt.** Tự quay / có license / fair use? Nếu là tải từ kênh khác thì
   nói rõ rủi ro trước, đừng lặng lẽ cắt.
2. **Mỗi trích đoạn 10–20 giây**, khớp đúng một luận điểm trong script. Không ghép thành
   montage dài không lời.
3. **Luôn có narration đè lên.** Đoạn footage không lời là đoạn yếu nhất về cả fair use
   lẫn phong cách — kênh này có mật độ lời 96–98%.
4. **Đóng khung 82% chiều ngang** trên nền lưới tối, thêm HUD. Công thức ở
   `premiere-recipes.md` (Treatment B/C).
5. **Telestration lên trên** — đây mới là phần biến clip thành phân tích.
6. **Ghi nguồn** trong mô tả video nếu clip không phải tự quay.

## Nhạc & SFX

Epidemic Sound · Artlist · Musicbed · Soundstripe — đều cần thuê bao.
Không dùng nhạc "no copyright" trôi nổi trên YouTube: phần lớn không có giấy tờ thật.

## Font (đều free, SIL OFL)

- EB Garamond / Cormorant Garamond — chapter card
- Inter — nhãn, số
- Archivo — tiêu đề chart
- Space Mono / JetBrains Mono — HUD giả

Tải từ Google Fonts hoặc GitHub của từng font.
