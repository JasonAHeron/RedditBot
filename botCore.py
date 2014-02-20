__author__ = 'jason'
import time
import praw
import inspect

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
    printFunction(file, sendResults)
    printFunction(file, searchBot)
    printFunction(file, runBot)
    print >> file, 'if __name__ == "__main__":'
    print >> file, '    runBot(subreddit_names, search_words, frequency, recipient)'
    file.close()

def runBot(subreddit_names, searchWords, frequency, recipient):
    r = botInit("none", "none", False)
    searchBot(r, subreddit_names, searchWords, frequency, recipient)

def printFunction(file, function):
    for line in inspect.getsourcelines(function)[0]:
        file.write(str(line))

def throwError(error = "unhandled", exit=True, code=0):
    print "There was an error: {}".format(error)
    if exit:
        exit(code)

def botInit(username, password, auto=True):
    r = praw.Reddit('PRAW learning and testing v0.3 by /u/syserror')
    try:
        if auto:
            r.login(username, password)
        else:
            r.login()
    except praw.errors.InvalidUserPass as err:
        throwError(err)
    return r

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

def sendResults(r, results, message = False, recipient = "none"):
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
                                results.append(msg)
                            else:
                                first_results.append(subreddit_name.upper() + " :: " + submission.title + " :: " + submission.short_link)
                            already_done.append(submission.id)
                except praw.errors.InvalidSubreddit as err:
                    throwError(err,False)
        if firstPass:
            sendResults(r, first_results)
        sendResults(r, results, True, recipient)
        firstPass = False
        time.sleep(max(frequency,20))