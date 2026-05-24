Dưới đây là nội dung tệp `README.md` được viết lại theo phong cách chuyên nghiệp, nghiêm túc, tuân thủ đúng chuẩn tài liệu kỹ thuật dành cho dự án phần mềm.

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