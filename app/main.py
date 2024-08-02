import logging
from .email_sender import send_email
from .data_fetcher import fetch_data
from .data_processor import generate_email_content
import os

EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')

def main() -> None:
    logging.info('Starting the main function')
    logging.info('Fetching data of interest')

    # hardcoded for now  
    cities = ['Sydney', 'Houston']
    
    # Fetch the raw data
    raw_data = fetch_data(cities)
    
    # Process the raw data to create the HTML content
    email_html_content = generate_email_content(raw_data)
    email_text_content = 'Please view this email in HTML format to see the latest news updates.'

    # Send the email with the processed content
    email_sent = send_email(
        to_addresses=EMAIL_RECIPIENT.split(','),
        subject="Latest News Update", 
        body_text=email_text_content, 
        body_html=email_html_content
    )

    if email_sent:
        logging.info('Email sent successfully')
    else:
        logging.error('Failed to send email')

if __name__ == '__main__':
    main()
