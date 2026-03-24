from flask import Flask, url_for, request, render_template, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from movie_rec_nn import film_nn
from movie_recomender import movie_recomender, movie_trailer
from extensions import db
import json
from types import SimpleNamespace

genres = {"Action" : 0, 
          "Comedy" : 1, 
          "Drama" : 2, 
          "Horror" : 3, 
          "Romance" : 4, 
          "SciFi" : 5, 
          "Thriller" : 6}

genre_ids = {"Action" : 28, 
             "Comedy" : 35, 
             "Drama" : 18, 
             "Horror" : 27, 
             "Romance" : 10749, 
             "SciFi" : 878, 
             "Thriller" : 53}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from models import User, FavoriteFilm

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def start_page():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        zipcode = int(request.form.get("zipcode"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(username=username, password=hashed_password, zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please log in.")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/survey_intro")
def survey_intro():
    return render_template("index.html")

@app.route("/survey", methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        age = int(request.form['age'])
        explosions = int(request.form.get('likes_explosions'))
        romance = int(request.form.get('likes_romance'))
        scary = int(request.form.get('likes_scary'))
        deep_story = int(request.form.get('likes_deep_story'))
        humor = int(request.form.get('likes_humor'))
        space = int(request.form.get('likes_space'))
        mystery = int(request.form.get('likes_mystery'))
        movie_length = int(request.form['preferred_length'])

        genre_choices = film_nn(age, 
                                explosions, 
                                romance, 
                                scary, 
                                deep_story, 
                                humor, 
                                space, 
                                mystery, 
                                movie_length)

        genre_list = []
        genre = None
        for key, value in genres.items():
            for g in genre_choices:
                if g == value:
                    genre_list.append(key)
                    break
        return redirect(url_for('results', 
                                genres=genre_list))

    return render_template("survey.html")

@app.route("/results")
def results():
    global movies
    global genre_list
    genre_list = request.args.getlist('genres')

    new_genre_list = []
    for key, value in genre_ids.items():
        for genre in genre_list:
            if genre == key:
                new_genre_list.append(value)
    
    genre_list_string = ", ".join(str(g) 
                                  for g in new_genre_list)

    movies = movie_recomender(genre_list_string)
    
    return render_template("results.html", 
                           user=current_user,
                           genres=genre_list, 
                           movies=movies)

@app.route("/movie_details/<int:movie_id>")
def movie_details(movie_id):
    global similar_movies
    global trailer_key
    for movie in movies:
        if movie['id'] == movie_id:
            similar_movie_genres = ", ".join(str(g) for 
                                             g in movie['movie_genre'])
            trailer_key = movie_trailer(movie_id)
            similar_movies = movie_recomender(similar_movie_genres)
            return render_template("movie_details.html", 
                                   movie=movie, 
                                   user=current_user,
                                   genres=genre_list, 
                                   trailer_key=trailer_key, 
                                   similar_movies=similar_movies)

    return redirect(url_for("results", genres=genre_list))

@app.route("/list_page")
@login_required
def list_page():
    user_favorites = [fav.film for fav in current_user.favorite_movies] 

    return render_template("list.html", 
                           favorites=user_favorites,
                           user=current_user, 
                           genres=genre_list)

@app.route("/add_favorite/<int:movie_id>")
def add_favorite(movie_id):
    for movie in movies:
        if movie['id'] == movie_id:
            fav_movie = FavoriteFilm(film=movie, user_id=current_user.id)
            db.session.add(fav_movie)
            db.session.commit()
            return redirect(request.referrer)
    return redirect(request.referrer)

@app.route("/delete_favorite/<int:movie_id>")
def delete_favorite(movie_id):
    for movie in movies:
        if movie['id'] == movie_id:
            for fav in FavoriteFilm.query.all():
                if fav.film == movie and fav.user_id == current_user.id:
                    db.session.delete(fav)
                    db.session.commit()
                    return redirect(request.referrer)

    return redirect(request.referrer)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)