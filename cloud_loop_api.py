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
            print(hex_message)
            self.hex_message = hex_message
            self.decoded_message = bytes.fromhex(self.hex_message).decode('ascii')
            self.recipient_list, self.message_subject, self.message = self.split_recipient()
        # Message to be Hex Encoded
        self.auth_token = None
        self.hardware_id = None
        self.message_to_encode = None
        self.message_from = None
        self.message_subject = None
        self.payload = None
        if message_to_encode:
            self.auth_token = Config.get_cloud_loop_auth_token()
            self.hardware_id = Config.get_rock_block_id()
            self.message_to_encode = message_to_encode
            if isinstance(message_from, list):
                self.message_from = message_from
            else:
                self.message_from = [message_from]
            self.message_subject = message_subject
            self.payload = self.get_payload()

    def split_recipient(self):
        print(self.decoded_message)
        message_parts = self.decoded_message.split(",")
        print(message_parts)
        message_subject = None
        message_split_index = 1
        for message_part_number, message_part in enumerate(message_parts):
            if not message_part.isnumeric() and not re.search(r'\S+@\S+', message_part):
                message_subject = message_part
                message_split_index = message_part_number
                break
        recipient_list = [message_part for message_part in message_parts[:message_split_index]
                          if message_part.isnumeric() or re.search(r'\S+@\S+', message_part)]
        message_text_begin_index = message_split_index - 1
        message_text = "".join(message_parts[message_text_begin_index:])
        recipient_list = CloudLoopMessage.contact_number_to_email(recipient_list)
        return recipient_list, message_subject, message_text

    @staticmethod
    def contact_number_to_email(email_list):
        email_list = [CloudLoopMessage.get_email_for_contact_number(email) if email.isnumeric()
                      else email for email in email_list]
        return email_list

    @staticmethod
    def get_email_for_contact_number(contact):
        contacts = Config.get_whitelist()
        for contact_number, email_address in contacts.items():
            if contact_number == contact:
                return email_address

    @staticmethod
    def email_to_contact_number(email_list):
        contacts = Config.get_whitelist()
        email_list = [CloudLoopMessage.get_contact_number_for_email(email) if email in contacts.values()
                      else email for email in email_list]
        return email_list

    @staticmethod
    def get_contact_number_for_email(email):
        contacts = Config.get_whitelist()
        for contact_number, email_address in contacts.items():
            if email_address == email:
                return contact_number

    def get_payload(self):
        payload = ""
        self.message_from = CloudLoopMessage.email_to_contact_number(self.message_from)
        for sender in self.message_from:
            payload += sender + ","
        payload += self.message_subject + "," + self.message_to_encode
        return payload.encode()

    def send_cloud_loop_message(self):
        if self.message_to_encode:
            send_message_api = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware="
            url = send_message_api + self.hardware_id + "&payload=" + self.payload.hex() + "&token=" + self.auth_token
            headers = {"Accept": "application/json"}
            return requests.get(url, headers=headers)
