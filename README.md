# Technical Challenge

> ⚠️ **AI tools are not recommended.** The goal is not to get everything right, but to demonstrate general knowledge of Python and API development.

## Objective

Complete the `app.py` file by implementing two REST API endpoints using FastAPI. All other files are already provided.

## Project Structure

| File | Description |
| --- | --- |
| `app.py` | ⚡ **Your focus**: API endpoints (file to be completed) |
| `processing.py` | Text processing functions |
| `database.py` | In-memory storage and history |
| `models.py` | Pydantic models: request, response and record |
| `requirements.txt` | Project dependencies |

## Endpoints

### `POST /analyze`

Receives a text and returns the character count. The analysis must be saved to history.

Request:

```json
{ "text": "Hello, world!" }
```

Response:

```json
{ "letter_count": 12 }
```

### `GET /history`

Returns all analyses performed since the application started.

Response:

```json
[{ "text": "Hello, world!", "letter_count": 12, "created_at": "..." }]
```

## Requirements

- Use FastAPI as the framework
- Import and use the models already defined in `models.py`
- Import and use the processing function from `processing.py`
- Import and use the in-memory history from `database.py`

## How to run

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Interactive docs available at http://localhost:8000/docs

## What will be evaluated

- Correctness of both endpoints
- Proper use of the provided models and functions
- Code clarity and organization
- Basic Python best practices (type hints, naming)
