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
        uart = serial.Serial("/dev/serial0", 19200)
        self.rock_block = RockBlock(uart)
        # print(self.rock_block.model)

    def talk_to_rock_block(self):
        print("Talking to satellite...")
        status = self.rock_block.satellite_transfer()
        retry = 0
        while status[0] > 8:
            time.sleep(10)
            status = self.rock_block.satellite_transfer()
            print(retry, status)
            retry += 1
        print("\nDONE.")

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
    rock_block_ping.talk_to_rock_block()
    hex_data = rock_block_ping.get_data_in()
    message_from_rock_block = CloudLoopMessage(hex_message=hex_data)
    message_to_write = [message_from_rock_block.recipient_list, message_from_rock_block.message_subject,
                        message_from_rock_block.message]
    message_file_name = "" + str(datetime.now()) + ".txt"
    with open(message_file_name, "w") as file:
        file.writelines(message_to_write)
