from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes_recognize import router as recognize_router
from app.config.settings import settings
from app.core import errors

app = FastAPI(
    title="Food Recognizer Service",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    if settings.require_auth and request.url.path.startswith(settings.api_prefix + "/"):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return errors.unauthorized_response()
        token = auth.replace("Bearer ", "").strip()
        allowed_keys = [key.strip() for key in settings.api_keys]
        if token not in allowed_keys:
            return errors.unauthorized_response()
    return await call_next(request)

app.include_router(
    recognize_router,
    prefix=settings.api_prefix,
    tags=["Food Recognize API"]
)
