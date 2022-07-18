import base64
import configparser
import re
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests as requests

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

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
        print("GMail Message Processing...")

        self.google_client_id = None
        self.google_client_secret = None
        self.google_topic = None
        self.refresh_token = None

        self.message_from = None
        self.message_to = None

        self.set_up_google_client_id(google_client_id)
        self.set_up_google_client_secret(google_client_secret)
        self.set_up_refresh_token()
        self.set_up_google_topic()

        self.set_up_email_recipient(message_to)
        self.set_up_email_sender(message_from)

        self.message_subject = message_subject
        self.message_text = message_text

        self.new_gmail_message = []
        self.max_message_size = None
        self.set_up_message_size()

        self.auth_token = None
        self.auth_expiry_format = "%m/%d/%Y, %H:%M:%S"

        self.gmail_message = None

        self.gmail_endpoint = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
        self.gmail_message_list_endpoint = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
        self.gmail_get_message_endpoint = "https://gmail.googleapis.com/gmail/v1/users/me/messages/"
        self.watch_endpoint = "https://gmail.googleapis.com/gmail/v1/users/me/watch"
        print("GMail Message Processed")

    def set_up_google_client_id(self, google_client_id):
        if google_client_id is None:
            self.google_client_id = Config.get_google_id()
        else:
            self.google_client_id = google_client_id

    def set_up_google_client_secret(self, google_client_secret):
        if google_client_secret is None:
            self.google_client_secret = Config.get_google_secret()
        else:
            self.google_client_secret = google_client_secret

    def set_up_google_topic(self):
        self.google_topic = Config.get_google_topic()

    def set_up_refresh_token(self):
        self.refresh_token = Config.get_google_refresh_token()

    def set_up_email_sender(self, message_from):
        if message_from is None:
            self.message_from = Config.get_email()
        else:
            self.message_from = message_from

    def set_up_email_recipient(self, message_to):
        if message_to is None:
            self.message_to = Config.get_email()
        else:
            self.message_to = message_to

    def set_up_message_size(self):
        self.max_message_size = Config.get_max_message_size()

    def get_api_headers(self):
        self.get_auth_token()
        return {
            'Authorization': f'Bearer {self.auth_token} ',
            'Accept': 'application / json',
            'Content-Type': 'application/json'
        }

    def get_auth_code_url(self):
        print("Getting GMail Auth Code URL...")
        scope = "https%3A//www.googleapis.com/auth/gmail.modify"
        access_type = "offline"
        response_code = "code"
        redirect_uri = "https%3A//localhost"
        authorization_url = "https://accounts.google.com/o/oauth2/auth" + "?" + \
                            "scope=" + scope + "&" + \
                            "access_type=" + access_type + "&" + \
                            "response_type=" + response_code + "&" + \
                            "redirect_uri=" + redirect_uri + "&" + \
                            "client_id=" + self.google_client_id
        print("GMail Auth Code URL Attained")
        return authorization_url

    def get_refresh_token(self, auth_code):
        print("Getting GMail Refresh Token...")
        url = "https://oauth2.googleapis.com/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'code': auth_code,
            'client_id': self.google_client_id,
            'client_secret': self.google_client_secret,
            'redirect_uri': "https://localhost",
            'grant_type': 'authorization_code'
        }
        response = requests.post(url, data=data, headers=headers)
        print(response.json())
        self.write_auth_config(response.json(), self.auth_expiry_format)
        print("GMail Refresh Token Attained")
        return response.json()['refresh_token']

    @staticmethod
    def write_auth_config(request_json, auth_expiry_format):
        auth_expiry_date_time = datetime.now() + timedelta(seconds=request_json['expires_in'])
        config_file = configparser.ConfigParser()
        config_file["AuthConfig"] = {
            "token": request_json['access_token'],
            "expires": auth_expiry_date_time.strftime(auth_expiry_format)
        }
        with open("../configurations.ini", "w") as file_object:
            config_file.write(file_object)

    @staticmethod
    def read_auth_config(auth_expiry_format):
        config_file = configparser.ConfigParser()
        if config_file.read("configurations.ini"):
            config_file.read("configurations.ini")
            return {
                "AuthConfig": {
                    "token": config_file["AuthConfig"]["token"],
                    "expires": datetime.strptime(config_file["AuthConfig"]["expires"],
                                                     auth_expiry_format)
                }
            }

    def check_auth_token_expired(self):
        print("Checking GMail Auth Token Expiry...")
        config_file = self.read_auth_config(self.auth_expiry_format)
        if config_file and config_file["AuthConfig"]["expires"] > datetime.now():
            return False
        print("GMail Auth Token Expired")
        return True

    def get_auth_token(self):
        url = "https://oauth2.googleapis.com/token"
        data = {
            'client_id': self.google_client_id,
            'client_secret': self.google_client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        if self.check_auth_token_expired():
            print("Getting New GMail Auth Token...")
            response = requests.post(url, json=data)
            if 'access_token' in response.json() and response.json()['access_token']:
                self.write_auth_config(response.json(), self.auth_expiry_format)
                self.auth_token = response.json()['access_token']
        else:
            auth_config = self.read_auth_config(self.auth_expiry_format)
            self.auth_token = auth_config["AuthConfig"]["token"]
        print("GMail Auth Token Attained")

    def gmail_create_message(self):
        if self.message_to:
            message = MIMEMultipart()
            message['To'] = ", ".join(self.message_to)
            message['From'] = self.message_from
            message['Subject'] = self.message_subject
            message.attach(MIMEText(self.message_text, 'plain'))
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {
                'raw': encoded_message
            }
            self.gmail_message = create_message

    def post_message(self):
        if self.gmail_message:
            print("Sending GMail Message")
            return requests.post(self.gmail_endpoint, headers=self.get_api_headers(), json=self.gmail_message)
        print("No GMail Message to Send")

    def send_gmail_message(self):
        self.gmail_create_message()
        self.post_message()

    def gmail_get_first_message_from_push(self):
        query_params = {'maxResults': str(1)}
        response = requests.get(self.gmail_message_list_endpoint, headers=self.get_api_headers(), params=query_params)
        if 'messages' in response.json():
            self.new_gmail_message = response.json()['messages'][0]

    def gmail_get_message_by_id(self, message):
        get_message_endpoint = self.gmail_get_message_endpoint + str(message['id'])
        response = requests.get(get_message_endpoint, headers=self.get_api_headers())
        print("GMail Message Attained by ID")
        message_from = None
        message_subject = None
        message_text = None
        send_message = True
        if 'DRAFT' in response.json()['labelIds'] or 'SENT' in response.json()['labelIds']:
            send_message = False
        if 'payload' in response.json() and send_message:
            message_payload = response.json()['payload']
            for header in message_payload['headers']:
                if header['name'] == 'From':
                    message_from = re.search(r'(?<=<).*?(?=>)', header['value']).group()
                if header['name'] == 'Subject':
                    message_subject = header['value']
            message_parts = message_payload['parts']
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
        print("GMail Message Dissected")
        return message_from, message_subject, message_text

    def gmail_re_watch(self):
        print("Starting GMail Re-Watch...")
        request_body = {
            'labelIds': ['INBOX'],
            'labelFilterAction': 'include',
            'topicName': self.google_topic
        }
        response = requests.post(self.watch_endpoint, headers=self.get_api_headers(), json=request_body)
        if 'historyId' in response.json():
            print("GMail Re-Watch Success")
        else:
            print("Gmail Re-Watch Failure")

    def get_new_gmail_message(self):
        return self.new_gmail_message


if __name__ == "__main__":
    gmail_re_watch = GMailMessage()
    gmail_re_watch.gmail_re_watch()
