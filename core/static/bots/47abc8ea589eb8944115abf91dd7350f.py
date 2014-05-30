import praw
import time
from tqdm import *
subreddit_names =  ['test']
search_words =  [['test']]
frequency = 20.0
recipient = "test"
def throwError(error = "unhandled", exit=True, code=0):
    print "There was an error: {}".format(error)
    if exit:
        exit(code)
def botInit(username, password, auto=True):
    r = praw.Reddit('RedditBot generator v1 by /u/syserror')
    try:
        if auto:
            r.login(username, password)
        else:
            r.login()
    except praw.errors.InvalidUserPass as err:
        throwError(err)
    return r
def printResponse(results,r = 0, recipient = "none"):
    for result in results:
        print result
def titleSearch(r, subreddit_names, searchWords, firstPass, already_done=[]):
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
def runBot(subreddit_names, searchWords, frequency, recipient, type, action):
    r = botInit("none", "none", False)
    SearchBot(r, subreddit_names, searchWords, frequency, recipient, type, 
        action)
if __name__ == "__main__":
    runBot(subreddit_names, search_words, frequency, recipient, title, print)
