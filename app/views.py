import os
from app import app, db
from flask import render_template, url_for, flash, redirect, request, abort, session
from app import mail
from flask_mail import Message
from app.forms import Signup, contactform, Login, Uploadvids, _Post, _Comment, Add_newbook, Add_usedbook, Add_supplies, Add_accessories, addtocart, Deletepost, Deletevids, Homepage
from .models import Users, Post, Comment, NewBook, UsedBook, Supplies, Accessories, Orders, Homepage_pics
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, current_user, login_required,UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from . import login_manager
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta
from time import ctime


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/', methods=["GET", "POST"])
def home():

    homeform = Homepage()

    if request.method == 'POST' and homeform.validate_on_submit():

        pic = homeform.pic.data
        picname = pic.filename
        caption = homeform.caption.data

        target = os.path.join(APP_ROOT, 'static/homepage_pics/')

        if not os.path.isdir(target):
            os.mkdir(target)

        pic.save("/".join([target, picname]))

        newpic = Homepage_pics(picname, caption)

        db.session.add(newpic)
        db.session.commit()
        flash('Added!', 'success')

        return redirect(url_for('home'))


    def get_pics():

        allpics = db.session.query(Homepage_pics).all()
        return allpics

    all_pics = get_pics()

    return render_template('home.html', homeform=homeform, all_pics=all_pics)



@app.route('/about/')
def about():

    return render_template('about.html')


@app.route('/tutorials/', methods=["GET", "POST"])
@login_required
def tutorials():

    if current_user.is_authorized == True:

        dele = Deletevids()

        if request.method == 'POST' and dele.validate_on_submit():

            vidname = dele.vid_name.data

            target = os.path.join(APP_ROOT, 'static/tutorial_vids/')

            os.remove("/".join([target, vidname]))

            flash('Video Deleted!', 'success')

            return redirect(url_for('tutorials'))

        videos = get_uploaded_videos()

        return render_template('tutorials.html', videos=videos, dele=dele)

    else:

        flash('You require admin approval to view this page !', 'info')
        return redirect(url_for('home'))




@app.route('/hyperdiscussons/', methods=["GET", "POST"])
@login_required
def hyperdiscussons():

    post = _Post()
    comment = _Comment()
    delete = Deletepost()

    # POST SECTION  ####################################################################################

    if request.method == 'POST' and post.validate_on_submit():


        if is_filled(post.picture.data) == True:

            target = os.path.join(APP_ROOT, 'static/post_photos/')

            if not os.path.isdir(target):
                os.mkdir(target)

            photo = post.picture.data
            photoname = photo.filename
            photo.save("/".join([target, photoname]))

            timestamp = ctime()
            newpost = Post(post.title.data, post.content.data, current_user.first_name, current_user.last_name, timestamp, photoname, current_user.username)
            db.session.add(newpost)
            db.session.commit()
            flash('Posted!', 'success')
            return redirect(url_for('hyperdiscussons'))

        else:

            timestamp = ctime()

            photoname = None
            newpost = Post(post.title.data, post.content.data, current_user.first_name, current_user.last_name, timestamp, photoname, current_user.username)
            db.session.add(newpost)
            db.session.commit()
            flash('Posted!', 'success')
            return redirect(url_for('hyperdiscussons'))



    # COMMENT SECTION  ###############################################################################################3
    if request.method == 'POST' and comment.validate_on_submit():

        time = ctime()

        newcomment = Comment(comment.body.data, comment.post_id.data, current_user.first_name, current_user.last_name, time)
        db.session.add(newcomment)
        db.session.commit()
        flash('Posted!', 'success')
        return redirect(url_for('hyperdiscussons'))


    content = get_posts()
    return render_template('hyperdiscussons.html', post=post, content=content, comment=comment, delete=delete)



def get_posts():

    posts = db.session.query(Post).all()
    return posts




@app.route('/deletepost/', methods=["GET", "POST"])
@login_required
def deletepost():

    delete = Deletepost()

    # DELETE POST SECTION ############################################################################################3
    if request.method == 'POST' and delete.validate_on_submit():

        post_ident = delete.postId.data
        picture_path = delete.pic_name.data

        if is_filled(picture_path) == True:
            target = os.path.join(APP_ROOT, 'static/post_photos/')

            os.remove("/".join([target, picture_path]))

        del_post = Post.query.filter_by(id=post_ident).first()
        del_comments = Comment.query.filter_by(post_id=post_ident).all()

        for i in del_comments:
            db.session.delete(i)
            db.session.commit()

        db.session.delete(del_post)
        db.session.commit()

        flash('Post Deleted!', 'success')
        return redirect(url_for('hyperdiscussons'))





@app.route('/eShop/', methods=["GET", "POST"])
def eShop():

    def get_newbooks():

        post = db.session.query(NewBook).all()
        return post

    def get_usedBooks():

        post = db.session.query(UsedBook).all()
        return post


    def get_supplies():

        post = db.session.query(Supplies).all()
        return post

    def get_accessories():

        post = db.session.query(Accessories).all()
        return post


    newbooks = get_newbooks()
    usedbooks = get_usedBooks()
    supplies = get_supplies()
    accessories = get_accessories()

    item = addtocart()  # add to cart form

    #if request.method == 'POST' and item.validate_on_submit(): #this is for the add to cart button






    return render_template('eShop.html', newbooks=newbooks, usedbooks=usedbooks, supplies=supplies, accessories=accessories, item=item)




@app.route('/addstock/', methods=["GET", "POST"])
@login_required
def addstock():

    if current_user.is_admin:

        Nbook = Add_newbook()
        Ubook = Add_usedbook()
        supply = Add_supplies()
        acc = Add_accessories()

        if request.method == 'POST' and Nbook.validate_on_submit():

            bname = Nbook.bookname.data
            bauthor = Nbook.author.data
            bprice = Nbook.price.data
            npicture = Nbook.picture.data
            npicture_name = npicture.filename
            stock_status = "In Stock"

            target = os.path.join(APP_ROOT, 'static/newbook_pics/')

            if not os.path.isdir(target):
                os.mkdir(target)

            npicture.save("/".join([target, npicture_name]))

            new_book = NewBook(bname, bauthor, bprice, npicture_name, stock_status)

            db.session.add(new_book)
            db.session.commit()
            flash('Stock Added!', 'success')
            return redirect(url_for('addstock'))




        if request.method == 'POST' and Ubook.validate_on_submit():

            cname = Ubook.ubookname.data
            cauthor = Ubook.uauthor.data
            cprice = Ubook.uprice.data
            cpicture = Ubook.upicture.data
            cpicture_name = cpicture.filename
            stock_status = "In Stock"

            target = os.path.join(APP_ROOT, 'static/usedbook_pics/')

            if not os.path.isdir(target):
                os.mkdir(target)

            cpicture.save("/".join([target, cpicture_name]))

            used_book = UsedBook(cname, cauthor, cprice, cpicture_name, stock_status)

            db.session.add(used_book)
            db.session.commit()
            flash('Stock Added!', 'success')
            return redirect(url_for('addstock'))



        if request.method == 'POST' and supply.validate_on_submit():

            sname = supply.supplyname.data
            sprice = supply.price.data
            stock_status = "In Stock"
            spicture = supply.picture.data
            spicture_name = spicture.filename

            target = os.path.join(APP_ROOT, 'static/supplies_pics/')

            if not os.path.isdir(target):
                os.mkdir(target)

            spicture.save("/".join([target, spicture_name]))

            new_supply = Supplies(sname, sprice, spicture_name, stock_status)

            db.session.add(new_supply)
            db.session.commit()
            flash('Stock Added!', 'success')
            return redirect(url_for('addstock'))


        if request.method == 'POST' and acc.validate_on_submit():

            ename = acc.accname.data
            eprice = acc.price.data
            stock_status = "In Stock"
            epicture = acc.picture.data
            epicture_name = epicture.filename

            target = os.path.join(APP_ROOT, 'static/accessory_pics/')

            if not os.path.isdir(target):
                os.mkdir(target)

            epicture.save("/".join([target, epicture_name]))

            new_accessory = Accessories(ename, eprice, epicture_name, stock_status)

            db.session.add(new_accessory)
            db.session.commit()
            flash('Stock Added!', 'success')
            return redirect(url_for('addstock'))



        return render_template('addstock.html', Nbook=Nbook, Ubook=Ubook, supply=supply, acc=acc)

    else:

        return redirect(url_for('home'))



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
                        "Please wait for admin approval before you are able to sign in.")

                msg.body = (body)

                conn.send(msg)

        except IntegrityError:

            flash('The entered username is taken!', 'danger')



    return render_template('signup.html', signupForm=signupForm)




@app.route('/resources/')
def resources():

    return render_template('resources.html')


@app.route('/contactus/', methods=["GET", "POST"])
def contactus():

    contact = contactform()

    if request.method == 'POST' and contact.validate_on_submit():

        with mail.connect() as conn:

            msg = Message(subject=contact.subject.data, sender=contact.email.data, recipients=["davidoliverbryson@gmail.com"])

            body = ("Name:"+" "+contact.name.data+"\n" +
                    "Email:"+" "+contact.email.data+"\n" +
                    "Message:"+" "+contact.message.data)

            msg.body = (body)


            conn.send(msg)


            flash('Message Sent', 'success')

            return redirect(url_for('home'))

    return render_template('contactus.html', contact=contact)




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
            #print(user.is_authorized)
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


@app.route('/uploads/', methods=['POST', 'GET'])
@login_required
def uploads():

    if current_user.is_admin == True:

        uploads = Uploadvids()

        if request.method == 'POST' and uploads.validate_on_submit():

            target = os.path.join(APP_ROOT, 'static/tutorial_vids/')

            if not os.path.isdir(target):
                os.mkdir(target)

            video = uploads.video.data
            videoname = secure_filename(video.filename)

            video.save("/".join([target, videoname]))
            flash('File Saved', 'success')
            return redirect(url_for('home'))

        return render_template('uploads.html', uploads=uploads)

    else:
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


@app.before_request
def before_request():
    session.permanent = False
    app.permanent_session_lifetime = timedelta(minutes=60)


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


def get_uploaded_videos():
    rootdir = os.getcwd()
    filenames = []
    for subdir, dirs, files in os.walk(rootdir + './app/static/tutorial_vids'):
	    for file in files:
             filenames.append(os.path.join( file).split('/')[-1])
    return filenames




class MyModelView (ModelView):  # add_view restriction
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)

    def not_auth(self):
        return "Not Authorized"



def is_filled(data):
   if data == None:
      return False
   if data == '':
      return False
   if data == []:
      return False
   if data =='None':
       return False
   return True

#Flask admin settings

admin = Admin(app)

admin.add_view(MyModelView(Users, db.session))
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(Comment, db.session))
admin.add_view(MyModelView(NewBook, db.session))
admin.add_view(MyModelView(UsedBook, db.session))
admin.add_view(MyModelView(Supplies, db.session))
admin.add_view(MyModelView(Accessories, db.session))
admin.add_view(MyModelView(Orders, db.session))
admin.add_view(MyModelView(Homepage_pics, db.session))