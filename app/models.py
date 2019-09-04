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

    year = db.Column(db.String(255))

    def __init__(self, first_name, last_name, username, password, email, year):

        self.first_name = first_name

        self.last_name = last_name

        self.username = username

        self.email = email

        self.password = generate_password_hash(password, method='pbkdf2:sha256')

        self.year = year


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

    publisher = db.Column(db.String(150), nullable=False)

    price = db.Column(db.Integer)

    photopath = db.Column(db.String(255), nullable=True)

    stock_status = db.Column(db.String(255), nullable=False)

    ISBN13 = db.Column(db.String(255), nullable=False)

    ISBN10 = db.Column(db.String(255), nullable=False)

    series = db.Column(db.String(255), nullable=False)

    Format = db.Column(db.String(255), nullable=False)

    publication_date = db.Column(db.String(255), nullable=False)

    dimensions = db.Column(db.String(255), nullable=False)

    language = db.Column(db.String(255), nullable=False)

    weight = db.Column(db.String(255), nullable=False)

    description = db.Column(db.String(255), nullable=False)



    def __init__(self, bookname, publisher, price, photopath, stock_status, ISBN13, ISBN10, series, Format, publication_date, dimensions, language, weight, description):

        self.bookname = bookname
        self.publisher = publisher
        self.price = price
        self.photopath = photopath
        self.stock_status = stock_status
        self.ISBN13 = ISBN13
        self.ISBN10 = ISBN10
        self.series = series
        self.Format = Format
        self.publication_date = publication_date
        self.dimensions = dimensions
        self.language = language
        self.weight = weight
        self.description = description

    def __repr__(self):

        return f"NewBook('{self.bookname}', '{self.price}')"






class UsedBook (db.Model):

    id = db.Column(db.Integer, primary_key=True)

    ubookname = db.Column(db.String(150), nullable=False)

    uauthor = db.Column(db.String(150), nullable=False)

    uprice = db.Column(db.Integer)

    uphotopath = db.Column(db.String(255), nullable=True)

    ustock_status = db.Column(db.String(255), nullable=False)

    uISBN13 = db.Column(db.String(255), nullable=False)

    uISBN10 = db.Column(db.String(255), nullable=False)

    uuseries = db.Column(db.String(255), nullable=False)

    uFormat = db.Column(db.String(255), nullable=False)

    upublication_date = db.Column(db.String(255), nullable=False)

    udimensions = db.Column(db.String(255), nullable=False)

    ulanguage = db.Column(db.String(255), nullable=False)

    uweight = db.Column(db.String(255), nullable=False)

    udescription = db.Column(db.String(255), nullable=False)


    def __init__(self, ubookname, uauthor, uprice, uphotopath, ustock_status, uISBN13, uISBN10, uuseries, uFormat, upublication_date, udimensions, ulanguage, uweight, udescription):

        self.ubookname = ubookname
        self.uauthor = uauthor
        self.uprice = uprice
        self.uphotopath = uphotopath
        self.ustock_status = ustock_status
        self.uISBN13 = uISBN13
        self.uISBN10 = uISBN10
        self.uuseries = uuseries
        self.uFormat = uFormat
        self.upublication_date = upublication_date
        self.udimensions = udimensions
        self.ulanguage = ulanguage
        self.uweight = uweight
        self.udescription = udescription


    def __repr__(self):
        return f"UsedBook('{self.ubookname}', '{self.uprice}')"



class Supplies (db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    price = db.Column(db.Integer)

    photopath = db.Column(db.String(255), nullable=True)

    stock_status = db.Column(db.String(255), nullable=False)

    description = db.Column(db.String(255), nullable=False)

    def __init__(self, name, price, photopath, stock_status, description):

        self.name = name
        self.price = price
        self.photopath = photopath
        self.stock_status = stock_status
        self.description = description


    def __repr__(self):
        return f"Supplies('{self.name}', '{self.price}')"



class Accessories(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    price = db.Column(db.Integer)

    photopath = db.Column(db.String(255), nullable=True)

    stock_status = db.Column(db.String(255), nullable=False)

    description = db.Column(db.String(255), nullable=False)

    def __init__(self, name, price, photopath, stock_status, description):

        self.name = name
        self.price = price
        self.photopath = photopath
        self.stock_status = stock_status
        self.description = description

    def __repr__(self):
        return f"Accessories('{self.name}', '{self.price}')"



class Orders (db.Model):

    id = db.Column(db.Integer, primary_key=True)

    custfname = db.Column(db.String(150), nullable=False)

    custlname = db.Column(db.String(150), nullable=False)

    phonenum = db.Column(db.String(200), nullable=False)

    total = db.Column(db.Integer)

    date = db.Column(db.DateTime, nullable=False)

    pay_option = db.Column(db.String(150), nullable=False)


    def __init__(self, custfname, custlname, phonenum, total, date, pay_option):

        self.custfname = custfname
        self.custlname = custlname
        self.phonenum = phonenum
        self.total = total
        self.date = date
        self.pay_option = pay_option


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




class News(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    n_title = db.Column(db.String(255), nullable=False)

    n_Dateposted = db.Column(db.DateTime, nullable=False)

    n_content = db.Column(db.Text, nullable=False)

    userfname = db.Column(db.String(100), nullable=False)

    userlname = db.Column(db.String(100), nullable=False)

    photopath = db.Column(db.String(255), nullable=True)

    n_username = db.Column(db.String(255), nullable=False)

    def __init__(self, n_title, n_content, userfname, userlname, n_Dateposted, photopath, n_username):

        self.n_title = n_title

        self.n_content = n_content

        self.userfname = userfname

        self.userlname = userlname

        self.n_Dateposted = n_Dateposted

        self.photopath = photopath

        self.n_username = n_username




    def __repr__(self):
        return f"Post('{self.n_title}', '{self.n_Dateposted}')"




class Filename (db.Model):

    id = db.Column(db.Integer, primary_key=True)

    file_name = db.Column(db.String(255), nullable=False)

    def __init__(self, file_name):

        self.file_name = file_name


    def __repr__(self):
        return f"Filename('{self.file_name}')"



class Cart(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(150), nullable=False)

    item_name = db.Column(db.String(150), nullable=False)

    price = db.Column(db.Integer)

    qty = db.Column(db.Integer)

    def __init__(self, username, item_name, price, qty):

        self.username = username
        self.item_name = item_name
        self.qty = qty
        self.price = int(price)*int(qty)


    def __repr__(self):
        return f"Cart('{self.item_name}')"