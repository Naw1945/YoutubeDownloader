import yt_dlp
from typing import Dict, Any, Optional


def fetch_metadata(url: str) -> Optional[Dict[str, Any]]:
    """Lấy thông tin video hoặc playlist từ URL với cấu hình bypass chống block."""
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'in_playlist',
        'no_warnings': True,  # Ẩn các warning rác về JS

        # Thêm cấu hình bọc giáp giả lập tương tự downloader
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"[Error] fetch_metadata: {e}")
        return None