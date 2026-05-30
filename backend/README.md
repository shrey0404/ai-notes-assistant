# AI Notes Assistant - Backend

FastAPI backend for the AI Notes Assistant application.

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- OpenAI API Key

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run application:
```bash
uvicorn app.main:app --reload
```

Application will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── note.py
│   ├── repositories/
│   │   └── note_repository.py
│   ├── schemas/
│   │   └── note.py
│   ├── services/
│   │   ├── note_service.py
│   │   └── ai_service.py
│   └── main.py
├── tests/
├── requirements.txt
└── Dockerfile
```

## Phase 1 Completed

✓ Project structure created
✓ Configuration management
✓ Database setup
✓ ORM models
✓ Pydantic schemas
✓ Repository layer
✓ Service layer (placeholder for AI)

## Next Phase

Phase 2: Database migrations and CRUD endpoints
