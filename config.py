import json
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
        # CAMPHOR_TREE_WHITELIST='["Foo", "bar"]'
        if 'CAMPHOR_TREE_WHITELIST' in os.environ:
            return json.loads(os.environ['CAMPHOR_TREE_WHITELIST'])

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
        return {
            '1': 'Emergency',
            '2': 'Urgent',
            '3': 'Info'
        }
