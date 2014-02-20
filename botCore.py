__author__ = 'jason'
import time
import praw
import inspect

#----------------------------------------------------------------------------#
# Hardcoded data curators
#----------------------------------------------------------------------------#

def getSubredditNames(input):
    subreddit_names = [str(subreddit) for subreddit in input.replace(" ", "").split(",")]
    return subreddit_names

def getSearchWords(input):
    searchWords = []
    newSearchWords = input.lower().split(",")
    newSearchWords = [str(searchWord.lstrip()) for searchWord in newSearchWords]
    searchWords.append(newSearchWords)
    return searchWords

def getFrequency(input):
    frequency = float(input)
    return frequency

def getRecipient(input):
    recipient = str(input)
    return recipient

#----------------------------------------------------------------------------#
# Compile Related Functions
#----------------------------------------------------------------------------#

def printFunction(file, function):
    for line in inspect.getsourcelines(function)[0]:
        file.write(str(line))

def compileBot(subreddit_names, search_words, frequency, recipient):
    file = open('AACompiled.py', 'w+')
    print >> file, 'import praw'
    print >> file, 'import time'
    print >> file, 'subreddit_names = ', subreddit_names
    print >> file, 'search_words = ', search_words
    print >> file, 'frequency = {}'.format(frequency)
    print >> file, 'recipient = "{}"'.format(recipient)
    printFunction(file, throwError)
    printFunction(file, botInit)
    printFunction(file, outputResults)
    printFunction(file, titleSearch)
    printFunction(file, titleSearchBot)
    printFunction(file, runBot)
    print >> file, 'if __name__ == "__main__":'
    print >> file, '    runBot(subreddit_names, search_words, frequency, recipient)'
    file.close()

#----------------------------------------------------------------------------#
# errors
#----------------------------------------------------------------------------#

def throwError(error = "unhandled", exit=True, code=0):
    print "There was an error: {}".format(error)
    if exit:
        exit(code)

#----------------------------------------------------------------------------#
# Bot Pieces
#----------------------------------------------------------------------------#
# Fundamental
#-------------------------------------#

def botInit(username, password, auto=True):
    r = praw.Reddit('PRAW learning and testing v0.5 by /u/syserror')
    try:
        if auto:
            r.login(username, password)
        else:
            r.login()
    except praw.errors.InvalidUserPass as err:
        throwError(err)
    return r

def runBot(subreddit_names, searchWords, frequency, recipient):
    r = botInit("none", "none", False)
    titleSearchBot(r, subreddit_names, searchWords, frequency, recipient)

#-------------------------------------#
# Result related
#-------------------------------------#

def outputResults(r, results, message = False, recipient = "none"):
    if message:
        for result in results:
            r.user.send_message(recipient, result)
    else:
        for result in results:
            print result

#-------------------------------------#
# Search related
#-------------------------------------#

def titleSearch(r, subreddit_names, searchWords, firstPass, already_done=[]):
    if firstPass:
        first_results = []
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
                            results.append(msg)
                        else:
                            first_results.append(subreddit_name.upper() + " :: " + submission.title + " :: " + submission.short_link)
                        already_done.append(submission.id)
            except praw.errors.InvalidSubreddit as err:
                throwError(err,False)
    if firstPass:
        return {'first_results':first_results , 'already_done':already_done}
    return {'results':results , 'already_done':already_done}

def commentSearch(r, subreddit_names, searchWords, firstPass, already_done=[]):
    if firstPass:
        first_results = []
    results = []
    for subreddit_name in subreddit_names:
        subreddit = r.get_subreddit(subreddit_name)
        for submission in subreddit.get_hot(limit=100):
            full_submission = r.get_submission(submission_id=submission.id)
            full_submission.replace_more_comments(limit=16, threshold=10)
            flat_comments = praw.helpers.flatten_tree(full_submission.comments)
            for comment in flat_comments:
                if not hasattr(comment, 'body'):
                    continue
                print comment.body

def commentTitleSearch(r, subreddit_names, searchWords):
    results = titleSearch(r, subreddit_names, searchWords, True)
    submission_ids = results['already_done']
    for submission_id in submission_ids:
        submission= r.get_submission(submission_id=submission_id)
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:
            print "{} :: {}".format(submission.title, comment)
            #if comment.body == "Hello" and comment.id not in already_done:
            #    comment.reply(' world!')

#-------------------------------------#
# Final Bots
#-------------------------------------#

def titleSearchBot(r, subreddit_names, searchWords, frequency, recipient):
    results = titleSearch(r, subreddit_names, searchWords, True)
    already_done = results['already_done']
    outputResults(r, results['first_results'])
    while True:
        results = titleSearch(r, subreddit_names, searchWords, False, already_done)
        already_done = results['already_done']
        outputResults(r, results['results'], True, recipient)
        time.sleep(max(frequency,20))


