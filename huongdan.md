HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY ỨNG DỤNG TẢI VIDEO YOUTUBE (DÀNH CHO MACOS)
Tài liệu này hướng dẫn chi tiết cách thiết lập môi trường và khởi chạy ứng dụng trên máy tính MacBook từ tệp mã nguồn tải về từ GitHub (không yêu cầu cài đặt công cụ Git).

Bước 1: Tải mã nguồn ứng dụng
Truy cập vào đường dẫn kho lưu trữ GitHub do người gửi cung cấp bằng trình duyệt web.

Nhấp vào nút màu xanh có chữ <> Code, sau đó chọn Download ZIP.

Sau khi tải xuống hoàn tất, nhấp đúp vào tệp .zip để giải nén thành một thư mục thông thường.

Bước 2: Cài đặt các công cụ nền cho hệ thống macOS
Ứng dụng yêu cầu hệ thống phải cấu hình sẵn môi trường Python, Node.js và công cụ giải mã FFmpeg để hoạt động.

Cài đặt Python 3 (Ngôn ngữ chạy ứng dụng):

Truy cập: python.org/downloads/macos/

Tải xuống phiên bản cài đặt định dạng .pkg mới nhất (Khuyến nghị bản Stable 3.11 hoặc 3.12).

Mở tệp vừa tải và tiến hành cài đặt theo các bước mặc định của hệ thống.

Cài đặt Node.js (Bộ giải mã thuật toán YouTube):

Truy cập: nodejs.org

Tải xuống bản cài đặt định dạng .pkg (Chọn phiên bản có nhãn LTS để đảm bảo tính ổn định).

Thực hiện chạy tệp và cài đặt vào hệ thống.

Cấu hình bộ gộp luồng video/audio (FFmpeg cho Mac):

Truy cập trang lưu trữ binary của Mac: evermeet.cx/ffmpeg/

Tải xuống tệp nén ffmpeg (Định dạng .zip hoặc .7z).

Giải nén để lấy một tệp thực thi duy nhất tên là ffmpeg.

Mở thư mục dự án đã giải nén ở Bước 1, tạo một thư mục mới tên là ffmpeg_bin nằm ngay tại thư mục gốc của dự án.

Sao chép (hoặc di chuyển) tệp ffmpeg vừa giải nén ở trên vào bên trong thư mục ffmpeg_bin này.

Bước 3: Cài đặt thư viện và khởi chạy ứng dụng
Mở ứng dụng Terminal tích hợp sẵn trên hệ điều hành macOS (Tìm trong Spotlight hoặc thư mục Applications/Utilities).

Nhập lệnh cd  (Lưu ý: Có một dấu cách phía sau chữ cd).

Kéo và thả thư mục dự án từ cửa sổ Finder vào thẳng màn hình Terminal để hệ thống tự điền đường dẫn, sau đó nhấn Enter.

Thực hiện cài đặt các thư viện Python cần thiết bằng cách sao chép và chạy lệnh sau:

Bash
pip3 install -r requirements.txt
Khởi chạy giao diện ứng dụng bằng lệnh:

Bash
python3 main.py
💡 Hướng dẫn đóng gói thành ứng dụng độc lập (.app)
Nếu không muốn mỗi lần sử dụng đều phải mở Terminal để gõ lệnh, bạn có thể tự đóng gói dự án thành một file ứng dụng Mac thông thường (click đúp để chạy):

Tại cửa sổ Terminal hiện tại (đã trỏ đúng thư mục dự án), chạy lệnh cài đặt bộ đóng gói:

Bash
pip3 install pyinstaller
Thực hiện lệnh biên dịch và đóng gói:

Bash
pyinstaller --noconsole --windowed --name="YTDownloader" main.py
Sau khi tiến trình kết thúc, mở thư mục dự án ra, truy cập vào thư mục dist/. Tại đây sẽ xuất hiện một tệp ứng dụng có tên là YTDownloader.app.

Sử dụng promt dưới đây để paste vào AI hướng dẫn
Bạn là AI hỗ trợ kỹ thuật cho người dùng macOS không chuyên công nghệ.

Nhiệm vụ của bạn:

* hướng dẫn người dùng cài đặt và chạy ứng dụng Python từ source code GitHub trên macOS
* giải thích cực kỳ dễ hiểu
* hướng dẫn từng bước rõ ràng
* ưu tiên thực hành
* không dùng thuật ngữ phức tạp nếu không cần

Bối cảnh:

* người dùng đã tải source code dạng ZIP từ GitHub
* không biết Git
* không quen Terminal
* chỉ cần chạy được app

Ứng dụng yêu cầu:

* Python 3
* Node.js
* FFmpeg
* pip
* PyInstaller

Project có cấu trúc:

```text id="vp0h9e"
project/
├── main.py
├── requirements.txt
├── core/
├── ui/
└── ffmpeg_bin/
```

FFmpeg binary phải nằm tại:

```text id="l3n5xu"
ffmpeg_bin/ffmpeg
```

Ứng dụng được chạy bằng:

```bash id="z9f7ke"
python3 main.py
```

Khi trả lời:

* luôn chia theo STEP/BƯỚC
* mỗi bước phải có:

  * mục tiêu
  * thao tác cụ thể
  * lệnh cần chạy
  * giải thích ngắn
* markdown rõ ràng
* có block code đầy đủ
* dễ copy-paste
* tối ưu cho macOS
* không lan man
* không yêu cầu Git
* không yêu cầu Homebrew
* không yêu cầu VSCode

Bạn phải hướng dẫn đầy đủ:

1. tải ZIP từ GitHub
2. giải nén project
3. cài Python trên macOS
4. cài Node.js
5. tải FFmpeg binary
6. tạo thư mục ffmpeg_bin
7. đặt file ffmpeg đúng vị trí
8. mở Terminal
9. dùng lệnh cd bằng kéo-thả thư mục
10. chạy:

```bash id="1mzw7j"
pip3 install -r requirements.txt
```

11. chạy app:

```bash id="v7q2ec"
python3 main.py
```

12. build thành file:

```text id="m8b4tp"
.app
```

bằng PyInstaller
13. xử lý lỗi phổ biến:

* command not found
* permission denied
* python3 not found
* pip3 not found
* ffmpeg missing
* app cannot be opened
* cảnh báo bảo mật macOS

Mục tiêu cuối cùng:
giúp một người dùng MacBook không biết lập trình vẫn có thể tự chạy ứng dụng thành công.
