

import re
from typing import List
from config import Config
from encoder.encoder import Encoder
from types_ import DefaultEmailChunkHeader, Email, EmailChunk


class DefaultEncoder(Encoder):
    @staticmethod
    def get_contact_number_for_email(email):
        contacts = Config.get_whitelist()
        for contact_number, email_address in contacts.items():
            if email_address == email:
                return contact_number

    @staticmethod
    def email_to_contact_number(email_list):
        contacts = Config.get_whitelist()
        email_list = [DefaultEncoder.get_contact_number_for_email(email) if email in contacts.values()
                      else email for email in email_list]
        return email_list

    def encode_email(self, email: Email) -> List[str]:
        sender_or_recipient = [email.sender_or_recipient]
        length_of_message_from = len(sender_or_recipient[0]) #len(self.message_from[0]) * len(self.message_from)
        max_chunk_size = int(Config.get_max_message_size()) - length_of_message_from - len(email.subject)
        message_to_encode = email.message
        total_message_length = len(message_to_encode)
        if total_message_length > max_chunk_size:
            message_to_encode = [message_to_encode[i: i + max_chunk_size]
                                      for i in range(0, total_message_length, max_chunk_size)]
        else:
            message_to_encode = [message_to_encode]
        print("Number of Message Chunks: " + str(len(message_to_encode)))
        message_from = DefaultEncoder.email_to_contact_number(sender_or_recipient)
        payload_list = []
        for part_number, message_text in enumerate(message_to_encode):
            payload = ""
            for sender in message_from:
                payload += sender + ","
            payload += email.subject
            payload += " (" + str(part_number + 1) + "/" + str(len(message_to_encode)) + ")" + ","
            payload += message_text
            payload = payload.replace('\r', '').replace('\n', '')
            payload_list.append(payload.encode().hex())
        return payload_list

    def decode_email_chunk(self, chunks: str) -> EmailChunk:
        email_chunks = bytes.fromhex(chunks).decode("UTF-8").split(',', 2)
        parts_re = re.search(r'\((\d+)/(\d+)\)', email_chunks[1])
        return EmailChunk(
            DefaultEmailChunkHeader(int(parts_re.group(1)), int(parts_re.group(2))),
            email_chunks[0],
            email_chunks[1],
            email_chunks[2],
        )
    