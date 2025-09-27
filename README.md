# 🎥 MoviWeb App

A Flask web application where users can manage their favorite movies. Movies are fetched dynamically from the OMDb API.

## Features
- User registration & selection
- Add, update, and delete favorite movies
- Fetch movie details (title, year, director, poster) from OMDb
- iOS-inspired design (rounded cards, blue buttons)
- Error handling with:
  - Flash messages for success/error
  - Custom 404 and 500 pages
- Health check endpoint: `/health` (returns JSON with status & user count)

## Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:Helvanljar/flask-movie-library.git
   cd flask-movie-library
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory:
   ```
   OMDB_API_KEY=your_api_key_here
   ```

5. Run the app:
   ```bash
   flask run
   ```
   Then open [http://localhost:5002](http://localhost:5000).

6. Optional: Check app health:
   ```bash
   curl http://localhost:5000/health
   ```

## Requirements
See [requirements.txt](requirements.txt).
