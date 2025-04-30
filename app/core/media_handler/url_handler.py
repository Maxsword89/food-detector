import requests

class URLHandler:
    @staticmethod
    def fetch_content(url: str) -> bytes:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.content
        except Exception:
            return None

    @staticmethod
    def validate_image_content(content: bytes) -> bool:
        return content[:8].startswith(b'\x89PNG') or content[:2] == b'\xff\xd8'

    @staticmethod
    def validate_audio_content(content: bytes) -> bool:
        return content[:4] in (b'fLaC', b'OggS') or content[:2] in (b'\xff\xf1', b'\xff\xf9')
