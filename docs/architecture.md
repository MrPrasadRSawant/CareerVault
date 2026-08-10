# CareerVault Architecture

This document describes the project structure and how the pieces fit together.

## Overview

CareerVault is split into two main applications:

| Component  | Location      | Stack                                             |
| ---------- | ------------- | ------------------------------------------------- |
| Backend    | `backend/`    | Python, FastAPI, SQLAlchemy, Alembic, JWT          |
| Frontend   | `frontend/`   | Quasar (Vue 3), TypeScript, Vite, Pinia, Axios    |
| Database   | (external)    | PostgreSQL (SQLite works for quick local dev)     |

## Backend

### Layout

```text
backend/
├── app/
│   ├── api/          # HTTP routes (auth, companies, opportunities, ...)
│   ├── core/         # config (pydantic-settings), security (bcrypt/JWT), database
│   ├── models/       # SQLAlchemy ORM models + enums + declarative Base
│   ├── repositories/ # thin data-access layer on top of the ORM
│   ├── schemas/      # Pydantic request/response models
│   ├── services/     # business logic (auth, file uploads)
│   └── main.py       # FastAPI app factory
├── alembic/          # database migrations
├── tests/            # pytest suite (SQLite in-memory)
├── requirements.txt
└── .env.example      # copy to .env and edit
```

### Request flow

```
HTTP request
  -> app/api/... (route)        validates input with schemas, enforces auth
  -> app/services/...           business logic
  -> app/repositories/...       CRUD on ORM models
  -> PostgreSQL (or SQLite)
```

### Configuration

All configuration lives in `app/core/config.py` and is loaded from the
environment / `.env` file via `pydantic-settings`. The application has sane
defaults (SQLite + development) so it can run without any `.env` for a quick
start.

Key settings:

| Variable                  | Default                          | Purpose                        |
| ------------------------- | -------------------------------- | ------------------------------ |
| `DATABASE_URL`            | `sqlite:///./careervault.db`     | SQLAlchemy database URL        |
| `SECRET_KEY`              | insecure default (replace it!)   | JWT signing key                |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60`                          | JWT lifetime                   |
| `UPLOAD_DIR`              | `uploads`                        | Where resume files are stored  |
| `DATABASE_POOL_SIZE`       | `5`                              | Persistent PostgreSQL connections per worker |
| `DATABASE_MAX_OVERFLOW`    | `10`                             | Additional temporary PostgreSQL connections per worker |
| `FRONTEND_URL`            | `http://localhost:9000`          | CORS allowed origin            |

### Authentication

* Passwords are hashed with `bcrypt`.
* On login/register the API returns a JWT bearer token.
* Protected endpoints expect `Authorization: Bearer <token>`.
* Use the Swagger UI `Authorize` button or the `/auth/login` endpoint to get a
  token.

### Database migrations

```bash
cd backend
.venv\Scripts\activate
alembic upgrade head       # apply pending migrations
alembic revision --autogenerate -m "describe change"  # create a new migration
```

### Running tests

```bash
cd backend
.venv\Scripts\activate
pytest
```

Tests use an in-memory SQLite database, so no PostgreSQL server is required.

## Frontend

### Layout

```text
frontend/
├── src/
│   ├── boot/axios.ts       # Axios instance + auth interceptors (Quasar boot file)
│   ├── layouts/            # MainLayout (header + navigation drawer)
│   ├── pages/              # Login, Register, Dashboard, Applications, Resumes
│   ├── router/             # vue-router routes + auth guard
│   ├── services/           # typed API clients (types.ts, api.ts)
│   └── stores/             # Pinia stores (auth)
├── quasar.config.ts        # build config, dev proxy
└── package.json
```

### How the frontend talks to the backend

1. Axios is configured in `src/boot/axios.ts`.
2. Its `baseURL` defaults to `/api/v1` and it injects the stored JWT on every
   request.
3. In development, `quasar.config.ts` proxies `/api` (including `/api/v1`) to
   `http://localhost:8000` (no CORS involved). To point at another backend,
   set `API_PROXY_TARGET` or `VITE_API_URL`.
4. On a 401 response the interceptor clears the token and redirects to
   `/login`.

## Docker

From the repository root:

```bash
docker compose up --build
```

This starts PostgreSQL, the backend (after applying migrations), and the
frontend. The backend reads `backend/.env` (create it from
`backend/.env.example` first).

## Roadmap alignment

* **Phase 1 (implemented):** JWT auth, opportunity management, company
  management, application tracking with status history, resume upload.
* **Phase 2+:** interview tracking, follow-up reminders, analytics, AI
  features, email integration. The models already define `interviews`,
  `follow_ups`, and `application_status_history` to support these.
