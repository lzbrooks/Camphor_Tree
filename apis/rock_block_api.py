import time
from datetime import datetime

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

    # TODO: test
    def check_mailbox(self):
        self._talk_to_rock_block()
        self._process_rock_block_status()
        self._save_rock_block_hex_data_to_file()

    def _talk_to_rock_block(self):
        print("Talking to satellite...")
        self.status_of_mailbox = self._get_satellite_transfer()
        print(self.status_of_mailbox)
        while self.status_of_mailbox[0] > 8:
            time.sleep(10)
            self.status_of_mailbox = self._get_satellite_transfer()
            print(self.status_of_mailbox)
        print("\nDONE.")

    def _process_rock_block_status(self):
        print(self.status_of_mailbox)
        if self.status_of_mailbox[2] == 0:
            print("No Messages Waiting")
        if self.status_of_mailbox[2] == 1:
            print("Message Received")
        print("Size in bytes of message: " + str(self.status_of_mailbox[4]))
        print("Number of Messages in Queue: " + str(self.status_of_mailbox[5]))

    def _save_rock_block_hex_data_to_file(self):
        hex_data = self._get_data_in()
        print(hex_data)
        if hex_data:
            message_from_rock_block = DecodeCloudLoopMessage(hex_message=hex_data)
            message_from_rock_block.decode_hex_message()
            message_to_write = message_from_rock_block.recipient_list + \
                               [message_from_rock_block.message_subject, message_from_rock_block.message_text]
            message_file_name = self._assemble_message_file_name()
            with open(message_file_name, "w") as file:
                file.writelines("%s\n" % line for line in message_to_write)
            print("Message Witten To: " + message_file_name)

    @staticmethod
    def _assemble_message_file_name():
        return "Inbox/" + datetime.now().strftime("%Y_%m_%d__%H_%M_%S") + ".txt"

    def _set_data_out(self, data):
        self.rock_block.data_out = data  # pragma: no cover

    def _get_data_in(self):
        return self.rock_block.data_in  # pragma: no cover

    def _get_satellite_transfer(self):
        return self.rock_block.satellite_transfer()  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    rock_block_ping = RockBlockAPI()
    rock_block_ping.check_mailbox()
