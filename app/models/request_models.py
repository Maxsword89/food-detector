from pydantic import BaseModel
from typing import Optional

class TextRecognitionRequest(BaseModel):
    text: str
    locale: Optional[str] = None

class ImageURLRequest(BaseModel):
    url: str
    locale: Optional[str] = None

class ImageBase64Request(BaseModel):
    image_base64: str
    locale: Optional[str] = None

class AudioURLRequest(BaseModel):
    url: str
    locale: Optional[str] = None

class AudioBase64Request(BaseModel):
    audio_base64: str
    locale: Optional[str] = None
