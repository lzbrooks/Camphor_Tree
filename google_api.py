import base64
from email.mime.text import MIMEText

import requests as requests

from config import Config

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
# if os.path.exists('token.json'):
#     creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# Service endpoint
# "https://gmail.googleapis.com"
# Sends the specified message to the recipients in the To, Cc, and Bcc headers.
# POST
# "/gmail/v1/users/{userId}/messages/send"
# POST
# "/upload/gmail/v1/users/{userId}/messages/send"
# Get attachments
# GET
# "/gmail/v1/users/{userId}/messages/{messageId}/attachments/{id}"
# Set up or update a push notification watch on the given user mailbox.
# POST
# "/gmail/v1/users/{userId}/watch"


class GMailMessage:
    def __init__(self, google_client_id=None, google_client_secret=None,
                 message_to=None, message_from=None, message_subject=None, message_text=None):

        # Google Client ID
        if google_client_id is None:
            self.google_client_id = Config.read_config_file()['GOOGLE']['CLIENT_ID']
        else:
            self.google_client_id = google_client_id

        # Google Client Secret
        if google_client_secret is None:
            self.google_client_secret = Config.read_config_file()['GOOGLE']['CLIENT_SECRET']
        else:
            self.google_client_secret = google_client_secret

        # Email Recipient
        if message_to is None:
            self.message_to = Config.read_config_file()['TREE']['Email']
        else:
            self.message_to = message_to

        self.message_from = message_from
        self.message_subject = message_subject
        self.message_text = message_text

        self.auth_key = None
        self.gmail_message = None
        self.gmail_endpoint = None

    def get_key(self):
        url = "https://www.googleapis.com/oauth2/v4/token"
        data = {
            'grant_type': 'client_credentials'
        }
        r = requests.post(url, json=data, auth=(self.google_client_id, self.google_client_secret))
        key = r.json()['access_token']
        self.auth_key = key

    def get_gmail_url(self):
        gmail_endpoint = "https://gmail.googleapis.com"
        user_id = "me"
        self.gmail_endpoint = gmail_endpoint + "/gmail/v1/users/" + user_id + "/messages/send"

    def gmail_create_message(self):
        message = MIMEText(self.message_text)
        message['To'] = self.message_to
        message['From'] = self.message_from
        message['Subject'] = self.message_subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'message': {
                'raw': encoded_message
            }
        }
        self.gmail_message = create_message

    def post_message(self):
        headers = {
            'Authorization': f'Bearer {self.auth_key} ',
            'Accept': 'application / json',
            'Content-Type': 'application/json'
        }
        response = requests.post(self.gmail_endpoint, headers=headers, json=self.gmail_message)
        return response

    def send_gmail_message(self):
        self.get_key()
        self.get_gmail_url()
        self.gmail_create_message()
        return self.post_message()
