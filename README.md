# Food Detector

Multimodal Food Recognition API — A FastAPI service for recognizing food from images, speech, and text, with multilingual support and OpenAI GPT-4o/Whisper integration.

---

## Features

- Recognize meals from:
  - Images (upload, URL, base64)
  - Audio recordings (upload, URL, base64)
  - Text descriptions
- Returns structured nutritional information:
  - English and localized dish names
  - Grams, calories, proteins, fats, carbohydrates
- Multilingual support with automatic translation
- OpenAI GPT-4o and Whisper API integration
- Environment-based configuration
- Swagger/OpenAPI auto-generated documentation

---

## Setup

### 1. Clone and prepare

```bash
git clone https://github.com/mx-dec0de/food-detector.git
cd food-detector
cp .env.template .env
```

Edit `.env` with your OpenAI key and preferred settings.

### 2. Install dependencies (for local dev)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Docker Deployment

### Public (with reverse proxy and domain)

Use with a reverse proxy like Traefik or Nginx. Make sure to configure your DNS.

```bash
docker compose -f docker-compose.public.yml up -d
```

Ensure your proxy points to `recognizer_service:8001`.

### Private (internal container-only network)

Use this to expose the API only to other Docker containers:

```bash
docker compose -f docker-compose.private.yml up -d
```

You can access it internally as:

```
http://recognizer_service:8001/api/...
```

---

## API Endpoints

| Method | Path                | Description                   |
|--------|---------------------|-------------------------------|
| GET    | `/ping`             | Health check                  |
| POST   | `/image/upload`     | Image via file upload         |
| POST   | `/image/url`        | Image via remote URL          |
| POST   | `/image/base64`     | Image via base64 string       |
| POST   | `/audio/upload`     | Audio via file upload         |
| POST   | `/audio/url`        | Audio via remote URL          |
| POST   | `/audio/base64`     | Audio via base64 string       |
| POST   | `/text`             | Free-form text description    |

All endpoints accept a `locale` (e.g., `en`, `indonesian`, `ru`, `chinese`) and return a structured JSON response with nutrition estimates.

---

## Environment Configuration

See `.env.template` for all configurable options.

Key options include:

- API keys and port
- OpenAI model selection
- Temperature and token settings for text, image, and audio
- Optional authentication enforcement

---

## License

MIT License.

