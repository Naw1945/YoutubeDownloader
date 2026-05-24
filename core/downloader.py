import yt_dlp
import os
import threading


class DownloaderTask:
    def __init__(self, video_id: str, url: str, title: str, thumb_url: str, format_type: str, quality: str,
                 save_path: str):
        self.video_id = video_id
        self.url = url
        self.title = title
        self.thumb_url = thumb_url
        self.format_type = format_type
        self.quality = quality
        self.save_path = save_path

        self.status = "Waiting"  # Waiting, Downloading, Completed, Failed, Canceled
        self.progress = 0.0
        self._cancel_flag = False

        # Callbacks cho UI
        self.on_progress = None
        self.on_complete = None
        self.on_error = None

    def cancel(self):
        self._cancel_flag = True
        self.status = "Canceled"

    def _progress_hook(self, d):
        if self._cancel_flag:
            raise yt_dlp.utils.DownloadError("User canceled the download.")

        if d['status'] == 'downloading':
            self.status = "Downloading"
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                self.progress = downloaded / total
                if self.on_progress:
                    self.on_progress(self.progress)

        elif d['status'] == 'finished':
            self.progress = 1.0
            if self.on_progress:
                self.on_progress(self.progress)

    def run(self):
        current_file_path = os.path.abspath(__file__)
        core_dir = os.path.dirname(current_file_path)
        project_root = os.path.dirname(core_dir)
        ffmpeg_path = os.path.join(project_root, 'ffmpeg_bin')

        print(f"[Debug] Thư mục chứa FFmpeg & Node được cấu hình là: {ffmpeg_path}")
        os.environ["PATH"] = ffmpeg_path + os.path.pathsep + os.environ.get("PATH", "")
        # ──────────────────────────────────────────────────────────────────────

        opts = {
            'outtmpl': os.path.join(self.save_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'quiet': True,
            'noprogress': True,
            'no_warnings': True,
            'ffmpeg_location': ffmpeg_path,
            'retries': 10,
            'fragment_retries': 10,
            'extractor_retries': 5,
            'http_chunk_size': 10485760,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            }
        }

        if self.format_type == "MP3":
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            # MP4 Setup
            if self.quality == "Best":
                opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            else:
                res = self.quality.replace('p', '')
                opts['format'] = f'bestvideo[ext=mp4][height<={res}]+bestaudio[ext=m4a]/best[ext=mp4]/best'

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([self.url])
            if not self._cancel_flag:
                self.status = "Completed"
                if self.on_complete:
                    self.on_complete()
        except Exception as e:
            if self._cancel_flag:
                self.status = "Canceled"
            else:
                self.status = "Failed"
            if self.on_error:
                self.on_error(str(e))