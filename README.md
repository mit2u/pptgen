# PPTGen

PPTGen is a Django + DRF service that turns a topic or short content prompt into structured slide data and exports a `.pptx` file.

## Features

- REST endpoints for submitting generation requests and retrieving prior results.
- Pluggable text/image generation provider path (`gemini` or `ollama` code path).
- Automatic PowerPoint export via `python-pptx`.
- Docker and local Python workflows.

## Tech stack

- Python
- Django
- Django REST Framework
- python-pptx

## Quick start (local)

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:

   ```bash
   python manage.py migrate
   ```

3. Create an admin user (optional but recommended for login):

   ```bash
   python manage.py createsuperuser
   ```

4. Start the server:

   ```bash
   python manage.py runserver
   ```

5. Open:
   - Login: `http://localhost:8000/api-auth/login/?next=/`
   - Submit topic/content: `http://localhost:8000/topic-submit/`
   - View generated records: `http://localhost:8000/slides/`

## Quick start (Docker)

```bash
docker compose up --build
```

Then open `http://localhost:8000`.

## Configuration

- Add `GEMINI_API_KEY=...` to an `.env` file if using Gemini-backed flows.
- You can adjust model names in `core/settings.py` (`TEXT_GENERATION`, `IMAGE_GENERATION`).

## API docs

See [`docs/API.md`](docs/API.md) for request/response fields and endpoint details.

## Testing

Run test suite:

```bash
python manage.py test
```

## Project structure

```text
pptgen/
├── core/               # Django project/app modules
├── docs/               # Project documentation
├── samples/            # Sample pptx files
├── manage.py
├── requirements.txt
├── Dockerfile
└── compose.yaml
```
