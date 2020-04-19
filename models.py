from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "capstone"
database_path = "postgres://{}@{}/{}".format(
    'akira', 'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Movie
Have title and release year
'''


class Movie(db.Model):
    # Define the name of Movie table
    __tablename__ = 'movies'

    # Define the attributes
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_year = Column(Integer)

    # Define a relationship to join with actors table
    actors = db.relationship('Actor', backref='movies')

    # Add data
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Update data
    def update(self):
        db.session.commit()

    # Delete data
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # Format data
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year
        }


'''
Actor
Have name, age and gender
'''


class Actor(db.Model):
    # Define the name of Actor table
    __tablename__ = 'actors'

    # Define the attributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    # Define a foreign key for joining movies table
    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.id'))

    # Add data
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Update data
    def update(self):
        db.session.commit()

    # Delete data
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # format data
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }
