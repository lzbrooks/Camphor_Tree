import json
from pathlib import Path

from apis.cloud_loop_api import HexEncodeForCloudLoop, DecodeCloudLoopMessage
from apis.google_api import GMailMessageGet, GMailMessageSend
from apis.rock_block_api import RockBlockAPI


def send_satellite_message(email, info_level, message_body, server_option):
    rock_block_message = HexEncodeForCloudLoop(message_from=email,
                                               message_subject=info_level,
                                               message_to_encode=message_body)
    if server_option == 'Satsuki':
        rock_block_message.send_cloud_loop_message()
    if server_option == 'Mei':
        rock_block_api = RockBlockAPI()
        rock_block_api.send_data_out(rock_block_message.payload_list)
    # TODO: add check for incorrect server option
    send_status = 'Send Success'
    return send_status


# TODO: testing here
def relay_cloud_loop_message_to_email(request_json_data):
    print("POST CloudLoop Ping Received")
    message_from_cloud_loop = DecodeCloudLoopMessage(hex_message=request_json_data)
    gmail_message = GMailMessageSend(message_to=message_from_cloud_loop.recipient_list,
                                     message_subject=message_from_cloud_loop.message_subject,
                                     message_text=message_from_cloud_loop.message)
    gmail_message.send_gmail_message()
    print("POST GMail Message Handled")


def get_latest_gmail_message_text():
    message_for_cloud_loop = GMailMessageGet()
    message_for_cloud_loop.gmail_get_first_message_from_push()
    message = message_for_cloud_loop.get_new_gmail_message()
    _, _, message_text = message_for_cloud_loop.gmail_get_message_by_id(message)
    return message_text


def message_text_is_new(message_text, message_file_name="last_gmail_message.json"):
    last_gmail_message_text = read_gmail_message_from_file(message_file_name)
    if message_text != last_gmail_message_text:
        save_gmail_message_to_file(message_file_name, message_text)
        return True
    else:
        print("Bounce This One")
        return False


def read_gmail_message_from_file(message_file_path):
    if Path(message_file_path).is_file():
        with open(message_file_path, 'r') as last_gmail_message_file:
            return json.load(last_gmail_message_file)["last_gmail_message"]


def save_gmail_message_to_file(message_file_path, message_text):
    gmail_message_json = {"last_gmail_message": message_text}
    write_gmail_message_to_file(gmail_message_json, message_file_path)
    print("Saved GMail Message to " + str(message_file_path))


def write_gmail_message_to_file(gmail_message_json, message_file_path):
    with open(message_file_path, "w") as file_object:
        json.dump(gmail_message_json, file_object)


def relay_email_message_to_cloud_loop():
    message_for_cloud_loop = GMailMessageGet()
    message_for_cloud_loop.gmail_get_first_message_from_push()
    message = message_for_cloud_loop.get_new_gmail_message()
    message_from, message_subject, message_text = message_for_cloud_loop.gmail_get_message_by_id(message)
    message_to_cloud_loop = HexEncodeForCloudLoop(message_from=message_from,
                                                  message_subject=message_subject,
                                                  message_to_encode=message_text)
    message_to_cloud_loop.send_cloud_loop_message()
    print("POST CloudLoop Message Handled")


# TODO: merge dissect_messages branch here and in main
# TODO: get google cloud account
