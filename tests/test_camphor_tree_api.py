import json

from apis.camphor_tree_api import send_satellite_message, relay_email_message_to_cloud_loop, \
    relay_cloud_loop_message_to_email, get_latest_gmail_message_text, message_text_is_new, read_gmail_message_from_file, \
    save_gmail_message_to_file


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

    def test_get_latest_gmail_message_text(self,
                                                  mock_gmail_api_set_up_google_client_id,
                                                  mock_gmail_api_set_up_set_up_google_client_secret,
                                                  mock_gmail_api_set_up_set_up_refresh_token,
                                                  mock_gmail_api_set_up_set_up_google_topic,
                                                  mock_gmail_api_set_up_set_up_email_recipient,
                                                  mock_gmail_api_set_up_set_up_email_sender,
                                                  mock_gmail_api_set_up_set_up_message_size,
                                                  mock_gmail_api_gmail_get_messages_from_push,
                                                  mock_gmail_api_get_new_gmail_messages,
                                                  mock_gmail_api_gmail_get_message_by_id):
        mock_gmail_api_gmail_get_message_by_id.return_value = "test_message_from", \
                                                              "test_message_subject", \
                                                              "test_message_text"
        message_text = get_latest_gmail_message_text()
        assert mock_gmail_api_gmail_get_messages_from_push.called
        assert mock_gmail_api_get_new_gmail_messages.called
        assert mock_gmail_api_gmail_get_message_by_id.called
        assert message_text == "test_message_text"

    def test_message_text_is_new_true(self, mock_read_gmail_message_from_file, mock_save_gmail_message_to_file):
        test_message_text = "test message body"
        mock_read_gmail_message_from_file.return_value = "old message body"
        message_new = message_text_is_new(test_message_text)
        assert message_new

    def test_message_text_is_new_true_empty(self, mock_read_gmail_message_from_file, mock_save_gmail_message_to_file):
        test_message_text = "test message body"
        mock_read_gmail_message_from_file.return_value = None
        message_new = message_text_is_new(test_message_text)
        assert message_new

    def test_message_text_is_new_false_no_diff(self,
                                               mock_read_gmail_message_from_file, mock_save_gmail_message_to_file):
        test_message_text = "test message body"
        mock_read_gmail_message_from_file.return_value = test_message_text
        message_new = message_text_is_new(test_message_text)
        assert not message_new

    def test_read_gmail_message_from_file(self, tmp_path):
        test_gmail_message_dict = {"last_gmail_message": "test gmail body"}
        test_message_file_name = "test_message_file.json"
        test_message_file_path = tmp_path / test_message_file_name
        with open(test_message_file_path, "w") as test_message_file_object:
            json.dump(test_gmail_message_dict, test_message_file_object)
        return_json = read_gmail_message_from_file(test_message_file_path)
        assert return_json == test_gmail_message_dict["last_gmail_message"]

    def test_save_gmail_message_to_file(self, tmp_path):
        test_message_text = "message body text"
        test_message_file_name = "test_message_file.json"
        test_message_file_path = tmp_path / test_message_file_name
        save_gmail_message_to_file(test_message_file_path, test_message_text)
        with open(test_message_file_path, 'r') as test_message_file_object:
            saved_json_message_text = json.load(test_message_file_object)["last_gmail_message"]
        assert saved_json_message_text == test_message_text
