"""Database models for the Movie Library app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User model representing app users."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    movies = db.relationship("Movie", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.name}>"

class Movie(db.Model):
    """Movie model representing movies in a user's library."""
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(300))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="movies")

    def __repr__(self):
        return f"<Movie {self.name}, {self.year}>"
