import os


class Config:
    @staticmethod
    def get_sister():
        return os.environ.get("CAMPHOR_TREE_SIS", "Satsuki")

    @staticmethod
    def get_pass():
        return os.environ.get("CAMPHOR_TREE_PASS", "satsuki")

    @staticmethod
    def get_relay_switch():
        # CAMPHOR_TREE_RELAY='True'
        # CAMPHOR_TREE_RELAY='False'
        return os.environ.get("CAMPHOR_TREE_RELAY", "True") == 'True'

    @staticmethod
    def get_email(message_from=None):
        return os.environ.get('CAMPHOR_TREE_EMAIL', message_from)

    @staticmethod
    def get_whitelist():
        # CAMPHOR_TREE_WHITELIST='1,email;2,email;3,email'
        env_whitelist = os.environ.get('CAMPHOR_TREE_WHITELIST')
        if env_whitelist:
            whitelist_emails = env_whitelist.split(";")
            whitelist = {}
            for email in whitelist_emails:
                email_key, email_val = email.split(",")
                whitelist[email_key] = email_val
            return whitelist

    @staticmethod
    def get_info_levels():
        return [('Emergency', 'Emergency'), ('Urgent', 'Urgent'), ('Info', 'Info')]

    @staticmethod
    def get_google_client_credentials_file():
        return os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

    @staticmethod
    def get_google_access_token_file():
        return os.environ.get("CAMPHOR_TREE_ACCESS_TOKEN_FILE", "token.json")

    @staticmethod
    def get_cloud_loop_auth_token():
        return os.environ.get("CAMPHOR_TREE_AUTH_TOKEN")

    @staticmethod
    def get_imei():
        return os.environ.get("CAMPHOR_TREE_IMEI")

    @staticmethod
    def get_rock_block_id():
        return os.environ.get("CAMPHOR_TREE_HARDWARE_ID")

    @staticmethod
    def get_google_topic():
        return os.environ.get("CAMPHOR_TREE_TOPIC")

    @staticmethod
    def get_google_sub():
        return os.environ.get("CAMPHOR_TREE_SUB")

    @staticmethod
    def get_max_message_size():
        return int(os.environ.get("CAMPHOR_TREE_MAX_SIZE", "250"))
