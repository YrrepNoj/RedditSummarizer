import praw
import logging.config
import os
import smmry_wrapper

logging.basicConfig(filename="app.log", filemode="w", format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    level=logging.INFO, datefmt="%d-%b-%y %H:%M:%S")

redditUsername = os.environ.get('REDDIT_USERNAME')
redditPassword = os.environ.get('REDDIT_PASSWORD')
redditUserAgent = os.environ.get('REDDIT_USER_AGENT')
redditClientSecret = os.environ.get('REDDIT_CLIENT_SECRET')
redditClientID = os.environ.get('REDDIT_CLIENT_ID')
lastPostSummerized = os.environ.get('REDDIT_LAST_POST')


redditClient = praw.Reddit(client_id=redditClientID,
                           client_secret=redditClientSecret,
                           password=redditPassword,
                           user_agent=redditUserAgent,
                           username=redditUsername)

logging.info("Logged in as user (%s).." % redditUsername)

bigString = ""
for submission in redditClient.redditor(redditUsername).upvoted(limit=10):
    if submission.id == lastPostSummerized:
        break

    if submission.is_self and len(submission.selftext.split()) > 400:
        print(len(submission.selftext.split()))
        logging.info("Summarizing a selfpost")
        summarization = smmry_wrapper.summarizeText(submission.selftext)

    elif not submission.is_self:
        logging.info("summarizing a linkpost")
        summarization = smmry_wrapper.summerizeURL(submission.url)

    if(summarization):
        print(submission.title)
        print(summarization.summarizationMap)
    else:
        logging.warning("Unable to summarize submission %s", submission.title)

    print("\n\n")
