import customtkinter as ctk
from PIL import Image
import requests
import io
import threading
from core.downloader import DownloaderTask


class DownloadCard(ctk.CTkFrame):
    def __init__(self, master, task: DownloaderTask, **kwargs):
        super().__init__(master, **kwargs)
        self.task = task

        # Map các hàm callback an toàn
        self.task.on_progress = self.update_progress
        self.task.on_complete = self.on_complete
        self.task.on_error = self.on_error

        # Cấu hình grid hệ thống card
        self.grid_columnconfigure(1, weight=1)

        # Thumbnail
        self.thumb_label = ctk.CTkLabel(self, text="Loading...", width=120, height=68, fg_color="gray20")
        self.thumb_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
        self._load_thumbnail_async()

        # Title & Định dạng video (Hàng 0)
        info_text = f"{self.task.title} ({self.task.format_type} - {self.task.quality})"
        self.title_label = ctk.CTkLabel(self, text=info_text, anchor="w", justify="left", font=("Arial", 12, "bold"))
        self.title_label.grid(row=0, column=1, sticky="ew", padx=10, pady=(10, 2))

        # Progress Bar hiển thị realtime (Hàng 1)
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=1, sticky="ew", padx=10, pady=2)

        # Status Label hiển thị trạng thái (Hàng 2)
        self.status_label = ctk.CTkLabel(self, text=self.task.status, font=("Arial", 11), text_color="yellow",
                                         anchor="w")
        self.status_label.grid(row=2, column=1, sticky="w", padx=10, pady=(0, 10))

        # Nút Cancel thông minh
        self.cancel_btn = ctk.CTkButton(
            self,
            text="Cancel",
            width=60,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=self.cancel_download
        )
        self.cancel_btn.grid(row=0, column=2, rowspan=3, padx=10, pady=10)

    def _load_thumbnail_async(self):
        def fetch_image():
            if not self.task.thumb_url:
                self.after(0, lambda: self.thumb_label.configure(text="No Image"))
                return
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                response = requests.get(self.task.thumb_url, headers=headers, timeout=5)
                image_data = Image.open(io.BytesIO(response.content))
                img = ctk.CTkImage(light_image=image_data, dark_image=image_data, size=(120, 68))
                self.after(0, lambda: self.thumb_label.configure(image=img, text=""))
            except Exception:
                self.after(0, lambda: self.thumb_label.configure(text="No Image"))

        threading.Thread(target=fetch_image, daemon=True).start()

    def update_progress(self, progress: float):
        # Tránh update UI nếu user đã chủ động bấm Cancel trước đó
        if self.task.status == "Canceled":
            return
        self.after(0, self._update_ui_progress, progress)

    def _update_ui_progress(self, progress: float):
        self.progress_bar.set(progress)
        self.status_label.configure(text=f"Downloading ({int(progress * 100)}%)", text_color="#2196f3")

    def on_complete(self):
        self.after(0, self._ui_complete)

    def _ui_complete(self):
        self.progress_bar.set(1.0)
        self.status_label.configure(text="Completed", text_color="#4caf50")
        # Hoàn thành thành công thì đổi nút thành Disabled dạng màu xám
        self.cancel_btn.configure(state="disabled", fg_color="gray", text="Done")

    def on_error(self, error_msg: str):
        self.after(0, lambda: self._ui_error(error_msg))

    def _ui_error(self, error_msg: str):
        # Khi bị lỗi, không block nút Cancel nữa mà chuyển công năng thành nút "Clear" hoặc giữ nguyên để user hủy task kẹt
        self.status_label.configure(text="Failed (Skipped)", text_color="#f44336")
        self.cancel_btn.configure(text="Clear", fg_color="gray30", hover_color="gray40")
        print(f"[Download Error] Task {self.task.title} failed: {error_msg}")

    def cancel_download(self):
        """Xử lý hủy luồng và dọn dẹp card UI lập tức khi bấm"""
        # Gửi tín hiệu cancel cho luồng core của yt-dlp ngắt lệnh ngay lập tức
        self.task.cancel()

        # Cập nhật trạng thái hiển thị trên card
        self.status_label.configure(text="Canceled / Cleared", text_color="gray")
        self.progress_bar.set(0)
        self.cancel_btn.configure(state="disabled", fg_color="gray")

        # Làm hiệu ứng mờ card đi để báo hiệu task đã bị loại bỏ
        self.configure(fg_color="gray10")
        self.title_label.configure(text_color="gray50")

        # Sau 0.5 giây tự động ẩn/xóa card này khỏi giao diện hàng chờ cho đỡ rối mắt
        self.after(500, self.pack_forget)