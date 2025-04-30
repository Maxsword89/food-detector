import io
import json
import openai

from app.core.recognizer.base_recognizer import BaseRecognizer
from app.models.response_models import RecognizeResponse
from app.config.settings import settings
from app.config import prompts
from app.core import errors

class AudioRecognizer(BaseRecognizer):
    async def recognize(self, audio_data: bytes, locale: str) -> RecognizeResponse:
        client = openai.OpenAI(api_key=settings.openai_api_key)
        schema = RecognizeResponse.model_json_schema()
        locale = locale or settings.default_locale
        prompt = prompts.AUDIO_RECOGNITION_PROMPT.format(locale=locale)

        buffer = io.BytesIO(audio_data)
        buffer.name = "audio.ogg"

        if settings.debug:
            print("[AudioRecognizer] Transcribing audio...")
        
        try:
            transcript = client.audio.transcriptions.create(
                model=settings.openai_audio_model,
                file=buffer,
                temperature=settings.audio_temperature
            )
        except Exception as e:
            if settings.debug:
                print("[AudioRecognizer] Transcription error:", str(e))
            raise errors.food_not_recognized()

        if settings.debug:
            print("[AudioRecognizer] Transcription result:", transcript.text)

        response = client.chat.completions.create(
            model=settings.openai_text_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": transcript.text}
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "food_estimator",
                        "description": "Extracts structured information about the meal, including name translation.",
                        "parameters": schema
                    }
                }
            ],
            tool_choice="required",
            temperature=settings.text_temperature,
            presence_penalty=settings.text_presence_penalty,
            frequency_penalty=settings.text_frequency_penalty,
            max_tokens=settings.text_max_tokens
        )

        tool_call = response.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)

        if settings.debug:
            print("[AudioRecognizer] Parsed output:", arguments)

        if not arguments.get("name_eng") or arguments.get("grams", 0) == 0:
            raise errors.food_not_recognized()

        return RecognizeResponse(**arguments)
