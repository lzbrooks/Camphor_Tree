from __future__ import print_function

import os.path

import re
import base64
from email.message import EmailMessage
from typing import Tuple
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.config import Config

_logger = logging.Logger(__name__)


class GMailAPI:
    def __init__(self, message_to=None, message_from=None, message_subject=None, message_text=None):
        self.creds = None
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        self.google_topic = Config.get_google_topic()

        self.new_gmail_message = None

        self.max_message_size = Config.get_max_message_size()

        self.message_to = Config.get_email(message_to)
        self.message_from = Config.get_email(message_from)
        self.message_subject = message_subject
        self.message_text = message_text
        self.gmail_message = None

    def get_top_inbox_message(self):
        try:
            with build('gmail', 'v1', credentials=self.creds) as service:
                message_list = service.users().messages().list(userId='me', maxResults='1').execute().json()
        except HttpError as error:
            print(f'An error occurred: {error}')
        if 'messages' in message_list:
            self.new_gmail_message = message_list['messages'][0]

    def send_gmail_message(self):
        """Create and send an email message
        Print the returned  message id
        Returns: Message object, including message id

        Load pre-authorized user credentials from the environment
        """
        self.get_creds()
        self.create_gmail_message()
        try:
            with build('gmail', 'v1', credentials=self.creds) as service:
                if self.gmail_message:
                    print("Sending GMail Message")
                    return (service.users().messages().send
                                    (userId="me", body=self.gmail_message).execute())
                print("No GMail Message to Send")
        except HttpError as error:
            print(f'An error occurred: {error}')

    def create_gmail_message(self):
        if self.message_to:
            message = EmailMessage()
            message['To'] = ", ".join(self.message_to)
            message['From'] = self.message_from
            message['Subject'] = self.message_subject
            message.set_content(self.message_text)
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {
                'raw': encoded_message
            }
            self.gmail_message = create_message

    def gmail_get_message_by_id(self, message):
        with build('gmail', 'v1', credentials=self.creds) as service:
            response_json = service.users().messages().get(userId='me', id=str(message['id'])).execute().json()
            print("GMail Message Attained by ID")
            send_message = True
            if 'DRAFT' in response_json['labelIds'] or 'SENT' in response_json['labelIds']:
                send_message = False
            if 'payload' in response_json and send_message:
                return self._dissect_message(response_json["payload"])
            print("GMail Message Dissected")
            return None, None, None

    def _dissect_message(self, message_payload) -> Tuple[str, str, str]:
        _logger.info(f"Dissecting message:\n{message_payload}")
        message_from, message_subject = self._dissect_message_headers(message_payload)
        message_text = self._dissect_message_parts(message_from, message_payload)
        print("GMail Message Dissected")
        return message_from, message_subject, message_text

    @staticmethod
    def _dissect_message_headers(message_payload):
        message_from = None
        message_subject = None
        for header in message_payload['headers']:
            if header['name'] == 'From':
                message_from = re.search(r'(?<=<).*?(?=>)', header['value']).group()
            if header['name'] == 'Subject':
                message_subject = header['value']
        return message_from, message_subject

    def _dissect_message_parts(self, message_from, message_payload):
        message_text = None
        message_parts = message_payload.get('parts', [message_payload])
        for message_part in message_parts:
            if 'mimeType' in message_part and message_part['mimeType'] == 'text/plain' \
                    and 'size' in message_part['body'] \
                    and 'data' in message_part['body']:
                size_in_bytes = message_part['body']['size']
                print("Inspecting Message Size")
                print("Max Message Size Allowed: " + self.max_message_size)
                print("Current Message Size: " + str(size_in_bytes))
                print("Message From: " + message_from)
                if size_in_bytes < int(self.max_message_size):
                    message_text = base64.urlsafe_b64decode(message_part['body']['data']).decode('utf-8')
                if size_in_bytes > int(self.max_message_size) \
                        and message_from in Config.get_whitelist().values():
                    message_text = base64.urlsafe_b64decode(message_part['body']['data']).decode('utf-8')
        return message_text

    def get_creds(self):
        if os.path.exists('token.json'):
            print("Access Token File Found")
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        else:
            print("Access Token File Not Found")
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("Getting New GMail Access Token...")
                self.creds.refresh(Request())
                print("GMail Access Token Attained")
            else:
                raise ValueError("No Valid Refresh Token")
            self.save_creds_to_file()

    def save_creds_to_file(self):
        with open('token.json', 'w') as token:
            token.write(self.creds.to_json())

    def refresh_with_browser(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', self.SCOPES)
        self.creds = flow.run_local_server(port=0)
        self.save_creds_to_file()

    def re_watch(self):
        request = {
            'labelIds': ['INBOX'],
            'labelFilterAction': 'include',
            'topicName': self.google_topic
        }
        with build('gmail', 'v1', credentials=self.creds) as service:
            service.users().watch(userId='me', body=request).execute()


if __name__ == "__main__":
    gmail_re_watch = GMailAPI()
    gmail_re_watch.re_watch()
