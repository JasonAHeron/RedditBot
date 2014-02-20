import praw
import time
subreddit_names =  ['hardwareswap', 'buildapcsales']
search_words =  [['$250', 'I']]
frequency = 20.0
recipient = "111qq"
def throwError(error = "unhandled", exit=True, code=0):
    print "There was an error: {}".format(error)
    if exit:
        exit(code)
def botInit(username, password, auto=True):
    r = praw.Reddit('PRAW learning and testing v0.5 by /u/syserror')
    try:
        if auto:
            r.login(username, password)
        else:
            r.login("111qq","9175Rape")
    except praw.errors.InvalidUserPass as err:
        throwError(err)
    return r
def outputResults(r, results, message = False, recipient = "none"):
    if message:
        for result in results:
            r.user.send_message(recipient, result)
    else:
        for result in results:
            print result
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

                
def titleSearchBot(r, subreddit_names, searchWords, frequency, recipient):
    commentSearch(r, subreddit_names, searchWords, True)
    already_done = results['already_done']
    outputResults(r, results['first_results'])
    while True:
        results = titleSearch(r, subreddit_names, searchWords, False, already_done)
        already_done = results['already_done']
        outputResults(r, results['results'], True, recipient)
        time.sleep(max(frequency,20))
def runBot(subreddit_names, searchWords, frequency, recipient):
    r = botInit("none", "none", False)
    titleSearchBot(r, subreddit_names, searchWords, frequency, recipient)
if __name__ == "__main__":
    runBot(subreddit_names, search_words, frequency, recipient)
