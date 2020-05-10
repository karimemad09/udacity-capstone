import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()

'''
setup_db(app)
...binds a flask application and a SQLAlchemy service

'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

    migrate = Migrate(app, db)


###########################
# ACTORS IN MOVIES RELATION Many to Many MODEL #
##########################
# actors_movies = db.Table('actors_movies',
#                          db.Column('actor_id', db.Integer,
#                                    db.ForeignKey('actors.id')),
#                          db.Column('movie_id', db.Integer,
#                                    db.ForeignKey('movies.id'))
#                          )

########################
# ACTOR MODEL
#################


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(), nullable=False)
    # actor_in_movies = db.relationship(
    #     'Movie', secondary=actors_movies, backref=db.backref('movies_actors',
    #                                                          lazy='dynamic'))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }


#################
# MOVIE MODEL
####################
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, title):
        self.title = title

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }
