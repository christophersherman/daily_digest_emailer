import logging
from azure.communication.email import EmailClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

load_dotenv()
ACS_ENDPOINT = os.getenv('ACS_ENDPOINT')
ACS_API_KEY = os.getenv('ACS_API_KEY')
SENDER_ADDRESS = os.getenv('SENDER_ADDRESS')

def send_email(to_addresses, subject, body_text, body_html=None):
    if not ACS_ENDPOINT or not ACS_API_KEY:
        logging.error('ACS endpoint or API key not found in environment variables')
        return False

    try:
        # Initialize the Email Client
        email_client = EmailClient(ACS_ENDPOINT, AzureKeyCredential(ACS_API_KEY))

        # Create the email message
        message = {
            "senderAddress": SENDER_ADDRESS,
            "content": {
                "subject": subject,
                "plainText": body_text,
                "html": body_html
            },
            "recipients": {
                "to": [{"address": address} for address in to_addresses]
            },
        }

        # Send the email
        poller = email_client.begin_send(message)
        result = poller.result()
        logging.info(f'Email sent successfully: {result}')
        return True

    except Exception as e:
        logging.error(f'Failed to send email: {str(e)}')
        return False

if __name__ == '__main__':
    to_addresses = ['crsherman98@gmail.com']
    subject = 'Test Email'
    body_text = 'This is a test email sent from Azure Functions using Azure Communication Services.'
    body_html = '<p>This is a <strong>test email</strong> sent from Azure Functions using Azure Communication Services.</p>'

    send_email(to_addresses, subject, body_text, body_html)
