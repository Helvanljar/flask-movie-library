import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv
from markupsafe import escape
from sqlalchemy.exc import IntegrityError
from models import db, Movie, User
from data_manager import DataManager
from omdb_service import fetch_movie

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecret"  # Needed for flash messages
db.init_app(app)

data_manager = DataManager()

# Smarter DB initialization
with app.app_context():
    inspector = db.inspect(db.engine)
    if not inspector.has_table("user") or not inspector.has_table("movie"):
        db.create_all()
        app.logger.info("Database tables created.")
    else:
        app.logger.info("Database already initialized.")


@app.route("/")
def index():
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    name = escape(request.form.get("name", "").strip())
    if not name:
        flash("Name cannot be empty.", "error")
        return redirect(url_for("index"))
    try:
        if User.query.filter_by(name=name).first():
            flash(f"User '{name}' already exists.", "error")
        else:
            data_manager.create_user(name)
            flash(f"User '{name}' created successfully!", "success")
    except IntegrityError:
        db.session.rollback()
        flash("A database integrity error occurred.", "error")
    except Exception as e:
        flash(f"Unexpected error: {e}", "error")
    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/movies", methods=["GET", "POST"])
def user_movies(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        title = escape(request.form.get("title", "").strip())
        if not title:
            flash("Movie title cannot be empty.", "error")
            return redirect(url_for("user_movies", user_id=user_id))
        try:
            data = fetch_movie(title)
            if data:
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
    new_data = {
        "name": escape(request.form.get("new_title", "").strip()),
        "director": escape(request.form.get("new_director", "").strip()),
        "year": escape(request.form.get("new_year", "").strip()),
        "poster_url": escape(request.form.get("new_poster", "").strip()),
    }
    new_data = {k: v for k, v in new_data.items() if v}
    if new_data:
        try:
            data_manager.update_movie(movie_id, new_data)
            flash("Movie updated successfully!", "success")
        except Exception as e:
            app.logger.error(f"Error updating movie: {e}")
            flash("Error updating movie.", "error")
    else:
        flash("Please provide at least one field to update.", "warning")
    return redirect(url_for("user_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    try:
        data_manager.delete_movie(movie_id)
        flash("Movie deleted.", "success")
    except Exception as e:
        app.logger.error(f"Error deleting movie: {e}")
        flash("Error deleting movie.", "error")
    return redirect(url_for("user_movies", user_id=user_id))


@app.route("/health")
def health_check():
    try:
        user_count = User.query.count()
        return jsonify(status="ok", users=user_count), 200
    except Exception as e:
        app.logger.error(f"Health check failed: {e}")
        return jsonify(status="error", message=str(e)), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
