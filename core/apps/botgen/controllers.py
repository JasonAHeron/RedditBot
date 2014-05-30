"""
                     ____           __    ___ __  ____        __ 
                    / __ \___  ____/ /___/ (_) /_/ __ )____  / /_
                   / /_/ / _ \/ __  / __  / / __/ __  / __ \/ __/
                  / _, _/  __/ /_/ / /_/ / / /_/ /_/ / /_/ / /_  
                 /_/ |_|\___/\__,_/\__,_/_/\__/_____/\____/\__/  
                                                                 
                        Written by Jason Heron & Nick Wood         
                                     (c) 2014
botgen/controllers.py 
blueprints for the main reddit bot generator
"""

# Imports
from flask import Blueprint, request, render_template, jsonify
from forms import SearchBotForm
from generator import getSubredditNames, getSearchWords, getFrequency, \
    getRecipient, compileBotCore

from hashlib import md5 as md5
from core.decorators.cors_decorators import crossdomain
from values import bot_path

# Define blueprint
bpnt_botgen = Blueprint('bpnt_botgen', __name__)

# Show the homepage
@bpnt_botgen.route('/', methods=['GET'])
def botgen_home():
    form = SearchBotForm(request.form)
    return render_template('botgen/home.html', form=form)

# Generate or retrieve a bot
@bpnt_botgen.route('/gen', methods=['POST'])
@crossdomain(origin='*')
def botgen_generate():

    # Pull params out of form data
    subreddit_names = getSubredditNames(request.form['subreddits'])
    search_words    = getSearchWords(request.form['searchwords'])
    frequency       = getFrequency(request.form['frequency'])
    recipient       = getRecipient(request.form['recipient'])

    # Enforce allowed search types and actions
    allowed_types    = ["title", "comment", "title_comment"]
    allowed_actions  = ["print", "message", "respond"]
    attempted_type   = request.form.get("type")
    attempted_action = request.form.get("action")

    if attempted_type in allowed_types:
        type = attempted_type
    else:
        type = "title"

    if attempted_action in allowed_actions:
        action = attempted_action
    else:
        action = "print"

    # build a message to hash using MD5 (not for security -- just for caching!)
    concat_hashmsg = ''.join([ 
            ''.join(subreddit_names), 
            ''.join(search_words[0]), 
            recipient, 
            type, 
            action
        ])

    # Hash the message
    arghash = md5()
    arghash.update(concat_hashmsg)
    arghash_digest = arghash.hexdigest().encode("utf-8")

    # Either compile the file, or ensure it exists
    compileBotCore(subreddit_names, search_words, frequency, recipient, type, 
        action, arghash_digest)

    # Now, open the file in read mode...
    filePath = bot_path(arghash_digest)
    retData  = {'hashcode': arghash_digest}

    # Read file into retData
    with open(filePath, "r") as botFile:
        retData['botcode'] = botFile.read()

    # Return as JSON
    return jsonify(**retData)


# About page
# TODO: this page doesn't quite work yet. FIX THIS!
@bpnt_botgen.route('/about', methods=['GET'])
def botgen_about():
    return render_template('botgen/about.html')

