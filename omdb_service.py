"""Service for fetching movie details from the OMDb API."""
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = "http://www.omdbapi.com/"

def fetch_movie_details(title: str):
    """Fetch movie info from OMDb by title."""
    if not OMDB_API_KEY:
        raise ValueError("OMDB_API_KEY not set. Add it to your .env file.")

    params = {"t": title, "apikey": OMDB_API_KEY}
    response = requests.get(OMDB_URL, params=params)
    data = response.json()

    if data.get("Response") == "True":
        return {
            "name": data.get("Title"),
            "director": data.get("Director"),
            "year": int(data.get("Year")) if data.get("Year") and data.get("Year").isdigit() else None,
            "poster_url": data.get("Poster") if data.get("Poster") != "N/A" else None
        }
    return None
