import logging
from .email_sender import send_email


def main() -> None:
    logging.info('Starting the main function')
    
    email_sent = send_email("Testing")
    if email_sent:
        logging.info('Email sent successfully')
    else:
        logging.error('Failed to send email')