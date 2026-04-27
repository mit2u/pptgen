# PPTGen API Guide

PPTGen exposes two primary REST endpoints via Django REST Framework:

## Authentication

The project uses DRF authentication and global `IsAuthenticated` permissions. You must authenticate before calling API endpoints.

- Login page: `/api-auth/login/?next=/`
- DRF browsable API auth URLs: `/api-auth/`

## Endpoints

### 1) Create slide deck request

- **URL:** `POST /topic-submit/`
- **Purpose:** Generate slides and persist a request record.

Request body fields:

- `topic` *(string, optional if `content` provided)*
- `content` *(string, optional if `topic` provided)*
- `provider` *(string, optional: `ollama` or `gemini`; defaults to `ollama` path in code)*
- `min_slides` *(integer, optional, minimum 1)*
- `max_slides` *(integer, optional, maximum 20)*
- `font` *(string, optional)*
- `color` *(string, optional, expected RGB hex without `#`, e.g. `FF0000`)*

Response includes:

- `ppt_link` (absolute URL to generated `.pptx`)
- `topic`, `content`, `font`, `color`, `min_slides`, `max_slides`, `provider`

### 2) Retrieve previously generated slide deck requests

- **URL:** `GET /slides/`
- **URL:** `GET /slides/{id}/`
- **Purpose:** List stored requests and inspect a specific generated request.

## Notes

- `topic` and `content` model fields are capped to 20 chars by current model definition.
- Generated `.pptx` files are written to the project working directory as `{id}.pptx`.
