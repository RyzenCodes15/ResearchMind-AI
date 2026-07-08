# ResearchMind AI

ResearchMind AI is a production-oriented AI research assistant scaffold built around Retrieval-Augmented Generation (RAG).

## What Is Included

- FastAPI backend with a health endpoint
- Next.js frontend with App Router, TypeScript, and Tailwind CSS
- PostgreSQL with the pgvector extension enabled
- SQLAlchemy and Alembic database infrastructure
- Docker and Docker Compose for local development

## Quick Start

Run the full stack with:

```bash
docker compose up --build
```

After startup, the services are available at:

- Frontend: http://localhost:3000
- Backend health: http://localhost:8000/health
- API health: http://localhost:8000/api/v1/health
- PostgreSQL: localhost:5432

## Environment Files

Use the example files as the starting point for local configuration:

- [backend/.env.example](backend/.env.example)
- [frontend/.env.example](frontend/.env.example)

## Backend Development

The backend uses Python 3.13, pip requirements files, SQLAlchemy, Alembic, Pydantic Settings, and Uvicorn.

## Frontend Development

The frontend uses the Next.js App Router with TypeScript and Tailwind CSS.

## Notes

- Only health endpoints are implemented.
- Authentication, RAG workflows, document processing, and vector search are intentionally deferred.
- PostgreSQL is started with pgvector available via the container image and init script.
