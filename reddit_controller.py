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
for submission in redditClient.redditor(redditUsername).upvoted(limit=5):
    if submission.id == lastPostSummerized:
        break

    if submission.is_self and len(submission.selftext) > 1000:
        logging.info("Summarizing a selfpost")
        summary = smmry_wrapper.summarizeText(submission.selftext)

    else:
        logging.info("summarizing a linkpost")
        summary = smmry_wrapper.summerizeURL(submission.url)

    if(summary):
        print(submission.title)
        print(summary['sm_api_content'])
    else:
        logging.warning("Unable to summarize submission %s", submission.title)

    print("\n\n")
