#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#

from flask import * # do not use '*'; actually input the dependencies.
from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import time
import praw

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

class BotForm(Form):
    name = TextField('Username')
    password = PasswordField('Password')
    subreddits = TextField('buildapcsales, hardwareswap')
    searchwords = TextField('cpu, gpu')
    frequency = TextField('20')
    recipient = TextField('jason')



global reddit_session
reddit_session = 0
global subreddit_names
subreddit_names = 0
global search_words
search_words = 0
global frequency
frequency = 0
global recipient
recipient = 0

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global reddit_session
        reddit_session = botInit(request.form['name'], request.form['password'])
        subreddit_names = getSubredditNames(request.form['subreddits'])
        search_words = getSearchWords(request.form['searchwords'])
        frequency = getFrequency(request.form['frequency'])
        recipient = getRecipient(request.form['recipient'])
        searchBot(reddit_session,subreddit_names,search_words,frequency,recipient)
        #if request.form['name'] == 'admin' and request.form['password'] == 'admin':
        return redirect(url_for('home'))
    else:
        form = BotForm(request.form)
        return render_template('forms/login.html', form = form)

#@app.route('/bot', methods=['GET', 'POST'])
#def bot():
    #return searchBot(reddit_session)

@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form = form)

@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form = form)

# Error handlers.

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





DEBUG = True

def throwError(error = "unhandled", exit=True, code=0):
    print "There was an error: {}".format(error)
    if exit:
        exit(code)

def botInit(username, password):
    r = praw.Reddit('PRAW learning and testing v0.3 by /u/syserror')
    try:
        r.login(username, password)
    except praw.errors.InvalidUserPass as err:
        throwError(err)
    return r

def getSubredditNames(input):
    subreddit_names = input.replace(" ", "").split(",")
    return subreddit_names

def getSearchWords(input):
    searchWords = []
    newSearchWords = input.lower().split(",")
    newSearchWords = [searchWord.lstrip() for searchWord in newSearchWords]
    searchWords.append(newSearchWords)
    return searchWords

def getFrequency(input):
    frequency = int(input)
    return frequency

def getRecipient(input):
    recipient = input
    return recipient

def dumpResults(r, results, message = False, recipient = "none"):
    if message:
        for result in results:
            r.user.send_message(recipient, result)
    else:
        for result in results:
            print result

def searchBot(r, subreddit_names, searchWords, frequency, recipient):

    already_done = []
    firstPass = True
    first_results = []
    while True:
        results = []
        for subreddit_name in subreddit_names:
            for searchWord in searchWords:
                subreddit = r.get_subreddit(subreddit_name)
                try:
                    for submission in subreddit.get_hot(limit=100):
                        title_text = submission.title.lower()
                        has_text = any(string in title_text for string in searchWord)
                        if submission.id not in already_done and has_text:
                            if not firstPass:
                                msg = '[NEW FIND IN: %s] %s (%s)' % (subreddit_name.upper(),submission.title ,submission.short_link)
                                #r.user.send_message(recipient, msg)
                                results.append(msg)
                            else:
                                first_results.append(subreddit_name.upper() + " :: " + submission.title + " :: " + submission.short_link)
                            already_done.append(submission.id)
                except praw.errors.InvalidSubreddit as err:
                    throwError(err,False)
        if firstPass:
            dumpResults(r, first_results)
        dumpResults(r, results, True, recipient)
        firstPass = False
        time.sleep(max(frequency,20))


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''



