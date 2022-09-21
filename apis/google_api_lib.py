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


class GMailAuth:
    def __init__(self):
        self.creds = None
        self.cred_file = Config.get_google_client_credentials_file()
        self.token_file = Config.get_google_access_token_file()
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        self.google_topic = Config.get_google_topic()

    def re_watch(self):
        self._get_creds()
        request = {
            'labelIds': ['INBOX'],
            'labelFilterAction': 'include',
            'topicName': self.google_topic
        }
        return self._google_api_re_watch(request)

    def refresh_with_browser(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.cred_file, self.SCOPES)
        self.creds = self._google_api_refresh_with_browser(flow)
        self._save_creds_to_file()

    def _get_creds(self):
        """Set self.creds
        Requires: GOOGLE_APPLICATION_CREDENTIALS env var set to credentials.json file path
        """
        if os.path.exists(self.token_file):
            print("Access Token File Found")
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        else:
            print("Access Token File Not Found")
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("Getting New GMail Access Token...")
                self._google_api_refresh_access_token()
                print("GMail Access Token Attained")
            else:
                raise ValueError("No Valid Refresh Token")
            self._save_creds_to_file()

    def _save_creds_to_file(self):
        with open(self.token_file, 'w') as token:
            token.write(self.creds.to_json())

    def _google_api_re_watch(self, request):
        with build('gmail', 'v1', credentials=self.creds) as service:
            re_watch_http_request = service.users().watch(userId='me', body=request)
            return self._google_api_execute_request(re_watch_http_request)

    @staticmethod
    def _google_api_refresh_with_browser(flow):
        return flow.run_local_server(port=0)  # pragma: no cover

    def _google_api_refresh_access_token(self):
        self.creds.refresh(Request())  # pragma: no cover

    def _google_api_execute_request(self, api_http_request):
        try:
            return self._google_api_execute_request_http_catch(api_http_request)
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

    @staticmethod
    def _google_api_execute_request_http_catch(api_http_request):
        return api_http_request.execute()  # pragma: no cover


class GMailAPI(GMailAuth):
    def __init__(self, message_to=None, message_from=None, message_subject=None, message_text=None):
        GMailAuth.__init__(self)
        self.max_message_size = Config.get_max_message_size()
        self.message_to = message_to
        self.message_from = Config.get_email(message_from)
        self.message_subject = message_subject
        self.message_text = message_text
        self.new_gmail_message = None
        self.gmail_message = None

    def get_top_inbox_message(self):
        self._get_creds()
        top_message = self._google_api_get_top_inbox_message()
        if 'messages' in top_message:
            return top_message['messages'][0]

    def get_gmail_message_by_id(self, message):
        self._get_creds()
        response_json = self._google_api_get_message(str(message['id']))
        print("GMail Message Attained by ID")
        send_message = True
        if 'DRAFT' in response_json['labelIds'] or 'SENT' in response_json['labelIds']:
            send_message = False
        if 'payload' in response_json and send_message:
            return self._dissect_message(response_json["payload"])
        print("GMail Message Dissected")
        return None, None, None

    def send_gmail_message(self):
        """Create and send an email message
        Returns: Message object, including message id
        Load pre-authorized user credentials from the environment
        """
        self._get_creds()
        self._create_gmail_message()
        if self.gmail_message:
            print("Sending GMail Message")
            return self._google_api_send_message()
        print("No GMail Message to Send")

    def _create_gmail_message(self):
        if self.message_to and isinstance(self.message_to, list):
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
                message_from = re.search(r'(?<=<).*?(?=>)', header['value'])
                if message_from:
                    message_from = message_from.group()
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

    def _google_api_get_top_inbox_message(self):
        with build('gmail', 'v1', credentials=self.creds) as service:
            top_inbox_http_request = service.users().messages().list(userId='me', maxResults='1')
            return self._google_api_execute_request(top_inbox_http_request)

    def _google_api_send_message(self):
        with build('gmail', 'v1', credentials=self.creds) as service:
            send_message_http_request = service.users().messages().send(userId='me', body=self.gmail_message)
            return (self._google_api_execute_request(
                send_message_http_request))

    def _google_api_get_message(self, message_id):
        with build('gmail', 'v1', credentials=self.creds) as service:
            get_message_http_request = service.users().messages().get(userId='me', id=message_id)
            return self._google_api_execute_request(get_message_http_request)


if __name__ == "__main__":  # pragma: no cover
    gmail_re_watch = GMailAuth()
    print(gmail_re_watch.re_watch())
