import praw
import time
from tqdm import *
subreddit_names =  ['hardwareswap']
search_words =  [['$250']]
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
            r.login()
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
    searchWords = searchWords[0]
    if firstPass:
        first_results = []
    results = []
    for subreddit_name in subreddit_names:
        subreddit = r.get_subreddit(subreddit_name)
        for submission in tqdm(subreddit.get_hot(limit=100),"comments",100):
            full_submission = r.get_submission(submission_id=submission.id)
            full_submission.replace_more_comments(limit=16, threshold=10)
            flat_comments = praw.helpers.flatten_tree(full_submission.comments)
            for comment in flat_comments:
                if not hasattr(comment, 'body'):
                    continue
                comment_text = comment.body.split()
                for searchWord in searchWords:
                    for comment_word in comment_text:
                        if (searchWord.lower() == comment_word.lower()) and comment.id not in already_done:
                            if not firstPass:
                                results.append(comment)
                            else:
                                first_results.append(subreddit_name.upper() + " :: " + submission.title + " :: " + submission.short_link + "\n" + "    :: " + comment.body)
                            already_done.append(comment.id)
    if firstPass:
        return {'first_results':first_results , 'already_done':already_done}
    return {'results':results , 'already_done':already_done}
def commentSearchBot(r, subreddit_names, searchWords, frequency, recipient):
    results = commentSearch(r, subreddit_names, searchWords, True)
    already_done = results['already_done']
    outputResults(r, results['first_results'])
    while True:
        results = commentSearch(r, subreddit_names, searchWords, False, already_done)
        already_done = results['already_done']
        outputResults(r, results['results'], True, recipient)
        time.sleep(max(frequency,20))
def runBot(subreddit_names, searchWords, frequency, recipient):
    r = botInit("none", "none", False)
    commentSearchBot(r, subreddit_names, searchWords, frequency, recipient)
if __name__ == "__main__":
    runBot(subreddit_names, search_words, frequency, recipient)
