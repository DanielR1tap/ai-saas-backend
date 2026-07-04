# AI SaaS Backend

Backend-only Python starter for an AI SaaS product.

## What This Means

The project is focused only on server-side engineering:

- API endpoints for clients and future frontend apps.
- AI orchestration layer for LLM providers.
- SaaS primitives such as users, plans, usage limits, and billing hooks.
- Database-ready structure for production growth.
- No frontend code.

## Structure

```text
backend/
  app/
    api/routes/        FastAPI routes
    core/              settings, security, shared infrastructure
    models/            database models
    schemas/           request and response schemas
    services/          business logic and AI logic
    main.py            FastAPI application entrypoint
  tests/               backend tests
```

## Current Backend Flow

1. A user registers with organization name, email, and password.
2. The backend creates a tenant and owner user.
3. The user logs in and receives a JWT access token.
4. Protected endpoints read the current user from the token.
5. AI requests are charged against the user's tenant credits.
6. AI request history is stored per tenant for audit and product UI.

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn backend.app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

First local run creates SQLite tables automatically. Production projects should use Alembic
migrations instead of automatic table creation.

## Run With Docker

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Docker starts two services:

- `api` - FastAPI backend on `http://127.0.0.1:8000`.
- `db` - PostgreSQL database on port `5432`.

In Docker mode `AUTO_CREATE_TABLES=false`, so schema changes are applied through Alembic:

```powershell
docker compose exec api alembic upgrade head
```

## Database Migrations

Alembic migrations live in `backend/migrations`.

Useful commands:

```powershell
alembic upgrade head
alembic revision --autogenerate -m "add table name"
alembic downgrade -1
```

Why this matters:

- Models describe tables in Python.
- Migrations describe how to change the real database.
- Production teams use migrations because they make schema changes repeatable and reviewable.

## Main API Endpoints

- `POST /api/v1/auth/register` - create tenant and owner user.
- `POST /api/v1/auth/login` - receive JWT access token.
- `GET /api/v1/auth/me` - read current authenticated user.
- `POST /api/v1/ai/complete` - run AI completion and store request history.
- `GET /api/v1/ai/requests` - list tenant AI request history.

## Environment

Set `AI_PROVIDER=mock` for local development without external API calls.
Set `AI_PROVIDER=openai` and `OPENAI_API_KEY=...` to use OpenAI.
