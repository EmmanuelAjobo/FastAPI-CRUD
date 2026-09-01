# FastAPI-CRUD

A complete FastAPI application covering full CRUD operations, JWT authentication, login, and a voting system.

## Features

- Full CRUD (Create, Read, Update, Delete) endpoints
- JWT-based authentication
- User login and registration
- Voting model (upvote/downvote on resources)
- Database migrations with Alembic

## Tech Stack

- **Framework:** FastAPI (Python)
- **Migrations:** Alembic
- **Dependency management:** uv
- **Auth:** JWT (OAuth2 password flow)

## Project Structure

```
FastAPI-CRUD/
├── alembic/          # Database migration scripts
├── app/              # Application source code (routes, models, schemas, auth)
├── alembic.ini        # Alembic configuration
├── main.py            # App entry point
├── pyproject.toml      # Project metadata and dependencies
├── requirement.txt     # Pinned dependencies
└── uv.lock             # Locked dependency versions (uv)
```

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) installed
- A running PostgreSQL (or your configured DB) instance

### Installation

```bash
git clone https://github.com/EmmanuelAjobo/FastAPI-CRUD.git
cd FastAPI-CRUD
uv sync
```

### Environment Variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run Migrations

```bash
alembic upgrade head
```

### Start the Server

```bash
uv run uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

Once running, interactive docs are available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints Overview

| Method | Endpoint          | Description                  |
|--------|-------------------|-------------------------------|
| POST   | `/login`     | Log in and receive JWT token |
| GET    | `/posts`          | List all items                |
| POST   | `/posts`          | Create a new item             |
| GET    | `/posts/{id}`     | Retrieve a single item        |
| PUT    | `/posts/{id}`     | Update an item                |
| DELETE | `/post/{id}`     | Delete an item                |
| POST   | `/vote`           | Cast a vote on an item        |

*Adjust the table above to match your actual route names and prefixes.*

## Running Tests

```bash
uv run pytest
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Emmanuel Ajobo**
[GitHub](https://github.com/EmmanuelAjobo) · [LinkedIn](https://linkedin.com/in/emmanuel-ajobo)
