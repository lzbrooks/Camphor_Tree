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

    @staticmethod
    def get_email():
        if 'CAMPHOR_TREE_EMAIL' in os.environ:
            return os.environ['CAMPHOR_TREE_EMAIL']

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
    def get_google_secret():
        if 'CAMPHOR_TREE_SECRET' in os.environ:
            return os.environ['CAMPHOR_TREE_SECRET']

    @staticmethod
    def get_google_id():
        if 'CAMPHOR_TREE_ID' in os.environ:
            return os.environ['CAMPHOR_TREE_ID']

    @staticmethod
    def get_info_levels():
        info_levels = [('Emergency', 'Emergency'), ('Urgent', 'Urgent'), ('Info', 'Info')]
        return info_levels

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

    @classmethod
    def get_max_message_size(cls):
        if 'CAMPHOR_TREE_MAX_SIZE' in os.environ:
            return os.environ['CAMPHOR_TREE_MAX_SIZE']
