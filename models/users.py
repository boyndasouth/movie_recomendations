from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(75), unique=True, nullable=False)
    zipcode = db.Column(db.Integer, primary_key=False, nullable=False)

    favorite_movies = db.relationship(
        "FavoriteFilm",
        backref="user",
        lazy=True
    )
    def __repr__(self):
        return f"<User {self.username}>"