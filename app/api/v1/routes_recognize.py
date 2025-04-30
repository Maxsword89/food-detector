from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.models.request_models import (
    ImageURLRequest,
    ImageBase64Request,
    AudioURLRequest,
    AudioBase64Request,
    TextRecognitionRequest
)
from app.models.response_models import RecognizeResponse
from app.core.media_handler.file_handler import FileHandler
from app.core.media_handler.url_handler import URLHandler
from app.core.media_handler.base64_handler import Base64Handler
from app.core.postprocessor.translator import Translator
from app.core.recognizer.image_recognizer import ImageRecognizer
from app.core.recognizer.audio_recognizer import AudioRecognizer
from app.core.recognizer.text_recognizer import TextRecognizer
from app.config.settings import settings

router = APIRouter()


async def recognize_and_translate(recognizer, data: bytes, locale: str = None) -> RecognizeResponse:
    locale = (locale or settings.default_locale).lower()
    try:
        if settings.debug:
            print("[Router] Calling recognizer with locale:", locale)

        result = await recognizer.recognize(data, locale)

        if settings.debug:
            print("[Router] Result from recognizer:", result.dict())

        result.name_loc = (
            await Translator.translate_text(result.name_eng, target_language=locale)
            if locale != "en" else result.name_eng
        )

        if settings.debug:
            print("[Router] Final translated result:", result.dict())

        return result
    except Exception as e:
        if settings.debug:
            print("[Router] ERROR during recognition and translation:", str(e))
        raise HTTPException(status_code=500, detail="Internal error during recognition")


@router.get("/ping", response_model=dict)
async def ping():
    return {"message": "pong"}


async def process_upload(file: UploadFile, recognizer_cls, validator, locale: str = None) -> RecognizeResponse:
    if settings.debug:
        print(f"[Router] Received file upload, locale: {locale}")
    if not await validator(file):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file format")
    data = await FileHandler.read_file(file)
    if settings.debug:
        print("[Router] Read file bytes:", len(data))
    recognizer = recognizer_cls()
    return await recognize_and_translate(recognizer, data, locale)


async def process_request(content: bytes, recognizer_cls, locale: str) -> RecognizeResponse:
    if settings.debug:
        print(f"[Router] Received data input, bytes: {len(content)}, locale: {locale}")
    recognizer = recognizer_cls()
    return await recognize_and_translate(recognizer, content, locale)


@router.post("/image/upload", response_model=RecognizeResponse)
async def recognize_image_upload(file: UploadFile = File(...), locale: str = None):
    return await process_upload(file, ImageRecognizer, FileHandler.validate_image, locale)


@router.post("/image/url", response_model=RecognizeResponse)
async def recognize_image_url(request: ImageURLRequest):
    if settings.debug:
        print("[Router] Image URL:", request.url)
        print("[Router] Locale:", request.locale)
    content = URLHandler.fetch_content(request.url)
    if not content or not URLHandler.validate_image_content(content):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image content")
    return await process_request(content, ImageRecognizer, request.locale)


@router.post("/image/base64", response_model=RecognizeResponse)
async def recognize_image_base64(request: ImageBase64Request):
    if settings.debug:
        print("[Router] Base64 image received, locale:", request.locale)
    content = Base64Handler.decode_base64_data(request.image_base64)
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid base64 data")
    return await process_request(content, ImageRecognizer, request.locale)


@router.post("/audio/upload", response_model=RecognizeResponse)
async def recognize_audio_upload(file: UploadFile = File(...), locale: str = None):
    return await process_upload(file, AudioRecognizer, FileHandler.validate_audio, locale)


@router.post("/audio/url", response_model=RecognizeResponse)
async def recognize_audio_url(request: AudioURLRequest):
    if settings.debug:
        print("[Router] Audio URL:", request.url)
        print("[Router] Locale:", request.locale)
    content = URLHandler.fetch_content(request.url)
    if not content or not URLHandler.validate_audio_content(content):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid audio content")
    return await process_request(content, AudioRecognizer, request.locale)


@router.post("/audio/base64", response_model=RecognizeResponse)
async def recognize_audio_base64(request: AudioBase64Request):
    if settings.debug:
        print("[Router] Base64 audio received, locale:", request.locale)
    content = Base64Handler.decode_base64_data(request.audio_base64)
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid base64 data")
    return await process_request(content, AudioRecognizer, request.locale)


@router.post("/text", response_model=RecognizeResponse)
async def recognize_text(request: TextRecognitionRequest):
    if settings.debug:
        print("[Router] Text input received.")
        print("Text:", request.text)
        print("Locale:", request.locale)
    recognizer = TextRecognizer()
    return await recognize_and_translate(recognizer, request.text.encode("utf-8"), locale=request.locale)
