from flask import Flask, render_template, url_for, redirect, request
from models import *
from sqlalchemy.exc import IntegrityError
import random
from sqlalchemy import union_all, select, update


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = returnDB()
db.init_app(app)
global genres
global actors
global actor_descriptions
global movies
genres = {1: "Action", 2: "Comedy", 3: "Drama", 4: "Horror", 5: "Romance", 6: "Science Fiction (Sci-Fi)", 7: "Thriller", 8: "Documentary"}
actors = {1: "Tom Hanks", 2: "Leonardo DiCaprio", 3: "Meryl Streep", 4: "Brad Pitt", 5: "Jennifer Lawrence", 6: "Denzel Washington", 7: "Scarlett Johansson", 8: "Johnny Depp"}
actor_descriptions = {
    "Tom Hanks": "Known for his versatility and ability to portray a wide range of characters, Tom Hanks has starred in iconic roles in movies like Forrest Gump, Cast Away, and Saving Private Ryan.",
    "Leonardo DiCaprio": "Leonardo DiCaprio is known for his intense performances and has starred in numerous critically acclaimed films, including Titanic, Inception, and The Revenant, for which he won his first Oscar.",
    "Meryl Streep": "Considered one of the greatest actresses of her generation, Meryl Streep is known for her unmatched talent and has received numerous awards for her roles in films such as Sophie's Choice, The Iron Lady, and Kramer vs. Kramer.",
    "Brad Pitt": "Brad Pitt is known for his charm and versatility as an actor, with notable roles in movies like Fight Club, Inglourious Basterds, and Once Upon a Time in Hollywood, for which he won an Academy Award.",
    "Jennifer Lawrence": "Jennifer Lawrence rose to fame with her role in The Hunger Games series and has since proven her talent with performances in Silver Linings Playbook, American Hustle, and Joy, winning an Oscar for the former.",
    "Denzel Washington": "Denzel Washington is celebrated for his powerful performances and has received critical acclaim for roles in films such as Training Day, Malcolm X, and Fences, winning multiple Oscars throughout his career.",
    "Scarlett Johansson": "Scarlett Johansson is known for her versatility and has portrayed memorable characters in movies like Lost in Translation, The Avengers series, and Marriage Story, showcasing her range as an actress.",
    "Johnny Depp": "Johnny Depp is known for his eccentric and transformative roles, with notable performances in films such as Pirates of the Caribbean, Edward Scissorhands, and Sweeney Todd, earning him critical acclaim and a dedicated fanbase."
}
movie_descriptions = {
    "The Godfather": "The Godfather is a classic crime film directed by Francis Ford Coppola, known for its powerful performances, intricate storytelling, and iconic quotes. It follows the Corleone crime family and their rise to power in the mafia.",
    "The Shawshank Redemption": "The Shawshank Redemption, directed by Frank Darabont, is a drama film based on Stephen King's novella. It tells the story of Andy Dufresne, a banker who is wrongly convicted of murder and forms a bond with fellow inmate Red while serving his sentence in Shawshank State Penitentiary.",
    "Pulp Fiction": "Pulp Fiction, directed by Quentin Tarantino, is a non-linear crime film known for its eclectic dialogue, stylish direction, and memorable characters. The film weaves multiple interconnected stories involving two hitmen, a boxer, a mob boss, and others in the criminal underworld.",
    "Forrest Gump": "Forrest Gump, directed by Robert Zemeckis, is a heartwarming drama that follows the life of Forrest Gump, a kind-hearted and intellectually challenged man who unwittingly becomes involved in significant historical events spanning several decades.",
    "The Dark Knight": "The Dark Knight, directed by Christopher Nolan, is a superhero film that explores the gritty and complex world of Gotham City. It follows Batman as he faces off against the Joker, a chaotic and unpredictable criminal mastermind.",
    "Schindler's List": "Schindler's List, directed by Steven Spielberg, is a powerful historical drama based on the true story of Oskar Schindler, a German businessman who saved the lives of over a thousand Polish Jews during the Holocaust by employing them in his factories.",
    "Titanic": "Titanic, directed by James Cameron, is a romantic disaster film set against the backdrop of the ill-fated maiden voyage of the RMS Titanic. The film follows the romance between Jack and Rose, two passengers from different social classes, as they struggle to survive the sinking ship.",
    "Inception": "Inception, directed by Christopher Nolan, is a mind-bending science fiction thriller that explores the concept of dreams within dreams. The film follows a team of thieves who enter the dreams of their targets to steal valuable information."
}
genre_descriptions = {
    "Action": "Action movies typically involve high-energy sequences, often featuring physical stunts, chases, and combat. These films often focus on protagonists facing formidable challenges and overcoming them through strength, skill, or wit.",
    "Comedy": "Comedy movies aim to entertain and amuse audiences through humor and light-hearted storytelling. They often feature comedic situations, witty dialogue, and eccentric characters, with the primary goal of eliciting laughter.",
    "Drama": "Drama movies explore complex themes and emotions, often focusing on interpersonal relationships, societal issues, and human struggles. These films aim to evoke a range of emotions and provoke thought and introspection in viewers.",
    "Horror": "Horror movies are designed to frighten and unsettle audiences, often through elements of suspense, tension, and gore. They frequently feature supernatural or psychological themes, and their primary goal is to evoke fear and unease.",
    "Romance": "Romance movies center around love and relationships, often portraying the joys, conflicts, and challenges of romantic connections. These films typically feature heartfelt moments, passionate encounters, and themes of love conquering obstacles.",
    "Science Fiction (Sci-Fi)": "Science fiction movies explore speculative or futuristic concepts, often involving advanced technology, space exploration, or alternate realities. These films can delve into philosophical questions and imaginative scenarios beyond the boundaries of current scientific understanding.",
    "Thriller": "Thriller movies are characterized by suspenseful and gripping narratives, often involving intense action, mystery, or danger. They aim to keep audiences on the edge of their seats, building tension and excitement throughout the story.",
    "Documentary": "Documentary films present factual accounts of real-life subjects, events, or issues. They aim to inform, educate, or raise awareness about a particular topic, often through interviews, archival footage, and investigative journalism."
}


movies = {1: "The Godfather", 2: "The Shawshank Redemption", 3: "Pulp Fiction", 4: "Forrest Gump", 5: "The Dark Knight", 6: "Schindler's List", 7: "Titanic", 8: "Inception"}



def initialize_tables():
    # Genres Table
    
        for index in genres:
            g = Genre(id = index, name = genres[index], description=genre_descriptions[genres[index]])
            db.session.add(g)
            db.session.commit()

        for index in actors:
            a = Actor(id = index, name = actors[index], description=actor_descriptions[actors[index]])
            db.session.add(a)
            db.session.commit()
        
        for index in movies:
            m = Movie(id = index, name = movies[index], genre_id = genres[index], year_released=random.randint(2000, 2024), description = movie_descriptions[movies[index]])
            db.session.add(m)
            db.session.commit()

        current_user = User(id = 0, email = "shreyas.sample@notreal.com", password = "")
        db.session.add(current_user)
        db.session.commit()

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    movie_desc = "84 years later, a 100 year-old woman named Rose DeWitt Bukater tells the story to her granddaughter Lizzy Calvert, Brock Lovett, Lewis Bodine, Bobby Buell and Anatoly Mikailavich on the Keldysh about her life set in April 10th 1912, on a ship called Titanic when young Rose boards the departing ship with the upper-class passengers and her mother, Ruth DeWitt Bukater, and her fiancé, Caledon Hockley. Meanwhile, a drifter and artist named Jack Dawson and his best friend Fabrizio De Rossi win third-class tickets to the ship in a game. And she explains the whole story from departure until the death of Titanic on its first and last voyage April 15th, 1912 at 2:20 in the morning."
    actor_desc = "Few actors in the world have had a career quite as diverse as Leonardo DiCaprio's. DiCaprio has gone from relatively humble beginnings, as a supporting cast member of the sitcom Growing Pains (1985) and low budget horror movies, such as Critters 3 (1991), to a major teenage heartthrob in the 1990s, as the hunky lead actor in movies such as Romeo + Juliet (1996) and Titanic (1997), to then become a leading man in Hollywood blockbusters, made by internationally renowned directors such as Martin Scorsese and Christopher Nolan."
    genre_desc = "Action movies are adrenaline-fueled spectacles known for their thrilling stunts, intense combat scenes, and fast-paced plots. Featuring heroic protagonists facing off against formidable foes, these films deliver non-stop excitement with explosive action sequences, daring escapes, and cutting-edge visual effects. From the iconic James Bond series to the epic battles of The Avengers, action movies offer an exhilarating cinematic experience that keeps audiences on the edge of their seats."
    userRows = db.session.query(User).count()
    movieRows = db.session.query(Movie).count()
    actorRows = db.session.query(Actor).count()
    genreRows = db.session.query(Genre).count()

    if request.method == 'POST':
        default_value = ""
        # movie
        movie_name = None
        actor_name = None
        genre_name = None

        #Determines if there is an existent movie selected - if not, create a new movie and set the current user's favorite movie to the new id for that movie
        if request.form.get('fMovieDrop'):
            db.session.query(User).update({User.favorite_movie_id: request.form.get('fMovieDrop')})
            db.session.commit()
        if request.form.get('fMovie'):
            # create a new movie
            movie_name = str(request.form.get('fMovie', default_value)).lower()
            m = Movie(id = movieRows + 1, name = str(request.form.get('fMovie', default_value)).lower(), genre_id = genres[random.randint(1, 8)], year_released=random.randint(2000, 2024), description = "")
            db.session.add(m)
            db.session.query(User).update({User.favorite_movie_id: m.id})
            db.session.commit()
            movies[len(movies) + 1] = str(request.form.get('fMovie', default_value)).lower()

        #Determines if there is an existent actor selected - if not, create a new actor and set the current user's favorite actor to the new id for that actor
        if request.form.get('fActorDrop'):
            db.session.query(User).update({User.favorite_actor_id: request.form.get('fActorDrop')})
            db.session.commit()
        if request.form.get('fActor'):
            actor_name = str(request.form.get('fActor', default_value)).lower()
            a = Actor(id = actorRows + 1, name = str(request.form.get('fActor', default_value)).lower(), description = "")
            db.session.add(a)
            db.session.query(User).update({User.favorite_actor_id: a.id})
            db.session.commit()
            actors[len(actors) + 1] = str(request.form.get('fActor', default_value)).lower()
            
        #Determines if there is an existent genre selected - if not, create a new genre and set the current user's favorite genre to the new id for that genre
        if request.form.get('fGenreDrop'):
            db.session.query(User).update({User.favorite_genre_id: request.form.get('fGenreDrop')})
            db.session.commit()
        if request.form.get('fGenre'):  
            genre_name = str(request.form.get('fGenre', default_value)).lower()
            g = Genre(id = genreRows + 1, name = str(request.form.get('fGenre', default_value)).lower(), description = "")
            db.session.add(g)
            db.session.query(User).update({User.favorite_genre_id: g.id})
            db.session.commit()
            genres[len(genres) + 1] = str(request.form.get('fGenre', default_value)).lower()

    return render_template('index.html', movie_description = movie_desc, actor_description = actor_desc, genre_description=genre_desc, movie_names = movies, genre_names = genres, actor_names = actors)




if __name__ == "__main__":
    # with app.app_context():
    #     initialize_tables()
    app.run(use_reloader=False)
