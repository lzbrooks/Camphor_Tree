from flask import Flask, render_template, request

from EmailForm import EmailForm
from LoginForm import LoginForm
from config import Config
from google_api import GMailMessage

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def console():
    server_option = Config.get_sister()
    login_form = LoginForm(request.form)
    email_form = EmailForm(request.form)
    if "submit-password" in request.form and not login_form.validate():
        return render_template('login.html', form=login_form, server_option=server_option)
    if "submit-password" in request.form and login_form.validate():
        send_status = 'Console'
        return render_template('email_form.html', form=email_form, server_option=server_option, send_status=send_status)
    if "submit-email" in request.form and email_form.validate():
        gmail_message = GMailMessage(message_from=email_form.email.data,
                                     message_subject=email_form.info_level.data,
                                     message_text=email_form.message_body.data)
        gmail_message.send_gmail_message()
        send_status = 'Send Success'
        return render_template('email_form.html', form=email_form, server_option=server_option, send_status=send_status)
    if "submit-email" in request.form and not email_form.validate():
        send_status = 'Send Failure'
        return render_template('email_form.html', form=email_form, server_option=server_option, send_status=send_status)
    return render_template('login.html', form=login_form, server_option=server_option)
