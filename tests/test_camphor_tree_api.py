import base64
import configparser

from apis.camphor_tree_api import send_satellite_message, relay_email_message_to_cloud_loop, \
    relay_cloud_loop_message_to_email, save_gmail_push_id_to_file, get_gmail_push_id_from_config, get_gmail_push_id, \
    push_id_is_new


class TestCamphorTreeApi:
    def test_send_satellite_message_satsuki(self, mock_cloud_loop_message_set_up_hex_encoded_message,
                                            mock_cloud_loop_message_set_up_message_to_hex_encode,
                                            mock_cloud_loop_message_send_cloud_loop_message):
        test_server_option = "Satsuki"
        send_status = send_satellite_message("test_email", "test_info_level", "test_message_body", test_server_option)
        assert mock_cloud_loop_message_set_up_hex_encoded_message.called
        assert mock_cloud_loop_message_set_up_message_to_hex_encode.called
        assert mock_cloud_loop_message_send_cloud_loop_message.called
        assert send_status == 'Send Success'

    def test_send_satellite_message_mei(self, mock_cloud_loop_message_set_up_hex_encoded_message,
                                        mock_cloud_loop_message_set_up_message_to_hex_encode,
                                        mock_rock_block_api_set_up_uart, mock_rock_block_api_send_data_out):
        test_server_option = "Mei"
        send_status = send_satellite_message("test_email", "test_info_level", "test_message_body", test_server_option)
        assert mock_rock_block_api_set_up_uart.called
        assert mock_rock_block_api_send_data_out.called
        assert send_status == 'Send Success'

    def test_relay_email_message_to_cloud_loop_no_messages(self, mock_gmail_api_set_up_google_client_id,
                                                           mock_gmail_api_set_up_set_up_google_client_secret,
                                                           mock_gmail_api_set_up_set_up_refresh_token,
                                                           mock_gmail_api_set_up_set_up_google_topic,
                                                           mock_gmail_api_set_up_set_up_email_recipient,
                                                           mock_gmail_api_set_up_set_up_email_sender,
                                                           mock_gmail_api_set_up_set_up_message_size,
                                                           mock_gmail_api_gmail_get_messages_from_push,
                                                           mock_cloud_loop_message_set_up_hex_encoded_message,
                                                           mock_cloud_loop_message_set_up_message_to_hex_encode,
                                                           mock_cloud_loop_message_send_cloud_loop_message):
        relay_email_message_to_cloud_loop()
        assert not mock_cloud_loop_message_set_up_hex_encoded_message.called
        assert not mock_cloud_loop_message_set_up_message_to_hex_encode.called
        assert not mock_cloud_loop_message_send_cloud_loop_message.called

    def test_relay_email_message_to_cloud_loop_one_message(self, mock_gmail_api_set_up_google_client_id,
                                                           mock_gmail_api_set_up_set_up_google_client_secret,
                                                           mock_gmail_api_set_up_set_up_refresh_token,
                                                           mock_gmail_api_set_up_set_up_google_topic,
                                                           mock_gmail_api_set_up_set_up_email_recipient,
                                                           mock_gmail_api_set_up_set_up_email_sender,
                                                           mock_gmail_api_set_up_set_up_message_size,
                                                           mock_gmail_api_gmail_get_messages_from_push,
                                                           mock_gmail_api_get_new_gmail_messages,
                                                           mock_gmail_api_gmail_get_message_by_id,
                                                           mock_cloud_loop_message_set_up_hex_encoded_message,
                                                           mock_cloud_loop_message_set_up_message_to_hex_encode,
                                                           mock_cloud_loop_message_send_cloud_loop_message):
        mock_gmail_api_get_new_gmail_messages.return_value = ["test_message"]
        mock_gmail_api_gmail_get_message_by_id.return_value = ("message_from", "message_subject", "message_text")

        relay_email_message_to_cloud_loop()
        assert mock_cloud_loop_message_set_up_hex_encoded_message.called
        assert mock_cloud_loop_message_set_up_message_to_hex_encode.called
        assert mock_cloud_loop_message_send_cloud_loop_message.called

    def test_relay_email_message_to_cloud_loop_message_list(self, mock_gmail_api_set_up_google_client_id,
                                                            mock_gmail_api_set_up_set_up_google_client_secret,
                                                            mock_gmail_api_set_up_set_up_refresh_token,
                                                            mock_gmail_api_set_up_set_up_google_topic,
                                                            mock_gmail_api_set_up_set_up_email_recipient,
                                                            mock_gmail_api_set_up_set_up_email_sender,
                                                            mock_gmail_api_set_up_set_up_message_size,
                                                            mock_gmail_api_gmail_get_messages_from_push,
                                                            mock_gmail_api_get_new_gmail_messages,
                                                            mock_gmail_api_gmail_get_message_by_id,
                                                            mock_cloud_loop_message_set_up_hex_encoded_message,
                                                            mock_cloud_loop_message_set_up_message_to_hex_encode,
                                                            mock_cloud_loop_message_send_cloud_loop_message):
        mock_gmail_api_get_new_gmail_messages.return_value = ["test_message_1", "test_message_2", "test_message_3"]
        mock_gmail_api_gmail_get_message_by_id.return_value = ("message_from", "message_subject", "message_text")

        relay_email_message_to_cloud_loop()
        assert mock_cloud_loop_message_set_up_hex_encoded_message.call_count == 3
        assert mock_cloud_loop_message_set_up_message_to_hex_encode.call_count == 3
        assert mock_cloud_loop_message_send_cloud_loop_message.call_count == 3

    def test_relay_cloud_loop_message_to_email(self, mock_gmail_api_set_up_google_client_id,
                                               mock_gmail_api_set_up_set_up_google_client_secret,
                                               mock_gmail_api_set_up_set_up_refresh_token,
                                               mock_gmail_api_set_up_set_up_google_topic,
                                               mock_gmail_api_set_up_set_up_email_recipient,
                                               mock_gmail_api_set_up_set_up_email_sender,
                                               mock_gmail_api_set_up_set_up_message_size,
                                               mock_gmail_api_send_gmail_message,
                                               mock_cloud_loop_message_set_up_hex_encoded_message,
                                               mock_cloud_loop_message_set_up_message_to_hex_encode,
                                               mock_cloud_loop_message_send_cloud_loop_message):
        relay_cloud_loop_message_to_email("test_request_json_data")
        assert mock_gmail_api_send_gmail_message.called

    # TODO: get full test data from gmail post
    def test_get_gmail_push_id(self):
        test_push_id = b'6675'
        test_gmail_message_data = b'{"historyId": ' + test_push_id + b'}'
        test_gmail_message_data = base64.urlsafe_b64encode(test_gmail_message_data)
        push_id = get_gmail_push_id(test_gmail_message_data)
        assert push_id == int(test_push_id.decode('utf-8'))

    def test_save_gmail_push_id_to_file(self, mock_open):
        test_push_id = "5"
        save_gmail_push_id_to_file("test_config_file_name", test_push_id)
        # TODO: add temp file catch to check file results
        assert mock_open.called

    # TODO: switch to hash of last email string in full, no config file
    # TODO: write tests for this different functionality
    def test_get_gmail_push_id_from_config(self, tmpdir):
        test_config_file_name = "test_config.ini"
        test_push_id = "5"
        read_config_file = configparser.ConfigParser()
        read_config_file["GMailMessageId"] = {"current": str(test_push_id)}
        assert read_config_file["GMailMessageId"]["current"] == test_push_id
        test_config_file_object = tmpdir.mkdir("subdir").join(test_config_file_name)
        read_config_file.write(test_config_file_object)

        checking_config_file = configparser.ConfigParser()
        checking_config_file.read(test_config_file_name)
        assert checking_config_file["GMailMessageId"]["current"] == test_push_id
        current_push_id = get_gmail_push_id_from_config(test_config_file_name)
        assert current_push_id == test_push_id

    def test_push_id_is_new(self, mock_get_gmail_push_id_from_config, mock_save_gmail_push_id_to_file):
        push_id_return = push_id_is_new("5")
        assert push_id_return is True
