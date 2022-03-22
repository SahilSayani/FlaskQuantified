from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 
# db.Model is a table essentially -> is the model of a table
#flask login has UserMixin which allows users to login and out easily
class User(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(150) ,unique=True)
    username=db.Column(db.String(150) ,unique=True)
    password = db.Column(db.String(150))
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    posts = db.relationship('Post', backref='user',passive_deletes=True)
    logs=db.relationship('Log', backref='users',passive_deletes=True)

class Post(db.Model): 
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.Text, nullable=False)
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    author=db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    tracker_type = db.Column(db.String(150))
    

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(150))
    notes = db.Column(db.String(150))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    added_date_time = db.Column(db.String(150))