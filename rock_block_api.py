import time
from datetime import datetime

import serial
from adafruit_rockblock import RockBlock

from cloud_loop_api import CloudLoopMessage

# Reqs:
# sudo pip3 install --upgrade adafruit-python-shell
# pip3 install Adafruit-Blinka
# pip3 install adafruit-circuitpython-rockblock


class RockBlockAPI:
    def __init__(self):
        print("RockBLOCK Processing...")
        uart = serial.Serial("/dev/serial0", 19200)
        self.rock_block = RockBlock(uart)
        print("RockBLOCK Processed")

    def talk_to_rock_block(self):
        print("Talking to satellite...")
        status = self.rock_block.satellite_transfer()
        while status[0] > 8:
            time.sleep(10)
            status = self.rock_block.satellite_transfer()
            print(status)
        print("\nDONE.")
        return status

    def get_data_in(self):
        return self.rock_block.data_in

    def set_data_out(self, data):
        self.rock_block.data_out = data

    def send_data_out(self, data):
        self.set_data_out(data)
        self.talk_to_rock_block()


# TODO: cron every day
if __name__ == "__main__":
    rock_block_ping = RockBlockAPI()
    status_of_mailbox = rock_block_ping.talk_to_rock_block()
    print(status_of_mailbox)
    if status_of_mailbox[2] == 0:
        print("No Messages Waiting")
    if status_of_mailbox[2] == 1:
        print("Message Received")
    print("Size in bytes of message: " + str(status_of_mailbox[4]))
    print("Number of Messages in Queue: " + str(status_of_mailbox[5]))
    time.sleep(10)
    hex_data = rock_block_ping.rock_block.data_in
    print(hex_data)
    if hex_data:
        message_from_rock_block = CloudLoopMessage(hex_message=hex_data)
        message_to_write = [message_from_rock_block.recipient_list, message_from_rock_block.message_subject,
                            message_from_rock_block.message]
        print("Message From:")
        print(message_from_rock_block.recipient_list)
        message_file_name = "" + str(datetime.now()) + ".txt"
        with open(message_file_name, "w") as file:
            file.writelines(message_to_write)
        print("Message Witten To: " + message_file_name)
