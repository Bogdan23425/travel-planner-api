# Travel Planner API

Travel Planner API is a FastAPI backend for managing travel projects and places travellers want to visit.

The application uses SQLite for storage and validates places through the Art Institute of Chicago API. Each project contains from 1 to 10 places, and the same external place cannot be added to one project more than once.

## Features

- Create, list, update and delete travel projects
- Create a project together with places in one request
- Add Art Institute places to an existing project
- Add and update notes for project places
- Mark places as visited
- Automatically mark a project as completed when all its places are visited
- Prevent deleting projects that contain visited places
- Validate external places before storing them

## API Documentation

Interactive OpenAPI documentation is available in Swagger UI at `/docs`.

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Run With Docker

```bash
docker compose up --build
```

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Docker
