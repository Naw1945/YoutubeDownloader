import yt_dlp
from typing import Dict, Any, Optional


def fetch_metadata(url: str) -> Optional[Dict[str, Any]]:
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'in_playlist',
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info and '_type' in info and info['_type'] == 'playlist':
                for entry in info.get('entries', []):
                    if entry:
                        thumb_url = ""
                        if entry.get('thumbnails'):
                            thumb_url = entry['thumbnails'][-1].get('url', '')
                        if not thumb_url:
                            thumb_url = entry.get('thumbnail', '')
                        if not thumb_url and entry.get('id'):
                            thumb_url = f"https://img.youtube.com/vi/{entry.get('id')}/hqdefault.jpg"
                        entry['thumbnail'] = thumb_url
            elif info and info.get('id'):
                thumb_url = ""
                if info.get('thumbnails'):
                    thumb_url = info['thumbnails'][-1].get('url', '')
                if not thumb_url:
                    thumb_url = info.get('thumbnail', '')
                if not thumb_url:
                    thumb_url = f"https://img.youtube.com/vi/{info.get('id')}/hqdefault.jpg"
                info['thumbnail'] = thumb_url
            return info
    except Exception as e:
        print(f"[Error] fetch_metadata: {e}")
        return None