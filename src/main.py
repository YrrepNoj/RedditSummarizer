#!/usr/bin/env python
"""Creates a digest from a users saved Reddit submissions & emails digest to user"""

import logging.config
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import gmail_client
import reddit_controller

logging.basicConfig(filename="app.log", filemode="a",
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    level=logging.INFO, datefmt="%d-%b-%y %H:%M:%S")

GMAIL_USERNAME = os.environ.get('GMAIL_USERNAME')
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
GMAIL_RECEIVER_USERNAME = os.environ.get('GMAIL_RECEIVER_USERNAME')

# GMAIL_CLIENT = get_mail_client(GMAIL_USERNAME, GMAIL_PASSWORD)
GMAIL_CLIENT = gmail_client.get_gmail_client(GMAIL_USERNAME, GMAIL_PASSWORD)
REDDIT_CLIENT = reddit_controller.get_reddit_client()

RECENTLY_VIEWED = []
try:
    RECENT_FILE = open('.recently_viewed', 'r')
    logging.info("Adding the contents of .RECENTLY_VIEWED to restrict our process request")
    for submission_id in RECENT_FILE:
        RECENTLY_VIEWED.append(submission_id[:-1])

except FileNotFoundError:
    logging.warning("Unabled to find the recentlyViewid files when starting a process request")

REDDIT_DIGEST, TOUCHED_SUBMISSIONS = reddit_controller.process_saved_reddit_submission(
    REDDIT_CLIENT,
    RECENTLY_VIEWED)
if TOUCHED_SUBMISSIONS:
    try:
        logging.info("Writing the recently viewed ID's")
        RECENT_FILE = open('.recently_viewed', 'w')
        for submission_id in TOUCHED_SUBMISSIONS:
            RECENT_FILE.write(submission_id + "\n")
    except Exception:
        logging.warning("Unable to write the recently viewed ID's %s", Exception)

if not REDDIT_DIGEST:
    REDDIT_DIGEST = "No new content for you to view today! Have a great day!"

MESSAGE = MIMEMultipart('alternative')
MESSAGE['Subject'] = "Daily Reddit Digest"
MESSAGE['From'] = GMAIL_USERNAME
MESSAGE['To'] = GMAIL_RECEIVER_USERNAME
MESSAGE_BODY = MIMEText(REDDIT_DIGEST, 'plain')
MESSAGE.attach(MESSAGE_BODY)

GMAIL_CLIENT.sendmail(GMAIL_USERNAME, GMAIL_RECEIVER_USERNAME, MESSAGE.as_string())
