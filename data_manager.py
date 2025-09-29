from models import db, User, Movie

class DataManager:
    def create_user(self, name):
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return user

    def get_users(self):
        return User.query.all()

    def get_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, new_data: dict):
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_data.get("name", movie.name)
            movie.director = new_data.get("director", movie.director)
            movie.year = new_data.get("year", movie.year)
            movie.poster_url = new_data.get("poster_url", movie.poster_url)
            db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
