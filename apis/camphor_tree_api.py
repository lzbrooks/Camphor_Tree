import json
from pathlib import Path

from apis.cloud_loop_api import HexEncodeForCloudLoop, DecodeCloudLoopMessage
from apis.google_api import GMailAPI
from apis.rock_block_api import RockBlockAPI


def send_satellite_message(email, info_level, message_body, server_option):
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


# TODO: test
def relay_cloud_loop_message_to_email(request_json_data, message_file_name="collated_cloud_loop_messages.json"):
    print("POST CloudLoop Ping Received")
    message_from_cloud_loop = DecodeCloudLoopMessage(hex_message=request_json_data)
    message_from_cloud_loop.decode_hex_message()
    complete_subject, complete_text = collate_cloud_loop_message(message_from_cloud_loop.message_hash_id,
                                                                 message_from_cloud_loop.message_part_number,
                                                                 message_from_cloud_loop.parts_total,
                                                                 message_from_cloud_loop.message_text,
                                                                 message_file_name)
    if complete_text:
        gmail_message = GMailAPI(message_to=message_from_cloud_loop.recipient_list,
                                 message_subject=complete_subject,
                                 message_text=complete_text)
        gmail_message.send_gmail_message()
    print("POST GMail Message Handled")


# TODO: test
def collate_cloud_loop_message(message_hash_id, message_part_number, parts_total,
                               message_text, message_file_path):
    # {"messages_being_collated": {#fbc84a": ["Info", "Testing"]}, {}}
    all_collated_parts = read_message_from_file(message_file_path)
    if not all_collated_parts:
        all_collated_parts = {"messages_being_collated": {message_hash_id: [None for _ in range(int(parts_total))]}}
    all_collated_parts["messages_being_collated"][message_hash_id][message_part_number - 1] = message_text
    current_message_parts = all_collated_parts["messages_being_collated"][message_hash_id]
    if None not in current_message_parts:
        remove_completely_collated_message(all_collated_parts, message_file_path,
                                           message_hash_id, message_part_number, parts_total)
        return assemble_complete_message_for_gmail(current_message_parts)
    write_message_to_file(all_collated_parts, message_file_path)
    print(f"Saved Cloud Loop Message")
    print(all_collated_parts["messages_being_collated"][message_hash_id][message_part_number - 1])
    print(f"To {message_file_path}")


# TODO: test
def assemble_complete_message_for_gmail(current_message_parts):
    complete_message_subject = current_message_parts[0]
    complete_message_text = "".join(current_message_parts)
    return complete_message_subject, complete_message_text


# TODO: test
def remove_completely_collated_message(all_collated_parts, message_file_path,
                                       message_hash_id, message_part_number, parts_total):
    print(f"Collation of Cloud Loop Message {message_hash_id} Complete At {message_part_number}/{parts_total}")
    all_collated_parts["messages_being_collated"].pop(message_hash_id)
    write_message_to_file(all_collated_parts, message_file_path)
    print(f"Removed {message_hash_id} From {message_file_path}")


def get_latest_gmail_message_parts():
    print("POST GMail Ping Received")
    message_for_cloud_loop = GMailAPI()
    message = message_for_cloud_loop.get_top_inbox_message()
    message_from, message_subject, message_text = message_for_cloud_loop.get_gmail_message_by_id(message)
    return message_from, message_subject, message_text


def message_text_is_new(message_text, message_file_name="last_gmail_message.json"):
    last_gmail_message_text = read_message_from_file(message_file_name)["last_gmail_message"]
    if message_text != last_gmail_message_text:
        save_gmail_message_to_file(message_file_name, message_text)
        print("New GMail Message Detected")
        return True
    else:
        print("Bounce This One")
        return False


def save_gmail_message_to_file(message_file_path, message_text):
    message_json = {"last_gmail_message": message_text}
    write_message_to_file(message_json, message_file_path)
    print(f"Saved GMail Message to {message_file_path}")


def relay_email_message_to_cloud_loop(message_from, message_subject, message_text):
    message_to_cloud_loop = HexEncodeForCloudLoop(message_from=message_from,
                                                  message_subject=message_subject,
                                                  message_to_encode=message_text)
    message_to_cloud_loop.send_cloud_loop_message()
    print("POST CloudLoop Message Handled")


def read_message_from_file(message_file_path):
    if Path(message_file_path).is_file():
        with open(message_file_path, 'r') as last_gmail_message_file:
            return json.load(last_gmail_message_file)


def write_message_to_file(message_json, message_file_path):
    with open(message_file_path, "w") as file_object:
        json.dump(message_json, file_object)
