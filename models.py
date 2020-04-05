import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

# database_name = "casting-agency"
# database_path = "postgres://postgres:stemed@{}/{}".format('localhost:5432', database_name)
database_path = "postgres://tgexvitobdprbf:18954e553e1fd53808b4cd709a0be8b0731386bf9f3ce8c3b942229d7f546654@ec2-52-87-58-157.compute-1.amazonaws.com:5432/d4cc456dat9e30"

db = SQLAlchemy()
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(50), nullable=False)
    release_date = Column(db.String(4), nullable=False)
    
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
