from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def returnDB():
    return db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    favorite_movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    favorite_genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    favorite_actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))

class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    year_released = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)

class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(150), unique=False, nullable=False)

class ActingJob(db.Model):
    __tablename__ = "actingJob"
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    
class Actor(db.Model):
    __tablename__="actor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(150), unique=False, nullable=False)

