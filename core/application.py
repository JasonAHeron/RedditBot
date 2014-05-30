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

<<<<<<< HEAD:core/application.py
# Import blueprints
from apps.botgen.controllers import bpnt_botgen
=======
from hashlib import md5 as md5

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
>>>>>>> ubuntu:app.py

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

        allowed_types = ["title", "comment", "title_comment"]
        allowed_actions = ["print", "message", "respond"]

        attempted_type = request.form.get("type")
        if attempted_type in allowed_types:
            type = attempted_type
        else:
            type = "title"

        attempted_action = request.form.get("action")
        if attempted_action in allowed_actions:
            action = attempted_action
        else:
            action = "print"


        arghash = md5()
        arghash.update(''.join(subreddit_names)+''.join(search_words[0])+recipient+type+action)
        arghash_digest = arghash.hexdigest().encode("utf-8")

        compileBotCore(subreddit_names, search_words, frequency, recipient, type, action, arghash_digest)

        return send_from_directory(directory='/var/www/Flask/RedditBot/static/bots/', filename='%s.py' % arghash_digest)
    else:
        form = searchBotForm(request.form)
        return render_template('pages/home.html', form=form)

# Get an existing bot by asking for its hex digest
@app.route('/bots/<bothex>', methods=['GET'])
def bots(bothex):
    return send_from_directory(directory='/var/www/Flask/RedditBot/static/bots/', filename='%s.py' % bothex)

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

<<<<<<< HEAD:core/application.py
=======
# Default port:
if __name__ == '__main__':
    app.run(debug= False)
>>>>>>> ubuntu:app.py
