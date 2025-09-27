# 🎥 Flask Movie Library

A Flask web application where users can register and manage a personal list of favorite movies.  
Movie details (title, director, year, poster) are fetched from the [OMDb API](http://www.omdbapi.com/).

---

## 🚀 Features

- User management (add/select users)
- Add movies to a user's favorites by title (fetched from OMDb)
- Update or delete movies from the list
- Display posters and details for each movie
- Error handling with custom 404 and 500 pages
- Simple, responsive UI

---

## 📂 Project Structure

```
flask-movie-library/
│-- app.py              # Main Flask app
│-- models.py           # SQLAlchemy models (User, Movie)
│-- data_manager.py     # CRUD operations with ORM
│-- omdb_service.py     # OMDb API integration
│-- requirements.txt    # Dependencies
│-- .env.example        # Example environment variables file
│-- static/
│   └── style.css       # Stylesheet
│-- templates/
│   │-- base.html
│   │-- index.html
│   │-- movies.html
│   │-- 404.html
│   └── 500.html
```

---

## ⚙️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/Helvanljar/flask-movie-library.git
   cd flask-movie-library
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate    # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables:
   - Copy `.env.example` to `.env`
   - Edit `.env` and replace with your actual OMDb key:
     ```
     OMDB_API_KEY=your_real_key_here
     ```

5. Run the app:
   ```bash
   python app.py
   ```

6. Open your browser at:  
   👉 http://127.0.0.1:5002/

---

## 🔑 Environment Variables

This project uses a `.env` file to store the OMDb API key securely.

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and replace with your actual key:
   ```
   OMDB_API_KEY=your_real_key_here
   ```

3. Keep your `.env` out of version control (add it to `.gitignore`).

---

## 🌐 Running the App on a Custom Port

By default, this app runs on port **5002**.  
You can change it in `app.py` if needed, or run:

```bash
flask run --port=5002
```

---

## 🛠 Technologies Used

- Python 3  
- Flask  
- SQLAlchemy  
- OMDb API  
- python-dotenv  
- HTML, CSS

---

## 👤 Author

- GitHub: [Helvanljar](https://github.com/Helvanljar)

