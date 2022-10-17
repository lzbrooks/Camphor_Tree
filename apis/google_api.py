from __future__ import print_function

import os.path

import re
import base64
from email.message import EmailMessage
from pprint import pprint
from typing import Tuple, Optional, Dict, Any, List
import logging
# from logging import handlers

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import Response

from config.config import Config

# smtp_handler = logging.handlers.SMTPHandler(mailhost=("smtp.gmail.com", 587),
#                                             fromaddr="sv.kiki.vn95@gmail.com",
#                                             toaddrs="sv.kiki.vn95@gmail.com",
#                                             subject=u"WARNING: Lost Camphor_Tree Email",
#                                             credentials=(Config.get_email(), Config.get_email_pass()),
#                                             secure=())
#
_logger = logging.Logger(__name__)
# _logger.addHandler(smtp_handler)

# import logging
# import logging.handlers
#
# smtp_handler = logging.handlers.SMTPHandler(mailhost=("smtp.gmail.com", 587),
#                                             fromaddr="sv.kiki.vn95@gmail.com",
#                                             toaddrs="sv.kiki.vn95@gmail.com",
#                                             subject=u"WARNING: Lost Camphor_Tree Email",
#                                             credentials=(EMAIL, PASSWORD),
#                                             secure=())
#
#
# logger = logging.getLogger()
# logger.addHandler(smtp_handler)
#
# try:
#   break
# except Exception as e:
#   logger.exception('Unhandled Exception')


# TODO: refactor class variables into more local ones where applicable
# TODO: handle possible Nones from Env Vars
class GMailAuth:
    creds: Optional[Credentials]
    cred_file: str
    token_file: str
    SCOPES: List[str]
    google_topic: Optional[str]

    def __init__(self):
        self.creds = None
        self.cred_file = Config.get_google_client_credentials_file()
        self.token_file = Config.get_google_access_token_file()
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        self.google_topic = Config.get_google_topic()

    def re_watch(self) -> None:
        self._get_creds()
        request = {
            'labelIds': ['INBOX'],
            'labelFilterAction': 'include',
            'topicName': self.google_topic
        }
        response_json = self._google_api_re_watch(request)
        if 'historyId' in response_json:
            print("GMail Re-Watch Success")
        else:
            print("Gmail Re-Watch Failure")

    def refresh_with_browser(self) -> None:
        flow = InstalledAppFlow.from_client_secrets_file(
            self.cred_file, self.SCOPES)
        self.creds = self._google_api_refresh_with_browser(flow)
        self._save_creds_to_file()

    # TODO: return creds
    def _get_creds(self) -> None:
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

    def _save_creds_to_file(self) -> None:
        with open(self.token_file, 'w') as token:
            token.write(self.creds.to_json())
        print(f"Token Written To {self.token_file}")

    def _google_api_re_watch(self, request: Dict[str, str]) -> Optional[Response]:
        with build('gmail', 'v1', credentials=self.creds) as service:
            re_watch_http_request = service.users().watch(userId='me', body=request)
            return self._google_api_execute_request(re_watch_http_request)

    @staticmethod
    def _google_api_refresh_with_browser(flow: InstalledAppFlow) -> Credentials:
        return flow.run_local_server(port=0)  # pragma: no cover

    def _google_api_refresh_access_token(self) -> None:
        self.creds.refresh(Request())  # pragma: no cover

    def _google_api_execute_request(self, api_http_request: Request) -> Optional[Dict[str, Any]]:
        try:
            return self._google_api_execute_request_http_catch(api_http_request)
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

    @staticmethod
    def _google_api_execute_request_http_catch(api_http_request: Request) -> Dict[str, Any]:
        return api_http_request.execute()  # pragma: no cover


class GMailAPI(GMailAuth):
    max_message_size: int
    message_to: Optional[str]
    message_from: Optional[str]
    message_subject: Optional[str]
    message_text: Optional[str]
    gmail_message: Optional[Dict[str, Optional[str]]]

    def __init__(self, message_to=None, message_from=None, message_subject=None, message_text=None):
        GMailAuth.__init__(self)
        self.max_message_size = Config.get_max_message_size()
        self.message_to = message_to
        self.message_from = Config.get_email(message_from)
        self.message_subject = message_subject
        self.message_text = message_text
        self.gmail_message = None

    def get_top_inbox_message(self) -> Optional[Dict[str, Any]]:
        self._get_creds()
        top_message = self._google_api_get_top_inbox_message()
        if 'messages' in top_message:
            print("Top Inbox GMail Activity Attained")
            return top_message['messages'][0]

    # TODO: change to get_gmail_message_parts
    # TODO: move google_api_get_message call to get_top_inbox_message
    # TODO: change message parameter to message_json
    def get_gmail_message_by_id(self, message: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
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

    # TODO: move _get_creds to _google_api_send_message
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

    # TODO: pull out message_to, message_from, message_subject, message_text to parameter (object class?)
    # TODO: return message_text
    def _create_gmail_message(self) -> None:
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

    def _dissect_message(self, message_payload: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        _logger.info(f"Dissecting message:\n{message_payload}")
        message_from, message_subject = self._dissect_message_headers(message_payload)
        message_text = self._dissect_message_parts(message_from, message_payload)
        print(f"Message Subject: {message_subject}")
        print(f"Message Body: {message_text}")
        print("GMail Message Dissected")
        return message_from, message_subject, message_text

    @staticmethod
    def _dissect_message_headers(message_payload: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
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

    def _dissect_message_parts(self, message_from: str, message_payload: Dict[str, Any]) -> Optional[str]:
        message_text = None
        message_parts = message_payload.get('parts', [message_payload])
        print("Message Parts:")
        pprint(message_parts)
        for message_part in message_parts:
            if 'mimeType' in message_part and message_part['mimeType'] == 'text/plain' \
                    and 'size' in message_part['body'] \
                    and 'data' in message_part['body']:
                size_in_bytes = message_part['body']['size']
                print("Inspecting Message Size")
                print(f"Max Message Size Allowed: {self.max_message_size}")
                print(f"Current Message Size: {size_in_bytes}")
                print(f"Message From: {message_from}")
                if size_in_bytes < self.max_message_size:
                    print("Valid: Message Under Max Size")
                    message_text = base64.urlsafe_b64decode(message_part['body']['data']).decode('utf-8')
                if size_in_bytes > self.max_message_size \
                        and message_from in Config.get_whitelist().values():
                    print("Valid: Message In Whitelist And Over Max Size")
                    message_text = base64.urlsafe_b64decode(message_part['body']['data']).decode('utf-8')
        return message_text

    def _google_api_get_top_inbox_message(self) -> Dict[str, Any]:
        with build('gmail', 'v1', credentials=self.creds) as service:
            top_inbox_http_request = service.users().messages().list(userId='me', maxResults='1')
            return self._google_api_execute_request(top_inbox_http_request)

    def _google_api_send_message(self) -> Dict[str, Any]:
        with build('gmail', 'v1', credentials=self.creds) as service:
            send_message_http_request = service.users().messages().send(userId='me', body=self.gmail_message)
            return (self._google_api_execute_request(
                send_message_http_request))

    def _google_api_get_message(self, message_id: str) -> Dict[str, Any]:
        with build('gmail', 'v1', credentials=self.creds) as service:
            get_message_http_request = service.users().messages().get(userId='me', id=message_id)
            return self._google_api_execute_request(get_message_http_request)
