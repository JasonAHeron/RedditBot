__author__ = 'jason'
import time
import praw
import inspect
import os.path

#----------------------------------------------------------------------------#
# Hardcoded data curators
#----------------------------------------------------------------------------#

def getSubredditNames(input):
    """
    getSubredditNames
    """

    subreddit_names = [
        str(subreddit) 
        for subreddit in input.replace(" ", "").split(",")
    ]

    return subreddit_names

def getSearchWords(input):
    """
    getSearchWords
    """

    searchWords = []
    newSearchWords = input.lower().split(",")
    newSearchWords = [str(searchWord.lstrip()) for searchWord in newSearchWords]
    searchWords.append(newSearchWords)
    return searchWords

def getFrequency(input):
    """
    getFrequency
    """

    frequency = float(input)
    return frequency

def getRecipient(input):
    """
    getRecipient
    """

    recipient = str(input)
    return recipient

#----------------------------------------------------------------------------#
# Compile Related Functions
#----------------------------------------------------------------------------#

def printFunction(file, function):
    """
    printFunction
    """

    for line in inspect.getsourcelines(function)[0]:
        file.write(str(line))

def compileBotCore(subreddit_names, search_words, frequency, recipient, 
    type="comment", action="print", hash_digest="AACompiled"):
    """
    compileBotCore
    """

    filePath = '/var/www/Flask/RedditBot/static/bots/%s.py' % hash_digest

    if not os.path.isfile(filePath):
        # If it's not there, create it
        try:
            file = open('/var/www/Flask/RedditBot/static/bots/%s.py' % hash_digest, 'w+')
        except IOError:
            # Log an exception
            return

        # Imports
        print >> file, 'import praw'
        print >> file, 'import time'
        print >> file, 'from tqdm import *'
        print >> file, 'subreddit_names = ', subreddit_names
        print >> file, 'search_words = ', search_words
        print >> file, 'frequency = {}'.format(frequency)
        print >> file, 'recipient = "{}"'.format(recipient)

        # boilerplate functions
        printFunction(file, throwError)
        printFunction(file, botInit)
        printFunction(file, eval(action + "Response"))

        # title search
        if(type is "title_comment"):
            printFunction(file, titleSearch)

        # Searchbot and runBot
        printFunction(file, eval(type + "Search"))
        printFunction(file, SearchBot)
        printFunction(file, runBot)

        # App start code
        print >> file, 'if __name__ == "__main__":'
        print >> file, "    runBot(%s, %s, %s, %s, %s, %s)" % (
                "subreddit_names",
                "search_words",
                "frequency",
                "recipient",
                type,
                action
            )
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
    """
    botInit
    """

    r = praw.Reddit('RedditBot generator v1 by /u/syserror')

    try:
        if auto:
            r.login(username, password)
        else:
            r.login()
    except praw.errors.InvalidUserPass as err:
        throwError(err)
    return r

def runBot(subreddit_names, searchWords, frequency, recipient, type, action):
    """
    runBot
    """

    r = botInit("none", "none", False)
    SearchBot(r, subreddit_names, searchWords, frequency, recipient, type, 
        action)

#-------------------------------------#
# Result related
#-------------------------------------#

def printResponse(results,r = 0, recipient = "none"):
    for result in results:
        print result

def messageResponse(results, r, recipient):
    for result in results:
        r.user.send_message(recipient, result)

def respondResponse(results, r = 0, recipient = "none"):
    for result in results:
        result.reply("test")

#-------------------------------------#
# Search related
#-------------------------------------#

def titleSearch(r, subreddit_names, searchWords, firstPass, already_done=[]):
    """
    titleSearch
    """

    #
    if firstPass:
        first_results = []
    results = []

    #
    for subreddit_name in subreddit_names:
        for searchWord in searchWords:
            subreddit = r.get_subreddit(subreddit_name)

            #
            try:
                getHot    = tqdm(subreddit.get_hot(limit=100))
                nameTuple = (("searching:{}".format(subreddit_name)), 100, 
                    False)

                #
                for submission in getHot, nameTuple:

                    title_text = submission.title.lower()
                    has_text   = any(
                        string in title_text for string in searchWord)

                    #
                    if submission.id not in already_done and has_text:
                        if not firstPass:
                            msg = '[NEW FIND IN: %s] %s (%s)' % (
                                    subreddit_name.upper(),
                                    submission.title,
                                    submission.short_link
                                )
                            results.append(msg)
                        else:
                            first_results.append("%s :: %s :: %s" %(
                                    subreddit_name.upper(),
                                    submission.title,
                                    submission.short_link
                                ))
                        already_done.append(submission.id)
            except praw.errors.InvalidSubreddit as err:
                throwError(err,False)

    # Return result as a dictionary of new results and results that have already
    # been done
    if firstPass:
        return {'first_results':first_results , 'already_done':already_done}
    return {'results':results , 'already_done':already_done}

def commentSearch(r, subreddit_names, searchWords, firstPass, already_done=[]):
    """
    commentSearch

    """

    searchWords = searchWords[0]
    if firstPass:
        first_results = []
    results = []

    # Iterate over subreddits
    for subreddit_name in subreddit_names:

        subreddit = r.get_subreddit(subreddit_name)
        getHot    = tqdm(subreddit.get_hot(limit=100))
        nameTuple = (("searching:{}".format(subreddit_name)),100, False)

        for submission in getHot, nameTuple:
            full_submission = r.get_submission(submission_id=submission.id)
            full_submission.replace_more_comments(limit=16, threshold=10)
            flat_comments = praw.helpers.flatten_tree(full_submission.comments)

            for comment in flat_comments:
                if not hasattr(comment, 'body'):
                    continue

                comment_text = comment.body.split()

                for searchWord in searchWords:
                    for comment_word in comment_text:

                        swLower = searchWord.lower()
                        cwLower = comment_word.lower()

                        if (swLower == cwLower) and comment.id not in already_done:
                            
                            if not firstPass:
                                results.append(comment)
                            else:
                                first_results.append("%s :: %s :: %s :: %s" % (
                                        subreddit_name.upper(),
                                        submission.title,
                                        submission.short_link,
                                        comment.body
                                    ))

                        already_done.append(comment.id)

    # Return result as a dictionary of new results and results that have already
    # been done
    if firstPass:
        return {'first_results' : first_results, 'already_done'  : already_done}
    return {'results' : results, 'already_done' : already_done}

def title_commentSearch(r, subreddit_names, searchWords, first_pass, 
    already_done=[]):
    """
    title_commentSearch
    """
    results        = titleSearch(r, subreddit_names, searchWords, True)
    submission_ids = results['already_done']

    for submission_id in submission_ids:
        submission    = r.get_submission(submission_id=submission_id)
        flat_comments = praw.helpers.flatten_tree(submission.comments)

        for comment in flat_comments:
            print "{} :: {}".format(submission.title, comment)

#-------------------------------------#
# Final Bot
#-------------------------------------#

def SearchBot(r, subreddit_names, searchWords, frequency, recipient, type, 
    action):
    """
    SearchBot
    """

    results      = eval(type+ "Search(r, subreddit_names, searchWords, True)")
    already_done = results['already_done']

    eval(action + "Response(results['first_results'], r, recipient)")
    while True:

        # Construct an eval
        # TODO: figure out a way to do this without needing to invoke eval!
        searchEval   = "%s Search(%s, %s, %s, %s, %s)" % (
                type,
                "r", 
                "subreddit_names", 
                "searchWords", 
                "False", 
                "already_done"
            )

        results      = eval(searchEval)
        already_done = results['already_done']
        eval(action + "Response(results['results'], r, recipient)")

        # Wait for 20 seconds before next interval
        time.sleep(max(frequency,20))