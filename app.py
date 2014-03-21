#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#

from flask import *
import logging
from logging import Formatter, FileHandler
from forms import *
from botCore import *

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

# Default port:
if __name__ == '__main__':
    app.run()
