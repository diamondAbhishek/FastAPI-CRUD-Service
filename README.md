# FastAPI CRUD Service

A simple, production-ready FastAPI application that provides CRUD (Create, Read, Update, Delete) operations for managing books. This project demonstrates best practices in Python, FastAPI, SQLAlchemy, and REST API design.

## Features

- ✅ **FastAPI** web framework with automatic API documentation
- ✅ **SQLAlchemy** ORM with PostgreSQL (default) / SQLite support
- ✅ **Pydantic** schemas for request/response validation
- ✅ **CRUD endpoints** with proper HTTP status codes
- ✅ **Pagination and filtering** support
- ✅ **Custom SQL queries** with aggregation
- ✅ **Transaction handling** demonstration
- ✅ **Comprehensive testing** (unit + integration tests)
- ✅ **Docker support** with docker-compose
- ✅ **Clean code organization** with proper structure

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration and session management
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── services.py          # Business logic services
│   └── routers/
│       ├── __init__.py
│       └── items.py         # CRUD endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_api.py          # Integration tests
│   └── test_services.py     # Unit tests
├── data/                    # (Optional) SQLite database files directory
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.11+ (or Docker)
- **PostgreSQL** (default, included in Docker Compose) or SQLite (for local development)

## Quick Start

### Option 1: Using Docker (Recommended)

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access the API:**
   - API: http://localhost:8000
   - Interactive API docs (Swagger): http://localhost:8000/docs
   - Alternative API docs (ReDoc): http://localhost:8000/redoc

3. **Stop the service:**
   ```bash
   docker-compose down
   ```

### Option 2: Local Development

**Note:** For local development without Docker, you have two options:

#### Option 2a: With PostgreSQL (Recommended)

1. **Install and start PostgreSQL locally:**
   - Make sure PostgreSQL is running on `localhost:5432`
   - Create a database: `createdb crud_service_db`
   - Or use the provided Docker Compose PostgreSQL service separately

2. **Set environment variable:**
   ```bash
   export DATABASE_URL="postgresql://fastapi_user:fastapi_password@localhost:5432/crud_service_db"
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Option 2b: With SQLite (Development Only)

1. **Set environment variable for SQLite:**
   ```bash
   export DATABASE_URL="sqlite:///./crud_service.db"
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

**Access the API:**
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs

## API Endpoints

### Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/items/` | Create a new book | 201, 400 |
| GET | `/items/` | List all books (with pagination & filtering) | 200 |
| GET | `/items/{id}` | Get a specific book | 200, 404 |
| PUT | `/items/{id}` | Update a book (full update) | 200, 404, 400 |
| PATCH | `/items/{id}` | Update a book (partial update) | 200, 404, 400 |
| DELETE | `/items/{id}` | Delete a book | 204, 404 |

### Query Parameters (GET /items/)

- `page` (int, default: 1): Page number
- `page_size` (int, default: 10, max: 100): Items per page
- `author` (string, optional): Filter by author name (case-insensitive partial match)

### Example Requests

**Create a book:**
```bash
curl -X POST "http://localhost:8000/api/v1/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "description": "A classic American novel"
  }'
```

**List books with pagination:**
```bash
curl "http://localhost:8000/api/v1/items/?page=1&page_size=10"
```

**Filter by author:**
```bash
curl "http://localhost:8000/api/v1/items/?author=Fitzgerald"
```

**Get a specific book:**
```bash
curl "http://localhost:8000/api/v1/items/1"
```

**Update a book:**
```bash
curl -X PUT "http://localhost:8000/api/v1/items/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby (Updated)",
    "author": "F. Scott Fitzgerald",
    "description": "A classic American novel - Updated edition"
  }'
```

**Delete a book:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/items/1"
```

## Data Model

### Book Entity

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | Integer | Primary Key, Auto-increment |
| `title` | String(200) | Unique, Non-null, Indexed |
| `description` | String(1000) | Nullable |
| `author` | String(100) | Non-null |
| `created_at` | DateTime | Auto-generated |
| `updated_at` | DateTime | Auto-updated |

## Testing

### Run all tests:
```bash
pytest
```

### Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

### Run specific test file:
```bash
pytest tests/test_api.py
pytest tests/test_services.py
```

### Run specific test:
```bash
pytest tests/test_api.py::test_create_item
```

The test suite includes:
- **Unit tests** for business logic (`test_services.py`)
- **Integration tests** for API endpoints (`test_api.py`)
- Custom SQL query tests (aggregation)
- Transaction handling tests

## Database Migrations

The application currently creates tables automatically on startup. For production use, consider using **Alembic** for migrations:

1. Install Alembic:
   ```bash
   pip install alembic
   ```

2. Initialize Alembic:
   ```bash
   alembic init alembic
   ```

3. Configure `alembic.ini` and `alembic/env.py` to use your database connection.

## Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string
  - **PostgreSQL (default in Docker)**: `postgresql://fastapi_user:fastapi_password@postgres:5432/crud_service_db`
  - **PostgreSQL (local)**: `postgresql://user:password@localhost:5432/dbname`
  - **SQLite (development)**: `sqlite:///./crud_service.db`

### PostgreSQL Configuration (Default)

The project is configured to use PostgreSQL by default when running with Docker Compose. The PostgreSQL service is automatically set up with:

- **Host**: `postgres` (within Docker network) or `localhost` (local development)
- **Internal Port**: `5432` (used by API service within Docker network)
- **External Port**: `5433` (for host access, to avoid conflict with local PostgreSQL)
- **Database**: `crud_service_db`
- **User**: `fastapi_user`
- **Password**: `fastapi_password`

**For Docker Compose:** The configuration is already set up. Just run `docker-compose up`.
- The API service connects internally to `postgres:5432` (no change needed)
- To connect from host machine, use `localhost:5433`

**For Local Development:** Make sure PostgreSQL is running and set the `DATABASE_URL` environment variable accordingly.

## Code Highlights

### Custom SQL Query (ORM Aggregation)
Located in `app/services.py`:
```python
def get_books_by_author_count(db: Session, min_books: int = 1):
    # Custom SQL query with GROUP BY and HAVING
    result = (
        db.query(Book.author, func.count(Book.id).label('book_count'))
        .group_by(Book.author)
        .having(func.count(Book.id) >= min_books)
        .order_by(func.count(Book.id).desc())
        .all()
    )
```

### Transaction Handling
Located in `app/services.py`:
```python
def bulk_create_books_transaction(db: Session, books_data: List[dict]):
    try:
        # Multiple operations in a single transaction
        for book_data in books_data:
            book = Book(**book_data)
            db.add(book)
        db.commit()  # Commit all or none
    except Exception as e:
        db.rollback()  # Rollback on any error
        raise e
```

## Development

### Code Style

The project follows PEP 8 Python style guidelines. Consider using:
- `black` for code formatting
- `flake8` or `pylint` for linting
- `mypy` for type checking

### Adding New Features

1. **New Model**: Add to `app/models.py`
2. **New Schema**: Add to `app/schemas.py`
3. **New Endpoint**: Add to `app/routers/items.py` or create a new router
4. **New Business Logic**: Add to `app/services.py`
5. **Tests**: Add corresponding tests in `tests/`

## License

This project is created as part of a backend assignment.

## Author

Created following FastAPI best practices and REST API design principles.

