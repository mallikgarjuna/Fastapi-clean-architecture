# FastAPI Clean Architecture

A **minimalistic production-ready FastAPI project template** following a modular and clean architecture principles.

I was confused to see many starter projects on github with unstructured code and inconsistent project structure, and with go guidelines for setting up a FastAPI project for beginners. I wanted to have a good starting point for my FastAPI projects and I could not find one anywhere online. So I decided to create one from scratch.

You can go through the git history to see how this project has evovled from a single `main.py` file to this current state of structured architecture.

- the starting main.py file is taken from the code example in the fastapi official docs. These docs are very well written with good explanations by Sebastián Ramírez (tiangolo), the creator of FastAPI and SQLModel libraries used in this project)

There are still a couple of things I want to do (like refactoring and adding new things) to make this as complete as possible for my use cases, and I'll try updating this over time.

## Features

- A minimalistic FastAPI application with **modular and clearn architecture**
  - specifically, **controller-service-repository** layered architecture
  - controller layer: for handling **HTTP requests and routing**
  - service layer: for handling **business logic and data access**
  - repository layer: for handling **database operations**
- Database integration using **SQLModel** (uses **SQLAlchemy** under the hood)
- Creating multiple database models with inheritance using SQLModel (which also uses Pydantic under the hood)
- Database migrations with **Alembic**
- Project wide settings configuration using **Pydantic-settings** (a separate mini library from **Pydantic**)
- **Dockerfile and docker-compose** set up for containerized development, and possibly production deployment
- Testing (using in-memory instead of file memory) with **Pytest** and mocking support from **Pytest-mock** plugin for pytest
- Sample **api.http** file for testing API endpoints in VSCode (REST Client extension is needed)

---

### Dependencies

- **uv**: for python project and virtual environment setup and management
- **git**: for tracking code changes and version control
- **fastapi**: for API!
- **sqlmodel**: for database tables and data models (uses sqlalchemy and pydantic under the hood)
- **alembic**: for database migrations
- **pydantic**: for data validation and serialization
- **pydantic-settings**: for project wide configuration settings
- **pytest**: for testing, with fixures (dependencies) confuration in conftest.py
- **pytest-mock**: (plugin for pytest) for mocking database repository while testing the service layer
- **logging**: for basic logging including logging to file and console set up
- **postgresql**: SQL database (can be replaced with **SQLite** in the configuration settings)
- **dockerfile**: for containerizing fastapi app
- **docker-compose**: for creating and running all services at once: fastapi-app, postgresql, alembic, and pgadmin services.
- **run.sh**: script file for making sure to start postgresql server on local machine before starting the fastapi server
- **api.http**: for testing the api inside vscode IDE (need REST Client vscode extension) with pre-defined API test endpoints

## Project tree structure

. # Project's root directory
├── app # Fastapi app
│ ├── models
│ ├── repositories
│ ├── routers
│ ├── services
│ ├── config.py
│ ├── db.py
│ ├── dependencies.py
│ ├── **init**.py
│ ├── logging_config.py
│ └── main.py
├── logs
│ └── app.log
├── migrations
│ ├── versions
│ ├── env.py
│ ├── README
│ └── script.py.mako
├── .pytest_cache
│ ├── v
│ ├── CACHEDIR.TAG
│ ├── .gitignore
│ └── README.md
├── tests
│ ├── test_repositories
│ ├── test_routers
│ ├── test_services
│ ├── conftest.py
│ └── **init**.py
├── alembic.ini
├── api.http
├── app.log
├── database.db
├── docker-compose.yml
├── Dockerfile
├── .dockerignore
├── .env
├── .gitignore
├── notes-mg.py
├── pyproject.toml
├── .python-version
├── README.md
├── run.sh
└── uv.lock

## Running this project

### Locally

```bash
uv run fastapi dev app/main.py

# OR

./run.sh
```

### Using Docker

```bash
docker-compose up --build
```

## Testing the API

- FastAPI's Swagger UI: http://localhost:8000/docs

OR

- Run inside VSCode with the "REST Client" extension
- in api.http file

## Inspiration

- FastAPI official docs
- SQLModel official docs
- `controller-service-repository` architecture from CodeWithMosh
