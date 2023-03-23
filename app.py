import os

from flask import Flask, render_template, redirect, session, flash, request, g
from flask_debugtoolbar import DebugToolbarExtension
from secret import key
from models import db, connect_db, User, FavoritePark, CollectedPark


app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = (os.environ.get('DATABASE_URL', 'postgresql:///park_collector'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', "chamberofsecrets")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)



@app.route('/')
def homepage():
    """"""
    
    return render_template ('home.html')