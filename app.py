from flask import Flask, render_template, request

from apis.camphor_tree_api import relay_email_message_to_cloud_loop, \
    relay_cloud_loop_message_to_email, send_satellite_message, get_latest_gmail_message_text, message_text_is_new
from forms.EmailForm import EmailForm
from forms.LoginForm import LoginForm
from config.config import Config

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
        send_status = send_satellite_message(email_form.email.data,
                                             email_form.info_level.data,
                                             email_form.message_body.data, server_option)
        return render_template('email_form.html', form=email_form, server_option=server_option, send_status=send_status)
    if not request.is_json and "submit-email" in request.form and not email_form.validate():
        send_status = 'Send Failure'
        return render_template('email_form.html', form=email_form, server_option=server_option, send_status=send_status)
    if request.is_json and "imei" in request.json and request.json['imei'] == Config.get_imei():
        relay_cloud_loop_message_to_email(request.json['data'])
        return "Success", 200
    if request.is_json and "subscription" in request.json and request.json['subscription'] == Config.get_google_sub():
        new_message_text = get_latest_gmail_message_text()
        if message_text_is_new(new_message_text):
            relay_email_message_to_cloud_loop()
        else:
            return "Bounced This One", 200
        return "Success", 200
    return render_template('login.html', form=login_form, server_option=server_option)
