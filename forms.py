from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired(message="Username can't be blank"), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(message="Password can't be blank"), Length(min=5)])
    email = StringField("Email", validators=[InputRequired(message="Please enter an email"), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(message="Please enter a first name")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Please enter a last name")])

class LoginForm(FlaskForm):
    """Form for user login."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=5)])


