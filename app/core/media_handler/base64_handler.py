import base64

class Base64Handler:
    @staticmethod
    def decode_base64_data(base64_data: str) -> bytes:
        try:
            return base64.b64decode(base64_data)
        except Exception:
            return None
