from wtforms import Form, StringField, TextAreaField, validators, RadioField

from config.config import Config


class EmailForm(Form):
    email = StringField('Email Address', validators=[validators.Length(min=6, max=35),
                                                     validators.InputRequired(),
                                                     validators.Email()])
    info_level = RadioField('Info Level', choices=Config.get_info_levels(),
                            validators=[validators.InputRequired()]
                            )
    message_body = TextAreaField('Message Body', validators=[validators.Length(max=250),
                                                             validators.DataRequired()])
