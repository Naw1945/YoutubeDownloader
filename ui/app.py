import os
import threading
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox

from core.queue_manager import QueueManager
from core.metadata import fetch_metadata
from core.downloader import DownloaderTask
from ui.components.download_card import DownloadCard


class YoutubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Trình Tải Video YouTube")
        self.geometry("850x720")
        self.minsize(850, 600)

        self.queue_manager = QueueManager()
        self.queue_manager.on_task_added = self.add_card_to_ui

        self.save_dir = os.path.abspath("downloads")

        self._build_ui()

    def _build_ui(self):
        input_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        input_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.url_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Dán link Video, link Kênh, link Danh sách phát YouTube vào đây",
            width=400
        )
        self.url_entry.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.download_btn = ctk.CTkButton(
            input_frame,
            text="Tải Xuống",
            font=("Arial", 13, "bold"),
            command=self.process_url
        )
        self.download_btn.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        input_frame.grid_columnconfigure(0, weight=1)

        opt_frame = ctk.CTkFrame(
            input_frame,
            fg_color="transparent"
        )
        opt_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=5
        )

        ctk.CTkLabel(
            opt_frame,
            text="Định dạng:"
        ).pack(
            side="left",
            padx=5
        )

        self.format_var = ctk.StringVar(value="MP4")

        self.format_menu = ctk.CTkOptionMenu(
            opt_frame,
            values=["MP4", "MP3"],
            variable=self.format_var,
            width=90
        )
        self.format_menu.pack(
            side="left",
            padx=5
        )

        ctk.CTkLabel(
            opt_frame,
            text="Chất lượng:"
        ).pack(
            side="left",
            padx=(15, 5)
        )

        self.quality_var = ctk.StringVar(value="1080p")

        self.quality_menu = ctk.CTkOptionMenu(
            opt_frame,
            values=["Tốt Nhất", "1080p", "720p", "480p"],
            variable=self.quality_var,
            width=110
        )
        self.quality_menu.pack(
            side="left",
            padx=5
        )

        self.dir_btn = ctk.CTkButton(
            opt_frame,
            text="Lưu vào...",
            width=90,
            fg_color="gray25",
            hover_color="gray35",
            command=self.choose_directory
        )
        self.dir_btn.pack(
            side="right",
            padx=5
        )

        self.open_dir_btn = ctk.CTkButton(
            opt_frame,
            text="📁 Mở Thư Mục",
            width=120,
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            command=self.open_storage_folder
        )
        self.open_dir_btn.pack(
            side="right",
            padx=5
        )

        filter_frame = ctk.CTkFrame(
            input_frame,
            fg_color="gray13",
            corner_radius=6
        )
        filter_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=5,
            padx=5
        )

        ctk.CTkLabel(
            filter_frame,
            text="Chế độ Playlist/Kênh:",
            font=("Arial", 11, "bold")
        ).pack(
            side="left",
            padx=10,
            pady=5
        )

        self.range_var = ctk.StringVar(value="Tải Toàn Bộ")

        self.range_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=[
                "Tải Toàn Bộ",
                "X Video Đầu Tiên",
                "X Video Cuối Cùng"
            ],
            variable=self.range_var,
            width=150,
            command=self._toggle_count_entry
        )
        self.range_menu.pack(
            side="left",
            padx=5,
            pady=5
        )

        self.count_label = ctk.CTkLabel(
            filter_frame,
            text="Số lượng (X):",
            text_color="gray60"
        )
        self.count_label.pack(
            side="left",
            padx=(15, 5),
            pady=5
        )

        self.count_entry = ctk.CTkEntry(
            filter_frame,
            width=60,
            placeholder_text="10"
        )
        self.count_entry.pack(
            side="left",
            padx=5,
            pady=5
        )

        self.count_entry.configure(state="disabled")

        storage_opt_frame = ctk.CTkFrame(
            input_frame,
            fg_color="gray13",
            corner_radius=6
        )
        storage_opt_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(5, 0),
            padx=5
        )

        self.auto_folder_var = ctk.StringVar(value="off")
        self.folder_checkbox = ctk.CTkCheckBox(
            storage_opt_frame,
            text="Phân loại theo thư mục tên Kênh",
            variable=self.auto_folder_var,
            onvalue="on",
            offvalue="off",
            font=("Arial", 11, "bold")
        )
        self.folder_checkbox.pack(
            side="left",
            padx=10,
            pady=8
        )

        self.custom_folder_entry = ctk.CTkEntry(
            storage_opt_frame,
            placeholder_text="Nhập tên thư mục riêng ",
            width=380
        )
        self.custom_folder_entry.pack(
            side="right",
            padx=10,
            pady=5,
            fill="x",
            expand=True
        )

        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            label_text="Danh Sách Hàng Chờ Tải Xuống"
        )
        self.scroll_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    def _toggle_count_entry(self, choice: str):
        if choice == "Tải Toàn Bộ":
            self.count_entry.delete(0, "end")
            self.count_entry.configure(state="disabled")
        else:
            self.count_entry.configure(state="normal")
            self.count_entry.insert(0, "5")

    def choose_directory(self):
        folder = filedialog.askdirectory(initialdir=self.save_dir)

        if folder:
            self.save_dir = folder

    def open_storage_folder(self):
        try:
            if not os.path.exists(self.save_dir):
                os.makedirs(
                    self.save_dir,
                    exist_ok=True
                )

            if os.name == "nt":
                os.startfile(self.save_dir)

            elif os.name == "darwin":
                subprocess.Popen([
                    "open",
                    self.save_dir
                ])

            else:
                subprocess.Popen([
                    "xdg-open",
                    self.save_dir
                ])

        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                f"Không thể mở thư mục: {e}"
            )

    def process_url(self):
        url = self.url_entry.get().strip()

        if not url:
            return

        self.download_btn.configure(
            state="disabled",
            text="Đang quét..."
        )

        threading.Thread(
            target=self._fetch_and_add,
            args=(url,),
            daemon=True
        ).start()

    def _fetch_and_add(self, url: str):
        info = fetch_metadata(url)

        self.after(
            0,
            lambda: self.download_btn.configure(
                state="normal",
                text="Tải Xuống"
            )
        )

        self.after(
            0,
            lambda: self.url_entry.delete(0, "end")
        )

        if not info:
            self.after(
                0,
                lambda: messagebox.showerror(
                    "Lỗi hệ thống",
                    "Không thể lấy thông tin video. Hãy kiểm tra lại đường dẫn mạng."
                )
            )
            return

        fmt = self.format_var.get()

        qty = self.quality_var.get()

        if qty == "Tốt Nhất":
            qty = "Best"

        mode = self.range_var.get()

        count_val = 0

        if mode != "Tải Toàn Bộ":
            try:
                count_val = int(
                    self.count_entry.get().strip()
                )

                if count_val <= 0:
                    raise ValueError

            except ValueError:
                self.after(
                    0,
                    lambda: messagebox.showerror(
                        "Lỗi nhập liệu",
                        "Vui lòng nhập một số nguyên dương hợp lệ cho số lượng (X)."
                    )
                )
                return

        entries = []

        if "entries" in info:
            entries = list(info["entries"])

            if mode == "X Video Đầu Tiên":
                entries = entries[:count_val]

            elif mode == "X Video Cuối Cùng":
                entries = entries[-count_val:]

        else:
            entries = [info]

        custom_folder_name = self.custom_folder_entry.get().strip()
        is_split_by_channel = (self.auto_folder_var.get() == "on")

        if custom_folder_name:
            final_save_path = os.path.join(self.save_dir, custom_folder_name)
        else:
            final_save_path = self.save_dir

        for entry in entries:
            if not entry:
                continue

            video_url = entry.get(
                "url",
                entry.get("webpage_url", url)
            )

            task = DownloaderTask(
                video_id=entry.get("id", "unknown"),
                url=video_url,
                title=entry.get(
                    "title",
                    "Video Không Rõ Tiêu Đề"
                ),
                thumb_url=entry.get("thumbnail", ""),
                format_type=fmt,
                quality=qty,
                save_path=final_save_path,
                split_by_channel=is_split_by_channel
            )

            self.after(
                0,
                self.queue_manager.add_task,
                task
            )

    def add_card_to_ui(self, task: DownloaderTask):
        card = DownloadCard(
            self.scroll_frame,
            task=task,
            fg_color="gray15",
            corner_radius=10
        )

        card.pack(
            fill="x",
            padx=10,
            pady=5
        )