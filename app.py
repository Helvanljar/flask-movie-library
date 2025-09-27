import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv
from models import db, Movie, User
from data_manager import DataManager

# Load environment variables
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecret"  # Needed for flash messages
db.init_app(app)

data_manager = DataManager()

# ✅ Create database/tables safely at startup
with app.app_context():
    try:
        db.create_all()
        app.logger.info("Database initialized successfully.")
    except Exception as e:
        app.logger.error(f"Error initializing database: {e}")
        flash("Database initialization failed. Please check logs.", "error")


@app.route("/")
def index():
    """Home page showing all users."""
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    """Add a new user."""
    name = request.form.get("name")
    if name:
        try:
            data_manager.create_user(name)
            flash(f"User '{name}' created successfully!", "success")
        except Exception as e:
            app.logger.error(f"Error creating user: {e}")
            flash("Error creating user.", "error")
    else:
        flash("Name cannot be empty.", "error")
    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/movies", methods=["GET", "POST"])
def user_movies(user_id):
    """List or add movies for a user."""
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        title = request.form.get("title")
        if not title:
            flash("Movie title cannot be empty.", "error")
            return redirect(url_for("user_movies", user_id=user_id))

        try:
            response = requests.get(
                "http://www.omdbapi.com/",
                params={"t": title, "apikey": OMDB_API_KEY},
                timeout=5
            )
            data = response.json()
            if data.get("Response") == "True":
                movie = Movie(
                    name=data.get("Title"),
                    director=data.get("Director"),
                    year=data.get("Year"),
                    poster_url=data.get("Poster"),
                    user_id=user.id,
                )
                data_manager.add_movie(movie)
                flash(f"Movie '{movie.name}' added!", "success")
            else:
                flash(f"Movie '{title}' not found on OMDb.", "error")
        except Exception as e:
            app.logger.error(f"Error fetching movie: {e}")
            flash("An error occurred while adding the movie.", "error")

    movies = data_manager.get_movies(user.id)
    return render_template("movies.html", user=user, movies=movies)


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_movie(user_id, movie_id):
    """Update the title of a movie."""
    new_title = request.form.get("new_title")
    if new_title:
        try:
            data_manager.update_movie(movie_id, new_title)
            flash("Movie updated successfully!", "success")
        except Exception as e:
            app.logger.error(f"Error updating movie: {e}")
            flash("Error updating movie.", "error")
    return redirect(url_for("user_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    """Delete a movie from the user's list."""
    try:
        data_manager.delete_movie(movie_id)
        flash("Movie deleted.", "success")
    except Exception as e:
        app.logger.error(f"Error deleting movie: {e}")
        flash("Error deleting movie.", "error")
    return redirect(url_for("user_movies", user_id=user_id))


# ✅ Health check route
@app.route("/health")
def health_check():
    """Health check endpoint to verify app and DB are working."""
    try:
        # Simple DB check: count users
        user_count = User.query.count()
        return jsonify(status="ok", users=user_count), 200
    except Exception as e:
        app.logger.error(f"Health check failed: {e}")
        return jsonify(status="error", message=str(e)), 500


# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True, port=5002)

