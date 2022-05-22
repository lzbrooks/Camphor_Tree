import os
import sys
from configparser import ConfigParser


class Config:
    def __init__(self, sister=None,
                 password=None,
                 email=None,
                 email_list=None,
                 info_level_list=None):
        self.config_parser = ConfigParser()
        self.config_parser['TREE'] = {}
        self.config_parser['WHITELIST'] = {}
        self.config_parser['URGENCY'] = {}

        # TREE #
        # Sister
        if sister is None and 'CAMPHOR_TREE_SIS' in os.environ:
            self.config_parser['TREE']['Sister'] = os.environ['CAMPHOR_TREE_SIS']
        else:
            self.config_parser['TREE']['Sister'] = 'Satsuki'

        # Password
        if password is None and 'CAMPHOR_TREE_PASS' in os.environ:
            self.config_parser['TREE']['Password'] = os.environ['CAMPHOR_TREE_PASS']
        else:
            self.config_parser['TREE']['Password'] = 'satsuki'

        # Email
        if 'CAMPHOR_TREE_EMAIL' in os.environ:
            self.config_parser['TREE']['Email'] = os.environ['CAMPHOR_TREE_EMAIL']

        # GOOGLE #
        # Google Client ID
        if 'CAMPHOR_TREE_ID' in os.environ:
            self.config_parser['GOOGLE']['CLIENT_ID'] = os.environ['CAMPHOR_TREE_ID']

        # Google Client Secret
        if 'CAMPHOR_TREE_SECRET' in os.environ:
            self.config_parser['GOOGLE']['CLIENT_SECRET'] = os.environ['CAMPHOR_TREE_SECRET']

        # WHITELIST #
        # Email Whitelist
        if email_list is None and sys.argv:
            for iteration, email in enumerate(sys.argv):
                email_key = "email_" + str(iteration)
                self.config_parser['WHITELIST'].update({
                    email_key: email
                })

        # URGENCY #
        # Info Level List
        if info_level_list is None:
            self.config_parser['URGENCY'] = {
                '1': 'Emergency',
                '2': 'Urgent',
                '3': 'Info'
            }

    def write_config_file(self):
        with open('config.ini', 'w') as configfile:
            self.config_parser.write(configfile)

    @staticmethod
    def read_config_file():
        config = ConfigParser()
        config.read('config.ini')
        return config
