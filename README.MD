# VerifyKE 🇰🇪

### A Community-Driven Platform for Reporting and Investigating Suspicious Activity

**VerifyKE** is a Kenya-focused fraud-reporting and verification platform designed to help people document suspicious encounters, investigate potentially risky entities, and contribute to a shared source of community intelligence.

The platform provides a structured way to submit reports involving suspicious phone numbers, websites, businesses, job offers, investment proposals, and other potentially fraudulent activity. Reports are stored in a PostgreSQL database, associated with their submitters, and made available for administrative review.

Built with **FastAPI, PostgreSQL, SQLAlchemy, JWT authentication, and RabbitMQ**, VerifyKE also explores event-driven architecture by publishing report-creation events to background workers.

> **Important principle:** A report is an allegation, not proof of wrongdoing. VerifyKE is designed around evidence, review, and responsible handling of user-submitted information. A single unverified report must not automatically label a person, business, or organization as fraudulent.

---

## Table of Contents

- [Project Overview](#project-overview)
- [The Problem](#the-problem)
- [Project Objectives](#project-objectives)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [How VerifyKE Works](#how-verifyke-works)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Database Migrations](#database-migrations)
- [Running the Application](#running-the-application)
- [Authentication and Authorization](#authentication-and-authorization)
- [API Reference](#api-reference)
- [RabbitMQ and Event-Driven Processing](#rabbitmq-and-event-driven-processing)
- [Testing the Application](#testing-the-application)
- [Security Considerations](#security-considerations)
- [Current Limitations](#current-limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

VerifyKE aims to make it easier to report and investigate suspicious activity by creating a centralized platform for structured community reports.

Rather than treating every submission as a confirmed incident, the system distinguishes between a report being submitted and a report being reviewed.

The current backend supports user registration, authentication, entity creation and lookup, report submission, administrative review, and a basic RabbitMQ messaging workflow.

### Project status

**Current stage: Backend foundation and initial event-driven integration**

| Component | Status |
|---|---|
| FastAPI application | Implemented |
| PostgreSQL database | Implemented |
| SQLAlchemy asynchronous database access | Implemented |
| Alembic migrations | Configured |
| User registration | Implemented |
| Argon2 password hashing | Implemented |
| JWT login and authentication | Implemented |
| Role-based admin authorization | Implemented |
| Entity creation and lookup | Implemented |
| Authenticated report submission | Implemented |
| Pending, verified, and rejected report states | Implemented |
| RabbitMQ connection and message publishing | Implemented |
| Report-created event consumer | Initial implementation |
| Automated risk scoring | Planned |
| Duplicate-report detection | Planned |
| Frontend application | Planned |
| Automated test suite | Planned |

*Status reflects the current development stage. Features should be considered complete only after their implementation and relevant tests have been verified.*

---

## The Problem

Fraudulent job offers, impersonation, suspicious investment proposals, and other deceptive schemes can cause financial and emotional harm.

People may encounter suspicious phone numbers, websites, or business identities without having a straightforward way to document what happened or investigate whether similar incidents have been reported.

Information can also be scattered across messaging groups, social media posts, and informal community discussions, making it difficult to find relevant reports or distinguish verified findings from unconfirmed claims.

VerifyKE explores how a structured reporting platform could help address these challenges.

### The proposed solution

The platform is designed around four principles:

1. **Structured reporting** — capture relevant information in a consistent format.
2. **Entity-based investigation** — associate reports with identifiable entities such as phone numbers or websites.
3. **Human review** — allow authorized administrators to review reports before changing their status.
4. **Scalable processing** — use asynchronous messaging to support background analysis as the system grows.

The long-term goal is to provide useful community intelligence without compromising privacy, fairness, or responsible reporting.

---

## Project Objectives

VerifyKE serves both as a practical fraud-reporting application and as a software engineering learning project.

Its objectives include:

- Build a REST API with FastAPI.
- Implement secure user registration and authentication.
- Apply role-based access control to administrative operations.
- Design relational database models and manage schema changes with Alembic.
- Associate reports with users and reported entities.
- Implement a report moderation lifecycle.
- Introduce RabbitMQ for asynchronous event processing.
- Establish a foundation for risk scoring and duplicate detection.
- Apply modular architecture, validation, error handling, and secure configuration practices.
- Build toward a usable frontend and deployment-ready application.

---

## Key Features

### 1. User registration

Users can create accounts using their name, email address, and password.

Passwords are hashed using Argon2 before being stored. The API returns public user information rather than exposing password hashes.

### 2. JWT authentication

Registered users can log in and receive a JSON Web Token (JWT) access token.

Protected endpoints use the token to identify the authenticated user.

### 3. Role-based authorization

VerifyKE distinguishes between ordinary users and administrators.

- **Users** can submit reports through authenticated endpoints.
- **Administrators** can access report-review endpoints.
- Unauthorized users receive an appropriate HTTP error when attempting restricted operations.

Administrative authorization checks the current user's role in the database.

### 4. Entity management

An entity represents an item associated with a report, such as:

- A phone number
- A website
- A business
- A social media account or other identifier

The current API supports entity creation, lookup by ID, and search by entity value.

Existing entities can be reused to avoid creating duplicate records through the ordinary creation flow.

### 5. Structured report submission

Authenticated users can submit reports containing:

- Title
- Description
- Category
- Associated entity

Each report is associated with the authenticated user's database ID and the selected entity's ID.

New reports begin with the `pending` status.

### 6. Administrative report moderation

Authorized administrators can retrieve pending reports and change a report's status to either:

- `verified`
- `rejected`

Only pending reports can be transitioned through the current verification and rejection endpoints.

These statuses describe the platform's review decision; they should not be interpreted as an automatic legal finding or a guarantee that every underlying allegation has been conclusively established.

### 7. RabbitMQ event messaging

When a report is created, the application publishes a `report.created` event to RabbitMQ after committing the report to PostgreSQL.

A separate worker consumes the event from the `report_created` queue.

The initial worker demonstrates message consumption and processing. Automated risk scoring and duplicate detection are planned extensions.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| Pydantic | Request validation and response schemas |
| Pydantic Settings | Application configuration |
| PostgreSQL | Relational database |
| SQLAlchemy | Asynchronous ORM and database access |
| asyncpg | Asynchronous PostgreSQL driver |
| Alembic | Database schema migrations |
| python-jose | JWT encoding and decoding |
| pwdlib | Password hashing utilities |
| Argon2 | Password hashing algorithm |
| RabbitMQ | Message broker |
| aio-pika | Asynchronous AMQP client |
| Uvicorn | ASGI application server |
| Docker | RabbitMQ containerization |
| Pytest | Planned automated testing |

### Why these technologies?

**FastAPI** provides a modern Python API framework with request validation, dependency injection, asynchronous endpoint support, and interactive OpenAPI documentation.

**PostgreSQL** provides relational storage for users, entities, reports, and their relationships.

**SQLAlchemy** manages database access through Python models and asynchronous sessions.

**Alembic** tracks database schema changes through versioned migrations.

**JWT** enables clients to authenticate requests without sending passwords on every request.

**Argon2** is designed for password hashing and is preferable to storing plain-text passwords.

**RabbitMQ** decouples report submission from background processing, allowing additional consumers to be introduced without putting all processing inside the HTTP request.

---

## System Architecture

VerifyKE uses a modular backend architecture that separates HTTP endpoints, business logic, database operations, security utilities, and message processing.

### High-level architecture

```mermaid
flowchart TD
    Client[API Client / Swagger UI]
    API[FastAPI Application]
    Auth[Authentication and Authorization]
    Routes[API Routers]
    Services[Application Services]
    DB[(PostgreSQL)]
    Broker[RabbitMQ]
    Worker[Risk Worker]
    Future[Future Risk and Duplicate Analysis]

    Client --> API
    API --> Auth
    Auth --> Routes
    Routes --> Services
    Services --> DB
    Services --> Broker
    Broker --> Worker
    Worker -. Future integration .-> Future
```

### Main architectural components

**API layer**

Receives HTTP requests, validates incoming data, applies authentication and authorization dependencies, and returns structured responses.

**Service layer**

Contains business logic that should remain separate from the HTTP interface.

**Database layer**

Uses SQLAlchemy models, asynchronous sessions, and PostgreSQL to persist application data.

**Security layer**

Provides password hashing, password verification, JWT decoding, current-user resolution, and administrator authorization.

**Messaging layer**

Publishes domain events to RabbitMQ using a consistent event structure.

**Worker layer**

Consumes queued events independently of the API process. The current risk worker logs received events; substantive risk analysis remains future work.

---

## How VerifyKE Works

### Report submission flow

```mermaid
sequenceDiagram
    actor User
    participant API as FastAPI
    participant DB as PostgreSQL
    participant MQ as RabbitMQ
    participant Worker as Risk Worker

    User->>API: Submit authenticated report
    API->>API: Validate request and JWT
    API->>DB: Confirm entity exists
    API->>DB: Insert report
    DB-->>API: Commit successful
    API->>MQ: Publish report.created
    MQ-->>Worker: Deliver queued event
    Worker->>Worker: Process event
    API-->>User: Return created report
```

The diagram describes the intended successful flow. In the current implementation, report persistence happens before message publishing. This means a broker failure after the database commit can leave a saved report without a corresponding event; the transactional outbox pattern is a planned reliability improvement.

### Report lifecycle

```mermaid
flowchart TD
    A[User submits report] --> B[Pending]
    B --> C{Administrator review}
    C -->|Accept report| D[Verified]
    C -->|Reject report| E[Rejected]
```

The report status records the moderation outcome. It does not automatically determine whether an entity is fraudulent.

---

## Project Structure

The repository is organized to keep the backend modular and allow additional functionality to be introduced without concentrating all logic in a single file.

```text
verifyKE/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── entity.py
│   │   │   └── report.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── entities.py
│   │   │       ├── reports.py
│   │   │       └── admin.py
│   │   ├── services/
│   │   │   └── report_service.py
│   │   └── messaging/
│   │       ├── __init__.py
│   │       ├── rabbitmq.py
│   │       └── events.py
│   ├── workers/
│   │   ├── __init__.py
│   │   └── risk_worker.py
│   ├── tests/
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
├── frontend/
│   └── (planned frontend application)
├── .gitignore
├── README.md
└── LICENSE
```

*This tree describes the current project layout and its intended locations. The contents of optional folders may expand as development continues.*

### Important files

| File | Responsibility |
|---|---|
| `app/main.py` | Creates the FastAPI application and registers routers |
| `app/core/config.py` | Loads application settings |
| `app/core/security.py` | Password security, JWT validation, and admin authorization |
| `app/db/database.py` | Database engine, sessions, and dependency |
| `app/db/models.py` | SQLAlchemy database models |
| `app/schemas/user.py` | User request and response schemas |
| `app/schemas/entity.py` | Entity request and response schemas |
| `app/schemas/report.py` | Report request and response schemas |
| `app/api/routes/auth.py` | Registration and login endpoints |
| `app/api/routes/entities.py` | Entity creation, retrieval, and search |
| `app/api/routes/reports.py` | Authenticated report submission |
| `app/api/routes/admin.py` | Administrator review endpoints |
| `app/services/report_service.py` | Report creation and event publishing |
| `app/messaging/rabbitmq.py` | RabbitMQ connection and event publishing |
| `app/messaging/events.py` | Report-created event definition |
| `workers/risk_worker.py` | Consumes report-created events |
| `alembic/` | Versioned database migrations |

---

## Getting Started

These instructions describe the current backend development setup on Linux or WSL. Docker Desktop with WSL integration is suitable for running RabbitMQ.

### Prerequisites

Install or configure the following:

- Python 3.11 or a compatible version supported by the project's dependencies
- PostgreSQL
- Docker Engine or Docker Desktop with WSL integration
- Git
- A terminal capable of running a Python virtual environment

Check the installed tools:

```bash
python3 --version
pip --version
psql --version
docker --version
git --version
```

### 1. Clone the repository

If you are cloning from your own GitHub repository:

```bash
git clone https://github.com/<your-username>/verifyKE.git
cd verifyKE
```

Replace the repository URL with the actual remote URL if it differs.

If you already have the project locally, navigate to its root directory instead.

### 2. Create a Python virtual environment

Navigate to the backend directory:

```bash
cd backend
```

Create the environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

### 3. Install dependencies

Install the project's dependencies:

```bash
pip install -r requirements.txt
```

The requirements file should include the dependencies used by the current implementation, including:

- `fastapi`
- `uvicorn[standard]`
- `sqlalchemy`
- `asyncpg`
- `alembic`
- `pydantic`
- `pydantic-settings`
- `python-dotenv`
- `python-jose[cryptography]`
- `pwdlib[argon2]`
- `python-multipart`
- `aio-pika`
- `email-validator`

Include `pytest` and `pytest-asyncio` when setting up the test suite.

If the requirements file is incomplete, install missing dependencies and update the file so the environment can be reproduced.

---

## Environment Configuration

Create a `.env` file inside `backend/`.

Example:

```env
DATABASE_URL=postgresql+asyncpg://verifyke_user:YOUR_DATABASE_PASSWORD@localhost:5432/verifyke_db

SECRET_KEY=REPLACE_WITH_A_LONG_RANDOM_SECRET

ENVIRONMENT=development
```

Generate a strong secret key with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copy the generated value into `SECRET_KEY`.

### Configuration reference

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string used by SQLAlchemy |
| `SECRET_KEY` | Secret used to sign and verify JWTs |
| `ENVIRONMENT` | Application environment, such as `development` or `production` |

The current RabbitMQ module uses a local development URL:

```text
amqp://guest:guest@localhost/
```

This is suitable only for the current local development setup. In a later configuration refinement, RabbitMQ credentials should be loaded from environment variables rather than hard-coded.

### Protect environment variables

Never commit `.env` or real credentials to Git.

Add the following entries to `.gitignore` if they are not already present:

```gitignore
# Environment variables and secrets
.env
.env.*
!.env.example

# Python virtual environments
venv/
.venv/

# Python generated files
__pycache__/
*.py[cod]

# Test and coverage artifacts
.pytest_cache/
.coverage
htmlcov/

# Local development artifacts
*.log
```

Keep `.env.example` in the repository with placeholder values so other developers know which variables are required.

---

## Database Setup

VerifyKE uses PostgreSQL for persistent application data.

### 1. Start PostgreSQL

On Ubuntu or WSL installations that use the service manager:

```bash
sudo service postgresql start
```

Check its status:

```bash
sudo service postgresql status
```

### 2. Create the database user and database

Open the PostgreSQL shell:

```bash
sudo -u postgres psql
```

Create the application user and database:

```sql
CREATE USER verifyke_user WITH PASSWORD 'YOUR_DATABASE_PASSWORD';

CREATE DATABASE verifyke_db OWNER verifyke_user;
```

Replace the example password with a strong password and use the same value in `DATABASE_URL`.

Exit:

```sql
\q
```

If the role or database already exists, inspect the existing setup instead of creating duplicates.

### 3. Verify the connection

Run:

```bash
psql -h localhost -U verifyke_user -d verifyke_db
```

List the tables:

```sql
\dt
```

After the migrations have been applied, the database should contain the tables defined by the current models, including:

- `users`
- `entities`
- `reports`
- `alembic_version`

Exit the PostgreSQL shell:

```sql
\q
```

---

## Database Migrations

VerifyKE uses Alembic to manage database schema changes.

Migrations provide a version-controlled way to create or modify tables as the application evolves.

### Apply existing migrations

From the backend directory:

```bash
alembic upgrade head
```

### Generate a migration

After changing a SQLAlchemy model:

```bash
alembic revision --autogenerate -m "describe your schema change"
```

Review the generated migration before applying it. Autogenerated migrations are a starting point and should not be applied blindly.

Apply the migration:

```bash
alembic upgrade head
```

### Inspect migration status

```bash
alembic current
alembic history
```

**Important:** Avoid using `Base.metadata.create_all()` as a replacement for the migration workflow in an application managed by Alembic. Keep schema changes reproducible through migrations.

---

## Running the Application

### 1. Start the API

From `backend/`, activate the virtual environment if necessary:

```bash
source venv/bin/activate
```

Start Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

### 2. Open the API documentation

FastAPI automatically exposes interactive API documentation:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **OpenAPI schema:** http://127.0.0.1:8000/openapi.json

### 3. Check application health

Open:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

This endpoint checks whether the API is responding. It is not a comprehensive health check of PostgreSQL, RabbitMQ, or background workers.

---

## Starting RabbitMQ

RabbitMQ provides the message broker used for asynchronous report events.

### 1. Start the container

If the container has already been created:

```bash
docker start verifyke-rabbitmq
```

If it has not been created, run:

```bash
docker run -d \
  --name verifyke-rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:4-management
```

If you already use a Docker Compose service for RabbitMQ, start it through Compose instead of creating a second container.

### 2. Verify the container

```bash
docker ps
```

The container should expose:

| Port | Purpose |
|---|---|
| `5672` | AMQP messaging protocol |
| `15672` | RabbitMQ management interface |

### 3. Open the management interface

Visit:

http://localhost:15672

For a fresh local container using RabbitMQ's default development configuration:

```text
Username: guest
Password: guest
```

Use these credentials only for local development. Configure a dedicated RabbitMQ user and password before deploying outside a trusted development environment.

### 4. Run the worker

Open a second terminal and navigate to the backend directory:

```bash
cd ~/portfolio/verifyKE/backend
source venv/bin/activate
```

Start the worker:

```bash
python -m workers.risk_worker
```

Expected output:

```text
Connecting to RabbitMQ...
Connected to RabbitMQ.
Waiting for messages on 'report_created'...
```

Keep this terminal running while testing report submission.

The worker runs independently of the FastAPI server. Stop it with `Ctrl+C` when you want to shut it down.

---

## Authentication and Authorization

VerifyKE separates authentication from authorization.

### Authentication

Authentication determines the identity of the user making a request.

The current process is:

1. Register an account.
2. Hash the password using Argon2.
3. Store the user in PostgreSQL.
4. Submit login credentials.
5. Verify the submitted password against the stored hash.
6. Issue a signed JWT access token.
7. Validate the token on protected requests.
8. Resolve the user from the database.

### Authorization

Authorization determines whether the authenticated user can perform a specific action.

The current application has two roles:

| Role | Intended access |
|---|---|
| `user` | Submit reports through authenticated endpoints |
| `admin` | Access report review and moderation endpoints |

The current admin dependency checks the user's role in PostgreSQL, rather than relying solely on a role claim inside an existing JWT.

### Promoting a development account

There is no public self-service admin promotion endpoint.

For local development, an administrator can be assigned directly through PostgreSQL:

```sql
UPDATE users
SET role = 'admin'
WHERE email = 'your-development-email@example.com';
```

Verify the change:

```sql
SELECT id, name, email, role
FROM users;
```

This is a development procedure, not a production account-management workflow. In production, administrator provisioning should be restricted, audited, and controlled.

---

## API Reference

The endpoints below describe the current API routes.

Use Swagger UI at `/docs` to inspect the exact request schemas and responses generated by the running application.

### Health

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Confirm that the API is running |
| `GET` | `/health` | Return a basic health response |

### Authentication

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| `POST` | `/auth/register` | Public | Register a user |
| `POST` | `/auth/login` | Public | Authenticate and issue a JWT |

The login endpoint uses OAuth2 password-form fields. The `username` field contains the user's email address.

### Entities

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| `POST` | `/entities/` | Public in the current implementation | Create or reuse an entity |
| `GET` | `/entities/{entity_id}` | Public | Retrieve an entity by ID |
| `GET` | `/entities/search/{value}` | Public | Search entity values |

Entity creation currently checks for an existing entity with the same type and value before creating a new row. Database-level uniqueness constraints and concurrent-request handling are planned improvements.

### Reports

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| `POST` | `/reports/` | Authenticated | Submit a report |

The report's `user_id` is derived from the authenticated user, not supplied by the client.

### Administration

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| `GET` | `/admin/reports/pending` | Admin | List reports awaiting review |
| `PATCH` | `/admin/reports/{report_id}/verify` | Admin | Verify a pending report |
| `PATCH` | `/admin/reports/{report_id}/reject` | Admin | Reject a pending report |

### Typical HTTP status codes

| Status | Meaning |
|---|---|
| `200 OK` | Request completed successfully |
| `201 Created` | A resource was created |
| `400 Bad Request` | The operation is invalid for the current state |
| `401 Unauthorized` | Authentication is missing or invalid |
| `403 Forbidden` | The user lacks the required permission |
| `404 Not Found` | The requested resource does not exist |
| `422 Unprocessable Entity` | Request validation failed |
| `500 Internal Server Error` | An unexpected server error occurred |

The actual status code depends on the endpoint and error condition.

---

## API Usage Examples

These examples use the local development server at `http://127.0.0.1:8000`.

### 1. Register a user

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "ReplaceWithAStrongPassword123!"
  }'
```

A successful response contains the user's public profile fields. It should not expose the password or its hash.

### 2. Log in

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test%40example.com&password=ReplaceWithAStrongPassword123!"
```

A successful login returns a bearer access token:

```json
{
  "access_token": "<JWT_ACCESS_TOKEN>",
  "token_type": "bearer"
}
```

Store the token in a local shell variable for subsequent examples:

```bash
TOKEN="PASTE_YOUR_ACCESS_TOKEN_HERE"
```

Do not commit real tokens or share them publicly.

### 3. Create an entity

```bash
curl -X POST http://127.0.0.1:8000/entities/ \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "phone",
    "value": "0712345678"
  }'
```

The response includes the entity ID. Use that ID when creating a report.

### 4. Submit a report

Replace `1` with the ID returned by entity creation.

```bash
curl -X POST http://127.0.0.1:8000/reports/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Suspicious job offer",
    "description": "I was asked to send money before receiving an interview.",
    "category": "job_scam",
    "entity_id": 1
  }'
```

A successful response includes the report ID, associated user ID, entity ID, creation timestamp, and initial `pending` status.

### 5. Review pending reports

Log in with an administrator account and set its token in `TOKEN`.

Then run:

```bash
curl http://127.0.0.1:8000/admin/reports/pending \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Verify a report

```bash
curl -X PATCH \
  http://127.0.0.1:8000/admin/reports/1/verify \
  -H "Authorization: Bearer $TOKEN"
```

### 7. Reject a report

Use a different pending report if the first one has already been verified:

```bash
curl -X PATCH \
  http://127.0.0.1:8000/admin/reports/2/reject \
  -H "Authorization: Bearer $TOKEN"
```

---

## RabbitMQ and Event-Driven Processing

RabbitMQ is used to decouple report submission from subsequent background processing.

### The producer

The report service acts as a producer when it publishes a `report.created` event.

The event contains identifiers rather than a full copy of the report:

```json
{
  "event_type": "report.created",
  "report_id": 1,
  "user_id": 1,
  "entity_id": 1
}
```

These identifiers allow consumers to retrieve the authoritative report and entity information from the database when needed.

### The queue

The initial queue is named:

```text
report_created
```

The queue is declared as durable, and published messages use persistent delivery mode.

These settings improve message durability, but they do not by themselves guarantee end-to-end delivery or processing. Publisher confirms, robust error handling, and database-to-broker reliability measures still need to be implemented.

### The consumer

The current worker is located at:

```text
backend/workers/risk_worker.py
```

It listens for messages, decodes JSON, and logs the received event fields.

Run it with:

```bash
python -m workers.risk_worker
```

When a new report is submitted successfully and the event is published, the worker should display the event type and the corresponding report, user, and entity IDs.

### Current event-processing flow

```mermaid
flowchart TD
    A[POST /reports/] --> B[Validate authenticated user]
    B --> C[Confirm entity exists]
    C --> D[Save report in PostgreSQL]
    D --> E[Publish report.created event]
    E --> F[RabbitMQ report_created queue]
    F --> G[Risk worker consumes message]
    G --> H[Log received event]
```

### Planned processing pipeline

The next iteration can expand the worker architecture to support:

- **Risk analysis:** identify risk indicators in a report.
- **Duplicate detection:** identify potentially related reports.
- **Entity intelligence:** aggregate relevant reports for an entity.
- **Notifications:** notify users or administrators about important workflow events.
- **Administrative review assistance:** present evidence and risk indicators to help reviewers make informed decisions.

Automated analysis should support human review rather than automatically treating an allegation as a confirmed fact.

### Reliability considerations

The current implementation publishes after the database transaction commits. This ordering prevents an event from being published before the report is successfully saved, but a broker outage can still leave a committed report without a published event.

Future reliability improvements should include:

- A transactional outbox or equivalent database-to-broker publishing strategy.
- Publisher confirms and explicit publishing-failure handling.
- Idempotent event processing to handle duplicate delivery.
- Retry and dead-letter policies for failed messages.
- Structured logging and monitoring.
- Event versioning and schema validation.
- Graceful worker shutdown and reconnect behavior.

These improvements are important before treating the messaging workflow as production-ready.

---

## Testing the Application

Testing should cover both ordinary application behavior and security boundaries.

### Manual smoke tests

Use Swagger UI to verify the following:

- [ ] The API starts successfully.
- [ ] The health endpoint returns a successful response.
- [ ] A new user can register.
- [ ] Duplicate email registration is rejected.
- [ ] Password hashes are stored instead of plain-text passwords.
- [ ] A user can log in with valid credentials.
- [ ] Invalid credentials are rejected.
- [ ] Entity creation and lookup work.
- [ ] An authenticated user can submit a report.
- [ ] An unauthenticated request to `POST /reports/` is rejected.
- [ ] A normal user cannot access administrator endpoints.
- [ ] An administrator can retrieve pending reports.
- [ ] A pending report can be verified or rejected.
- [ ] A report that is no longer pending cannot be reviewed again through the same transition endpoint.
- [ ] RabbitMQ receives the report-created event.
- [ ] The risk worker consumes and logs the event.

### Automated testing

Pytest is the intended framework for automated tests.

Run the test suite from the backend directory:

```bash
pytest -v
```

The automated test suite is still to be developed. Future tests should cover authentication, report creation, authorization, invalid status transitions, database behavior, and RabbitMQ integration.

Tests should use isolated test data and a dedicated test database rather than modifying real application records.

---

## Security Considerations

VerifyKE handles user accounts, submitted allegations, and potentially sensitive identifiers. Security and responsible information handling are core design requirements.

### Password protection

- Never store plain-text passwords.
- Use a dedicated password-hashing algorithm such as Argon2.
- Do not return password hashes in API responses.
- Keep authentication error messages from revealing unnecessary account details.

### Token security

- Use a strong secret key.
- Keep token lifetimes limited.
- Never commit tokens or secrets to version control.
- Use HTTPS in deployed environments.
- Consider token revocation and refresh-token policies as the authentication system evolves.

### Access control

- Protect report submission with authentication.
- Restrict moderation endpoints to administrators.
- Avoid public endpoints that allow users to change their own roles.
- Review entity-creation permissions before production deployment.
- Test authorization failures as carefully as successful requests.

### Responsible reporting

- Clearly distinguish unverified reports from reviewed findings.
- Avoid automatically declaring people or businesses fraudulent based on a single submission.
- Provide a process for correcting inaccurate information and disputing reports.
- Minimize the collection and public exposure of personal information.
- Consider moderation, abuse reporting, evidence retention, and audit logs before public launch.

### Operational security

- Keep `.env` out of Git.
- Use dedicated credentials for PostgreSQL and RabbitMQ.
- Avoid default RabbitMQ credentials outside isolated development.
- Add request rate limits and abuse prevention before public deployment.
- Log useful operational events without unnecessarily exposing passwords, tokens, or sensitive report details.

---

## Current Limitations

VerifyKE is under active development. The current implementation demonstrates the core backend flow, but it is not yet a complete public fraud-reporting service.

Known areas for improvement include:

1. **Background analysis:** the initial risk worker receives and logs events but does not yet calculate risk scores.
2. **Duplicate detection:** related-report identification has not yet been implemented.
3. **Message reliability:** database commits and RabbitMQ publishing are separate operations.
4. **Entity uniqueness:** application-level duplicate checks should be reinforced with database constraints and concurrency-safe handling.
5. **Auditability:** administrative status changes need a dedicated audit trail.
6. **Moderation workflow:** evidence handling, review notes, dispute processes, and review history remain future work.
7. **Testing:** a comprehensive automated test suite has not yet been established.
8. **Frontend:** a user-facing reporting and investigation interface is planned.
9. **Production deployment:** monitoring, rate limiting, production secrets, HTTPS, backups, and operational controls need to be completed.
10. **Privacy and governance:** public display rules, retention policies, and procedures for inaccurate or disputed reports require careful design.

These limitations define the next engineering milestones rather than invalidating the functionality already implemented.

---

## Roadmap

The roadmap prioritizes correctness, security, and meaningful background processing before expanding the product.

### Phase 1 — Backend foundation

- [x] Establish the FastAPI application.
- [x] Configure PostgreSQL and SQLAlchemy.
- [x] Define user, entity, and report models.
- [x] Configure Alembic migrations.
- [x] Implement registration and login.
- [x] Introduce Argon2 password hashing.
- [x] Implement JWT authentication.
- [x] Protect report submission.
- [x] Implement entity endpoints.
- [x] Implement administrator authorization.
- [x] Add report verification and rejection endpoints.

### Phase 2 — Event-driven foundation

- [x] Run RabbitMQ locally.
- [x] Create RabbitMQ publishing utilities.
- [x] Define the `report.created` event.
- [x] Publish events after report creation.
- [x] Build an initial risk worker.
- [x] Demonstrate event consumption.

### Phase 3 — Reliability and data integrity

- [ ] Move RabbitMQ settings into environment-based configuration.
- [ ] Add database-level entity uniqueness constraints.
- [ ] Add an event-publishing reliability strategy, such as a transactional outbox.
- [ ] Implement retry and dead-letter handling.
- [ ] Make event processing idempotent.
- [ ] Add administrative audit logs.
- [ ] Expand automated unit and integration tests.

### Phase 4 — Risk and duplicate analysis

- [ ] Design a transparent, explainable risk-scoring service.
- [ ] Identify relevant report indicators and supporting evidence.
- [ ] Implement duplicate-report detection.
- [ ] Aggregate reports by entity.
- [ ] Add worker-level monitoring and structured logging.
- [ ] Keep automated findings separate from human moderation decisions.

### Phase 5 — Frontend application

- [ ] Build the reporting interface.
- [ ] Implement user registration and login screens.
- [ ] Build entity search and report-detail pages.
- [ ] Create a user report-history view.
- [ ] Build an administrative moderation dashboard.
- [ ] Add responsive layouts and accessible interactions.

### Phase 6 — Production readiness

- [ ] Containerize the application and its dependencies.
- [ ] Add health checks for PostgreSQL and RabbitMQ.
- [ ] Configure production secrets and HTTPS.
- [ ] Implement request rate limiting and abuse controls.
- [ ] Add monitoring, logging, and backup procedures.
- [ ] Define privacy, retention, and dispute-handling policies.
- [ ] Deploy to a suitable hosting environment.

---

## Contributing

Contributions, suggestions, and constructive feedback are welcome.

If contributing to the project:

1. Fork the repository.
2. Create a feature branch.
3. Keep API routes, business logic, database access, and messaging responsibilities separate.
4. Add or update database migrations when changing models.
5. Add tests for new functionality and security-sensitive behavior.
6. Document configuration changes.
7. Submit a pull request describing the change and how it was tested.

Suggested branch naming:

```text
feature/report-risk-analysis
feature/duplicate-detection
feature/admin-audit-logs
fix/rabbitmq-retry-handling
```

For security-sensitive issues, avoid publishing exploitable details or real user data in public discussions.

---

## License

This project should be distributed under the license included in the repository.

If the repository does not yet contain a license, choose and add an appropriate license before inviting external contributions or presenting the project as open source.

---

## Author and Project Context

**VerifyKE** is a portfolio-oriented software engineering project focused on backend development, secure API design, relational data modeling, asynchronous messaging, and responsible fraud-reporting workflows.

The project demonstrates the progression from a conventional API backed by PostgreSQL to an event-driven architecture that can later support background analysis and moderation assistance.

**Core technologies:** Python · FastAPI · PostgreSQL · SQLAlchemy · Alembic · JWT · Argon2 · RabbitMQ · Docker

**Repository:** Add the public GitHub repository URL when available.

---

*VerifyKE is a developing software project, not an official government service, law-enforcement system, or independent guarantee that a reported entity is fraudulent. Reports and automated indicators must be interpreted in context and handled responsibly.*