import base64
from email.mime.text import MIMEText

import requests as requests

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
from config import Config


class GMailMessage:
    def __init__(self, google_client_id=None, google_client_secret=None,
                 message_to=None, message_from=None, message_subject=None, message_text=None):

        # Google Client ID
        if google_client_id is None:
            self.google_client_id = Config.get_google_id()
        else:
            self.google_client_id = google_client_id

        # Google Client Secret
        if google_client_secret is None:
            self.google_client_secret = Config.get_google_secret()
        else:
            self.google_client_secret = google_client_secret

        # Google Refresh Token
        self.refresh_token = Config.get_refresh_token()

        # Email Recipient
        if message_to is None:
            self.message_to = Config.get_email()
        else:
            self.message_to = message_to

        self.message_from = message_from
        self.message_subject = message_subject
        self.message_text = message_text

        self.auth_token = None
        self.gmail_message = None
        self.gmail_endpoint = None

    def get_auth_token(self):
        url = "https://oauth2.googleapis.com/token"
        data = {
            'client_id': self.google_client_id,
            'client_secret': self.google_client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        r = requests.post(url, json=data)
        key = r.json()['access_token']
        self.auth_token = key

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
            'Authorization': f'Bearer {self.auth_token} ',
            'Accept': 'application / json',
            'Content-Type': 'application/json'
        }
        response = requests.post(self.gmail_endpoint, headers=headers, json=self.gmail_message)
        return response

    def send_gmail_message(self):
        self.get_auth_token()
        self.get_gmail_url()
        self.gmail_create_message()
        return self.post_message()
