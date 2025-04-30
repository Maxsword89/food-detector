import openai
import json
from app.core.recognizer.base_recognizer import BaseRecognizer
from app.models.response_models import RecognizeResponse
from app.config.settings import settings
from app.config import prompts
from app.core import errors

class TextRecognizer(BaseRecognizer):
    async def recognize(self, text_data: bytes, locale: str) -> RecognizeResponse:
        client = openai.OpenAI(api_key=settings.openai_api_key)
        schema = RecognizeResponse.model_json_schema()
        locale = locale or settings.default_locale
        prompt = prompts.TEXT_RECOGNITION_PROMPT.format(locale=locale)

        if settings.debug:
            print("[TextRecognizer] Locale:", locale)
            print("[TextRecognizer] Prompt:")
            print(prompt)

        response = client.chat.completions.create(
            model=settings.openai_text_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text_data.decode('utf-8')}
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
            top_p=1.0,
            presence_penalty=settings.text_presence_penalty,
            frequency_penalty=settings.text_frequency_penalty,
            max_tokens=settings.text_max_tokens
        )

        if not response.choices[0].message.tool_calls:
            raise errors.food_not_recognized()

        tool_call = response.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)

        if settings.debug:
            print("[TextRecognizer] Tool function arguments:")
            print(arguments)

        if not arguments.get("name_eng") or arguments.get("grams", 0) == 0:
            raise errors.food_not_recognized()

        return RecognizeResponse(**arguments)
