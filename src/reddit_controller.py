#!/usr/bin/env python
"""Utility made using the PRAW library to get saved Reddit Submissions from a users account."""

import logging.config

import praw
import smmry_wrapper
from account_info import *

logging.basicConfig(filename="app.log", filemode="a",
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    level=logging.INFO, datefmt="%d-%b-%y %H:%M:%S")


def get_reddit_client():
    """Utility to get a Reddit Client"""
    reddit_username = redditUsername
    reddit_password = redditPassword
    reddit_user_agent = redditUserAgent
    reddit_client_secret = redditClientSecret
    reddit_client_id = redditClientID

    logging.info("Logged in as user (%s).." % reddit_username)
    reddit_client = praw.Reddit(client_id=reddit_client_id,
                                client_secret=reddit_client_secret,
                                password=reddit_password,
                                user_agent=reddit_user_agent,
                                username=reddit_username)
    return reddit_client


def process_saved_reddit_submission(reddit_client, recently_viewed):
    """Utility to get a list of Reddit Submissions that have been saved by the client"""
    digest = ""
    touched_submissions = []
    unsummarized_submissions = []
    for submission in reddit_client.redditor(reddit_client.user.me().name).saved(limit=25):
        if submission.id in recently_viewed:
            logging.info("Reached a submission that we have processed before. Stopping now.")
            break

        touched_submissions.append(submission.id)
        if isinstance(submission, praw.models.Submission):
            summarization = None

            submission.unsave()
            submission.save("ReadLater")

            if submission.is_self and len(submission.selftext.split()) > 400:
                logging.info("Summarizing a selfpost")
                summarization = smmry_wrapper.summerize_url(submission.url)

            elif not submission.is_self:
                logging.info("summarizing a linkpost")
                summarization = smmry_wrapper.summerize_url(submission.url)
            else:
                # A selfpost that was not long enough for us to consider summarizing
                unsummarized_submissions.append(submission)

            if summarization:
                if summarization.get_error_code():
                    logging.warning("Unable to summarize submission %s : %s. Error Code: %s",
                                    submission.shortlink, submission.title,
                                    summarization.get_error_code())
                    unsummarized_submissions.append(submission)
                    continue
                digest += "Reddit Submission Title: " + submission.title
                artical_title = summarization.get_title()
                if artical_title:
                    digest += "\nArticle Title: " + artical_title
                percentage_reduced = summarization.get_percentage_reduced()
                if percentage_reduced:
                    digest += "\nText Reduced By: " + percentage_reduced
                summarized_text = summarization.get_summarized_text()

                digest += "\nReddit Link: " + submission.shortlink

                if not submission.is_self:
                    digest += "\nArticle Link: " + submission.url

                if summarized_text:
                    digest += "\n" + summarized_text
                digest += "\n" + "------------------------------------------------------------\n\n"
            else:
                logging.warning("Unable to summarize submission %s", submission.title)

    # Add all of the unsummarized submissions to the end of the list
    if unsummarized_submissions:
        digest += "\n\n--------------Unsummarized Submissions--------------"
        for submission in unsummarized_submissions:
            digest += "\n" + submission.title + "  :  " + submission.shortlink
    return digest, touched_submissions
