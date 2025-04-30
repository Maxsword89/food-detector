class BaseRecognizer:
    async def recognize(self, data: bytes, locale: str):
        raise NotImplementedError
