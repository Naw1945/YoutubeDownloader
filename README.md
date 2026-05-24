
```markdown
# Ứng Dụng Tải Video YouTube (Desktop Application)

Dự án xây dựng một ứng dụng desktop hoàn chỉnh, hỗ trợ tải video và âm thanh (MP3) từ nền tảng YouTube. Ứng dụng được tối ưu hóa giao diện tiếng Việt, hỗ trợ xử lý tải hàng loạt theo danh sách phát (Playlist) hoặc toàn bộ kênh (Channel).

Hệ thống được phát triển dựa trên ngôn ngữ **Python 3.11+**, sử dụng thư viện **CustomTkinter** để xây dựng giao diện người dùng (GUI) và thư viện **yt-dlp** làm lõi xử lý tải xuống, đảm bảo tốc độ tối đa và tối ưu hóa khả năng bypass cơ chế chặn bot của YouTube.

---

## Các Tính Năng Chính

- **Tải xuống đa chế độ:** Hỗ trợ xử lý liên kết video đơn lẻ, liên kết danh sách phát hoặc liên kết trang chủ của một kênh YouTube.
- **Bộ lọc số lượng nâng cao:** Cho phép người dùng tùy chọn tải toàn bộ danh sách, hoặc giới hạn chỉ tải X video đầu tiên hoặc X video cuối cùng.
- **Tự động chuyển đổi định dạng:** Hỗ trợ tách luồng âm thanh và tự động mã hóa sang định dạng MP3 chất lượng cao (192kbps).
- **Giao diện đa luồng (Multi-threading):** Tiến trình tải xuống và giải mã được thực thi trên các luồng độc lập, đảm bảo giao diện chính không bị đóng băng (Not Responding) trong suốt quá trình xử lý.
- **Cập nhật tiến độ thời gian thực:** Hiển thị trực quan trạng thái, ảnh thu nhỏ (Thumbnail) và thanh tiến trình tải xuống của từng tiến trình riêng biệt.
- **Cơ chế chống chặn kết nối:** Giả lập các client ứng dụng di động (Android/iOS) và tự động thiết lập cơ chế kết nối lại (Retry) khi đường truyền chập chờn, khắc phục triệt để lỗi ngắt kết nối đột ngột (Error 10054).
- **Quản lý tệp tin tiện lợi:** Cho phép thay đổi thư mục lưu trữ tùy ý và tích hợp tính năng mở nhanh thư mục chứa tệp tin từ giao diện ứng dụng.

---

## Yêu Cầu Hệ Thống Và Cài Đặt

### Bước 1: Cài đặt các thư viện Python phụ thuộc
Sau khi sao chép mã nguồn về máy tính, mở giao diện dòng lệnh (Terminal/Command Prompt) tại thư mục gốc của dự án và thực thi lệnh sau:

```bash
pip install -r requirements.txt

```

### Bước 2: Cấu hình các công cụ bổ trợ (Binary Runtimes)

Ứng dụng yêu cầu công cụ xử lý đa phương tiện (**FFmpeg**) để gộp luồng video/audio và môi trường chạy JavaScript (**Node.js**) để giải mã thuật toán của YouTube.

Người dùng cần tạo một thư mục tên là **`ffmpeg_bin`** tại thư mục gốc của dự án, sau đó thực hiện cấu hình theo hệ điều hành tương ứng:

#### 1. Cấu hình trên hệ điều hành Windows

* Truy cập trang chủ [gyan.dev](https://www.google.com/search?q=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) để tải xuống tệp nén FFmpeg. Giải nén và sao chép hai tệp `ffmpeg.exe` và `ffprobe.exe` vào thư mục `ffmpeg_bin`.
* Truy cập [nodejs.org](https://www.google.com/search?q=https://nodejs.org/dist/v20.11.1/node-v20.11.1-win-x64.zip) để tải xuống phiên bản Node.js Portable. Giải nén và sao chép tệp `node.exe` vào thư mục `ffmpeg_bin`.

#### 2. Cấu hình trên hệ điều hành macOS

Trên macOS, không cần thêm tệp vào thư mục `ffmpeg_bin`. Thực hiện cài đặt trực tiếp vào hệ thống thông qua các bước sau:

* Mở Terminal và cài đặt FFmpeg thông qua trình quản lý gói Homebrew: `brew install ffmpeg`
* Tải và cài đặt gói Node.js chuẩn (định dạng `.pkg`) từ trang chủ [nodejs.org](https://nodejs.org/).

---

## Hướng Dẫn Khởi Chạy Ứng Dụng

Thực hiện lệnh sau tại thư mục gốc của dự án để khởi động giao diện người dùng:

```bash
python main.py

```

---

## Hướng Dẫn Đóng Gói Thành Tệp Thực Thi (.exe / .app)

Để đóng gói ứng dụng thành một tệp đơn lẻ có thể chạy độc lập mà không cần môi trường Python, sử dụng thư viện `PyInstaller`:

```bash
# Cài đặt công cụ đóng gói
pip install pyinstaller

# Lệnh đóng gói trên hệ điều hành Windows (Xuất bản tệp .exe)
pyinstaller --noconsole --name="YTDownloader" main.py

# Lệnh đóng gói trên hệ điều hành macOS (Xuất bản ứng dụng .app)
pyinstaller --noconsole --windowed --name="YTDownloader" main.py

```

*Sản phẩm sau khi đóng gói thành công sẽ nằm trong thư mục `dist/`.*

---

## Cấu Trúc Thư Mục Dự Án

```text
youtube_downloader/
│
├── main.py              # Điểm khởi chạy chính của ứng dụng
├── requirements.txt     # Danh sách các thư viện Python cần cài đặt
├── .gitignore           # Cấu hình loại bỏ các tệp tin rác và tệp tin mã máy của Git
│
├── core/                # Tầng xử lý logic nghiệp vụ ngầm (Backend Logic)
│   ├── downloader.py    # Điều khiển tiến trình yt-dlp và cấu hình vị trí FFmpeg
│   ├── metadata.py      # Trích xuất thông tin tiêu đề, hình ảnh và danh sách video
│   └── queue_manager.py # Quản lý hàng chờ và phân phối luồng tải xuống
│
├── ui/                  # Tầng xử lý giao diện người dùng (Frontend GUI)
│   ├── app.py           # Thiết lập bố cục, bộ lọc số lượng và cửa sổ ứng dụng chính
│   └── components/
│       └── download_card.py # Thiết kế thành phần hiển thị tiến trình của từng video
│
└── ffmpeg_bin/          # Thư mục chứa các tệp thực thi bổ trợ (Đã được cấu hình bỏ qua trên Git)

```

```

```
Markdown
---

## Quy Trình Xử Lý Khi YouTube Cập Nhật Thuật Toán

YouTube thường xuyên cập nhật cơ chế mã hóa (Signature Cipher) và hệ thống chặn bot, điều này có thể dẫn đến các lỗi đột xuất như: `This video is not available`, lỗi trích xuất dữ liệu (Extraction Error), hoặc không thể tải ảnh thu nhỏ.

Khi xảy ra các hiện tượng trên, người vận hành hoặc người dùng cuối thực hiện xử lý theo các bước kiểm tra và khắc phục sau:

### Bước 1: Cập nhật thư viện lõi `yt-dlp` lên phiên bản mới nhất
Đội ngũ phát triển `yt-dlp` luôn phát hành các bản vá lỗi trong vòng vài giờ sau khi YouTube thay đổi thuật toán. Đây là giải pháp khắc phục 90% các lỗi liên quan đến việc không nhận diện được liên kết.

Mở giao diện dòng lệnh tại thư mục dự án và thực thi:
```bash
pip install -U --no-cache-dir yt-dlp
Bước 2: Xóa bộ nhớ đệm (Cache) của ứng dụng
yt-dlp lưu trữ chứng thư và cấu hình phiên làm việc cũ trong bộ nhớ đệm hệ thống. Khi thuật toán YouTube thay đổi, dữ liệu cũ này có thể gây xung đột.

Thực hiện lệnh sau để xóa sạch bộ nhớ đệm:

Bash
yt-dlp --rm-cache-dir
Bước 3: Đóng gói lại tệp thực thi (Nếu ứng dụng đã được build)
Nếu ứng dụng đã được đóng gói thành tệp .exe hoặc .app độc lập để chuyển giao cho người dùng không rành về IT, người phát triển bắt buộc phải thực hiện lại quy trình đóng gói (như hướng dẫn tại mục Đóng gói ứng dụng) sau khi đã hoàn thành Bước 1 và Bước 2 trên máy phát triển.

Bước 4: Kiểm tra trạng thái IP (Trường hợp bị chặn diện rộng)
Nếu đã cập nhật phiên bản mới nhất nhưng tất cả các video vẫn báo lỗi kết nối hoặc lỗi chặn truy cập, có khả năng địa chỉ IP mạng hiện tại đã bị đưa vào danh sách đen (Blacklist) của Google do tần suất gửi yêu cầu (Request) quá tải.

Cách khắc phục: Tạm thời thay đổi địa chỉ IP bằng cách khởi động lại thiết bị Modem mạng, hoặc sử dụng các giải pháp mạng riêng ảo (VPN/Proxy) để thay đổi tuyến đường truyền dữ liệu.