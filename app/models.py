from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
import datetime


class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(80))

    last_name = db.Column(db.String(80))

    username = db.Column(db.String(80), unique=True)

    password = db.Column(db.String(255))

    email = db.Column(db.String(255))

    is_admin = db.Column(db.Boolean, default=False)

    is_authorized = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, username, password, email):

        self.first_name = first_name

        self.last_name = last_name

        self.username = username

        self.email = email

        self.password = generate_password_hash(password, method='pbkdf2:sha256')



    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:

            return unicode(self.id)  # python 2 support

        except NameError:

            return str(self.id)  # python 3 support

    def __repr__(self):

        return '<User %r>' % self.username



class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now().strftime("%d-%m-%y %H:%M"))

    content = db.Column(db.Text, nullable=False)

    user_fname = db.Column(db.String(100), nullable=False)

    user_lname = db.Column(db.String(100), nullable=False)

    comments = db.relationship('Comment', backref='post', lazy=True)


    def __init__(self, title, content, user_fname, user_lname):

        self.title = title

        self.content = content

        self.user_fname = user_fname

        self.user_lname = user_lname


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"




class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    body = db.Column(db.String(100), nullable=False)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now().strftime("%d-%m-%y %H:%M"))

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    first_n = db.Column(db.String(100), nullable=False)

    last_n = db.Column(db.String(100), nullable=False)

    def __init__(self, body, post_id, first_n, last_n):

        self.body = body
        self.post_id = post_id
        self.first_n = first_n
        self.last_n = last_n

    def __repr__(self):
        return f"Comment('{self.body}', '{self.timestamp}')"