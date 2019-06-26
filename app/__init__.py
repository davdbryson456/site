from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = "su93rs3cr3tk3y"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:davdbryson456@localhost/userdata"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # added just to suppress a warning

db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
#app.config['MAIL_DEFAULT_SENDER'] = ('David','davidbryson@hotmail.com')
app.config['MAIL_USERNAME'] = 'davidbryson@hotmail.com'
app.config['MAIL_PASSWORD'] = 'davdbryson7536'
mail = Mail(app)



app.config.from_object(__name__)

from app import views
