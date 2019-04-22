import reddit_controller
import gmailClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import logging.config

logging.basicConfig(filename="app.log", filemode="w", format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    level=logging.INFO, datefmt="%d-%b-%y %H:%M:%S")

gmailUsername = os.environ.get('GMAIL_USERNAME')
gmailPassword = os.environ.get('GMAIL_PASSWORD')
gmailReceiverUsername = os.environ.get('GMAIL_RECEIVER_USERNAME')

gmailClient = gmailClient.getGmailClient(gmailUsername, gmailPassword)
redditClient = reddit_controller.getRedditClient()

recentlyViewed = []
try:
    recentFile = open('.recentlyViewed', 'r')
    logging.info("Adding the contents of .recentlyViewed to restrict our process request")
    for id in recentFile:
        recentlyViewed.append(id[:-1])

except FileNotFoundError:
    logging.warning("Unabled to find the recentlyViewid files when starting a process request")

redditDigest, touchedSubmissions = reddit_controller.processSavedRedditSubmission(redditClient, recentlyViewed)

if len(touchedSubmissions) > 0:
    try:
        logging.info("Writing the recently viewed ID's")
        recentFile = open('.recentlyViewed', 'w')
        for id in touchedSubmissions:
            recentFile.write(id + "\n")
    except Exception:
        logging.warning("Unable to write the recently viewed ID's %s", Exception)

if not redditDigest:
    redditDigest = "No new content for you to view today! Have a great day!"

msg = MIMEMultipart('alternative')
msg['Subject'] = "Daily Reddit Digest"
msg['From'] = gmailUsername
msg['To'] = gmailReceiverUsername
messageBody = MIMEText(redditDigest, 'plain')
msg.attach(messageBody)

gmailClient.sendmail(gmailUsername, gmailReceiverUsername, msg.as_string())