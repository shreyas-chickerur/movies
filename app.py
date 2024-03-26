from flask import Flask, render_template, url_for, redirect, request
from models import *
from sqlalchemy.exc import IntegrityError
import random
from sqlalchemy import union_all, select


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = returnDB()
db.init_app(app)
global current_user



def initialize_tables():
    # Genres Table
    
        genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Science Fiction (Sci-Fi)", "Thriller", "Documentary"]
        i = 0
        for i in range(len(genres)):
            print(i)
            genre = genres[i]
            g = Genre(id = i, name = genre, description="")
            db.session.add(g)
            db.session.commit()
            i += 1

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    movie_desc = "84 years later, a 100 year-old woman named Rose DeWitt Bukater tells the story to her granddaughter Lizzy Calvert, Brock Lovett, Lewis Bodine, Bobby Buell and Anatoly Mikailavich on the Keldysh about her life set in April 10th 1912, on a ship called Titanic when young Rose boards the departing ship with the upper-class passengers and her mother, Ruth DeWitt Bukater, and her fiancé, Caledon Hockley. Meanwhile, a drifter and artist named Jack Dawson and his best friend Fabrizio De Rossi win third-class tickets to the ship in a game. And she explains the whole story from departure until the death of Titanic on its first and last voyage April 15th, 1912 at 2:20 in the morning."
    actor_desc = "Few actors in the world have had a career quite as diverse as Leonardo DiCaprio's. DiCaprio has gone from relatively humble beginnings, as a supporting cast member of the sitcom Growing Pains (1985) and low budget horror movies, such as Critters 3 (1991), to a major teenage heartthrob in the 1990s, as the hunky lead actor in movies such as Romeo + Juliet (1996) and Titanic (1997), to then become a leading man in Hollywood blockbusters, made by internationally renowned directors such as Martin Scorsese and Christopher Nolan."
    genre_desc = "Action movies are adrenaline-fueled spectacles known for their thrilling stunts, intense combat scenes, and fast-paced plots. Featuring heroic protagonists facing off against formidable foes, these films deliver non-stop excitement with explosive action sequences, daring escapes, and cutting-edge visual effects. From the iconic James Bond series to the epic battles of The Avengers, action movies offer an exhilarating cinematic experience that keeps audiences on the edge of their seats."
    if request.method == 'POST':
        default_value = ""
        movie_name = str(request.form.get('fMovie', default_value)).lower()
        actor_name = str(request.form.get('fActor', default_value)).lower()
        genre_name = str(request.form.get('fGenre', default_value)).lower()

        movie_query = db.session.execute(db.select(Movie).filter_by(name=movie_name))
        years = range(1980, 2024)
        movie_genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Science Fiction (Sci-Fi)", "Thriller", "Documentary"]
        
        if len(list(movie_query)) == 0:
            # insert it into the movie table
            movie = Movie(id = random.randint(1,100), name = movie_name, genre_id=movie_genres[random.randint(0, len(movie_genres) - 1)], year_released = 2000)
            db.session.add(movie)
            db.session.commit()
        
        # Update genre
        genre_query = select(Genre).where(Genre.name==genre_name)
        new_genre_id = db.session.execute(genre_query)
        print("Entered name: ", genre_name)
        print(val for val in list(db.session.execute(select(Genre))))

    return render_template('index.html', movie_description = movie_desc, actor_description = actor_desc, genre_description=genre_desc)

@app.route("/users/create/<int:id>/<string:email>", methods=["GET", "POST"])
def user_create(id, email):
    user = User(id=id,email=email, password="blah")
    db.session.add(user)
    try:
        db.session.commit()
        current_user = user
    except IntegrityError:
        db.session.rollback()
    return "Successfully added user!"




if __name__ == "__main__":
    # with app.app_context():
    #     initialize_tables()
    app.run(use_reloader=False)
