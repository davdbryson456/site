import os
import uuid
from app import app, db
from flask import render_template, url_for, flash, redirect, request, abort, session
from app import mail
from flask_mail import Message
from app.forms import Signup, contactform, Login, onevids, _Post, _Comment, Add_newbook, Add_usedbook, Add_supplies, Add_accessories, addtocart,\
    Deletepost, Deletevids, Homepage, Resources, resources_del, resource_files, file_del, eshop_del, cartt_del, checkoutt, year2vids, year3vids, Deletevids2, Deletevids3

from .models import Users, Post, Comment, NewBook, UsedBook, Supplies, Accessories, Orders, Homepage_pics, News, Filename, Cart, one_vids, two_vids, three_vids
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
        dele2 = Deletevids2()
        dele3 = Deletevids3()

        if dele.validate_on_submit():

            target = os.path.join(APP_ROOT, 'static/year1_vids/')

            os.remove("/".join([target, dele.vid_name.data]))

            del_post = one_vids.query.filter_by(id=dele.p_id.data).first()

            db.session.delete(del_post)
            db.session.commit()

            flash('Video Deleted!', 'success')

            return redirect(url_for('tutorials'))





        videos = db.session.query(one_vids).all()
        videos2 = db.session.query(two_vids).all()
        videos3 = db.session.query(three_vids).all()

        return render_template('tutorials.html', videos=videos, dele=dele, dele2=dele2, videos2=videos2, videos3=videos3 , dele3=dele3)

    else:

        flash('You require admin approval to view this page !', 'info')
        return redirect(url_for('home'))



@app.route('/dele2/', methods=["GET", "POST"])
@login_required
def dele2():

    dele2 = Deletevids2()

    if dele2.validate_on_submit():
        target2 = os.path.join(APP_ROOT, 'static/year2_vids/')

        os.remove("/".join([target2, dele2.vid_name2.data]))

        del_post = two_vids.query.filter_by(id=dele2.p_id2.data).first()

        db.session.delete(del_post)
        db.session.commit()

        flash('Video Deleted!', 'success')

        return redirect(url_for('tutorials'))


@app.route('/dele3/', methods=["GET", "POST"])
@login_required
def dele3():

    dele3 = Deletevids3()

    if dele3.validate_on_submit():

        target3 = os.path.join(APP_ROOT, 'static/year3_vids/')

        os.remove("/".join([target3, dele3.vid_name3.data]))

        del_post = three_vids.query.filter_by(id=dele3.p_id3.data).first()

        db.session.delete(del_post)
        db.session.commit()

        flash('Video Deleted!', 'success')

        return redirect(url_for('tutorials'))



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



@app.route('/eShop/', methods=["GET", "POST"])
@login_required
def eShop():

    items = addtocart()  # add to cart form
    eshop = eshop_del()


    newbooks = get_newbooks()
    usedbooks = get_usedBooks()
    supplies = get_supplies()
    accessories = get_accessories()


    if request.method == 'POST':

        itemname = items.product_name.data
        itemqty = items.qty.data
        itemprice = items.item_price.data



        newitem = Cart(current_user.username, itemname, itemprice, itemqty)
        db.session.add(newitem)
        db.session.commit()

        flash('Added to cart!', 'success')
        return redirect(url_for('eShop'))


    return render_template('eShop.html', newbooks=newbooks, usedbooks=usedbooks, supplies=supplies, accessories=accessories, items=items, eshop=eshop)





@app.route('/cart/', methods=["GET", "POST"])
@login_required
def cart():

    cart = cartt_del()

    cart_items = Cart.query.filter_by(username=current_user.username).all()

    return render_template('cart.html', cart_items=cart_items, cart=cart)





@app.route('/cart_del/', methods=["GET", "POST"])
@login_required
def cart_del():

    cart = cartt_del()

    if request.method == 'POST' and cart.validate_on_submit():

        del_item = Cart.query.filter_by(id=cart.cart_id.data).first()

        db.session.delete(del_item)
        db.session.commit()

        return redirect(url_for('cart'))






@app.route('/checkout/', methods=["GET", "POST"])
@login_required
def checkout():
    payment = checkoutt()

    cart_stuff = Cart.query.filter_by(username=current_user.username).all()

    if request.method == 'POST':

        if cart_stuff ==[]:

            flash('Your cart is empty', 'danger')
        else:
            return render_template('checkout.html', cart_stuff=cart_stuff, payment=payment)

    return redirect(url_for('eShop'))



@app.route('/placeorder/', methods=["GET", "POST"])
@login_required
def placeorder():

    if request.method == 'POST':

        payment = checkoutt()
        pay_options = payment.payment.data
        phone_num = payment.phone_num.data
        total = payment.total.data
        firstname = current_user.first_name
        lastname = current_user.last_name

        cart_stuff = Cart.query.filter_by(username=current_user.username).all()


        with mail.connect() as conn:
            msg = Message(subject="New Order!", sender="noreply@hyperacademics.com", recipients=["davidbryson@hotmail.com"])

            msg.html = render_template('neworder.html', cart_stuff=cart_stuff, total=total, pay_options=pay_options,
                                           phone_num=phone_num, firstname=firstname, lastname=lastname)

            conn.send(msg)


        with mail.connect() as conn:
            msg = Message(subject="Order Confirmation", sender="noreply@hyperacademics.com", recipients=[current_user.email])

            msg.html = render_template('custconfirm.html', cart_stuff=cart_stuff, total=total, pay_options=pay_options,
                                           phone_num=phone_num, firstname=firstname, lastname=lastname)

            conn.send(msg)


        for a in cart_stuff:
            db.session.delete(a)
            db.session.commit()

        flash('A Order Confirmation will be sent to your email,you will be contacted in 24 hours!', 'success')

        return redirect(url_for('checkout'))



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
            ISBN10 = Nbook.ISBN10.data
            ISBN13 = Nbook.ISBN13.data
            series = Nbook.series.data
            Format = Nbook.Format.data
            publication_date = Nbook.publication_date.data
            dimensions = Nbook.dimensions.data
            language = Nbook.language.data
            weight = Nbook.weight.data
            description = Nbook.description.data

            target = os.path.join(APP_ROOT, 'static/newbook_pics/')

            if not os.path.isdir(target):
                os.mkdir(target)

            npicture.save("/".join([target, npicture_name]))

            new_book = NewBook(bname, bauthor, bprice, npicture_name, stock_status, ISBN13, ISBN10, series, Format, publication_date, dimensions, language, weight, description)

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
            cISBN10 = Ubook.uISBN10.data
            cISBN13 = Ubook.uISBN13.data
            cseries = Ubook.useries.data
            cFormat = Ubook.uFormat.data
            cpublication_date = Ubook.upublication_date.data
            cdimensions = Ubook.udimensions.data
            clanguage = Ubook.ulanguage.data
            cweight = Ubook.uweight.data
            cdescription = Ubook.udescription.data

            target = os.path.join(APP_ROOT, 'static/usedbook_pics/')

            if not os.path.isdir(target):
                os.mkdir(target)

            cpicture.save("/".join([target, cpicture_name]))

            used_book = UsedBook(cname, cauthor, cprice, cpicture_name, stock_status, cISBN13, cISBN10, cseries, cFormat, cpublication_date, cdimensions, clanguage, cweight, cdescription )

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
            sdescription = supply.description.data

            target = os.path.join(APP_ROOT, 'static/supplies_pics/')

            if not os.path.isdir(target):
                os.mkdir(target)

            spicture.save("/".join([target, spicture_name]))

            new_supply = Supplies(sname, sprice, spicture_name, stock_status, sdescription)

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
            edescription = acc.description.data

            target = os.path.join(APP_ROOT, 'static/accessory_pics/')

            if not os.path.isdir(target):
                os.mkdir(target)

            epicture.save("/".join([target, epicture_name]))

            new_accessory = Accessories(ename, eprice, epicture_name, stock_status, edescription)

            db.session.add(new_accessory)
            db.session.commit()
            flash('Stock Added!', 'success')
            return redirect(url_for('addstock'))



        return render_template('addstock.html', Nbook=Nbook, Ubook=Ubook, supply=supply, acc=acc)

    else:

        return redirect(url_for('home'))




@app.route('/nbook_del/', methods=["GET", "POST"])
@login_required
def nbook_del():

    eshop = eshop_del()

    if request.method == 'POST' and eshop.validate_on_submit():

        item = eshop.item_id.data
        picture = eshop.pic_Name.data


        target = os.path.join(APP_ROOT, 'static/newbook_pics/')

        os.remove("/".join([target, picture]))

        del_post = NewBook.query.filter_by(id=item).first()

        db.session.delete(del_post)
        db.session.commit()

        flash('Item Deleted!', 'success')
        return redirect(url_for('eShop'))



@app.route('/ubook_del/', methods=["GET", "POST"])
@login_required
def ubook_del():

    eshop = eshop_del()

    if request.method == 'POST' and eshop.validate_on_submit():

        item = eshop.item_id.data
        picture = eshop.pic_Name.data


        target = os.path.join(APP_ROOT, 'static/usedbook_pics/')

        os.remove("/".join([target, picture]))

        del_post = UsedBook.query.filter_by(id=item).first()

        db.session.delete(del_post)
        db.session.commit()

        flash('Item Deleted!', 'success')
        return redirect(url_for('eShop'))



@app.route('/supply_del/', methods=["GET", "POST"])
@login_required
def supply_del():

    eshop = eshop_del()

    if request.method == 'POST' and eshop.validate_on_submit():

        item = eshop.item_id.data
        picture = eshop.pic_Name.data


        target = os.path.join(APP_ROOT, 'static/supplies_pics/')

        os.remove("/".join([target, picture]))

        del_post = Supplies.query.filter_by(id=item).first()

        db.session.delete(del_post)
        db.session.commit()

        flash('Item Deleted!', 'success')
        return redirect(url_for('eShop'))


@app.route('/acc_del/', methods=["GET", "POST"])
@login_required
def acc_del():
    eshop = eshop_del()

    if request.method == 'POST' and eshop.validate_on_submit():

        item = eshop.item_id.data
        picture = eshop.pic_Name.data

        target = os.path.join(APP_ROOT, 'static/accessory_pics/')

        os.remove("/".join([target, picture]))

        del_post = Accessories.query.filter_by(id=item).first()

        db.session.delete(del_post)
        db.session.commit()

        flash('Item Deleted!', 'success')
        return redirect(url_for('eShop'))


@app.route('/signup/', methods=["GET", "POST"])
def signup():

    signupForm = Signup()

    if request.method == 'POST' and signupForm.validate_on_submit():

        try:
            user = Users(signupForm.firstname.data, signupForm.lastname.data, signupForm.username.data, signupForm.password.data, signupForm.email.data, signupForm.year.data)
            db.session.add(user)
            db.session.commit()

            flash('Successfully Registered', 'success')

            with mail.connect() as conn:

                msg = Message(subject="Welcome to HyperAcademics!", sender="noreply@hyperacademics.com",
                              recipients=[signupForm.email.data])

                body = ("Your Username is:"+" "+signupForm.username.data)


                msg.body = (body)

                conn.send(msg)

        except IntegrityError:

            flash('The entered username is taken!', 'danger')



    return render_template('signup.html', signupForm=signupForm)




@app.route('/resources/', methods=["GET", "POST"])
def resources():

    rform = Resources()

    uiop = resources_del()

    file = resource_files()

    filedel = file_del()

    if request.method == 'POST' and rform.validate_on_submit():

        if is_filled(rform.r_picture.data) == True:

            target = os.path.join(APP_ROOT, 'static/resource_photos/')

            if not os.path.isdir(target):
                os.mkdir(target)

            rphoto = rform.r_picture.data
            rphotoname = rphoto.filename
            rphoto.save("/".join([target, rphotoname]))

            postTime = ctime()
            newspost = News(rform.r_title.data, rform.r_content.data, current_user.first_name, current_user.last_name, postTime, rphotoname, current_user.username)
            db.session.add(newspost)
            db.session.commit()
            flash('Posted!', 'success')
            return redirect(url_for('resources'))

        else:

            qwerty = ctime()

            rphotoname = None
            newspost = News(rform.r_title.data, rform.r_content.data, current_user.first_name, current_user.last_name, qwerty, rphotoname, current_user.username)
            db.session.add(newspost)
            db.session.commit()
            flash('Posted!', 'success')
            return redirect(url_for('resources'))


    if request.method == 'POST' and file.validate_on_submit():

        target = os.path.join(APP_ROOT, 'static/resource_files/')

        if not os.path.isdir(target):
            os.mkdir(target)


        rfile = file.File.data
        rfilename = rfile.filename
        rfile.save("/".join([target, rfilename]))

        newfile = Filename(rfilename)

        db.session.add(newfile)
        db.session.commit()
        flash('File Added!', 'success')

        return redirect(url_for('resources'))


    def getPostss():

        posts = db.session.query(News).all()
        return posts


    def get_filenames():

        files = db.session.query(Filename).all()
        return files



    news = getPostss()

    newfiles = get_filenames()

    return render_template('resources.html', rform=rform, news=news, uiop=uiop, file=file, newfiles=newfiles, filedel=filedel)






@app.route('/resources_delete/', methods=["GET", "POST"])
@login_required
def resources_delete():

    uiop = resources_del()


    if request.method == 'POST' and uiop.validate_on_submit():

        post = uiop.p_Id.data
        picture = uiop.picName.data

        if is_filled(picture) == True:

            target = os.path.join(APP_ROOT, 'static/resource_photos/')

            os.remove("/".join([target, picture]))

        del_post = News.query.filter_by(id=post).first()


        db.session.delete(del_post)
        db.session.commit()

        flash('Post Deleted!', 'success')
        return redirect(url_for('resources'))



@app.route('/del_file/', methods=["GET", "POST"])
@login_required
def del_file():

    filedel = file_del()

    if request.method == 'POST' and filedel.validate_on_submit():

        fileid = filedel.file_id.data
        filename = filedel.fileName.data


        target = os.path.join(APP_ROOT, 'static/resource_files/')

        os.remove("/".join([target, filename]))

        zxc = Filename.query.filter_by(id=fileid).first()

        db.session.delete(zxc)
        db.session.commit()

        flash('File Deleted!', 'success')
        return redirect(url_for('resources'))




@app.route('/contactus/', methods=["GET", "POST"])
def contactus():

    contact = contactform()

    if request.method == 'POST' and contact.validate_on_submit():

        with mail.connect() as conn:

            msg = Message(subject=contact.subject.data, sender=contact.email.data, recipients=["admin@hyperacademics.com"])

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

        uploads = onevids()
        y2uploads = year2vids()
        y3uploads = year3vids()

        vidtitle = uploads.vid_title.data
        c_title = uploads.c_title.data

        if request.method == 'POST' and uploads.validate_on_submit():

            target = os.path.join(APP_ROOT, 'static/year1_vids/')

            if not os.path.isdir(target):
                os.mkdir(target)

            video = uploads.video.data
            videoname = secure_filename(video.filename)

            video.save("/".join([target, videoname]))

            newvid = one_vids(c_title, vidtitle, videoname)
            db.session.add(newvid)
            db.session.commit()

            flash('File Saved', 'success')
            return redirect(url_for('uploads'))



        if request.method == 'POST' and y2uploads.validate_on_submit():

            vidtitle2 = y2uploads.vid_title2.data
            c_title2 = y2uploads.c_title2.data

            target = os.path.join(APP_ROOT, 'static/year2_vids/')

            if not os.path.isdir(target):
                os.mkdir(target)

            video2 = y2uploads.video2.data
            videoname2 = secure_filename(video2.filename)

            video2.save("/".join([target, videoname2]))

            newvid2 = two_vids(c_title2, vidtitle2, videoname2)
            db.session.add(newvid2)
            db.session.commit()

            flash('File Saved', 'success')
            return redirect(url_for('uploads'))



        if request.method == 'POST' and y3uploads.validate_on_submit():

            vidtitle3 = y3uploads.vid_title3.data
            c_title3 = y3uploads.c_title3.data

            target = os.path.join(APP_ROOT, 'static/year3_vids/')

            if not os.path.isdir(target):
                os.mkdir(target)

            video3 = y3uploads.video3.data
            videoname3 = secure_filename(video3.filename)

            video3.save("/".join([target, videoname3]))

            newvid3 = three_vids(c_title3, vidtitle3, videoname3)
            db.session.add(newvid3)
            db.session.commit()

            flash('File Saved', 'success')
            return redirect(url_for('uploads'))



        return render_template('uploads.html', uploads=uploads, y2uploads=y2uploads, y3uploads=y3uploads)

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
admin.add_view(MyModelView(News, db.session))
admin.add_view(MyModelView(Filename, db.session))
admin.add_view(MyModelView(Cart, db.session))