from typing import Literal

class MediaValidator:
    @staticmethod
    def validate_mime_type(content: bytes, media_type: Literal["image", "audio"]) -> bool:
        if media_type == "image":
            return content[:4] == b'\xff\xd8\xff\xe0' or content[:8] == b'\x89PNG\r\n\x1a\n'
        if media_type == "audio":
            return content.startswith(b'ID3') or content.startswith(b'RIFF') or content.startswith(b'OggS')
        return False
