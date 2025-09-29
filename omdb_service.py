import os
import requests
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")


def fetch_movie(title):
    """Fetch movie data from OMDb API by title. Returns dict or None."""
    response = requests.get(
        "http://www.omdbapi.com/",
        params={"t": title, "apikey": OMDB_API_KEY},
        timeout=5
    )
    data = response.json()
    return data if data.get("Response") == "True" else None
