from fastapi import UploadFile

class FileHandler:
    @staticmethod
    async def read_file(file: UploadFile) -> bytes:
        return await file.read()

    @staticmethod
    async def validate_image(file: UploadFile) -> bool:
        content_type = file.content_type
        return content_type in ["image/jpeg", "image/png", "image/webp"]

    @staticmethod
    async def validate_audio(file: UploadFile) -> bool:
        content_type = file.content_type
        return content_type in ["audio/mpeg", "audio/wav", "audio/ogg"]
