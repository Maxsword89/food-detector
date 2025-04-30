import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    # Common
    default_locale: str = os.getenv("DEFAULT_LOCALE", "ru")
    api_keys: list[str] = os.getenv("API_KEYS", "").split(",")
    api_prefix: str = os.getenv("API_PREFIX", "api")
    port: int = int(os.getenv("PORT", 8001))
    debug: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
    require_auth: bool = os.getenv("REQUIRE_AUTH", "false").lower() == "true"

    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_api_base: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1/chat/completions")
    openai_text_model: str = os.getenv("OPENAI_TEXT_MODEL", "gpt-4o")
    openai_image_model: str = os.getenv("OPENAI_IMAGE_MODEL", "gpt-4.1")
    openai_audio_model: str = os.getenv("OPENAI_AUDIO_MODEL", "whisper-1")

    # Image
    image_max_tokens: int = int(os.getenv("IMAGE_MAX_TOKENS", 512))
    image_detail: str = os.getenv("IMAGE_DETAIL", "high")
    image_temperature: float = float(os.getenv("IMAGE_TEMPERATURE", 0.4))

    # Text
    text_max_tokens: int = int(os.getenv("TEXT_MAX_TOKENS", 512))
    text_temperature: float = float(os.getenv("TEXT_TEMPERATURE", 0.7))
    text_frequency_penalty: float = float(os.getenv("TEXT_FREQUENCY_PENALTY", 0.0))
    text_presence_penalty: float = float(os.getenv("TEXT_PRESENCE_PENALTY", 0.0))

    # Audio
    audio_temperature: float = float(os.getenv("AUDIO_TEMPERATURE", 0.0))

settings = Settings()
