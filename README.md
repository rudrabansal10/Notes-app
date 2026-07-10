# 📝 Notes App

A simple full-stack notes application with a **FastAPI** backend (PostgreSQL via SQLAlchemy) and a **Streamlit** frontend for creating, viewing, updating, and deleting notes.

This project is a basic CRUD (Create, Read, Update, Delete) notes manager built to practice connecting a Python backend API to a database and a lightweight frontend. 

## Features

- 📋 View all saved notes at once
- 🔍 Look up a specific note by its ID
- ➕ Add a new note with a name and content
- ✏️ Update an existing note's name or content
- 🗑️ Delete a note by ID
- Multi-line note content is preserved and displayed correctly
- Simple action-driven frontend: pick an action, fill in a form, submit
- Environment-based configuration via `.env` (no hardcoded credentials)

## Tech Stack

- **Backend framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** Streamlit
- **HTTP client (frontend → backend):** `requests`
- **Config management:** python-dotenv

## Project Structure

```
Notes_app/
├── main.py                  # FastAPI backend (API routes)
├── models.py                 # Pydantic models (Note schema)
├── database.py                # DB engine/session setup
├── notes_app_frontend/
│   └── app.py                  # Streamlit frontend
├── .env                        # Local environment variables (not committed)
└── .env.example                 # Example env file
```

## Setup

### 1. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv streamlit requests
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and set your database URL:

```
DATABASE_URL=postgresql://user:password@localhost:5432/notes_db
```

### 3. Run the backend

```bash
uvicorn main:app --reload
```

API available at `http://127.0.0.1:8000` (interactive docs at `/docs`).

### 4. Run the frontend

In a separate terminal:

```bash
streamlit run notes_app_frontend/app.py
```

The frontend expects the backend to be running at `http://127.0.0.1:8000` by default.

## API Endpoints

| Method | Endpoint      | Description            | Request Body |
|--------|---------------|--------------------------|----------------|
| GET    | `/notes`      | Get all notes            | —              |
| GET    | `/notes/{id}` | Get a note by ID         | —              |
| POST   | `/notes`      | Add a new note           | `{id, name, content}` |
| PUT    | `/notes/{id}` | Update a note            | `{id, name, content}` |
| DELETE | `/notes/{id}` | Delete a note            | —              |
