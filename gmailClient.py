import os
import smtplib
import logging.config

logging.basicConfig(filename="app.log", filemode="w", format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s", level=logging.INFO, datefmt="%d-%b-%y %H:%M:%S")

def getGmailClient(gmailUsername, gmailPassword):
    logging.info("Connecting to smtplib server")
    try:

        emailClient = smtplib.SMTP("smtp.gmail.com", 587)
        emailClient.ehlo()
        emailClient.starttls()
        emailClient.login(gmailUsername, gmailPassword)
    except:
        logging.error("Unable to connect to smtplib server")

    return emailClient
