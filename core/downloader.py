import yt_dlp
import os
import sys


class DownloaderTask:
    def __init__(self, video_id: str, url: str, title: str, thumb_url: str, format_type: str, quality: str,
                 save_path: str, split_by_channel: bool = False):
        self.video_id = video_id
        self.url = url
        self.title = title
        self.thumb_url = thumb_url
        self.format_type = format_type
        self.quality = quality
        self.save_path = save_path
        self.split_by_channel = split_by_channel

        self.status = "Waiting"
        self.progress = 0.0
        self.speed = "0 KB/s"
        self.eta = "00:00"
        self._cancel_flag = False

        self.on_progress = None
        self.on_complete = None
        self.on_error = None

    def cancel(self):
        self._cancel_flag = True
        self.status = "Canceled"

    def _format_speed(self, speed_bytes):
        if not speed_bytes:
            return "0 KB/s"
        if speed_bytes < 1048576:
            return f"{speed_bytes / 1024:.1f} KB/s"
        return f"{speed_bytes / 1048576:.1f} MB/s"

    def _format_eta(self, eta_seconds):
        if not eta_seconds:
            return "00:00"
        mins, secs = divmod(int(eta_seconds), 60)
        hours, mins = divmod(mins, 60)
        if hours > 0:
            return f"{hours:02d}:{mins:02d}:{secs:02d}"
        return f"{mins:02d}:{secs:02d}"

    def _progress_hook(self, d):
        if self._cancel_flag:
            raise yt_dlp.utils.DownloadError("User canceled the download.")

        if d['status'] == 'downloading':
            self.status = "Downloading"
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)

            if total > 0:
                self.progress = downloaded / total

            self.speed = self._format_speed(d.get('speed'))
            self.eta = self._format_eta(d.get('eta'))

            if self.on_progress:
                self.on_progress(self.progress, self.speed, self.eta)

        elif d['status'] == 'finished':
            self.progress = 1.0
            self.speed = "0 KB/s"
            self.eta = "00:00"
            if self.on_progress:
                self.on_progress(self.progress, self.speed, self.eta)

    def run(self):
        if hasattr(sys, '_MEIPASS'):
            ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg_bin')
            base_dir = os.path.dirname(sys.executable)
        else:
            current_file_path = os.path.abspath(__file__)
            core_dir = os.path.dirname(current_file_path)
            project_root = os.path.dirname(core_dir)
            ffmpeg_path = os.path.join(project_root, 'ffmpeg_bin')
            base_dir = project_root

        if not os.path.isabs(self.save_path):
            abs_save_path = os.path.abspath(os.path.join(base_dir, self.save_path))
        else:
            abs_save_path = self.save_path

        os.makedirs(abs_save_path, exist_ok=True)
        os.environ["PATH"] = ffmpeg_path + os.path.pathsep + os.environ.get("PATH", "")

        opts = {
            'progress_hooks': [self._progress_hook],
            'quiet': True,
            'noprogress': True,
            'no_warnings': True,
            'ffmpeg_location': ffmpeg_path,
            'extractor_args': {
                'youtube': {
                    'client': ['android', 'web', 'ios'],
                    'skip': ['dash', 'hls']
                }
            },
            'retries': 15,
            'fragment_retries': 15,
            'extractor_retries': 5,
            'http_chunk_size': 10485760,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'no-cache',
            }
        }

        if self.split_by_channel:
            opts['outtmpl'] = os.path.join(abs_save_path, '%(uploader)s', '%(title)s.%(ext)s')
        else:
            opts['outtmpl'] = os.path.join(abs_save_path, '%(title)s.%(ext)s')

        if self.format_type == "MP3":
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
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