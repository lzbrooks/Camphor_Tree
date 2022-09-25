import os


class Config:
    @staticmethod
    def get_sister():
        if 'CAMPHOR_TREE_SIS' in os.environ:
            return os.environ['CAMPHOR_TREE_SIS']
        else:
            return 'Satsuki'

    @staticmethod
    def get_pass():
        if 'CAMPHOR_TREE_PASS' in os.environ:
            return os.environ['CAMPHOR_TREE_PASS']
        else:
            return 'satsuki'

    # TODO: test
    @staticmethod
    def get_relay_switch():
        # CAMPHOR_TREE_RELAY=True
        # CAMPHOR_TREE_RELAY=False
        if 'CAMPHOR_TREE_RELAY' in os.environ:
            return os.environ['CAMPHOR_TREE_RELAY'] == 'True'
        else:
            return True

    @staticmethod
    def get_email(message_from=None):
        if not message_from:
            if 'CAMPHOR_TREE_EMAIL' in os.environ:
                return os.environ['CAMPHOR_TREE_EMAIL']
        return message_from

    @staticmethod
    def get_whitelist():
        # CAMPHOR_TREE_WHITELIST=1,email;2,email;3,email
        if 'CAMPHOR_TREE_WHITELIST' in os.environ:
            whitelist_emails = os.environ['CAMPHOR_TREE_WHITELIST'].split(";")
            whitelist = {}
            for email in whitelist_emails:
                email_key = email.split(",")[0]
                email_val = email.split(",")[1]
                whitelist[email_key] = email_val
            return whitelist

    @staticmethod
    def get_google_secret(google_client_secret=None):
        if not google_client_secret:
            if 'CAMPHOR_TREE_SECRET' in os.environ:
                return os.environ['CAMPHOR_TREE_SECRET']
        return google_client_secret

    @staticmethod
    def get_google_id(google_client_id=None):
        if not google_client_id:
            if 'CAMPHOR_TREE_ID' in os.environ:
                return os.environ['CAMPHOR_TREE_ID']
        return google_client_id

    @staticmethod
    def get_info_levels():
        info_levels = [('Emergency', 'Emergency'), ('Urgent', 'Urgent'), ('Info', 'Info')]
        return info_levels

    # TODO: test
    @staticmethod
    def get_google_client_credentials_file():
        if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
            return os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        else:
            return 'credentials.json'

    # TODO: test
    @staticmethod
    def get_google_access_token_file():
        if 'CAMPHOR_TREE_ACCESS_TOKEN_FILE' in os.environ:
            return os.environ['CAMPHOR_TREE_ACCESS_TOKEN_FILE']
        else:
            return 'token.json'

    @staticmethod
    def get_google_refresh_token():
        if 'CAMPHOR_TREE_REFRESH_TOKEN' in os.environ:
            return os.environ['CAMPHOR_TREE_REFRESH_TOKEN']

    @staticmethod
    def get_cloud_loop_auth_token():
        if 'CAMPHOR_TREE_AUTH_TOKEN' in os.environ:
            return os.environ['CAMPHOR_TREE_AUTH_TOKEN']

    @staticmethod
    def get_imei():
        if 'CAMPHOR_TREE_IMEI' in os.environ:
            return os.environ['CAMPHOR_TREE_IMEI']

    @staticmethod
    def get_rock_block_id():
        if 'CAMPHOR_TREE_HARDWARE_ID' in os.environ:
            return os.environ['CAMPHOR_TREE_HARDWARE_ID']

    @staticmethod
    def get_google_topic():
        if 'CAMPHOR_TREE_TOPIC' in os.environ:
            return os.environ['CAMPHOR_TREE_TOPIC']

    @staticmethod
    def get_google_sub():
        if 'CAMPHOR_TREE_SUB' in os.environ:
            return os.environ['CAMPHOR_TREE_SUB']

    @staticmethod
    def get_max_message_size():
        if 'CAMPHOR_TREE_MAX_SIZE' in os.environ:
            return int(os.environ['CAMPHOR_TREE_MAX_SIZE'])
