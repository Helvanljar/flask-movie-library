"""Main Flask application for the Movie Library."""
from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, Movie, User
from omdb_service import fetch_movie_details

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moviweb.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
data_manager = DataManager()

@app.route("/", methods=["GET"])
def index():
    """Homepage: show all users and add user form."""
    users = data_manager.get_users()
    return render_template("index.html", users=users)

@app.route("/users", methods=["POST"])
def create_user():
    """Handle form submission to create a new user."""
    name = request.form.get("name")
    if name:
        data_manager.create_user(name)
    return redirect(url_for("index"))

@app.route("/users/<int:user_id>/movies", methods=["GET", "POST"])
def user_movies(user_id):
    """Show or add movies for a specific user."""
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        title = request.form.get("title")
        if title:
            try:
                details = fetch_movie_details(title)
                if details:
                    new_movie = Movie(
                        name=details["name"],
                        director=details["director"],
                        year=details["year"],
                        poster_url=details["poster_url"],
                        user_id=user.id
                    )
                    data_manager.add_movie(new_movie)
            except Exception as e:
                app.logger.error(f"Error adding movie: {e}")
                return "Error adding movie", 500
        return redirect(url_for("user_movies", user_id=user.id))

    movies = data_manager.get_movies(user.id)
    return render_template("movies.html", user=user, movies=movies)

@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_movie(user_id, movie_id):
    """Update the title of a movie."""
    new_title = request.form.get("new_title")
    if new_title:
        data_manager.update_movie(movie_id, new_title)
    return redirect(url_for("user_movies", user_id=user_id))

@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    """Delete a movie from a user's list."""
    data_manager.delete_movie(movie_id)
    return redirect(url_for("user_movies", user_id=user_id))

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page."""
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    """Custom 500 page."""
    return render_template("500.html"), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)
