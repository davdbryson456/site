from app import app, db
from flask import render_template, url_for, flash, redirect, request, abort
from app import mail
from flask_mail import Message
from app.forms import Signup, contactform, Login
from .models import Users
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, current_user, login_required,UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from . import login_manager
from werkzeug.security import check_password_hash

@app.route('/')
def home():

    return render_template('home.html')



@app.route('/about/')
def about():

    return render_template('about.html')


@app.route('/tutorials/')
@login_required
def tutorials():

    return render_template('tutorials.html')


@app.route('/books/')
def books():

    return render_template('books.html')



@app.route('/signup/', methods=["GET", "POST"])
def signup():

    signupForm = Signup()

    if request.method == 'POST' and signupForm.validate_on_submit():

        try:
            user = Users(signupForm.firstname.data, signupForm.lastname.data, signupForm.username.data, signupForm.password.data, signupForm.email.data)
            db.session.add(user)
            db.session.commit()

            flash('Successfully Registered', 'success')

            with mail.connect() as conn:

                msg = Message(subject="Welcome to HyperAcademics!", sender="davidbryson@hotmail.com",
                              recipients=[signupForm.email.data])

                body = ("Your Username is:"+" "+signupForm.username.data+"\n" +
                        "Please wait for admin approval before you are able to sign in")

                msg.body = (body)

                conn.send(msg)

        except IntegrityError:

            flash('The entered username is taken!','danger')



    return render_template('signup.html', signupForm = signupForm)



@app.route('/medicalsupplies/')
def medicalsupplies():

    return render_template('medicalsupplies.html')


@app.route('/resources/')
def resources():

    return render_template('resources.html')


@app.route('/contactus/', methods=["GET", "POST"])
def contactus():

    contact = contactform()

    if request.method == 'POST' and contact.validate_on_submit():

        with mail.connect() as conn:

            msg = Message(subject=contact.subject.data, sender="davidbryson@hotmail.com", recipients=["davidoliverbryson@gmail.com"])

            body = ("Name:"+" "+contact.name.data+"\n" +
                    "Email:"+" "+contact.email.data+"\n" +
                    "Message:"+" "+contact.message.data)

            msg.body = (body)


            conn.send(msg)


            flash('Message Sent','success')

            return redirect(url_for('home'))

    return render_template('contactus.html', contact = contact)






@app.route('/login/', methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    login = Login()
    if request.method == 'POST' and login.validate_on_submit():


        username = login.username.data
        password = login.password.data
        user = Users.query.filter_by(username=username).first()

        if user is not None and check_password_hash(user.password, password):

            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True

            login_user(user, remember=remember_me)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:

            flash('Username or Password is incorrect.', 'danger')
    return render_template('login.html', login=login)


@app.route('/logout/')
@login_required
def logout():

    logout_user()

    flash('You have been logged out.', 'danger')

    return redirect(url_for('home'))



@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class MyModelView (ModelView):  # add_view restriction
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)
    def not_auth(self):
        return "Not Authorized"


#Flask admin settings

admin = Admin(app)
admin.add_view(MyModelView(Users, db.session))