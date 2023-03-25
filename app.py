import os

from flask import Flask, render_template, redirect, session, flash, request, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests

from models import db, connect_db, User, FavoritePark, CollectedPark
from forms import RegisterForm, LoginForm
from secret import key

CURR_USER_KEY = 'curr_user'
API_BASE_URL = "https://developer.nps.gov/api/v1"
HEADERS = {"X-Api-Key":key}
PARK_LIMIT = 450

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
  else:
    return render_template ('home-anon.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
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

@app.route('/login', methods=['GET','POST'])
def login():
  """Handle user login."""
  form = LoginForm()

  if form.validate_on_submit():
    user = User.authenticate(form.username.data, form.password.data)

    if user:
      do_login(user)
      flash(f'Welcome back, {user.username}!', 'success')
      return redirect('/')
    
    else:
      flash('Invalid credentials.', 'warning')

  return render_template('login.html', form=form)

@app.route('/logout')
def logout():
  """Handle user logout."""
  do_logout()
  flash("See you later!", 'success')
  return redirect('/login')

##########
# Park routes

@app.route('/parks/topic/<topic_id>', methods=['GET'])
def get_parks_by_topic(topic_id):
  """Get all national parks by a particular topic."""
  park_topic = requests.get(f'{API_BASE_URL}/topics/parks', 
                            headers=HEADERS,
                            params={'id': topic_id, 'limit':PARK_LIMIT})

  return render_template('/parks/show.html', parks=park_topic.json())






##########
# API routes
@app.route('/api/topics', methods=['GET'])
def list_topics():
  """Return JSON with all park topics."""
  all_topics = requests.get(f'{API_BASE_URL}/topics', 
                            headers=HEADERS,
                            params={'limit': PARK_LIMIT})
  return jsonify(all_topics.json())

@app.route('/api/park/<code>', methods=['GET'])
def get_park(code):
  """Return JSON with info for specific park."""
  park = requests.get(f'{API_BASE_URL}/parks', 
                            headers=HEADERS,
                            params={'parkCode': code, 'limit': PARK_LIMIT})
  return jsonify(park.json())


##########
# Helper functions to be moved








