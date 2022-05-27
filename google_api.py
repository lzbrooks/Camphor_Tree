import base64
import json
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
        self.refresh_token = Config.get_google_refresh_token()

        # Google Pub/Sub Topic
        self.google_topic = Config.get_google_topic()

        # Email Recipient
        if message_to is None:
            self.message_to = Config.get_email()
        else:
            self.message_to = message_to

        # Email Sender
        if message_from is None:
            self.message_from = Config.get_email()
        else:
            self.message_from = message_from
        self.message_subject = message_subject
        self.message_text = message_text

        self.new_gmail_messages = []
        self.max_message_size = Config.get_max_message_size()

        self.auth_token = None
        self.get_auth_token()
        self.gmail_message = None
        self.gmail_endpoint = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
        self.gmail_history_endpoint = "https://gmail.googleapis.com/gmail/v1/users/me/history"
        self.gmail_get_message_endpoint = "https://gmail.googleapis.com/gmail/v1/users/me/messages/"
        self.watch_endpoint = "https://gmail.googleapis.com/gmail/v1/users/me/watch"
        self.api_headers = {
            'Authorization': f'Bearer {self.auth_token} ',
            'Accept': 'application / json',
            'Content-Type': 'application/json'
        }

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

    def gmail_create_message(self):
        message = MIMEText(self.message_text)
        message['To'] = self.message_to
        message['From'] = self.message_from
        message['Subject'] = self.message_subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {
            'raw': encoded_message
        }
        self.gmail_message = create_message

    def post_message(self):
        response = requests.post(self.gmail_endpoint, headers=self.api_headers, json=self.gmail_message)
        return response

    def send_gmail_message(self):
        self.gmail_create_message()
        return self.post_message()

    def gmail_get_messages_from_push(self, encoded_push_message):
        push_message = base64.urlsafe_b64decode(encoded_push_message)
        json_push_message = json.loads(push_message)
        history_id = json_push_message['historyId']
        print("New GMail Push HistoryId: " + str(history_id))
        query_params = {'startHistoryId': str(history_id)}
        response = requests.get(self.gmail_history_endpoint, headers=self.api_headers, params=query_params)
        print(response.json())
        if 'history' in response.json():
            # 'messagesAdded': [{'message':
            #     {'id': '18100f73879a9d43', 'threadId': '18100f73879a9d43', 'labelIds': ['DRAFT']}
            #     }]
            self.new_gmail_messages = [message['messagesAdded'][0]['message'] for message in response.json()['history']
                                       if 'messagesAdded' in message]
            print("New Messages: ")
            [print(message) for message in self.new_gmail_messages]

    def gmail_get_message_by_id(self, message):
        get_message_endpoint = self.gmail_get_message_endpoint + str(message['id'])
        response = requests.get(get_message_endpoint, headers=self.api_headers)
        message_from = None
        message_subject = None
        message_text = None
        if 'payload' in response.json():
            message_payload = response.json()['payload']
            print("New Message Payload: " + message_payload)
            for header in message_payload['headers']:
                if header['name'] == 'From':
                    message_from = header['value']
                if header['name'] == 'Subject':
                    message_subject = header['value']
            size_in_bytes = message_payload['body']['size']
            if size_in_bytes < int(self.max_message_size) and 'data' in message_payload['body']:
                message_text = base64.urlsafe_b64decode(message_payload['body']['data'])
            # TODO: if size bigger and from whitelist, send in multiple emails instead
        print("New Message Processed:")
        print(message_from)
        print(message_subject)
        print(message_text)
        return message_from, message_subject, message_text

    def gmail_re_watch(self):
        print("Starting GMail Re-Watch...")
        request_body = {
            'labelIds': ['INBOX'],
            'labelFilterAction': 'include',
            'topicName': self.google_topic
        }
        response = requests.post(self.watch_endpoint, headers=self.api_headers, json=request_body)
        if 'historyId' in response.json():
            print("GMail Re-Watch Success")
        else:
            print("Gmail Re-Watch Failure")


# TODO: cron every day
if __name__ == "__main__":
    gmail_re_watch = GMailMessage()
    gmail_re_watch.gmail_re_watch()
