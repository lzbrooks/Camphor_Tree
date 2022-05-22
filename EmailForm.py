from wtforms import Form, StringField, TextAreaField, validators, ValidationError, RadioField

from config import Config


class EmailForm(Form):
    email = StringField('Email Address', validators=[validators.Length(min=6, max=35),
                                                     validators.InputRequired(),
                                                     validators.Email()])
    info_level = RadioField('Info Level', choices=Config.get_info_levels(),
                            validators=[validators.InputRequired()]
                            )
    message_body = TextAreaField('Message Body', validators=[validators.Length(min=4, max=270),
                                                             validators.DataRequired()])

    def validate_email(self, email):
        email_whitelist = Config.get_whitelist()
        if self.email.data not in email_whitelist:
            raise ValidationError("Invalid")
