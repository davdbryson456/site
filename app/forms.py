from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, PasswordField, HiddenField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired



class Signup (Form):

    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    year = SelectField('year', choices=[('1', '1'), ('2', '2'), ('3', '3')])



class contactform (Form):

    subject = StringField('Subject', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])


class Login (Form):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class onevids(Form):

    vid_title = StringField('y1 vids', validators=[DataRequired()])
    c_title = StringField('y1 vids', validators=[DataRequired()])
    video = FileField('Videos must be in mp4 format', validators=[FileRequired(), FileAllowed(['mp4'], 'Videos only!')])


class _Post(Form):

    title = StringField('Title', [InputRequired()])
    content = TextAreaField('Content', [InputRequired()])
    picture = FileField('Pictures must be in .jpg format', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'PDF'], 'Pictures only!')])


class _Comment (Form):

    body = TextAreaField('Comment', validators=[DataRequired()])
    post_id = HiddenField()



class Add_newbook (Form):

    bookname = TextAreaField('Book name', validators=[DataRequired()])
    author = TextAreaField('Author', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    picture = FileField('Pictures must be in .jpg format', validators=[FileAllowed(['jpg'], 'Pictures only!')])
    ISBN10 = TextAreaField('Book name', validators=[DataRequired()])
    ISBN13 = TextAreaField('Book name', validators=[DataRequired()])
    series = TextAreaField('Book name', validators=[DataRequired()])
    Format = TextAreaField('Book name', validators=[DataRequired()])
    publication_date = TextAreaField('Book name', validators=[DataRequired()])
    dimensions = TextAreaField('Book name', validators=[DataRequired()])
    language = TextAreaField('Book name', validators=[DataRequired()])
    weight = TextAreaField('Book name', validators=[DataRequired()])
    description = TextAreaField('Book name', validators=[DataRequired()])



class Add_usedbook (Form):

    ubookname = TextAreaField('Book name', validators=[DataRequired()])
    uauthor = TextAreaField('Author', validators=[DataRequired()])
    uprice = IntegerField('price', validators=[DataRequired()])
    upicture = FileField('Pictures must be in .jpg format', validators=[FileAllowed(['jpg'], 'Pictures only!')])
    uISBN10 = TextAreaField('Book name', validators=[DataRequired()])
    uISBN13 = TextAreaField('Book name', validators=[DataRequired()])
    useries = TextAreaField('Book name', validators=[DataRequired()])
    uFormat = TextAreaField('Book name', validators=[DataRequired()])
    upublication_date = TextAreaField('Book name', validators=[DataRequired()])
    udimensions = TextAreaField('Book name', validators=[DataRequired()])
    ulanguage = TextAreaField('Book name', validators=[DataRequired()])
    uweight = TextAreaField('Book name', validators=[DataRequired()])
    udescription = TextAreaField('Book name', validators=[DataRequired()])




class Add_supplies (Form):

    supplyname = TextAreaField('Supply name', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    picture = FileField('Pictures must be in .jpg format', validators=[FileAllowed(['jpg'], 'Pictures only!')])
    description = TextAreaField('description', validators=[DataRequired()])


class Add_accessories (Form):

    accname = TextAreaField('Accessory name', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    picture = FileField('Pictures must be in .jpg format', validators=[FileAllowed(['jpg'], 'Pictures only!')])
    description = TextAreaField('description', validators=[DataRequired()])


class addtocart (Form):

    product_name = HiddenField()
    item_price = HiddenField()
    qty = SelectField('Quantity', choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (6, 'Six'), (7, 'Seven'), (8, 'Eight'), (9, 'Nine')])




class Deletepost (Form):

    postId = HiddenField()
    pic_name = HiddenField()


class Deletevids (Form):

    vid_name = HiddenField()
    p_id = HiddenField()


class Deletevids2 (Form):

    vid_name2 = HiddenField()
    p_id2 = HiddenField()


class Deletevids3(Form):

    vid_name3 = HiddenField()
    p_id3 = HiddenField()


class Homepage (Form):

    pic = FileField('Pictures must be in jpg format', validators=[FileRequired(), FileAllowed(['jpg'], 'Pictures only!')])

    caption = TextAreaField('Caption')


class Resources (Form):

    r_title = StringField('Title', [InputRequired()])
    r_content = TextAreaField('Content', [InputRequired()])
    r_picture = FileField('Pictures must be in .jpg format', validators=[FileAllowed(['jpg'], 'Pictures only!')])


class resources_del (Form):

    p_Id = HiddenField()
    picName = HiddenField()


class resource_files (Form):

    File = FileField('', validators=[FileRequired(), FileAllowed(['pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'txt', 'rtf', 'html', 'zip', 'mp3', 'wma', 'mpg', 'flv', 'avi', 'jpg', 'jpeg', 'png', 'gif', 'pptx'], 'Files!')])


class file_del (Form):

    fileName = HiddenField()

    file_id = HiddenField()


class eshop_del(Form):

    pic_Name = HiddenField()

    item_id = HiddenField()


class cartt_del(Form):

    cart_id = HiddenField()


class checkoutt(Form):

    payment = SelectField('payment', choices=[('Cash','Cash'), ('Card','Card')])
    phone_num = StringField('Phone Number', [InputRequired()])
    total = HiddenField()


class year2vids (Form):

    vid_title2 = StringField('y1 vids', validators=[DataRequired()])
    c_title2 = StringField('y1 vids', validators=[DataRequired()])
    video2 = FileField('Videos must be in mp4 format', validators=[FileRequired(), FileAllowed(['mp4'], 'Videos only!')])


class year3vids (Form):

    vid_title3 = StringField('y1 vids', validators=[DataRequired()])
    c_title3 = StringField('y1 vids', validators=[DataRequired()])
    video3 = FileField('Videos must be in mp4 format', validators=[FileRequired(), FileAllowed(['mp4'], 'Videos only!')])

