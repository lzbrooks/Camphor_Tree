import os
import time
from datetime import datetime

import json
from pathlib import Path

import serial
from adafruit_rockblock import RockBlock

from apis.cloud_loop_api import DecodeCloudLoopMessage


# Reqs:
# sudo pip3 install --upgrade adafruit-python-shell
# pip3 install Adafruit-Blinka
# pip3 install adafruit-circuitpython-rockblock


class RockBlockAPI:
    def __init__(self, status_of_mailbox=None):
        print("RockBLOCK Processing...")
        uart = serial.Serial("/dev/serial0", 19200)
        self.rock_block = RockBlock(uart)
        self.status_of_mailbox = status_of_mailbox
        print("RockBLOCK Processed")

    def send_data_out(self, data):
        for message in data:
            self._set_data_out(message.encode())
            self._talk_to_rock_block()

    def _talk_to_rock_block(self):
        print("Talking to satellite...")
        self.status_of_mailbox = self._get_satellite_transfer()
        print(self.status_of_mailbox)
        while self.status_of_mailbox[0] > 8:
            time.sleep(10)
            self.status_of_mailbox = self._get_satellite_transfer()
            print(self.status_of_mailbox)
        print("\nDONE.")

    # (0, 1, 1, 1, 6, 8) means:
    # 0 - Your blank MO message has been sent successfully during the mailbox check.
    # 1 - This is blank MO message number 1.
    # 1 - You have successfully received a new MT message.
    # 1 - This is MT message number 1.
    # 6 - This MT message is 6 bytes long.
    # 8 - You have 8 more MT messages in the queue waiting to be downloaded.
    def _process_rock_block_status(self):
        print(self.status_of_mailbox)
        if self.status_of_mailbox[2] == 0:
            print("No Messages Waiting")
        if self.status_of_mailbox[2] == 1:
            print("Message Received")
        print("Size in bytes of message: " + str(self.status_of_mailbox[4]))
        print("Number of Messages in Queue: " + str(self.status_of_mailbox[5]))

    def _set_data_out(self, data):
        self.rock_block.data_out = data  # pragma: no cover

    def _get_data_in(self):
        return self.rock_block.data_in  # pragma: no cover

    def _get_satellite_transfer(self):
        return self.rock_block.satellite_transfer()  # pragma: no cover


class CheckMail(RockBlockAPI):
    def __init__(self, recipient_list=None, message_hash_id=None,
                 message_part_number=None, parts_total=None, message_text=None,
                 collating_message_file_path=None, complete_message_file_path=None, status_of_mailbox=None):
        super().__init__(status_of_mailbox=status_of_mailbox)
        self.recipient_list = recipient_list
        self.message_hash_id = message_hash_id
        self.message_part_number = message_part_number
        self.parts_total = parts_total
        self.message_text = message_text
        self.complete_message_file_path = complete_message_file_path
        self.collating_message_file_path = collating_message_file_path

    def check_mailbox(self):
        self._talk_to_rock_block()
        self._process_rock_block_status()
        self._save_rock_block_hex_data_to_file()

    # TODO: test
    def _save_rock_block_hex_data_to_file(self):
        hex_data = self._get_data_in()
        print(hex_data)
        if hex_data:
            self._extract_message_parts(hex_data)
            self.complete_message_file_path = self._assemble_complete_message_file_path()
            self.collating_message_file_path = self._assemble_collating_message_file_path()
            collated_parts = self._collate_cloud_loop_message()
            if collated_parts:
                self.write_message_to_file(collated_parts, self.complete_message_file_path)
                print(f"Saved Cloud Loop Message {collated_parts} To {self.complete_message_file_path}")

    # TODO: test
    def _extract_message_parts(self, hex_data):
        message_from_rock_block = DecodeCloudLoopMessage(hex_message=hex_data)
        message_from_rock_block.decode_hex_message()
        self.recipient_list = message_from_rock_block.recipient_list
        self.message_hash_id = message_from_rock_block.message_hash_id
        self.message_part_number = message_from_rock_block.message_part_number
        self.parts_total = message_from_rock_block.parts_total
        self.message_text = message_from_rock_block.message_text

    # TODO: test
    def _collate_cloud_loop_message(self):
        # {"#fbc84a": ["Info", "Testing"]}
        collated_parts = self.read_message_from_file(self.collating_message_file_path)
        current_list_number = int(self.message_part_number) - 1
        if not collated_parts:
            collated_parts = {self.message_hash_id: [None for _ in range(int(self.parts_total))]}
        collated_parts[self.message_hash_id][current_list_number] = self.message_text
        print(collated_parts)
        if None not in collated_parts[self.message_hash_id]:
            self._remove_completely_collated_message_file()
            return self._assemble_complete_message(collated_parts)
        self.write_message_to_file(collated_parts, self.collating_message_file_path)
        print(f"Saved Message \"{collated_parts[self.message_hash_id][current_list_number]}\"")
        print(f"To {self.collating_message_file_path}")

    # TODO: test
    def _assemble_complete_message(self, collated_parts):
        complete_message_subject = collated_parts[self.message_hash_id][0]
        complete_message_text = "".join(collated_parts[self.message_hash_id][1:])
        return {"From": self.recipient_list, "Subject": complete_message_subject, "Body": complete_message_text}

    # TODO: test
    def _remove_completely_collated_message_file(self):
        print(f"Collation of Message {self.message_hash_id} Complete At {self.message_part_number}/{self.parts_total}")
        if os.path.exists(self.collating_message_file_path):
            os.remove(self.collating_message_file_path)
        print(f"Removed {self.message_hash_id} From {self.collating_message_file_path}")

    # TODO: test
    def _assemble_collating_message_file_path(self):
        if self.collating_message_file_path:
            return self.collating_message_file_path
        return f'Inbox/{self.message_hash_id}.txt'

    # TODO: test
    def _assemble_complete_message_file_path(self):
        if self.complete_message_file_path:
            return self.complete_message_file_path
        return f'Inbox/{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}.txt'

    @staticmethod
    def read_message_from_file(message_file_path):
        if Path(message_file_path).is_file():
            with open(message_file_path, 'r') as last_gmail_message_file:
                return json.load(last_gmail_message_file)

    @staticmethod
    def write_message_to_file(message_json, message_file_path):
        with open(message_file_path, "w") as file_object:
            json.dump(message_json, file_object)
