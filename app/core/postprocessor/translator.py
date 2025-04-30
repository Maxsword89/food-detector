import openai
from app.config.settings import settings
from app.config import prompts

class Translator:
    @staticmethod
    async def translate_text(text: str, target_language: str) -> str:
        if not text or not target_language:
            return text

        client = openai.OpenAI(api_key=settings.openai_api_key)

        prompt = prompts.TRANSLATION_PROMPT.format(target_language=target_language)

        response = client.chat.completions.create(
            model=settings.openai_text_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
        )

        return response.choices[0].message.content.strip()
