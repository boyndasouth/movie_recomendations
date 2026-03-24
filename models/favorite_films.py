from extensions import db

class FavoriteFilm(db.Model):
    __tablename__ = "favorite_films"

    id = db.Column(db.Integer, primary_key=True)
    film = db.Column(db.JSON)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Favorite Film {self.film.get('title')}>"