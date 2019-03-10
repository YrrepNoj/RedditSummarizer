import reddit_controller
import gmailClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os
gmailUsername = os.environ.get('GMAIL_USERNAME')
gmailPassword = os.environ.get('GMAIL_PASSWORD')
gmailReceiverUsername = os.environ.get('GMAIL_RECEIVER_USERNAME')

gmailClient = gmailClient.getGmailClient(gmailUsername, gmailPassword)
redditClient = reddit_controller.getRedditClient()

redditDigest = reddit_controller.processSavedRedditSubmission(redditClient)

print(redditDigest)

msg = MIMEMultipart('alternative')
msg['Subject'] = "Daily Reddit Digest"
msg['From'] = gmailUsername
msg['To'] = gmailReceiverUsername
messageBody = MIMEText(redditDigest, 'plain')
msg.attach(messageBody)

gmailClient.sendmail(gmailUsername, gmailReceiverUsername, msg.as_string())