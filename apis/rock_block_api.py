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
    def __init__(self):
        self.rock_block = None
        self.set_up_uart()

    def set_up_uart(self):
        print("RockBLOCK Processing...")
        uart = serial.Serial("/dev/serial0", 19200)
        self.rock_block = RockBlock(uart)
        print("RockBLOCK Processed")

    def talk_to_rock_block(self):
        print("Talking to satellite...")
        status = self.get_satellite_transfer()
        while status[0] > 8:
            time.sleep(10)
            self.get_satellite_transfer()
            print(status)
        print("\nDONE.")
        return status

    def get_satellite_transfer(self):
        return self.rock_block.satellite_transfer()

    def get_data_in(self):
        return self.rock_block.data_in

    def set_data_out(self, data):
        self.rock_block.data_out = data

    def send_data_out(self, data):
        for message in data:
            self.set_data_out(message.encode())
            self.talk_to_rock_block()


def process_rock_block_status(status_of_mailbox):
    print(status_of_mailbox)
    if status_of_mailbox[2] == 0:
        print("No Messages Waiting")
    if status_of_mailbox[2] == 1:
        print("Message Received")
    print("Size in bytes of message: " + str(status_of_mailbox[4]))
    print("Number of Messages in Queue: " + str(status_of_mailbox[5]))


def save_rock_block_hex_data_to_file(hex_data):
    print(hex_data)
    if hex_data:
        message_from_rock_block = DecodeCloudLoopMessage(hex_message=hex_data)
        message_to_write = message_from_rock_block.recipient_list + \
                           [message_from_rock_block.message_subject, message_from_rock_block.message]
        message_file_name = "Inbox/" + datetime.now().strftime("%Y_%m_%d__%H_%M_%S") + ".txt"
        with open(message_file_name, "w") as file:
            file.writelines("%s\n" % line for line in message_to_write)
        print("Message Witten To: " + message_file_name)


if __name__ == "__main__":
    rock_block_ping = RockBlockAPI()
    satellite_status = rock_block_ping.talk_to_rock_block()
    process_rock_block_status(satellite_status)
    hex_data_in = rock_block_ping.get_data_in()
    save_rock_block_hex_data_to_file(hex_data_in)
