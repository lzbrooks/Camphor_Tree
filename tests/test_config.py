import os

from config.config import Config


class TestConfig:
    def test_config_get_sister_satsuki(self, mocker):
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_SIS": "Satsuki"})
        config_return = Config().get_sister()
        assert config_return == "Satsuki"

    def test_config_get_sister_mei(self, mocker):
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_SIS": "Mei"})
        config_return = Config().get_sister()
        assert config_return == "Mei"

    def test_config_get_sister_default(self):
        config_return = Config().get_sister()
        assert config_return == "Satsuki"

    def test_config_get_pass_en_var(self, mocker):
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_PASS": "test_password"})
        config_return = Config().get_pass()
        assert config_return == "test_password"

    def test_config_get_pass_default(self):
        config_return = Config().get_pass()
        assert config_return == "satsuki"

    def test_config_get_relay_switch_true(self, mocker):
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_RELAY": "True"})
        config_return = Config().get_relay_switch()
        assert config_return

    def test_config_get_relay_switch_false(self, mocker):
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_RELAY": "False"})
        config_return = Config().get_relay_switch()
        assert not config_return

    def test_config_get_relay_switch_default(self):
        config_return = Config().get_relay_switch()
        assert config_return

    def test_config_get_email_env_var(self, mocker):
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_EMAIL": "test_sender@gmail.com"})
        config_return = Config().get_email()
        assert config_return == "test_sender@gmail.com"

    def test_config_get_email_parameter(self):
        config_return = Config().get_email("test_sender@gmail.com")
        assert config_return == "test_sender@gmail.com"

    def test_config_get_email_default(self):
        config_return = Config().get_email()
        assert not config_return

    def test_config_get_whitelist_multiple(self, mocker):
        whitelist = '1,test_sender_1@gmail.com;2,test_sender_2@gmail.com;3,test_sender_3@gmail.com'
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_WHITELIST": whitelist})
        config_return = Config().get_whitelist()
        assert config_return == {'1': 'test_sender_1@gmail.com',
                                 '2': 'test_sender_2@gmail.com',
                                 '3': 'test_sender_3@gmail.com'}

    def test_config_get_whitelist_single(self, mocker):
        whitelist = '1,test_sender_1@gmail.com'
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_WHITELIST": whitelist})
        config_return = Config().get_whitelist()
        assert config_return == {'1': 'test_sender_1@gmail.com'}

    def test_config_get_whitelist_default(self):
        config_return = Config().get_whitelist()
        assert not config_return

    def test_config_get_info_levels(self):
        config_return = Config().get_info_levels()
        assert config_return == [('Emergency', 'Emergency'), ('Urgent', 'Urgent'), ('Info', 'Info')]

    def test_config_get_google_client_credentials_file_env_var(self, mocker, tmp_path):
        tmp_token_file = tmp_path / 'credentials.json'
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_token_file.as_posix()})
        config_return = Config().get_google_client_credentials_file()
        assert config_return == tmp_token_file.as_posix()

    def test_config_get_google_client_credentials_file_default(self):
        config_return = Config().get_google_client_credentials_file()
        assert config_return == 'credentials.json'

    def test_config_get_google_access_token_file_env_var(self, mocker, tmp_path):
        tmp_token_file = tmp_path / 'token.json'
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        config_return = Config().get_google_access_token_file()
        assert config_return == tmp_token_file.as_posix()

    def test_config_get_google_access_token_file_default(self):
        config_return = Config().get_google_access_token_file()
        assert config_return == 'token.json'

    def test_config_get_cloud_loop_auth_token_env_var(self, mocker):
        google_auth_token = 'test_auth_token'
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_AUTH_TOKEN": google_auth_token})
        config_return = Config().get_cloud_loop_auth_token()
        assert config_return == google_auth_token

    def test_config_get_cloud_loop_auth_token_default(self):
        config_return = Config().get_cloud_loop_auth_token()
        assert not config_return

    def test_config_get_imei_env_var(self, mocker):
        cloud_loop_imei = 'test_imei'
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_IMEI": cloud_loop_imei})
        config_return = Config().get_imei()
        assert config_return == cloud_loop_imei

    def test_config_get_imei_default(self):
        config_return = Config().get_imei()
        assert not config_return

    def test_config_get_rock_block_id_env_var(self, mocker):
        rock_block_id = 'test_rock_block_id'
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_HARDWARE_ID": rock_block_id})
        config_return = Config().get_rock_block_id()
        assert config_return == rock_block_id

    def test_config_get_rock_block_id_default(self):
        config_return = Config().get_rock_block_id()
        assert not config_return

    def test_config_get_google_topic_env_var(self, mocker):
        google_topic = 'test_google_topic'
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_TOPIC": google_topic})
        config_return = Config().get_google_topic()
        assert config_return == google_topic

    def test_config_get_google_topic_default(self):
        config_return = Config().get_google_topic()
        assert not config_return

    def test_config_get_google_sub_env_var(self, mocker):
        google_sub = 'test_google_sub'
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_SUB": google_sub})
        config_return = Config().get_google_sub()
        assert config_return == google_sub

    def test_config_get_google_sub_default(self):
        config_return = Config().get_google_sub()
        assert not config_return

    def test_config_get_max_message_size_env_var(self, mocker):
        max_message_size = '250'
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_MAX_SIZE": max_message_size})
        config_return = Config().get_max_message_size()
        assert config_return == int(max_message_size)

    def test_config_get_max_message_size_default(self):
        config_return = Config().get_max_message_size()
        assert not config_return
