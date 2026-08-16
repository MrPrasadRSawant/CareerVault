# CareerVault

CareerVault is a job opportunity and application management platform designed to help applicants organize their complete job-search journey in one place.

Users can save important job opportunities, maintain application details, store the exact resume used for each application, track recruitment progress, and manage follow-ups.

The platform is designed to support future AI-powered features such as email response monitoring, application status detection, resume-to-job matching, and follow-up recommendations.

## Features

### Opportunity Management

* Save important job opportunities
* Store company and role information
* Maintain job descriptions
* Save job application links
* Record required skills and experience
* Track opportunity status

### Application Tracking

* Mark opportunities as applied
* Record the application date
* Track application progress
* Maintain interview stages
* Add notes and follow-up details
* Track rejected, selected, and pending applications

### Resume Management

* Upload and maintain multiple resume versions
* Associate a specific resume with an application
* Check which resume was used for each company
* Maintain resume history
* Store cover letters and supporting documents

### Future AI Features

* Monitor emails for recruiter responses
* Detect interview invitations automatically
* Suggest application status updates
* Generate follow-up reminders
* Match resumes with job descriptions
* Calculate resume and job compatibility scores
* Identify missing skills
* Provide job-search insights and analytics

## Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic
* Pydantic
* JWT Authentication

### Frontend

* Quasar Framework
* Vue.js
* TypeScript
* Axios

### Database

* PostgreSQL

### Future Integrations

* Gmail API
* Microsoft Outlook API
* Large Language Models
* Browser extension for saving job opportunities
* Background job scheduler

## Project Goals

CareerVault aims to:

* Keep all job opportunities in one organized workspace
* Reduce dependency on spreadsheets and bookmarks
* Maintain the exact resume used for every application
* Help applicants track recruitment progress
* Prevent missed follow-ups
* Provide AI-powered assistance during the job-search process

## Planned Modules

* User Authentication
* User Profile
* Company Management
* Job Opportunity Management
* Application Tracking
* Resume Management
* Cover Letter Management
* Interview Tracking
* Follow-up Management
* Email Integration
* Notifications
* AI Resume Matching
* AI Email Response Monitoring
* Career Analytics

## Suggested Project Structure

```text
CareerVault/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── boot/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── router/
│   │   ├── services/
│   │   └── stores/
│   ├── quasar.config.ts
│   └── package.json
│
├── docs/
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

## Initial Database Entities

The initial version may contain the following entities:

* Users
* Companies
* Job Opportunities
* Applications
* Resumes
* Cover Letters
* Interviews
* Follow-ups
* Application Status History

## Application Workflow

```text
Save Opportunity
      ↓
Review Job Description
      ↓
Select Resume Version
      ↓
Apply for the Position
      ↓
Record Application Details
      ↓
Track Recruiter Responses
      ↓
Manage Interviews and Follow-ups
      ↓
Record Final Result
```

## Roadmap

### Phase 1: Core Application

* [ ] User authentication
* [ ] Opportunity management
* [ ] Company management
* [ ] Application tracking
* [ ] Resume upload and management
* [ ] Application status history

### Phase 2: Productivity Features

* [ ] Interview tracking
* [ ] Follow-up reminders
* [ ] Dashboard and analytics
* [ ] Search and filtering
* [ ] Document management
* [ ] Notifications

### Phase 3: AI Features

* [ ] Resume and job-description matching
* [ ] Missing-skill identification
* [ ] Email response classification
* [ ] Interview invitation detection
* [ ] Automatic application status suggestions
* [ ] AI-generated follow-up recommendations

### Phase 4: Integrations

* [ ] Gmail integration
* [ ] Microsoft Outlook integration
* [ ] Browser extension
* [ ] Job-page data extraction
* [ ] Calendar integration

## Getting Started

### Prerequisites

* Python 3.11 or later
* Node.js 20 or later
* PostgreSQL
* Quasar CLI

### Backend Setup

```bash
git clone https://github.com/<your-username>/CareerVault.git
cd CareerVault/backend

python -m venv .venv
```

Activate the virtual environment.

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux or macOS

```bash
source .venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.example .env
```

Run the database migrations:

```bash
alembic upgrade head
```

Create the private product-owner administrator account. This account is kept
separate from applicant registration and receives exactly one role,
`system_admin`. The command prompts for a password of at least 12 characters:

```bash
python -m app.scripts.create_system_admin \
  --email owner@example.com \
  --name "CareerVault Owner"
```

When running with Docker, execute the same command in the backend container:

```bash
docker compose exec backend python -m app.scripts.create_system_admin \
  --email owner@example.com \
  --name "CareerVault Owner"
```

Applicants and administrators both sign in at `/login`. The authenticated user's
role determines whether the app opens the applicant dashboard or the system admin
control center. Public registration always creates a `job_applicant`; existing
users are assigned that role by the database migration. Administrator and
applicant tokens cannot access each other's APIs. The administration API exposes
only account identity, role, registration timestamps, and access status; it does
not expose applicants' opportunities, applications, resumes, or career details.

### Registration capacity

Public applicant registration is capped at 1,000 accounts per UTC calendar
day by default. The System Admin can change the limit from **Platform
settings**. The value is stored in `system_settings`; atomic daily usage is
stored in `daily_registration_counters`. When the limit is reached, the API
returns HTTP `429` with a `Retry-After` header. Existing users can continue to
sign in normally.

### Authentication audit and session records

CareerVault records successful and failed authentication events for incident
review. System administrators can review the account reference (when known),
role, outcome, coarse failure reason, event time, validated client IP address,
and a sanitized user-agent string limited to 512 characters. Passwords, access
tokens, request/response bodies, and career records are never included.

Unknown email addresses are not stored. A keyed one-way identifier fingerprint
is retained only to correlate repeated attempts against the same unknown
identifier. Audit records are removed after `AUTH_AUDIT_RETENTION_DAYS` (90
days by default).

Each issued token is associated with a server-side session. Explicit sign-out
produces an exact session duration. If a browser closes or loses connectivity
without signing out, duration is labeled as an estimate based on the last
authenticated request. Session activity writes are throttled by
`AUTH_SESSION_ACTIVITY_UPDATE_SECONDS`.

Every login attempt is appended as a separate audit event; existing events are
never updated to represent a later attempt. Known accounts are temporarily
locked for 20 minutes after three consecutive invalid-password attempts by
default. A successful login resets the consecutive-failure count. System
Admins can change both the attempt threshold and lockout duration from
**Platform settings**. The values are stored as `failed_login_attempt_limit`
and `login_lockout_duration_minutes` in `system_settings`.

Password length is also database-configurable. The defaults accept 8–20
characters, and System Admins can adjust the minimum and maximum from
**Platform settings** while both remain inside the 8–20 boundary. The settings
are stored as `password_min_length` and `password_max_length`. The same policy
is enforced for registration, regular user login, and System Admin login.

The recorded IP uses the ASGI client address. In a reverse-proxy deployment,
configure the application server to trust forwarding headers only from your
controlled proxy; the application does not trust arbitrary
`X-Forwarded-For` values directly.

### Exception diagnostics

Unexpected server errors are appended to the `exception_logs` table and can be
reviewed by System Admins from **Exception logs**. Each entry contains a unique
request ID, timestamp, authenticated user reference when safely available,
HTTP method, route template, status, exception type, sanitized message and
stack trace, issue fingerprint, validated IP address, user agent, and runtime
environment. The fingerprint groups recurring errors without replacing their
individual occurrences.

Request bodies, authorization tokens, cookies, and query-string values are not
stored. Email addresses, token-shaped values, password/secret assignments, and
database parameter blocks found in exception text are redacted. Expected client
responses such as 401, 404, and 422 are not treated as application exceptions.
Logs are retained for `EXCEPTION_LOG_RETENTION_DAYS` (90 days by default). If
the database itself is unavailable, persistence cannot succeed and the handler
falls back to the server's standard error logger while still returning a safe
request ID to the client.

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000/api/v1
```

API documentation:

```text
http://localhost:8000/api/v1/docs
```

### Frontend Setup

```bash
cd frontend
npm install
quasar dev
```

The frontend will usually be available at:

```text
http://localhost:9000
```

## Environment Variables

Backend environment variables are loaded from `backend/.env`. Copy the example
file and adjust the values:

```bash
cp backend/.env.example backend/.env
```

The backend runs with sensible defaults (SQLite + a development secret) even
without a `.env`, but you should configure PostgreSQL and a strong `SECRET_KEY`
for real use.

```env
APP_NAME=CareerVault
APP_ENV=development
ENABLE_API_DOCS=true
SECRET_KEY=replace-with-a-secure-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60

DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/careervault
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_POOL_TIMEOUT_SECONDS=30
DATABASE_POOL_RECYCLE_SECONDS=1800

FRONTEND_URL=http://localhost:9000
```

For quick local development without PostgreSQL, use `DATABASE_URL=sqlite:///./careervault.db`.

The frontend API URL is configured in `frontend/.env`:

```env
VITE_API_URL=http://localhost:8004/api/v1
```

Set this to the full backend API URL used by the frontend, for example
`http://localhost:8004/api/v1`. `ENABLE_API_DOCS=true` keeps Swagger, ReDoc,
and the OpenAPI schema available in both development and production. Set it to
`false` only when documentation must be disabled.

## Docker

A `docker-compose.yml` starts PostgreSQL, the backend, and the frontend:

```bash
docker compose up --build
```

## Concurrent requests and background work

The API uses PostgreSQL connection pooling and runs two Uvicorn workers by
default in Docker and the supplied systemd service. Tune `WEB_CONCURRENCY` to
the available CPU and database connection budget. Each worker uses up to
`DATABASE_POOL_SIZE + DATABASE_MAX_OVERFLOW` connections.

Routes that perform ordinary database CRUD remain synchronous and FastAPI runs
them in its worker thread pool, so they can serve concurrent users. Upload
writes are moved off the ASGI event loop. For small, non-critical follow-up
work, use FastAPI `BackgroundTasks`; jobs that must survive a restart should
be moved to a durable queue when one is introduced.

## Server deployment

The included `nginx.conf` and `careervault.service` are configured for
`https://careervault.prasadsawant.com` with the project in
`/var/www/CareerVault/Dev`. The Nginx configuration expects a Let's Encrypt
certificate at `/etc/letsencrypt/live/careervault.prasadsawant.com/`.

### One-command deployment

On the server, run the deployment script from the repository root:

```bash
cd /var/www/CareerVault/Dev
sudo bash deploy.sh
```

It fast-forwards `main`, updates Python dependencies, runs Alembic migrations,
builds the frontend, installs the included systemd and Nginx configuration,
validates Nginx, restarts the API, and checks the local health endpoint. The
backend virtual environment and `backend/.env` must already exist.

Production frontend builds use `frontend/.env.production`, which sets:

```env
VITE_API_URL=https://careervault.prasadsawant.com/api/v1
```

## API Documentation

FastAPI automatically provides interactive API documentation.

* Swagger UI: `/api/v1/docs`
* ReDoc: `/api/v1/redoc`
* OpenAPI Schema: `/api/v1/openapi.json`

## Security Considerations

CareerVault may store sensitive career-related data. The application should therefore:

* Hash passwords securely
* Protect APIs using authentication and authorization
* Validate uploaded files
* Restrict file access by user
* Encrypt sensitive integration credentials
* Avoid storing email passwords
* Use OAuth for Gmail and Outlook integrations
* Maintain audit logs for important activities

## Contribution

Contributions, feature suggestions, and bug reports are welcome.

To contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Create a pull request

## License

This project is licensed under the MIT License.

## Project Status

CareerVault is currently under active development.

The initial focus is on opportunity management, application tracking, and resume version management. AI-powered automation and email integrations will be introduced in later phases.
