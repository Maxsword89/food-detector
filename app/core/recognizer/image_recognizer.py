import base64
import requests
import os

from app.core.recognizer.base_recognizer import BaseRecognizer
from app.core.recognizer.text_recognizer import TextRecognizer
from app.models.response_models import RecognizeResponse
from app.config.settings import settings
from app.config import prompts
from app.core import errors


class ImageRecognizer(BaseRecognizer):
    async def recognize(self, image_data: bytes, locale: str) -> RecognizeResponse:
        try:

            image_b64 = base64.b64encode(image_data).decode("utf-8")

            url = settings.openai_api_base
            headers = {
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json"
            }

            prompt = prompts.IMAGE_RECOGNITION_PROMPT
            payload = {
                "model": settings.openai_image_model,
                "messages": [
                    {"role": "system", "content": prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_b64}",
                                    "detail": settings.image_detail
                                }
                            },
                            {
                                "type": "text",
                                "text": "Describe the food in the image."
                            }
                        ]
                    }
                ],
                "max_tokens": settings.image_max_tokens,
                "temperature": settings.image_temperature
            }

            if settings.debug:
                print("[ImageRecognizer] Payload constructed.")
                print(f"Model: {settings.openai_image_model}")
                print(f"Detail: {settings.image_detail}")
                print(f"Max tokens: {settings.image_max_tokens}")
                print(f"Locale: {locale}")
                print(f"Image base64 size: {len(image_b64)} chars")

            response = requests.post(url, headers=headers, json=payload)

            if settings.debug:
                print("[ImageRecognizer] OpenAI response status:", response.status_code)

            if response.status_code != 200:
                if settings.debug:
                    print("[ImageRecognizer] Response text:", response.text)
                raise errors.food_not_recognized()

            data = response.json()
            description = data["choices"][0]["message"]["content"].strip()

            if settings.debug:
                print("[ImageRecognizer] Vision description:")
                print(description)

            if not description:
                raise errors.food_not_recognized()

            return await TextRecognizer().recognize(description.encode("utf-8"), locale or settings.default_locale)

        except Exception as e:
            if settings.debug:
                print("[ImageRecognizer] Error:", str(e))
            raise errors.food_not_recognized()
