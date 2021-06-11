from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField 
from wtforms.widgets import PasswordInput
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email

class RegisterForm(FlaskForm):
    """generate register form"""

    style={'class': 'btn btn-success btn-lg'}

    username = StringField('Usrname', validators=[InputRequired()])
    password = StringField('Password', widget=PasswordInput(hide_value=False), validators=[InputRequired()])
    email = EmailField('Email',  validators=[InputRequired(), Email()])
    first_name = StringField('First name', validators=[InputRequired()])
    last_name = StringField('Last name', validators=[InputRequired()])
    submit = SubmitField("Register", render_kw=style)

class LoginForm(FlaskForm):
    """generate register form"""

    style={'class': 'btn btn-success btn-lg'}

    username = StringField('Usrname', validators=[InputRequired()])
    password = StringField('Password', widget=PasswordInput(hide_value=False), validators=[InputRequired()])
    submit = SubmitField("Log In", render_kw=style)

class FeedbackForm(FlaskForm):

    style={'class': 'btn btn-success btn-lg'}

    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField("Notes", validators=[InputRequired()])
    submit = SubmitField("Add feedback", render_kw=style)