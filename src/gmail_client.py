"""This script gets a gmail client through smtp"""

import logging.config
import smtplib

logging.basicConfig(filename="app.log", filemode="a",
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    level=logging.INFO, datefmt="%d-%b-%y %H:%M:%S")


def get_gmail_client(gmail_username, gmail_password):
    """Attempts to get a gmail smtp client"""
    logging.info("Connecting to smtplib server")
    email_client = None
    try:
        email_client = smtplib.SMTP("smtp.gmail.com", 587)
        email_client.ehlo()
        email_client.starttls()
        email_client.login(gmail_username, gmail_password)
    except smtplib.SMTPException as error:
        logging.error("Unable to connect to smtplib server: %s", error)

    return email_client
