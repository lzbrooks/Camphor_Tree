from wtforms import Form, PasswordField, validators, ValidationError

from config import Config


class LoginForm(Form):
    password = PasswordField('Password', validators=[
        validators.InputRequired()
    ])

    def validate_password(self, password):
        reference_password = Config.get_pass()
        if self.password.data != reference_password:
            raise ValidationError("Incorrect")
