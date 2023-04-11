import os
import re

from flask import Flask, render_template, redirect, session, flash, request, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests

from models import db, connect_db, User, BookmarkedPark, CollectedPark, Park
from forms import RegisterForm, LoginForm, EditForm

app = Flask(__name__)
app.app_context().push()

uri = os.environ.get("DATABASE_URL", "postgresql:///park_collector")
if uri.startswith("postgres://"):
  uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri

api_key = os.environ.get("API_KEY", "NPS_API_KEY")
app.config["API_KEY"] = api_key

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "chamberofsecrets")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)
connect_db(app)

db.create_all()

CURR_USER_KEY = 'curr_user'
API_BASE_URL = "https://developer.nps.gov/api/v1"
HEADERS = {"X-Api-Key": api_key}
PARK_LIMIT = 468

##########
# Homepage and error page
@app.route('/')
def homepage():
  """Show homepage. If logged in: search bar. Anonymous user: sign up prompt."""
  if g.user:
    return render_template('home.html')
  else:
    return render_template ('home-anon.html')

@app.errorhandler(404)
def page_not_found(e):
  """404 page"""
  return render_template('404.html')

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
  park_topic_data = park_topic.json()

  return render_template('/parks/show.html', parks=park_topic_data, topic_id=topic_id)

@app.route('/park', methods=['GET','POST'])
def query_park_code():
  """Retrieve form data and query for park code using park name."""
  park_name = request.form['q']
  try:
    park = Park.query.filter_by(park_name=park_name).first()
    park_code = park.park_code
    return redirect(f'/park/{park_code}')
  except AttributeError:
    flash('Please select a valid park.', 'danger')
    return redirect('/') 

@app.route('/park/<park_code>')
def get_single_park(park_code):
  """Get a national park by park code."""
  
  park = requests.get(f'{API_BASE_URL}/parks', 
                              headers=HEADERS,
                              params={'parkCode': park_code, 'limit': PARK_LIMIT})
  park_data = park.json()
  
  return render_template('/parks/park.html', park=park_data, park_code=park_code)

##########
# User routes
@app.route('/users/profile', methods = ['GET', 'POST'])
def edit_user():
  """Update profile for current user."""
  if not g.user:
    flash("Access unauthorized.", "danger")
    return redirect('/')

  user = g.user
  form = EditForm(obj=user)
  if form.validate_on_submit():
    if User.authenticate(user.username, form.password.data):
      user.username = form.username.data
      user.email = form.email.data
      user.first_name = form.first_name.data
      user.last_name = form.last_name.data

      db.session.add(user)
      db.session.commit()
      return redirect('/')
    
    flash('Wrong password, please try again.', 'danger')

  return render_template('users/profile.html', form=form)

@app.route('/users/delete', methods=['POST'])
def delete_user():
  """Delete user."""
  if not g.user:
    flash("Access unauthorized.", "danger")
    return redirect("/")

  do_logout()

  db.session.delete(g.user)
  db.session.commit()

  return redirect('/signup')

@app.route('/users/<int:user_id>/bookmarked')
def show_bookmarked(user_id):
  """Show bookmarked parks for a particular user."""
  if user_id != g.user.id:
    flash("Access unauthorized.", "danger")
    return redirect('/')
  
  user = User.query.get_or_404(user_id)
    
  return render_template('users/bookmarked.html', user=user)

@app.route('/users/<int:user_id>/collected')
def show_collected(user_id):
  """Show collected parks for a particular user."""
  if user_id != g.user.id:
    flash("Access unauthorized.", "danger")
    return redirect('/')
  
  user = User.query.get_or_404(user_id)
    
  return render_template('users/collected.html', user=user, total=PARK_LIMIT)
  
##########
# API routes
@app.route('/api/topics')
def list_topics():
  """Return JSON with all park topics."""
  all_topics = requests.get(f'{API_BASE_URL}/topics', 
                            headers=HEADERS,
                            params={'limit': PARK_LIMIT})
  return jsonify(all_topics.json())

@app.route('/api/parks')
def get_all_parks():
  """Add basic park info for all parks to database."""
  parks = requests.get(f'{API_BASE_URL}/parks', 
                            headers=HEADERS,
                            params={'limit': PARK_LIMIT})
  parks_data = parks.json()
  parks = []
  
  for park in parks_data['data']:
    park_code = park['parkCode']
    park_name = park['fullName']
    park_state = park['addresses'][0]['stateCode']
    new_park = Park(park_code=park_code, park_name=park_name, park_state=park_state)
    parks.append(new_park)

  db.session.add_all(parks)
  db.session.commit()

  return jsonify(message= 'Success')

@app.route('/api/parks/names')
def get_park_names():
  """Return JSON of all park names from database."""
  parks = Park.query.all()
  names = []
  for park in parks:
    names.append(park.park_name)
  return jsonify({'names': names})

@app.route('/api/park/<parkCode>')
def get_park(parkCode):
  """Return JSON with info for specific park from external API."""
  one_park = requests.get(f'{API_BASE_URL}/parks', 
                            headers=HEADERS,
                            params={'parkCode': parkCode, 'limit': PARK_LIMIT})
  return jsonify(one_park.json())

@app.route('/api/bookmark', methods=['GET','POST']) 
def add_bookmark():
  """Handle adding park to bookmarked table in database."""
  if request.method == 'GET':
    flash("Invalid request.", "warning")
    return redirect('/')

  bookmark_park = BookmarkedPark(park_code=request.json['parkCode'], park_name=request.json['parkName'], user_id=(session[CURR_USER_KEY]))
  
  db.session.add(bookmark_park)
  db.session.commit()
 
  return jsonify(message= 'Success')

@app.route('/api/bookmark/<parkCode>', methods=['DELETE'])
def delete_bookmark(parkCode):
  """Delete a particular bookmarked park from database and respond with delete message."""
  park = BookmarkedPark.query.filter(BookmarkedPark.park_code==parkCode, BookmarkedPark.user_id==(session[CURR_USER_KEY])).first()

  db.session.delete(park)
  db.session.commit()
  
  return jsonify(message= 'Deleted')


@app.route('/api/collect', methods=['GET','POST'])
def add_collect():
  """Handle adding park to collected table in database."""
  if request.method == 'GET':
    flash("Invalid request.", "warning")
    return redirect('/')
  
  collected_park = CollectedPark(park_code=request.json['parkCode'], park_name=request.json['parkName'], user_id=(session[CURR_USER_KEY]))

  db.session.add(collected_park)
  db.session.commit()

  return jsonify(message= 'Success')

@app.route('/api/collect/<parkCode>', methods=['DELETE'])
def delete_collect(parkCode):
  """Delete a particular collected park in database and respond with delete message."""
  park = CollectedPark.query.filter(CollectedPark.park_code==parkCode, CollectedPark.user_id==(session[CURR_USER_KEY])).first()

  db.session.delete(park)
  db.session.commit()
  
  return jsonify(message= 'Deleted')
















