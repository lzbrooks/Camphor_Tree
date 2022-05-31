import base64
import configparser
import json

from flask import Flask, render_template, request

from EmailForm import EmailForm
from LoginForm import LoginForm
from cloud_loop_api import CloudLoopMessage
from config import Config
from google_api import GMailMessage
from rock_block_api import RockBlockAPI

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def console():
    server_option = Config.get_sister()
    login_form = LoginForm(request.form)
    email_form = EmailForm(request.form)
    if not request.is_json and "submit-password" in request.form and not login_form.validate():
        return render_template('login.html', form=login_form, server_option=server_option)
    if not request.is_json and "submit-password" in request.form and login_form.validate():
        send_status = 'Console'
        return render_template('email_form.html', form=email_form, server_option=server_option, send_status=send_status)
    if not request.is_json and "submit-email" in request.form and email_form.validate():
        rock_block_message = CloudLoopMessage(message_from=email_form.email.data,
                                              message_subject=email_form.info_level.data,
                                              message_to_encode=email_form.message_body.data)
        if server_option == 'Satsuki':
            rock_block_message.send_cloud_loop_message()
        if server_option == 'Mei':
            rock_block_api = RockBlockAPI()
            rock_block_api.send_data_out(rock_block_message.payload_list)
        send_status = 'Send Success'
        return render_template('email_form.html', form=email_form, server_option=server_option, send_status=send_status)
    if not request.is_json and "submit-email" in request.form and not email_form.validate():
        send_status = 'Send Failure'
        return render_template('email_form.html', form=email_form, server_option=server_option, send_status=send_status)
    if request.is_json and "imei" in request.json and request.json['imei'] == Config.get_imei():
        print("POST CloudLoop Ping Received")
        message_from_cloud_loop = CloudLoopMessage(hex_message=request.json['data'])
        gmail_message = GMailMessage(message_to=message_from_cloud_loop.recipient_list,
                                     message_subject=message_from_cloud_loop.message_subject,
                                     message_text=message_from_cloud_loop.message)
        gmail_message.send_gmail_message()
        print("POST GMail Message Handled")
        return "Success", 200
    if request.is_json and "subscription" in request.json and request.json['subscription'] == Config.get_google_sub():
        print("POST GMail Ping Received")
        # push_id = request.json['message']['messageId']
        push_id = json.loads(base64.urlsafe_b64decode(request.json['message']['data']).decode('utf-8'))['historyId']
        print("New Push ID: " + str(push_id))
        config_file_name = "historyId.ini"
        config_file = configparser.ConfigParser()
        if config_file.read(config_file_name):
            config_file.read(config_file_name)
            current_push_id = config_file["GMailMessageId"]["current"]
            print("Old Push ID: " + str(current_push_id))
            if int(push_id) != int(current_push_id):
                config_file["GMailMessageId"]["current"] = str(push_id)
                with open(config_file_name, "w") as file_object:
                    config_file.write(file_object)
                print("Saved Push ID " + str(push_id) + " to " + config_file_name)
            else:
                print("Bounced This One")
                return "Bounced This One", 200
        else:
            config_file["GMailMessageId"] = {"current": str(push_id)}
            with open(config_file_name, "w") as file_object:
                config_file.write(file_object)
            print("Saved Push ID " + str(push_id) + " to " + config_file_name)
        message_for_cloud_loop = GMailMessage()
        message_for_cloud_loop.gmail_get_messages_from_push()
        for message in message_for_cloud_loop.new_gmail_messages:
            message_from, message_subject, message_text = message_for_cloud_loop.gmail_get_message_by_id(message)
            message_to_cloud_loop = CloudLoopMessage(message_from=message_from,
                                                     message_subject=message_subject,
                                                     message_to_encode=message_text)
            message_to_cloud_loop.send_cloud_loop_message()
            print("POST CloudLoop Message Handled")
        return "Success", 200
    return render_template('login.html', form=login_form, server_option=server_option)
