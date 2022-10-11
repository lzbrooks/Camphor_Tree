import os
from typing import Optional, List, Dict


class Config:
    @staticmethod
    def get_sister() -> str:
        return os.environ.get("CAMPHOR_TREE_SIS", "Satsuki")

    @staticmethod
    def get_pass() -> str:
        return os.environ.get("CAMPHOR_TREE_PASS", "satsuki")

    @staticmethod
    def get_relay_switch() -> bool:
        # CAMPHOR_TREE_RELAY='True'
        # CAMPHOR_TREE_RELAY='False'
        return os.environ.get("CAMPHOR_TREE_RELAY", "True") == 'True'

    @staticmethod
    def get_email(message_from: str = None) -> Optional[str]:
        return os.environ.get('CAMPHOR_TREE_EMAIL', message_from)

    @staticmethod
    def get_whitelist() -> Optional[Dict[str, str]]:
        # CAMPHOR_TREE_WHITELIST='1,email;2,email;3,email' -> bool
        # TODO: use a list like collated_massage_parts instead of dict
        env_whitelist = os.environ.get('CAMPHOR_TREE_WHITELIST')
        whitelist = {}
        if env_whitelist:
            whitelist_emails = env_whitelist.split(";")
            for email in whitelist_emails:
                email_key, email_val = email.split(",")
                whitelist[email_key] = email_val
        return whitelist

    @staticmethod
    def get_info_levels() -> List[tuple]:
        return [('Emergency', 'Emergency'), ('Urgent', 'Urgent'), ('Info', 'Info')]

    @staticmethod
    def get_google_client_credentials_file() -> str:
        return os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

    @staticmethod
    def get_google_access_token_file() -> str:
        return os.environ.get("CAMPHOR_TREE_ACCESS_TOKEN_FILE", "token.json")

    @staticmethod
    def get_cloud_loop_auth_token() -> Optional[str]:
        return os.environ.get("CAMPHOR_TREE_AUTH_TOKEN")

    @staticmethod
    def get_imei() -> Optional[str]:
        return os.environ.get("CAMPHOR_TREE_IMEI")

    @staticmethod
    def get_rock_block_id() -> Optional[str]:
        return os.environ.get("CAMPHOR_TREE_HARDWARE_ID")

    @staticmethod
    def get_google_topic() -> Optional[str]:
        return os.environ.get("CAMPHOR_TREE_TOPIC")

    @staticmethod
    def get_google_sub() -> Optional[str]:
        return os.environ.get("CAMPHOR_TREE_SUB")

    @staticmethod
    def get_max_message_size() -> int:
        return int(os.environ.get("CAMPHOR_TREE_MAX_SIZE", "250"))
