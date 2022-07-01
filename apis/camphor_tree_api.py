import base64
import configparser
import json

from flask import request

from apis.cloud_loop_api import CloudLoopMessage
from apis.google_api import GMailMessage
from apis.rock_block_api import RockBlockAPI


def send_satellite_message(email_form, server_option):
    rock_block_message = CloudLoopMessage(message_from=email_form.email.data,
                                          message_subject=email_form.info_level.data,
                                          message_to_encode=email_form.message_body.data)
    if server_option == 'Satsuki':
        rock_block_message.send_cloud_loop_message()
    if server_option == 'Mei':
        rock_block_api = RockBlockAPI()
        rock_block_api.send_data_out(rock_block_message.payload_list)
    send_status = 'Send Success'
    return send_status


def relay_email_message_to_cloud_loop():
    message_for_cloud_loop = GMailMessage()
    message_for_cloud_loop.gmail_get_messages_from_push()
    for message in message_for_cloud_loop.new_gmail_messages:
        message_from, message_subject, message_text = message_for_cloud_loop.gmail_get_message_by_id(message)
        message_to_cloud_loop = CloudLoopMessage(message_from=message_from,
                                                 message_subject=message_subject,
                                                 message_to_encode=message_text)
        message_to_cloud_loop.send_cloud_loop_message()
        print("POST CloudLoop Message Handled")


def relay_cloud_loop_message_to_email():
    print("POST CloudLoop Ping Received")
    message_from_cloud_loop = CloudLoopMessage(hex_message=request.json['data'])
    gmail_message = GMailMessage(message_to=message_from_cloud_loop.recipient_list,
                                 message_subject=message_from_cloud_loop.message_subject,
                                 message_text=message_from_cloud_loop.message)
    gmail_message.send_gmail_message()
    print("POST GMail Message Handled")


def get_gmail_push_id(gmail_message_data):
    print("POST GMail Ping Received")
    # push_id = request.json['message']['messageId']
    push_id = json.loads(base64.urlsafe_b64decode(gmail_message_data).decode('utf-8'))['historyId']
    print("New Push ID: " + str(push_id))
    return push_id


def save_gmail_push_id_to_file(config_file, config_file_name, push_id):
    config_file["GMailMessageId"] = {"current": str(push_id)}
    with open(config_file_name, "w") as file_object:
        config_file.write(file_object)
    print("Saved Push ID " + str(push_id) + " to " + config_file_name)


def get_gmail_push_id_from_config(config_file, config_file_name):
    config_file.read(config_file_name)
    current_push_id = config_file["GMailMessageId"]["current"]
    print("Old Push ID: " + str(current_push_id))
    return current_push_id


def push_id_is_new(push_id):
    config_file_name = "historyId.ini"
    config_file = configparser.ConfigParser()
    if config_file.read(config_file_name):
        current_push_id = get_gmail_push_id_from_config(config_file, config_file_name)
        if int(push_id) != int(current_push_id):
            save_gmail_push_id_to_file(config_file, config_file_name, push_id)
            return True
        else:
            print("Bounce This One")
            return False
    else:
        save_gmail_push_id_to_file(config_file, config_file_name, push_id)
    return True
