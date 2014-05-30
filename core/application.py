"""
    ____           __    ___ __  ____        __ 
   / __ \___  ____/ /___/ (_) /_/ __ )____  / /_
  / /_/ / _ \/ __  / __  / / __/ __  / __ \/ __/
 / _, _/  __/ /_/ / /_/ / / /_/ /_/ / /_/ / /_  
/_/ |_|\___/\__,_/\__,_/_/\__/_____/\____/\__/  
                                                
       Written by Jason Heron & Nick Wood
                 (c) 2014
                 
application.py

this file contains the main application startup code -- it is imported by 
deploy.py to start the RedditBot application
"""

# Import what we need from Flask
from flask import *
import logging
from logging import Formatter, FileHandler
from forms import *
from botCore import *

# Import blueprints
from apps.botgen.controllers import bpnt_botgen

# Initialize the app
app = Flask(__name__)
app.config.from_object('config')

# Register blueprints
app.register_blueprint(bpnt_botgen)

'''
# Define some controllers (TODO: use blueprints)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        subreddit_names = getSubredditNames(request.form['subreddits'])
        search_words = getSearchWords(request.form['searchwords'])
        frequency = getFrequency(request.form['frequency'])
        recipient = getRecipient(request.form['recipient'])

        if request.form.get("title"):
            type = "title"
        elif request.form.get("comment"):
            type = "comment"
        elif request.form.get("title_comment"):
            type = "title_comment"

        if request.form.get("print"):
            action = "print"
        elif request.form.get("message"):
            action = "message"
        elif request.form.get("respond"):
            action = "respond"

        compileBotCore(subreddit_names, search_words, frequency, recipient, type, action)
        return send_from_directory(directory='.', filename='AACompiled.py')
    else:
        form = searchBotForm(request.form)
        return render_template('pages/home.html', form=form)

@app.route('/about')
def about():
    return render_template('pages/about.html')

#----------------------------------------------------------------------------#
# Error handlers.
#----------------------------------------------------------------------------#

@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
'''

