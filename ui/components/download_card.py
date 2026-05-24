import customtkinter as ctk
from PIL import Image
import requests
import io
import threading
from core.downloader import DownloaderTask

_THUMBNAIL_LOCK = threading.BoundedSemaphore(3)


class DownloadCard(ctk.CTkFrame):
    def __init__(self, master, task: DownloaderTask, **kwargs):
        super().__init__(master, **kwargs)
        self.task = task

        self.task.on_progress = self.update_progress
        self.task.on_complete = self.on_complete
        self.task.on_error = self.on_error

        self.grid_columnconfigure(1, weight=1)

        self.thumb_label = ctk.CTkLabel(self, text="Chờ tải...", width=120, height=68, fg_color="gray20")
        self.thumb_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

        self._load_thumbnail_async()

        info_text = f"{self.task.title} ({self.task.format_type} - {self.task.quality})"

        self.title_label = ctk.CTkLabel(
            self,
            text=info_text,
            anchor="w",
            justify="left",
            font=("Arial", 12, "bold")
        )
        self.title_label.grid(row=0, column=1, sticky="ew", padx=10, pady=(10, 2))

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=1, sticky="ew", padx=10, pady=2)

        self.status_label = ctk.CTkLabel(
            self,
            text=self.task.status,
            font=("Arial", 11),
            text_color="yellow",
            anchor="w"
        )
        self.status_label.grid(row=2, column=1, sticky="w", padx=10, pady=(0, 10))

        self.cancel_btn = ctk.CTkButton(
            self,
            text="Hủy",
            width=60,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=self.cancel_download
        )
        self.cancel_btn.grid(row=0, column=2, rowspan=3, padx=10, pady=10)

    def _load_thumbnail_async(self):
        def fetch_image():
            if (not self.task.thumb_url or not isinstance(self.task.thumb_url, str)) and self.task.video_id:
                self.task.thumb_url = f"https://img.youtube.com/vi/{self.task.video_id}/hqdefault.jpg"

            if not self.task.thumb_url or not self.task.thumb_url.startswith("http"):
                self.after(0, lambda: self.thumb_label.configure(text="Không ảnh"))
                return

            with _THUMBNAIL_LOCK:
                try:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                    }

                    import urllib3
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

                    response = requests.get(
                        self.task.thumb_url,
                        headers=headers,
                        timeout=5,
                        verify=False
                    )

                    if response.status_code == 200:
                        raw_data = io.BytesIO(response.content)
                        image_data = Image.open(raw_data).convert("RGB")
                        img = ctk.CTkImage(
                            light_image=image_data,
                            dark_image=image_data,
                            size=(120, 68)
                        )
                        self.after(
                            0,
                            lambda: self.thumb_label.configure(image=img, text="")
                        )
                    else:
                        self.after(
                            0,
                            lambda: self.thumb_label.configure(text="Lỗi ảnh")
                        )

                except Exception:
                    self.after(
                        0,
                        lambda: self.thumb_label.configure(text="Không ảnh")
                    )

        threading.Thread(
            target=fetch_image,
            daemon=True
        ).start()

    def update_progress(self, progress: float, speed: str = "0 KB/s", eta: str = "00:00"):
        if self.task.status == "Canceled":
            return
        self.after(0, self._update_ui_progress, progress, speed, eta)

    def _update_ui_progress(self, progress: float, speed: str, eta: str):
        self.progress_bar.set(progress)
        self.status_label.configure(
            text=f"Đang tải ({int(progress * 100)}%)  |  Tốc độ: {speed}  |  Còn lại: {eta}",
            text_color="#2196f3"
        )

    def on_complete(self):
        self.after(0, self._ui_complete)

    def _ui_complete(self):
        self.progress_bar.set(1.0)
        self.status_label.configure(
            text="Hoàn thành",
            text_color="#4caf50"
        )
        self.cancel_btn.configure(
            state="disabled",
            fg_color="gray",
            text="Xong"
        )

    def on_error(self, error_msg: str):
        self.after(0, lambda: self._ui_error(error_msg))

    def _ui_error(self, error_msg: str):
        self.status_label.configure(
            text="Lỗi (Bỏ qua)",
            text_color="#f44336"
        )
        self.cancel_btn.configure(
            text="Xóa",
            fg_color="gray30",
            hover_color="gray40"
        )
        print(f"[Lỗi tải] Video {self.task.title} thất bại: {error_msg}")

    def cancel_download(self):
        self.task.cancel()
        self.status_label.configure(
            text="Đã hủy",
            text_color="gray"
        )
        self.progress_bar.set(0)
        self.cancel_btn.configure(
            state="disabled",
            fg_color="gray"
        )
        self.configure(fg_color="gray10")
        self.title_label.configure(
            text_color="gray50"
        )
        self.after(500, self.pack_forget)