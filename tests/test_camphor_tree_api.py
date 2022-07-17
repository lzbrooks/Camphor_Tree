import configparser

from apis.camphor_tree_api import send_satellite_message, relay_email_message_to_cloud_loop, \
    relay_cloud_loop_message_to_email, save_gmail_push_id_to_file


class TestCamphorTreeApi:
    def test_send_satellite_message_satsuki(self, mock_cloud_loop_message_set_up_hex_encoded_message,
                                            mock_cloud_loop_message_set_up_message_to_hex_encode,
                                            mock_cloud_loop_message_send_cloud_loop_message):
        mock_cloud_loop_message_set_up_hex_encoded_message.return_value = None
        mock_cloud_loop_message_set_up_message_to_hex_encode.return_value = None
        mock_cloud_loop_message_send_cloud_loop_message.return_value = None
        test_server_option = "Satsuki"
        send_status = send_satellite_message("test_email", "test_info_level", "test_message_body", test_server_option)
        assert mock_cloud_loop_message_set_up_hex_encoded_message.called
        assert mock_cloud_loop_message_set_up_message_to_hex_encode.called
        assert mock_cloud_loop_message_send_cloud_loop_message.called
        assert send_status == 'Send Success'

    def test_send_satellite_message_mei(self, mock_cloud_loop_message_set_up_hex_encoded_message,
                                        mock_cloud_loop_message_set_up_message_to_hex_encode,
                                        mock_rock_block_api_set_up_uart, mock_rock_block_api_send_data_out):
        mock_cloud_loop_message_set_up_hex_encoded_message.return_value = None
        mock_cloud_loop_message_set_up_message_to_hex_encode.return_value = None
        mock_rock_block_api_set_up_uart.return_value = None
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
        mock_gmail_api_set_up_google_client_id.return_value = None
        mock_gmail_api_set_up_set_up_google_client_secret.return_value = None
        mock_gmail_api_set_up_set_up_refresh_token.return_value = None
        mock_gmail_api_set_up_set_up_google_topic.return_value = None
        mock_gmail_api_set_up_set_up_email_recipient.return_value = None
        mock_gmail_api_set_up_set_up_email_sender.return_value = None
        mock_gmail_api_set_up_set_up_message_size.return_value = None
        mock_gmail_api_gmail_get_messages_from_push.return_value = None

        mock_cloud_loop_message_set_up_hex_encoded_message.return_value = None
        mock_cloud_loop_message_set_up_message_to_hex_encode.return_value = None
        mock_cloud_loop_message_send_cloud_loop_message.return_value = None

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
        mock_gmail_api_set_up_google_client_id.return_value = None
        mock_gmail_api_set_up_set_up_google_client_secret.return_value = None
        mock_gmail_api_set_up_set_up_refresh_token.return_value = None
        mock_gmail_api_set_up_set_up_google_topic.return_value = None
        mock_gmail_api_set_up_set_up_email_recipient.return_value = None
        mock_gmail_api_set_up_set_up_email_sender.return_value = None
        mock_gmail_api_set_up_set_up_message_size.return_value = None

        mock_gmail_api_gmail_get_messages_from_push.return_value = None
        mock_gmail_api_get_new_gmail_messages.return_value = ["test_message"]
        mock_gmail_api_gmail_get_message_by_id.return_value = ("message_from", "message_subject", "message_text")

        mock_cloud_loop_message_set_up_hex_encoded_message.return_value = None
        mock_cloud_loop_message_set_up_message_to_hex_encode.return_value = None
        mock_cloud_loop_message_send_cloud_loop_message.return_value = None

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
        mock_gmail_api_set_up_google_client_id.return_value = None
        mock_gmail_api_set_up_set_up_google_client_secret.return_value = None
        mock_gmail_api_set_up_set_up_refresh_token.return_value = None
        mock_gmail_api_set_up_set_up_google_topic.return_value = None
        mock_gmail_api_set_up_set_up_email_recipient.return_value = None
        mock_gmail_api_set_up_set_up_email_sender.return_value = None
        mock_gmail_api_set_up_set_up_message_size.return_value = None

        mock_gmail_api_gmail_get_messages_from_push.return_value = None
        mock_gmail_api_get_new_gmail_messages.return_value = ["test_message_1", "test_message_2", "test_message_3"]
        mock_gmail_api_gmail_get_message_by_id.return_value = ("message_from", "message_subject", "message_text")

        mock_cloud_loop_message_set_up_hex_encoded_message.return_value = None
        mock_cloud_loop_message_set_up_message_to_hex_encode.return_value = None
        mock_cloud_loop_message_send_cloud_loop_message.return_value = None

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
        mock_gmail_api_set_up_google_client_id.return_value = None
        mock_gmail_api_set_up_set_up_google_client_secret.return_value = None
        mock_gmail_api_set_up_set_up_refresh_token.return_value = None
        mock_gmail_api_set_up_set_up_google_topic.return_value = None
        mock_gmail_api_set_up_set_up_email_recipient.return_value = None
        mock_gmail_api_set_up_set_up_email_sender.return_value = None
        mock_gmail_api_set_up_set_up_message_size.return_value = None
        mock_gmail_api_send_gmail_message.return_value = None

        mock_cloud_loop_message_set_up_hex_encoded_message.return_value = None
        mock_cloud_loop_message_set_up_message_to_hex_encode.return_value = None
        mock_cloud_loop_message_send_cloud_loop_message.return_value = None

        relay_cloud_loop_message_to_email("test_request_json_data")
        assert mock_gmail_api_send_gmail_message.called

    def test_save_gmail_push_id_to_file(self, mock_open):
        test_config_file = configparser.ConfigParser()
        test_push_id = "5"
        save_gmail_push_id_to_file(test_config_file, "test_config_file_name", test_push_id)
        assert test_config_file["GMailMessageId"] == {"current": str(test_push_id)}
        assert mock_open.called
