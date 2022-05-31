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
        self.message_subject = None
        self.auth_token = None
        self.hardware_id = None
        self.message_to_encode = None
        self.message_from = None
        self.payload_list = None
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
            self.message_to_encode = message_to_encode
            if isinstance(message_from, list):
                self.message_from = message_from
            else:
                self.message_from = [message_from]
            self.message_subject = message_subject
            self.payload_list = self.get_payload()
            print("Message Encoded")

    def decode_hex_message(self):
        # From JSON payload hex string to bytes
        if not isinstance(self.hex_message, bytes):
            print("Changing Hex to Bytes")
            self.hex_message = bytes.fromhex(self.hex_message)
        self.decoded_message = self.hex_message.decode()

    def split_recipient(self):
        message_parts = self.decoded_message.split(",")
        info_subjects = [subject for subject in message_parts if re.search(r'Info \(./.\)', subject)]
        urgent_subjects = [subject for subject in message_parts if re.search(r'Urgent \(./.\)', subject)]
        emergency_subjects = [subject for subject in message_parts if re.search(r'Emergency \(./.\)', subject)]
        if info_subjects:
            message_subject = info_subjects[0]
        elif urgent_subjects:
            message_subject = urgent_subjects[0]
        elif emergency_subjects:
            message_subject = emergency_subjects[0]
        else:
            message_subject = None
        if message_subject:
            recipient_list = message_parts[:message_parts.index(message_subject)]
            message_text_list = message_parts[message_parts.index(message_subject) + 1:]
        else:
            message_subject = ""
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
        print(self.recipient_list)
        print(self.message_subject)
        print(self.message)

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
        max_chunk_size = int(Config.get_max_message_size())
        total_message_length = len(self.message_to_encode)
        if total_message_length > max_chunk_size:
            self.message_to_encode = [self.message_to_encode[i: i + max_chunk_size]
                                      for i in range(0, total_message_length, max_chunk_size)]
        else:
            self.message_to_encode = [self.message_to_encode]
        print("Number of Message Chunks: " + str(len(self.message_to_encode)))
        self.message_from = CloudLoopMessage.email_to_contact_number(self.message_from)
        payload_list = []
        for part_number, message_text in enumerate(self.message_to_encode):
            payload = ""
            for sender in self.message_from:
                payload += sender + ","
            payload += self.message_subject
            payload += " (" + str(part_number + 1) + "/" + str(len(self.message_to_encode)) + ")" + ","
            payload += message_text
            payload = payload.replace('\r', '').replace('\n', '')
            payload_list.append(payload)
        return payload_list

    def send_cloud_loop_message(self):
        if self.message_to_encode:
            for payload_part_number, payload in enumerate(self.payload_list):
                print("Sending CloudLoop Message")
                print("Sending part " + str(payload_part_number + 1) + " of " + str(len(self.payload_list)))
                send_message_api = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware="
                url = send_message_api + self.hardware_id + \
                      "&payload=" + payload.encode().hex() + "&token=" + self.auth_token
                headers = {"Accept": "application/json"}
                print(url)
                # requests.get(url, headers=headers)
                print(payload)
                print("Sent part " + str(payload_part_number + 1) + " of " + str(len(self.payload_list)))
        else:
            print("No CloudLoop Message to Send")
