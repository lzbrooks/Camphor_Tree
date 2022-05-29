import re
import struct

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
        self.message_subject = None
        self.auth_token = None
        self.hardware_id = None
        self.message_to_encode = None
        self.message_from = None
        self.payload = None
        self.recipient_list = []
        self.message_subject = None
        self.message = None
        # Hex Encoded Message
        if hex_message:
            print("Hex Message Processing...")
            self.hex_message = hex_message
            self.decoded_message = None
            self.decode_hex_message()
            self.split_recipient()
            print("Hex Message Processed")
        # Message to be Hex Encoded
        if message_to_encode:
            print("Message Encoding...")
            self.auth_token = Config.get_cloud_loop_auth_token()
            self.hardware_id = Config.get_rock_block_id()
            # TODO: handle list
            self.message_to_encode = message_to_encode
            if isinstance(message_from, list):
                self.message_from = message_from
            else:
                self.message_from = [message_from]
            self.message_subject = message_subject
            # TODO: handle list of message_to_encode in for loop
            self.payload = self.get_payload()
            print("Message Encoded")

    def decode_hex_message(self):
        # From JSON payload hex string to bytes
        if not isinstance(self.hex_message, bytes):
            print("Changing Hex to Bytes")
            self.hex_message = bytes.fromhex(self.hex_message)
        self.decoded_message = self.hex_message.decode()

    def split_recipient(self):
        message_parts = self.decoded_message.split(",")
        message_subject = None
        if 'Info' in message_parts:
            message_subject = 'Info'
            recipient_list = message_parts[:message_parts.index('Info')]
            message_text_list = message_parts[message_parts.index('Info') + 1:]
        elif 'Urgent' in message_parts:
            message_subject = 'Urgent'
            recipient_list = message_parts[:message_parts.index('Urgent')]
            message_text_list = message_parts[message_parts.index('Urgent') + 1:]
        elif 'Emergency' in message_parts:
            message_subject = 'Emergency'
            recipient_list = message_parts[:message_parts.index('Emergency')]
            message_text_list = message_parts[message_parts.index('Emergency') + 1:]
        else:
            recipient_list = message_parts
            message_text_list = message_parts
        recipient_list_filtered = CloudLoopMessage.get_recipient_list(recipient_list)
        recipient_list_mapped = CloudLoopMessage.contact_number_to_email(recipient_list_filtered)
        if len(recipient_list_mapped) < len(recipient_list):
            message_text_list = message_parts
        message_text = "".join(message_text_list)
        self.recipient_list = recipient_list_mapped
        self.message_subject = message_subject
        self.message = message_text

    @staticmethod
    def get_recipient_list(message_parts):
        message_list = [message_part for message_part in message_parts
                        if message_part.isnumeric() or re.search(r'\S+@\S+', message_part)]
        return message_list

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
        # TODO: for loop over messages to encode (only message_text differ, increment subject line counter)
        # TODO: make sure message chunks are smaller than max - take into account counter text
        # TODO: return list of payloads
        payload = ""
        self.message_from = CloudLoopMessage.email_to_contact_number(self.message_from)
        for sender in self.message_from:
            payload += sender + ","
        payload += self.message_subject + "," + self.message_to_encode
        payload = payload.replace('\r', '').replace('\n', '')
        return payload.encode()

    def send_cloud_loop_message(self):
        # TODO: for loop over payloads
        if self.message_to_encode:
            print("Sending CloudLoop Message")
            print(self.payload.hex())
            send_message_api = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware="
            url = send_message_api + self.hardware_id + "&payload=" + self.payload.hex() + "&token=" + self.auth_token
            headers = {"Accept": "application/json"}
            return requests.get(url, headers=headers)
        print("No CloudLoop Message to Send")
