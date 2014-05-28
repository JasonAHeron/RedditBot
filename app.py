#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#

from flask import *
import logging
from logging import Formatter, FileHandler
from forms import *
from botCore import *

from hashlib import md5 as md5

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

#----------------------------------------------------------------------------#
# Form Classes.
#----------------------------------------------------------------------------#

class searchBotForm(Form):
    subreddits = TextField('buildapcsales, hardwareswap')
    searchwords = TextField('cpu, gpu')
    frequency = TextField('20')
    recipient = TextField('jason')

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

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
        arghash_digest = arghash.digest().encode("utf-8")

        compileBotCore(subreddit_names, search_words, frequency, recipient, type, action, arghash_digest)


        return send_from_directory(directory='/var/www/Flask/RedditBot/static/bots/', filename='%s.py' % arghash_digest)
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

# Default port:
if __name__ == '__main__':
    app.run(debug= False)
