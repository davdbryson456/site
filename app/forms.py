from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired



class Signup (Form):

    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    email = StringField('E-mail', validators=[DataRequired(), Email()])


class contactform (Form):

    subject = StringField('Subject', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])


class Login (Form):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class Uploadvids(Form):

    video = FileField('Videos must be in mp4 format', validators=[FileRequired(), FileAllowed(['mp4'], 'Videos only!')])


class _Post(Form):

    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Pictures must be in .jpg format', validators=[FileAllowed(['jpg'], 'Pictures only!')])

class _Comment(Form):

    body = TextAreaField('Comment', validators=[DataRequired()])
    post_id = HiddenField()