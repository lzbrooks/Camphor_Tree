import random
import re
import requests

from config.config import Config


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


class HexEncodeForCloudLoop:
    def __init__(self, message_from=None, message_subject=None, message_to_encode=None):
        self.auth_token = Config.get_cloud_loop_auth_token()
        self.hardware_id = Config.get_rock_block_id()
        self.max_chunk_size = Config.get_max_message_size()
        self.contacts = Config.get_whitelist()
        if isinstance(message_from, list) or not message_from:
            self.message_from = message_from
        else:
            self.message_from = [message_from]
        self.message_to_encode = message_to_encode
        self.message_subject = message_subject
        self.message_chunk_list = []
        self.hex_message_id = self._assemble_hex_message_id()

    def send_cloud_loop_message(self):
        if self.message_to_encode:
            payload_list = self.get_payload()
            for payload_part_number, payload in enumerate(payload_list):
                self._send_payload_part(payload, payload_list, payload_part_number)
        else:
            print("No CloudLoop Message to Send")

    def get_payload(self):
        print("Message Encoding...")
        self.message_from = self._email_to_contact_number(self.message_from)
        self._chunk_message()
        payload_list = []
        for part_number, message_text in enumerate(self.message_chunk_list):
            payload = self._assemble_payload_part(message_text, part_number)
            payload_list.append(payload)
        print("Message Encoded")
        return payload_list

    def _send_payload_part(self, payload, payload_list, payload_part_number):
        print("Sending CloudLoop Message")
        print(f"Sending part {payload_part_number + 1} of {len(payload_list)}")
        url = self._get_cloud_loop_payload_url(payload)
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        print(response)
        print(payload)
        print(f"Sent part {payload_part_number + 1} of {len(payload_list)}")

    def _chunk_message(self):
        self.message_chunk_list.append(self.message_subject[:self.max_chunk_size])
        total_message_length = len(self.message_to_encode)
        self.message_chunk_list += [self.message_to_encode[i: i + self.max_chunk_size]
                                    for i in range(0, total_message_length, self.max_chunk_size)]
        print("Number of Message Chunks: " + str(len(self.message_chunk_list)))

    def _assemble_payload_part(self, message_text, part_number):
        payload = self._assemble_payload_tagline(part_number)
        payload += message_text
        payload = payload.replace('\r', '').replace('\n', '')
        return payload

    def _assemble_payload_tagline(self, part_number):
        payload = ""
        for sender in self.message_from:
            payload += sender + ","
        payload += self.hex_message_id
        payload += f" ({part_number + 1}/{len(self.message_chunk_list)}),"
        return payload

    def _email_to_contact_number(self, email_list):
        email_list = [self._get_contact_number_for_email(email) if email in self.contacts.values()
                      else email for email in email_list]
        return email_list

    def _get_contact_number_for_email(self, email):
        for contact_number, email_address in self.contacts.items():
            if email_address == email:
                return contact_number

    def _get_cloud_loop_payload_url(self, payload):
        send_message_api = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware="
        url = send_message_api + self.hardware_id + \
              "&payload=" + payload.encode().hex() + "&token=" + self.auth_token
        return url

    @staticmethod
    def _assemble_hex_message_id():
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))


class DecodeCloudLoopMessage:
    def __init__(self, hex_message=None):
        self.contacts = Config.get_whitelist()
        self.hex_message = hex_message
        self.decoded_message = None
        self._message_text_list = []
        self.recipient_list = []
        self.message_subject = None
        self.message_text = None

    def decode_hex_message(self):
        print("Hex Message Processing...")
        self._decode_message_from_hex()
        self._extract_all_message_parts()
        print("Hex Message Processed")

    def _decode_message_from_hex(self):
        # From JSON payload hex string to bytes
        if not isinstance(self.hex_message, bytes):
            print("Changing Hex to Bytes")
            self.hex_message = bytes.fromhex(self.hex_message)
        self.decoded_message = self.hex_message.decode()

    def _extract_all_message_parts(self):
        message_parts = self.decoded_message.split(",")
        self._extract_message_subject(message_parts)
        self._split_on_subject(message_parts)
        self._assemble_message_recipient_list()
        self.message_text = "".join(self._message_text_list)
        print(self.recipient_list)
        print(self.message_subject)
        print(self.message_text)

    def _extract_message_subject(self, message_parts):
        message_subjects = [subject for subject in message_parts if re.search(r'#[a-fA-F\d]{6}', subject)]
        if message_subjects:
            self.message_subject = message_subjects[0]

    def _split_on_subject(self, message_parts):
        if self.message_subject:
            self.recipient_list = message_parts[:message_parts.index(self.message_subject)]
            self._message_text_list = message_parts[message_parts.index(self.message_subject) + 1:]
        else:
            self.message_subject = ""
            self.recipient_list = message_parts
            self._message_text_list = message_parts

    def _assemble_message_recipient_list(self):
        recipient_list_filtered = self._get_recipient_list(self.recipient_list)
        self.recipient_list = self._contact_number_to_email(recipient_list_filtered)

    @staticmethod
    def _get_recipient_list(message_parts):
        message_list = [message_part for message_part in message_parts
                        if message_part.isnumeric() or re.search(r'\S+@\S+', message_part)]
        return message_list

    def _contact_number_to_email(self, email_list):
        email_list = [self._get_email_for_contact_number(email) if email.isnumeric()
                      else email for email in email_list]
        return email_list

    def _get_email_for_contact_number(self, contact):
        for contact_number, email_address in self.contacts.items():
            if contact_number == contact:
                return email_address
