from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Email

class contactform (Form):

    subject = StringField('Subject', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])