from wtforms import Form, StringField, TextAreaField, validators, ValidationError, RadioField

from config import Config


class EmailForm(Form):
    email = StringField('Email Address', validators=[validators.Length(min=6, max=35),
                                                     validators.InputRequired(),
                                                     validators.Email()])
    info_level = RadioField('Info Level', choices=Config.read_config_file().items('URGENCY'),
                            validators=[validators.InputRequired()]
                            )
    message_body = TextAreaField('Message Body', validators=[validators.Length(min=4, max=270),
                                                             validators.DataRequired()])

    def validate_email(self, email):
        email_whitelist = Config.read_config_file()['WHITELIST'].values()
        if self.email.data not in email_whitelist:
            raise ValidationError("Invalid")
