from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired

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
