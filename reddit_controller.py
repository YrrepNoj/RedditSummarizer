import praw
import logging.config
import os
import smmry_wrapper
import pprint

logging.basicConfig(filename="app.log", filemode="w", format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    level=logging.INFO, datefmt="%d-%b-%y %H:%M:%S")
def getRedditClient():
    redditUsername = os.environ.get('REDDIT_USERNAME')
    redditPassword = os.environ.get('REDDIT_PASSWORD')
    redditUserAgent = os.environ.get('REDDIT_USER_AGENT')
    redditClientSecret = os.environ.get('REDDIT_CLIENT_SECRET')
    redditClientID = os.environ.get('REDDIT_CLIENT_ID')

    logging.info("Logged in as user (%s).." % redditUsername)
    redditClient = praw.Reddit(client_id=redditClientID,
                               client_secret=redditClientSecret,
                               password=redditPassword,
                               user_agent=redditUserAgent,
                               username=redditUsername)

    return redditClient

#TODO: Add remaining api calls to the end of the digest
def processSavedRedditSubmission(redditClient):

    digest = ""
    unsummarizedSubmissions = []
    for submission in redditClient.redditor(redditClient.user.me().name).saved(limit=15):

        if isinstance(submission, praw.models.Submission):
            summarization = None

            submission.unsave();
            submission.save("ReadLater")

            if submission.is_self and len(submission.selftext.split()) > 400:
                logging.info("Summarizing a selfpost")
                summarization = smmry_wrapper.summarizeText(submission.selftext)

            elif not submission.is_self:
                logging.info("summarizing a linkpost")
                summarization = smmry_wrapper.summerizeURL(submission.url)
            else:
                # A selfpost that was not long enough for us to consider summarizing
                unsummarizedSubmissions.append(submission)

            if(summarization):
                if(summarization.getErrorCode()):
                    logging.warning("Unable to summarize submission %s : %s. Error Code: %s",
                                    submission.shortlink, submission.title, summarization.getErrorCode())
                    unsummarizedSubmissions.append(submission)
                    continue
                digest += "Reddit Submission Title: " + submission.title
                articalTitle = summarization.getTitle()
                if articalTitle:
                    digest += "\nArticle Title: " + articalTitle
                percentageReduced = summarization.getPercentageReduced()
                if percentageReduced:
                    digest += "\nText Reduced By: " + percentageReduced
                summarizedText = summarization.getSummarizedText()

                digest += "\nReddit Link: " + submission.shortlink

                if(not submission.is_self):
                    digest += "\nArticle Link: " + submission.url

                if summarizedText:
                    sentences = summarizedText.split('\n ')
                    digest += "\n" + summarizedText
                digest += "\n" + "---------------------------------------------------------------\n\n"
            else:
                logging.warning("Unable to summarize submission %s", submission.title)

    # Add all of the unsummarized submissions to the end of the list
    if len(unsummarizedSubmissions) > 0:
        digest += "\n\n--------------Unsummarized Submissions--------------"
        for submission in unsummarizedSubmissions:
            digest += "\n" + submission.title + "  :  " + submission.shortlink
    return digest
