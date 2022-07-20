import pytest
from serial import SerialException


class TestAppConsoleFlow:
    def test_login_page_default_load(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'submit-password' in response.data
        assert b'Satsuki Console' in response.data

    def test_login_page_default_login(self, client):
        response = client.post('/', data={"password": "satsuki",
                                          "submit-password": "Login"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data
        assert b'Console' in response.data

    def test_login_page_invalid_login(self, client):
        response = client.post('/', data={"password": "nope",
                                          "submit-password": "Login"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'submit-password' in response.data
        assert b'Satsuki Console' in response.data

    def test_email_page_valid_email(self, client, mock_send_satellite_message):
        mock_send_satellite_message.return_value = "Send Success"
        response = client.post('/', data={"email": "satsuki@mocker.com",
                                          "info_level": "Info",
                                          "message_body": "Testing",
                                          "submit-email": "Send Email"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data
        assert b'Send Success' in response.data

    def test_email_page_short_invalid_email(self, client):
        response = client.post('/', data={"email": "nope",
                                          "info_level": "Info",
                                          "message_body": "Testing",
                                          "submit-email": "Send Email"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data

        assert b'Field must be between 6 and 35 characters long.' in response.data
        assert b'Invalid email address.' in response.data

        assert b'Send Failure' in response.data

    def test_email_page_long_invalid_email(self, client):
        response = client.post('/', data={"email": "invalid",
                                          "info_level": "Info",
                                          "message_body": "Testing",
                                          "submit-email": "Send Email"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data

        assert b'Field must be between 6 and 35 characters long.' not in response.data
        assert b'Invalid email address.' in response.data

        assert b'Send Failure' in response.data

    def test_relay_valid_cloud_loop_message(self, client, mock_get_imei, mock_relay_cloud_loop_message_to_email):
        mock_get_imei.return_value = "2000"
        assert mock_get_imei() == "2000"
        response = client.post('/', json={"imei": "2000", "data": "test data"})
        assert response.status_code == 200
        assert response.data == b'Success'

    def test_relay_invalid_cloud_loop_message(self, client, mock_get_imei, mock_relay_cloud_loop_message_to_email):
        mock_get_imei.return_value = "2000"
        assert mock_get_imei() == "2000"
        response = client.post('/', json={"imei": "3000", "data": "test data"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'submit-password' in response.data
        assert b'Satsuki Console' in response.data

    def test_relay_valid_sub_email_ping(self, client,
                                        mock_get_google_sub,
                                        mock_get_latest_gmail_message_text,
                                        mock_message_text_is_new,
                                        mock_relay_email_message_to_cloud_loop):
        mock_get_google_sub.return_value = "test_sub"
        mock_message_text_is_new.return_value = True
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Success'

    def test_bounce_duplicate_sub_email_ping(self, client,
                                             mock_get_google_sub,
                                             mock_get_latest_gmail_message_text,
                                             mock_message_text_is_new,
                                             mock_relay_email_message_to_cloud_loop):
        mock_get_google_sub.return_value = "test_sub"
        mock_message_text_is_new.return_value = False
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Bounced This One'


class TestAppConsoleFlowIntegration:
    def test_email_page_valid_email_satsuki(self, client, mock_cloud_loop_api_get_cloud_loop_auth_token,
                                            mock_cloud_loop_api_get_rock_block_id,
                                            mock_cloud_loop_message_get_max_message_size,
                                            mock_cloud_loop_message_get_whitelist,
                                            mock_cloud_loop_api_get_cloud_loop_payload_url,
                                            mock_cloud_loop_api_requests_get):
        test_hardware_id = "2003"
        test_payload_string = "satsuki@mocker.com,Info (1/1),Testing"
        test_auth_token = "3"
        test_payload_url = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware=" + test_hardware_id + \
                           "&payload=" + test_payload_string.encode().hex() + \
                           "&token=" + test_auth_token
        mock_cloud_loop_api_get_cloud_loop_auth_token.return_value = test_auth_token
        mock_cloud_loop_api_get_rock_block_id.return_value = test_hardware_id
        mock_cloud_loop_message_get_max_message_size.return_value = "250"
        mock_cloud_loop_api_get_cloud_loop_payload_url.return_value = test_payload_url

        response = client.post('/', data={"email": "satsuki@mocker.com",
                                          "info_level": "Info",
                                          "message_body": "Testing",
                                          "submit-email": "Send Email"})
        assert mock_cloud_loop_message_get_max_message_size.called
        assert mock_cloud_loop_message_get_whitelist.called
        mock_cloud_loop_api_get_cloud_loop_payload_url.assert_called_with(test_payload_string)
        mock_cloud_loop_api_requests_get.assert_called_with(test_payload_url, headers={'Accept': 'application/json'})

        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data
        assert b'Send Success' in response.data

    def test_email_page_valid_email_satsuki_with_returns(self, client, mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                         mock_cloud_loop_api_get_rock_block_id,
                                                         mock_cloud_loop_message_get_max_message_size,
                                                         mock_cloud_loop_message_get_whitelist,
                                                         mock_cloud_loop_api_requests_get):
        test_hardware_id = "2003"
        test_payload_string = "satsuki@mocker.com,Info (1/1),Testing"
        test_auth_token = "3"
        test_payload_url = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware=" + test_hardware_id + \
                           "&payload=" + test_payload_string.encode().hex() + \
                           "&token=" + test_auth_token
        mock_cloud_loop_api_get_cloud_loop_auth_token.return_value = test_auth_token
        mock_cloud_loop_api_get_rock_block_id.return_value = test_hardware_id
        mock_cloud_loop_message_get_max_message_size.return_value = "250"

        response = client.post('/', data={"email": "satsuki@mocker.com",
                                          "info_level": "Info",
                                          "message_body": "\r\nTesting\r\n",
                                          "submit-email": "Send Email"})
        assert mock_cloud_loop_message_get_max_message_size.called
        assert mock_cloud_loop_message_get_whitelist.called
        mock_cloud_loop_api_requests_get.assert_called_with(test_payload_url, headers={'Accept': 'application/json'})

        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data
        assert b'Send Success' in response.data

    def test_email_page_valid_long_email_satsuki(self, client, mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                 mock_cloud_loop_api_get_rock_block_id,
                                                 mock_cloud_loop_message_get_max_message_size,
                                                 mock_cloud_loop_message_get_whitelist,
                                                 mock_cloud_loop_api_requests_get):
        test_hardware_id = "2003"
        # test_payload_string_one = "satsuki@mocker.com,Info (1/3),Really, So there is no character limit for " \
        #                           "the email address? Really...Hawaii "
        # test_payload_string_two = "satsuki@mocker.com,Info (2/3),to Samoa? Test Person Test Place, Test State, " \
        #                           "12345 test_sender@gmail.com H/O: "
        test_payload_string_three = "satsuki@mocker.com,Info (3/3), 000-000-0000 Cell: 000-000-0000 -----Original"
        test_auth_token = "3"
        # test_payload_url_one = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware=" + test_hardware_id + \
        #                        "&payload=" + test_payload_string_one.encode().hex() + \
        #                        "&token=" + test_auth_token
        # test_payload_url_two = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware=" + test_hardware_id + \
        #                        "&payload=" + test_payload_string_two.encode().hex() + \
        #                        "&token=" + test_auth_token
        test_payload_url_three = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware=" + test_hardware_id + \
                                 "&payload=" + test_payload_string_three.encode().hex() + \
                                 "&token=" + test_auth_token
        mock_cloud_loop_api_get_cloud_loop_auth_token.return_value = test_auth_token
        mock_cloud_loop_api_get_rock_block_id.return_value = test_hardware_id
        mock_cloud_loop_message_get_max_message_size.return_value = "100"

        response = client.post('/', data={"email": "satsuki@mocker.com",
                                          "info_level": "Info",
                                          "message_body": "Really, So there is no character limit for the email "
                                                          "address? Really...Hawaii to Samoa? Test Person Test Place, "
                                                          "Test State, 12345 test_sender@gmail.com H/O: 000-000-0000 "
                                                          "Cell: 000-000-0000 -----Original",
                                          "submit-email": "Send Email"})
        assert mock_cloud_loop_message_get_max_message_size.called
        assert mock_cloud_loop_message_get_whitelist.called
        # print("First")
        # print(test_payload_url_one)
        # mock_cloud_loop_api_requests_get.assert_any_call(test_payload_url_one,
        #                                                  headers={'Accept': 'application/json'})
        # print("Second")
        # print(test_payload_url_two)
        # mock_cloud_loop_api_requests_get.assert_any_call(test_payload_url_two,
        #                                                  headers={'Accept': 'application/json'})
        # print("Third")
        # print(test_payload_url_three)
        # mock_cloud_loop_api_requests_get.assert_any_call(test_payload_url_three,
        #                                                  headers={'Accept': 'application/json'})
        mock_cloud_loop_api_requests_get.assert_called_with(test_payload_url_three,
                                                            headers={'Accept': 'application/json'})
        assert mock_cloud_loop_api_requests_get.call_count == 3

        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data
        assert b'Send Success' in response.data

    def test_email_page_valid_email_mei_no_serial(self, client,
                                                  mock_get_sister,
                                                  mock_cloud_loop_message_get_max_message_size,
                                                  mock_cloud_loop_message_get_whitelist,
                                                  mock_rock_block_api_get_satellite_transfer):
        mock_cloud_loop_message_get_max_message_size.return_value = "250"
        mock_get_sister.return_value = 'Mei'

        with pytest.raises(SerialException, match=r"could not open port /dev/serial0"):
            client.post('/', data={"email": "satsuki@mocker.com",
                                   "info_level": "Info",
                                   "message_body": "Testing",
                                   "submit-email": "Send Email"})
        assert mock_cloud_loop_message_get_max_message_size.called
        assert mock_cloud_loop_message_get_whitelist.called

    def test_email_page_valid_email_mei(self, client,
                                        mock_get_sister,
                                        mock_rock_block_api_set_up_uart,
                                        mock_rock_block_api_set_data_out,
                                        mock_cloud_loop_message_get_max_message_size,
                                        mock_cloud_loop_message_get_whitelist,
                                        mock_rock_block_api_get_satellite_transfer):
        mock_cloud_loop_message_get_max_message_size.return_value = "250"
        mock_get_sister.return_value = 'Mei'
        mock_rock_block_api_get_satellite_transfer.return_value = (0,)

        response = client.post('/', data={"email": "satsuki@mocker.com",
                                          "info_level": "Info",
                                          "message_body": "Testing",
                                          "submit-email": "Send Email"})
        assert mock_cloud_loop_message_get_max_message_size.called
        assert mock_cloud_loop_message_get_whitelist.called

        assert response.status_code == 200
        assert b'Mei - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data
        assert b'Send Success' in response.data

    # def test_email_page_valid_email_mei_satellite_retry(self, client,
    #                                                     mock_get_sister,
    #                                                     mock_rock_block_api_set_up_uart,
    #                                                     mock_rock_block_api_set_data_out,
    #                                                     mock_cloud_loop_message_get_max_message_size,
    #                                                     mock_cloud_loop_message_get_whitelist,
    #                                                     mock_rock_block_api_get_satellite_transfer,
    #                                                     mock_rock_block_api_time_sleep):
    #     mock_cloud_loop_message_get_max_message_size.return_value = "250"
    #     mock_get_sister.return_value = 'Mei'
    #     mock_rock_block_api_get_satellite_transfer.return_value = (10,)
    #
    #     response = client.post('/', data={"email": "satsuki@mocker.com",
    #                                       "info_level": "Info",
    #                                       "message_body": "Testing",
    #                                       "submit-email": "Send Email"})
    #     assert mock_cloud_loop_message_get_max_message_size.called
    #     assert mock_cloud_loop_message_get_whitelist.called
    #     assert mock_rock_block_api_time_sleep.called
    #
    #     assert response.status_code == 200
    #     assert b'Mei - Camphor Tree' in response.data
    #     assert b'Email Address' in response.data
    #     assert b'Info Level' in response.data
    #     assert b'Emergency' in response.data
    #     assert b'Urgent' in response.data
    #     assert b'value="Info"' in response.data
    #     assert b'Message Body' in response.data
    #     assert b'Send Email' in response.data
    #     assert b'Send Success' in response.data

    def test_relay_valid_cloud_loop_message(self, client, mock_get_imei,
                                            mock_gmail_api_set_up_set_up_message_size,
                                            mock_google_api_requests_post):
        mock_get_imei.return_value = "2000"
        test_hex_data = "satsuki@mocker.com,Info (1/1),Testing".encode().hex()
        mock_gmail_api_set_up_set_up_message_size.return_value = "100"
        response = client.post('/', json={"imei": "2000", "data": test_hex_data})
        assert mock_google_api_requests_post.called

        assert response.status_code == 200
        assert response.data == b'Success'

    # TODO: test integration
    def test_relay_valid_sub_email_ping(self, client,
                                        mock_get_google_sub,
                                        mock_gmail_api_set_up_set_up_message_size,
                                        mock_google_api_requests_get,
                                        mock_cloud_loop_api_requests_get,
                                        mock_gmail_api_get_new_gmail_message,
                                        mock_write_gmail_message_to_file,
                                        mock_relay_email_message_to_cloud_loop):
        mock_get_google_sub.return_value = "test_sub"
        # TODO: fill out with dummy data
        mock_gmail_api_get_new_gmail_message.return_value = {"id": "413"}
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Success'

    #                                             mock_gmail_api_set_up_set_up_message_size,
    #                                             mock_google_api_requests_get,
    #                                             mock_cloud_loop_api_requests_get):
    #         mock_get_imei.return_value = "2000"
    #         test_hex_data = "test data".encode().hex()
    #         mock_gmail_api_set_up_set_up_message_size.return_value = "4"
    #         mock_google_api_requests_get.return_value = {"message": test_hex_data}
    #         response = client.post('/', json={"imei": "2000", "data": test_hex_data})
    #         assert mock_google_api_requests_get.called
    #         assert mock_cloud_loop_api_requests_get.called
    #
    #         assert response.status_code == 200
    #         assert response.data == b'Success'

    # TODO: test integration
    def test_bounce_duplicate_sub_email_ping(self, client,
                                             mock_get_google_sub,
                                             mock_get_latest_gmail_message_text,
                                             mock_message_text_is_new,
                                             mock_relay_email_message_to_cloud_loop):
        mock_get_google_sub.return_value = "test_sub"
        mock_message_text_is_new.return_value = False
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Bounced This One'
