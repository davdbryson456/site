from app import app
from flask import render_template, url_for, flash, redirect
from app import mail
from flask_mail import Message
from app.forms import contactform

@app.route('/')
def home():

    return render_template('home.html')



@app.route('/about/')
def about():

    return render_template('about.html')


@app.route('/tutorials/')
def tutorials():

    return render_template('tutorials.html')


@app.route('/books/')
def books():

    return render_template('books.html')


@app.route('/medicalsupplies/')
def medicalsupplies():

    return render_template('medicalsupplies.html')


@app.route('/resources/')
def resources():

    return render_template('resources.html')


@app.route('/contactus/', methods=["GET", "POST"])
def contactus():

    contact = contactform()

    if contact.validate_on_submit():

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

    return render_template('login.html')



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