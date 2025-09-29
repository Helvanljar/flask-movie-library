# 🎥 MoviWeb App (Improved)

A Flask web app to manage users and their favorite movies. Fetches details from OMDb.
This build includes stronger validation, modular OMDb service, richer updates, error handling, and iOS-inspired UI.

## Features
- Add/select users (duplicate name check, sanitized input)
- Per-user movies: add, update (title/director/year/poster), delete
- OMDb lookup via dedicated `omdb_service.py`
- Flash messages + 404/500 pages
- `/health` endpoint to verify app & DB
- Auto-creates SQLite DB on first run
- Clean iOS-like UI

## Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and paste your OMDb key
flask run --host=0.0.0.0 --port=5000
```
Open http://localhost:5000

## Health Check
```bash
curl http://localhost:5000/health
```

## Environment
```
OMDB_API_KEY=your_api_key_here
```
