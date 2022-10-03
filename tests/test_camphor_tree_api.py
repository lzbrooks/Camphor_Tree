import json

from apis.camphor_tree_api import send_satellite_message, relay_email_message_to_cloud_loop, \
    relay_cloud_loop_message_to_email, get_latest_gmail_message_parts, message_text_is_new, \
    save_gmail_message_to_file, read_message_from_file


class TestCamphorTreeApi:
    def test_send_satellite_message_satsuki(self, mock_cloud_loop_api_get_cloud_loop_auth_token,
                                            mock_cloud_loop_api_get_rock_block_id,
                                            mock_cloud_loop_message_send_cloud_loop_message):
        test_server_option = "Satsuki"
        send_status = send_satellite_message("test_email", "test_info_level", "test_message_body", test_server_option)
        assert mock_cloud_loop_api_get_cloud_loop_auth_token.called
        assert mock_cloud_loop_api_get_rock_block_id.called
        assert mock_cloud_loop_message_send_cloud_loop_message.called
        assert send_status == 'Send Success'

    def test_send_satellite_message_mei(self, mock_cloud_loop_api_get_cloud_loop_auth_token,
                                        mock_rock_block_api_serial,
                                        mock_rock_block_api_adafruit_rockblock,
                                        mock_cloud_loop_api_get_rock_block_id,
                                        mock_cloud_loop_message_get_payload,
                                        mock_rock_block_api_send_data_out):
        test_server_option = "Mei"
        send_status = send_satellite_message("test_email", "test_info_level", "test_message_body", test_server_option)
        assert mock_cloud_loop_message_get_payload.called
        assert mock_rock_block_api_send_data_out.called
        assert send_status == 'Send Success'

    def test_send_satellite_message_invalid_server_option(self, mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                          mock_cloud_loop_api_get_rock_block_id,
                                                          mock_cloud_loop_message_get_payload,
                                                          mock_rock_block_api_send_data_out):
        test_server_option = "Shichikoyama"
        send_status = send_satellite_message("test_email", "test_info_level", "test_message_body", test_server_option)
        assert not mock_cloud_loop_message_get_payload.called
        assert not mock_rock_block_api_send_data_out.called
        assert send_status == 'Incorrect Server Mode'

    def test_relay_email_message_to_cloud_loop_no_message(self, capfd,
                                                          mock_gmail_api_google_api_get_top_inbox_message,
                                                          mock_gmail_api_google_api_get_message,
                                                          mock_gmail_api_get_creds,
                                                          mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                          mock_cloud_loop_api_get_rock_block_id,
                                                          mock_cloud_loop_api_requests_get):
        relay_email_message_to_cloud_loop(None, None, None)
        captured = capfd.readouterr()
        assert captured.out == 'No CloudLoop Message to Send\nPOST CloudLoop Message Handled\n'
        assert mock_cloud_loop_api_get_cloud_loop_auth_token.called
        assert mock_cloud_loop_api_get_rock_block_id.called
        assert not mock_cloud_loop_api_requests_get.called

    def test_relay_email_message_to_cloud_loop_one_message(self, mock_gmail_api_get_message_size,
                                                           mock_gmail_get_top_inbox_message,
                                                           mock_gmail_api_get_gmail_message_by_id,
                                                           mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                           mock_cloud_loop_api_get_rock_block_id,
                                                           mock_cloud_loop_message_send_cloud_loop_message):
        mock_gmail_get_top_inbox_message.return_value = "test_message"
        relay_email_message_to_cloud_loop("test_sender", "#fbc84a (2/2)", "Testing")
        assert mock_gmail_api_get_message_size.called
        assert mock_cloud_loop_api_get_cloud_loop_auth_token.called
        assert mock_cloud_loop_api_get_rock_block_id.called
        assert mock_cloud_loop_message_send_cloud_loop_message.called

    def test_relay_cloud_loop_message_to_email(self, capfd, mock_gmail_api_get_email,
                                               mock_gmail_api_send_gmail_message,
                                               mock_cloud_loop_message_send_cloud_loop_message):
        mock_gmail_api_get_email.return_value = "test_sender@gmail.com"
        test_hex_json = "test_sender@gmail.com,#fbc84a (2/2),test request json data".encode().hex()
        relay_cloud_loop_message_to_email(test_hex_json)
        captured = capfd.readouterr()
        assert mock_gmail_api_send_gmail_message.called
        assert captured.out == ('POST CloudLoop Ping Received\n'
                                'Hex Message Processing...\n'
                                'Changing Hex to Bytes\n'
                                "['test_sender@gmail.com']\n"
                                '#fbc84a (2/2)\n'
                                'test request json data\n'
                                'Hex Message Processed\n'
                                'POST GMail Message Handled\n')

    def test_get_latest_gmail_message_text(self, mock_gmail_api_get_message_size,
                                           mock_gmail_get_top_inbox_message,
                                           mock_gmail_api_get_gmail_message_by_id):
        mock_gmail_api_get_gmail_message_by_id.return_value = "test_message_from", \
                                                              "test_message_subject", \
                                                              "test_message_text"
        message_from, message_subject, message_text = get_latest_gmail_message_parts()
        assert mock_gmail_api_get_message_size.called
        assert mock_gmail_get_top_inbox_message.called
        assert mock_gmail_api_get_gmail_message_by_id.called
        assert message_from == 'test_message_from'
        assert message_subject == 'test_message_subject'
        assert message_text == 'test_message_text'

    def test_message_text_is_new_true(self, mock_read_message_from_file, mock_save_gmail_message_to_file):
        test_message_text = "test message body"
        mock_read_message_from_file.return_value = {"last_gmail_message": "old message body"}
        message_new = message_text_is_new(test_message_text)
        assert message_new

    def test_message_text_is_new_true_empty(self, mock_read_message_from_file, mock_save_gmail_message_to_file):
        test_message_text = "test message body"
        mock_read_message_from_file.return_value = None
        mock_read_message_from_file.return_value = {"last_gmail_message": "not_duplicate"}
        message_new = message_text_is_new(test_message_text)
        assert message_new

    def test_message_text_is_new_false_no_diff(self,
                                               mock_read_message_from_file, mock_save_gmail_message_to_file):
        test_message_text = "test message body"
        mock_read_message_from_file.return_value = {"last_gmail_message": test_message_text}
        message_new = message_text_is_new(test_message_text)
        assert not message_new

    def test_read_gmail_message_from_file(self, tmp_path):
        test_gmail_message_dict = {"last_gmail_message": "test gmail body"}
        test_message_file_name = "test_message_file.json"
        test_message_file_path = tmp_path / test_message_file_name
        with open(test_message_file_path, "w") as test_message_file_object:
            json.dump(test_gmail_message_dict, test_message_file_object)
        return_json = read_message_from_file(test_message_file_path)
        assert return_json == {'last_gmail_message': test_gmail_message_dict["last_gmail_message"]}

    def test_save_gmail_message_to_file(self, tmp_path):
        test_message_text = "message body text"
        test_message_file_name = "test_message_file.json"
        test_message_file_path = tmp_path / test_message_file_name
        save_gmail_message_to_file(test_message_file_path, test_message_text)
        with open(test_message_file_path, 'r') as test_message_file_object:
            saved_json_message_text = json.load(test_message_file_object)["last_gmail_message"]
        assert saved_json_message_text == test_message_text
