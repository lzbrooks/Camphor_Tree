import re

import requests

from config import Config


# rock_block_response = {
#     'imei': request.json()['imei'],  # integer
#     'serial_number': request.json()['serial'],  # integer
#     'mo_message_number': request.json()['momsn'],  # integer
#     'transmit_time': request.json()['transmit_time'],  # UTC => 21-10-31 10:41:50
#     'iridium_latitude': request.json()['iridium_latitude'],  # float
#     'iridium_longitude': request.json()['iridium_longitude'],  # float
#     'iridium_km_acc': request.json()['iridium_cep'],  # integer
#     'hex_message': request.json()['data']  # hex-encoded
# }

class CloudLoopMessage:
    def __init__(self, hex_message=None, message_from=None, message_subject=None, message_to_encode=None):
        # Hex Encoded Message
        if hex_message:
            self.hex_message = hex_message
            self.decoded_message = bytes.fromhex(self.hex_message).decode('ascii')
            self.recipient_list, self.message_subject, self.message = self.split_recipient()
        # Message to be Hex Encoded
        if message_to_encode:
            self.auth_token = Config.get_cloud_loop_auth_token()
            self.hardware_id = Config.get_rock_block_id()
            self.message_to_encode = message_to_encode
            self.message_from = message_from
            self.message_subject = message_subject
            self.payload = self.get_payload()

    def split_recipient(self):
        message_parts = self.decoded_message.split(",")
        recipient_list = []
        subject_and_body = []
        for message_part in message_parts:
            if message_part.isnumeric():
                recipient_list.append(message_part)
            if re.search(r'\S+@\S+', message_part):
                recipient_list.append(message_part)
            else:
                subject_and_body.append(message_part)
        recipient_list = CloudLoopMessage.contact_number_to_email(recipient_list)
        return recipient_list, subject_and_body[0], subject_and_body[1]

    @staticmethod
    def contact_number_to_email(email_list):
        contacts = Config.get_whitelist()
        email_list = [contacts[email] if email.isnumeric() else email for email in email_list]
        return email_list

    @staticmethod
    def email_to_contact_number(email_list):
        contacts = Config.get_whitelist()
        email_list = [contacts.index(email) if contacts.index(email) else email for email in email_list]
        return email_list

    def get_payload(self):
        payload = ""
        self.message_from = CloudLoopMessage.email_to_contact_number(self.message_from)
        for sender in self.message_from:
            payload += sender + ","
        payload += self.message_subject + "," + self.message_to_encode
        return self.message_to_encode.hex(payload)

    def send_cloud_loop_message(self):
        if self.message_to_encode:
            send_message_api = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware="
            url = send_message_api + self.hardware_id + "&payload=" + self.payload + "&token=" + self.auth_token
            headers = {"Accept": "application/json"}
            return requests.get(url, headers=headers)
