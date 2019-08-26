from flask import Flask , session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail



app = Flask(__name__)

# database settings
app.config['SECRET_KEY'] = "su93rs3cr3tk3y"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:davdbryson456@localhost/userdata"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # added just to suppress a warning
db = SQLAlchemy(app)

# Mail server settings
app.config['MAIL_SERVER'] = 'mail.hyperacademics.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'noreply@hyperacademics.com'
app.config['MAIL_PASSWORD'] = ']?^<5:ZsT.BMv'
mail = Mail(app)


# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"
login_manager.refresh_view = 'relogin'
login_manager.needs_refresh_message = "Session timed out, please re-login"
login_manager.needs_refresh_message_category = "info"



app.config.from_object(__name__)

# uploads config
app.config['UPLOAD_FOLDER'] = "./app/static/uploads"





# add upload folder configs that were in youtube video
from app import views
