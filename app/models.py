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

    date_posted = db.Column(db.DateTime, nullable=False)

    content = db.Column(db.Text, nullable=False)

    user_fname = db.Column(db.String(100), nullable=False)

    user_lname = db.Column(db.String(100), nullable=False)

    photopath = db.Column(db.String(255), nullable=True)

    username = db.Column(db.String(255), nullable=False)

    comments = db.relationship('Comment', backref='post', lazy=True)


    def __init__(self, title, content, user_fname, user_lname, date_posted, photopath, username):

        self.title = title

        self.content = content

        self.user_fname = user_fname

        self.user_lname = user_lname

        self.date_posted = date_posted

        self.photopath = photopath

        self.username = username

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"




class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    body = db.Column(db.String(100), nullable=False)

    timestamp = db.Column(db.DateTime, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    first_n = db.Column(db.String(100), nullable=False)

    last_n = db.Column(db.String(100), nullable=False)

    def __init__(self, body, post_id, first_n, last_n, timestamp):

        self.body = body
        self.post_id = post_id
        self.first_n = first_n
        self.last_n = last_n
        self.timestamp = timestamp

    def __repr__(self):
        return f"Comment('{self.body}', '{self.timestamp}')"



class NewBook (db.Model):

    id = db.Column(db.Integer, primary_key=True)

    bookname = db.Column(db.String(150), nullable=False)

    author = db.Column(db.String(150), nullable=False)

    price = db.Column(db.Integer)

    photopath = db.Column(db.String(255), nullable=True)

    stock_status = db.Column(db.String(255), nullable=False)


    def __init__(self, bookname, author, price, photopath, stock_status):

        self.bookname = bookname
        self.author = author
        self.price = price
        self.photopath = photopath
        self.stock_status = stock_status

    def __repr__(self):

        return f"NewBook('{self.bookname}', '{self.price}')"




class UsedBook (db.Model):

    id = db.Column(db.Integer, primary_key=True)

    ubookname = db.Column(db.String(150), nullable=False)

    uauthor = db.Column(db.String(150), nullable=False)

    uprice = db.Column(db.Integer)

    uphotopath = db.Column(db.String(255), nullable=True)

    ustock_status = db.Column(db.String(255), nullable=False)


    def __init__(self, ubookname, uauthor, uprice, uphotopath, ustock_status):

        self.ubookname = ubookname
        self.uauthor = uauthor
        self.uprice = uprice
        self.uphotopath = uphotopath
        self.ustock_status = ustock_status


    def __repr__(self):
        return f"UsedBook('{self.ubookname}', '{self.uprice}')"



class Supplies (db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    price = db.Column(db.Integer)

    photopath = db.Column(db.String(255), nullable=True)

    stock_status = db.Column(db.String(255), nullable=False)


    def __init__(self, name, price, photopath, stock_status):

        self.name = name
        self.price = price
        self.photopath = photopath
        self.stock_status = stock_status


    def __repr__(self):
        return f"Supplies('{self.name}', '{self.price}')"



class Accessories(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    price = db.Column(db.Integer)

    photopath = db.Column(db.String(255), nullable=True)

    stock_status = db.Column(db.String(255), nullable=False)


    def __init__(self, name, price, photopath, stock_status):

        self.name = name
        self.price = price
        self.photopath = photopath
        self.stock_status = stock_status


    def __repr__(self):
        return f"Accessories('{self.name}', '{self.price}')"



class Orders (db.Model):

    id = db.Column(db.Integer, primary_key=True)

    custname = db.Column(db.String(150), nullable=False)

    ordernum = db.Column(db.Integer)

    order = db.Column(db.String(200), nullable=False)

    total = db.Column(db.Integer)


    def __init__(self, custname, ordernum, order, total):

        self.custname = custname
        self.ordernum = ordernum
        self.order = order
        self.total = total


    def __repr__(self):
        return f"Orders('{self.custname}', '{self.price}')"


class Homepage_pics (db.Model):

    id = db.Column(db.Integer, primary_key=True)

    pic_name = db.Column(db.String(255), nullable=False)

    caption = db.Column(db.String(255), nullable=True)

    def __init__(self, pic_name, caption):

        self.pic_name = pic_name
        self.caption = caption


    def __repr__(self):
        return f"Orders('{self.pic_name}', '{self.caption}')"