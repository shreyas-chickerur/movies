from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    movie_desc = "84 years later, a 100 year-old woman named Rose DeWitt Bukater tells the story to her granddaughter Lizzy Calvert, Brock Lovett, Lewis Bodine, Bobby Buell and Anatoly Mikailavich on the Keldysh about her life set in April 10th 1912, on a ship called Titanic when young Rose boards the departing ship with the upper-class passengers and her mother, Ruth DeWitt Bukater, and her fiancé, Caledon Hockley. Meanwhile, a drifter and artist named Jack Dawson and his best friend Fabrizio De Rossi win third-class tickets to the ship in a game. And she explains the whole story from departure until the death of Titanic on its first and last voyage April 15th, 1912 at 2:20 in the morning."
    actor_desc = "Few actors in the world have had a career quite as diverse as Leonardo DiCaprio's. DiCaprio has gone from relatively humble beginnings, as a supporting cast member of the sitcom Growing Pains (1985) and low budget horror movies, such as Critters 3 (1991), to a major teenage heartthrob in the 1990s, as the hunky lead actor in movies such as Romeo + Juliet (1996) and Titanic (1997), to then become a leading man in Hollywood blockbusters, made by internationally renowned directors such as Martin Scorsese and Christopher Nolan."
    genre_desc = "Action movies are adrenaline-fueled spectacles known for their thrilling stunts, intense combat scenes, and fast-paced plots. Featuring heroic protagonists facing off against formidable foes, these films deliver non-stop excitement with explosive action sequences, daring escapes, and cutting-edge visual effects. From the iconic James Bond series to the epic battles of The Avengers, action movies offer an exhilarating cinematic experience that keeps audiences on the edge of their seats."
    return render_template('index.html', movie_description = movie_desc, actor_description = actor_desc, genre_description=genre_desc)

if __name__ == "__main__":
    app.run(debug=True)
