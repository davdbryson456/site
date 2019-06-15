from app import app
from flask import render_template,url_for


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


@app.route('/contactus/')
def contactus():

    return render_template('contactus.html')


@app.route('/login/')
def login():

    return render_template('login.html')