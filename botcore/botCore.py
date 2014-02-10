__author__ = 'rita'
DEBUG = True
import time
import praw
import string


def throwError(error = "unhandled", exit=True, code=0):
    print "There was an error: {}".format(error)
    if exit:
        exit(code)

def botInit(username, password):
    r = praw.Reddit('PRAW learning and testing v0.2 by /u/derrideaninc based on v0.1 by /u/syserror')
    try:
        r.login(username,password)
    except praw.errors.InvalidUserPass as err:
        throwError(err)
    return r

def getSubredditNames():
    subreddit_names = raw_input("Subreddit(s) to search (example: buildapcsales for /r/buildapcsales)\n"
                            "For multiple subreddits, separate by commas: ").replace(" ", "").split(",")
    return subreddit_names

def getSearchWords():
    searchWords = []
    newSearchWords = (raw_input("Search for (example: monitor): ").lower().split(","))
    newSearchWords = [searchWord.lstrip() for searchWord in newSearchWords]
    searchWords.append(newSearchWords)
    return searchWords

def getFrequency():
    frequency = int(raw_input("Page refresh rate in seconds (be nice to reddit, min 20sec): "))
    return frequency

def getRecipient():
    recipient = raw_input("Who should I reddit message my results to (example: jason for /u/jason): ")
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


searchBot(botInit(),getSubredditNames(),getSearchWords(),getFrequency(),getRecipient())