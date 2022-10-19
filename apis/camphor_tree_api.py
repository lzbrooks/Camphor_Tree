import json
from pathlib import Path
from typing import Optional, Tuple, Dict

from apis.cloud_loop_api import HexEncodeForCloudLoop, DecodeCloudLoopMessage
from apis.google_api import GMailAPI
from apis.rock_block_api import RockBlockAPI


def send_satellite_message(email: str, info_level: str, message_body: str, server_option: str) -> str:
    rock_block_message = HexEncodeForCloudLoop(message_from=email,
                                               message_subject=info_level,
                                               message_to_encode=message_body)
    if server_option == 'Satsuki':
        rock_block_message.send_cloud_loop_message()
        send_status = 'Send Success'
    elif server_option == 'Mei':
        rock_block_api = RockBlockAPI()
        rock_block_api.send_data_out(rock_block_message.get_payload())
        send_status = 'Send Success'
    else:
        send_status = 'Incorrect Server Mode'
    return send_status


def relay_cloud_loop_message_to_email(request_json_data: str) -> None:
    print("POST CloudLoop Ping Received")
    message_from_cloud_loop = DecodeCloudLoopMessage(hex_message=request_json_data)
    message_from_cloud_loop.decode_hex_message()
    gmail_message = GMailAPI(message_to=message_from_cloud_loop.recipient_list,
                             message_subject=message_from_cloud_loop.message_subject,
                             message_text=message_from_cloud_loop.message_text)
    gmail_message.send_gmail_message()
    print("POST GMail Message Handled")


def get_latest_gmail_message_parts() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    print("POST GMail Ping Received")
    message_for_cloud_loop = GMailAPI()
    message = message_for_cloud_loop.get_top_inbox_message()
    message_from, message_subject, message_text = message_for_cloud_loop.get_gmail_message_by_id(message)
    return message_from, message_subject, message_text


def message_text_is_new(message_text: str, message_file_name: str = "last_gmail_message.json") -> bool:
    last_gmail_message_text = read_gmail_message_from_file(message_file_name)
    if message_text != last_gmail_message_text:
        save_gmail_message_to_file(message_file_name, message_text)
        print("New GMail Message Detected")
        return True
    else:
        print("Bounce This One")
        return False


def read_gmail_message_from_file(message_file_path: str) -> str:
    if Path(message_file_path).is_file():
        with open(message_file_path, 'r') as last_gmail_message_file:
            return json.load(last_gmail_message_file)["last_gmail_message"]


def save_gmail_message_to_file(message_file_path: str, message_text: str) -> None:
    gmail_message_json = {"last_gmail_message": message_text}
    write_gmail_message_to_file(gmail_message_json, message_file_path)
    print("Saved GMail Message to " + str(message_file_path))


def write_gmail_message_to_file(gmail_message_json: Dict[str, str], message_file_path: str) -> None:
    with open(message_file_path, "w") as file_object:
        json.dump(gmail_message_json, file_object)


def relay_email_message_to_cloud_loop(message_from: str, message_subject: str, message_text: str) -> None:
    message_to_cloud_loop = HexEncodeForCloudLoop(message_from=message_from,
                                                  message_subject=message_subject,
                                                  message_to_encode=message_text)
    message_to_cloud_loop.send_cloud_loop_message()
    print("POST CloudLoop Message Handled")
