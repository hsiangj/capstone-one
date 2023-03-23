import os

from flask import Flask, render_template, redirect, session, flash, request, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, FavoritePark, CollectedPark
from forms import RegisterForm, LoginForm
from secret import key

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = (os.environ.get('DATABASE_URL', 'postgresql:///park_collector'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', "chamberofsecrets")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)

##########
# User signup/login/logout

@app.before_request
def add_user_to_g():
  """If logged in, add current user to Flask global."""

  if CURR_USER_KEY in session:
    g.user = User.query.get(session[CURR_USER_KEY])

  else:
    g.user = None

def do_login(user):
  """Log in user."""

  session[CURR_USER_KEY] = user.id

def do_logout():
  """Log out user."""
  
  if CURR_USER_KEY in session: 
    del session[CURR_USER_KEY]


@app.route('/')
def homepage():
  """Show homepage. If logged in: search bar. Anonymous user: sign up prompt."""
  if g.user:
    return render_template('home.html')

  return render_template ('home-anon.html')


@app.route('/signup', methods=['GET', 'POST'])
def register_user():
  """Handle user signup. Create new user and add to DB. Redirect to home page.
    If form not valid, present form. 
    If there already is a user with that username: flash message and re-present form.
  """
  if CURR_USER_KEY in session:
    del session[CURR_USER_KEY]

  form = RegisterForm()

  if form.validate_on_submit():
    try:
      user = User.signup(
        username=form.username.data,
        password=form.password.data,
        email=form.email.data,
        first=form.first_name.data,
        last=form.last_name.data
      )
      db.session.add(user)
      db.session.commit()
    except IntegrityError:
      flash('Username already taken, try a different one!', 'danger')
      return render_template('signup.html', form=form)

    do_login(user)
    return redirect('/')

  else:  
    return render_template('signup.html', form=form)

