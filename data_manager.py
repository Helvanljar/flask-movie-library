"""DataManager class handles CRUD operations using SQLAlchemy ORM."""
from models import db, User, Movie

class DataManager:
    """Encapsulates CRUD operations for Users and Movies."""

    def create_user(self, name: str) -> User:
        """Create and save a new user."""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        """Return all users."""
        return User.query.all()

    def get_movies(self, user_id: int):
        """Return all movies for a user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie: Movie) -> Movie:
        """Add a movie to the database."""
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id: int, new_title: str):
        """Update the title of a movie."""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_title
            db.session.commit()
        return movie

    def delete_movie(self, movie_id: int):
        """Delete a movie by ID."""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
        return movie
