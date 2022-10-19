import pytest
from serial import SerialException

from tests.data import two_part_email, bob_skipped_email


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

    def test_email_page_valid_email_no_relay(self, client,
                                             mock_get_relay_switch,
                                             mock_send_satellite_message):
        mock_get_relay_switch.return_value = False
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
        assert b'Relay Disabled' in response.data

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
                                        mock_get_latest_gmail_message_parts,
                                        mock_message_text_is_new,
                                        mock_relay_email_message_to_cloud_loop):
        mock_get_google_sub.return_value = "test_sub"
        mock_get_latest_gmail_message_parts.return_value = ("test_sender", "#fbc84a (2/2)", "Testing")
        mock_message_text_is_new.return_value = True
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Success'

    def test_relay_valid_sub_email_ping_no_relay(self, client,
                                                 mock_get_google_sub,
                                                 mock_get_latest_gmail_message_parts,
                                                 mock_message_text_is_new,
                                                 mock_get_relay_switch,
                                                 mock_relay_email_message_to_cloud_loop):
        mock_get_google_sub.return_value = "test_sub"
        mock_get_latest_gmail_message_parts.return_value = ("test_sender", "#fbc84a (2/2)", "Testing")
        mock_message_text_is_new.return_value = True
        mock_get_relay_switch.return_value = False
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Bounced This One'

    def test_bounce_duplicate_sub_email_ping(self, client,
                                             mock_get_google_sub,
                                             mock_get_latest_gmail_message_parts,
                                             mock_message_text_is_new,
                                             mock_relay_email_message_to_cloud_loop):
        mock_get_google_sub.return_value = "test_sub"
        mock_get_latest_gmail_message_parts.return_value = ("test_sender", "#fbc84a (2/2)", "Testing")
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
                                            mock_cloud_loop_message_assemble_hex_message_id,
                                            mock_cloud_loop_api_get_cloud_loop_payload_url,
                                            mock_cloud_loop_api_requests_get):
        test_hardware_id = "2003"
        mock_cloud_loop_message_assemble_hex_message_id.return_value = "#fbc84a"
        test_payload_string = "satsuki@mocker.com,#fbc84a (2/2),Testing"
        test_auth_token = "3"
        test_payload_url = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware=" + test_hardware_id + \
                           "&payload=" + test_payload_string.encode().hex() + \
                           "&token=" + test_auth_token
        mock_cloud_loop_api_get_cloud_loop_auth_token.return_value = test_auth_token
        mock_cloud_loop_api_get_rock_block_id.return_value = test_hardware_id
        mock_cloud_loop_message_get_max_message_size.return_value = 250
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
                                                         mock_cloud_loop_message_assemble_hex_message_id,
                                                         mock_cloud_loop_api_requests_get):
        test_hardware_id = "2003"
        mock_cloud_loop_message_assemble_hex_message_id.return_value = "#fbc84a"
        test_payload_string = "satsuki@mocker.com,#fbc84a (2/2),Testing"
        test_auth_token = "3"
        test_payload_url = "https://api.cloudloop.com/DataMt/DoSendMessage?hardware=" + test_hardware_id + \
                           "&payload=" + test_payload_string.encode().hex() + \
                           "&token=" + test_auth_token
        mock_cloud_loop_api_get_cloud_loop_auth_token.return_value = test_auth_token
        mock_cloud_loop_api_get_rock_block_id.return_value = test_hardware_id
        mock_cloud_loop_message_get_max_message_size.return_value = 250

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
                                                 mock_cloud_loop_message_assemble_hex_message_id,
                                                 mock_cloud_loop_api_requests_get):
        test_hardware_id = "2003"
        mock_cloud_loop_message_assemble_hex_message_id.return_value = "#fbc84a"
        # test_payload_string_one = "satsuki@mocker.com,Info (1/3),Really, So there is no character limit for " \
        #                           "the email address? Really...Hawaii "
        # test_payload_string_two = "satsuki@mocker.com,Info (2/3),to Samoa? Test Person Test Place, Test State, " \
        #                           "12345 test_sender@gmail.com H/O: "
        # 000-000-0000 Cell: 000-000-0000 -----Origin
        test_payload_string_three = "satsuki@mocker.com,#fbc84a (4/4),al"
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
        mock_cloud_loop_message_get_max_message_size.return_value = 100

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
        assert mock_cloud_loop_api_requests_get.call_count == 4

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
                                                  mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                  mock_cloud_loop_api_get_rock_block_id,
                                                  mock_rock_block_api_get_satellite_transfer):
        mock_get_sister.return_value = 'Mei'

        with pytest.raises(SerialException, match=r"could not open port /dev/serial0"):
            client.post('/', data={"email": "satsuki@mocker.com",
                                   "info_level": "Info",
                                   "message_body": "Testing",
                                   "submit-email": "Send Email"})
        assert mock_cloud_loop_api_get_cloud_loop_auth_token.called
        assert mock_cloud_loop_api_get_rock_block_id.called
        assert not mock_rock_block_api_get_satellite_transfer.called

    def test_email_page_valid_email_mei(self, client,
                                        mock_get_sister,
                                        mock_rock_block_api_serial,
                                        mock_rock_block_api_adafruit_rockblock,
                                        mock_rock_block_api_set_data_out,
                                        mock_cloud_loop_message_get_max_message_size,
                                        mock_cloud_loop_message_get_whitelist,
                                        mock_rock_block_api_get_satellite_transfer):
        mock_cloud_loop_message_get_max_message_size.return_value = 250
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
                                            mock_gmail_api_get_message_size,
                                            mock_gmail_api_send_gmail_message):
        mock_get_imei.return_value = "2000"
        test_hex_data = "satsuki@mocker.com,#fbc84a (1/2),Info".encode().hex()
        mock_gmail_api_get_message_size.return_value = "100"
        response = client.post('/', json={"imei": "2000", "data": test_hex_data})
        assert mock_gmail_api_send_gmail_message.called

        assert response.status_code == 200
        assert response.data == b'Success'

    def test_relay_valid_sub_email_ping_two_parts(self, client,
                                                  mock_get_google_sub,
                                                  mock_gmail_api_get_creds,
                                                  mock_gmail_api_get_message_size,
                                                  mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                  mock_cloud_loop_api_get_rock_block_id,
                                                  mock_cloud_loop_api_requests_get,
                                                  mock_gmail_get_top_inbox_message,
                                                  mock_gmail_api_google_api_get_message,
                                                  mock_write_gmail_message_to_file,
                                                  mock_google_api_get_whitelist):
        mock_get_google_sub.return_value = "test_sub"
        mock_gmail_api_get_message_size.return_value = 250
        mock_cloud_loop_api_get_cloud_loop_auth_token.return_value = "3"
        mock_cloud_loop_api_get_rock_block_id.return_value = "2003"
        mock_gmail_get_top_inbox_message.return_value = two_part_email.email
        mock_gmail_api_google_api_get_message.return_value = two_part_email.email
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Success'

    def test_bounce_duplicate_sub_email_ping_two_parts(self, client,
                                                       mock_get_google_sub,
                                                       mock_gmail_api_get_message_size,
                                                       mock_cloud_loop_api_requests_get,
                                                       mock_gmail_get_top_inbox_message,
                                                       mock_gmail_api_get_creds,
                                                       mock_gmail_api_google_api_get_message,
                                                       mock_write_gmail_message_to_file,
                                                       mock_google_api_get_whitelist,
                                                       mock_read_gmail_message_from_file):
        duplicate_message_sender = "test_sender@gmail.com"
        duplicate_message_text = "Yep, I've observed some pretty large emails going back and " \
                                 "forth. I do\r\ndouble-check emails in cloudloop so if " \
                                 "something gets lost I'll forward it,\r\nbut so far the new " \
                                 "integration has not failed to deliver anything\r\n"
        mock_get_google_sub.return_value = "test_sub"
        mock_gmail_api_get_message_size.return_value = 100
        mock_gmail_get_top_inbox_message.return_value = two_part_email.email
        mock_gmail_api_google_api_get_message.return_value = two_part_email.email
        mock_read_gmail_message_from_file.return_value = duplicate_message_text
        mock_google_api_get_whitelist.return_value = {"0": duplicate_message_sender}
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Bounced This One'

    def test_relay_valid_sub_email_ping_no_parts(self, client,
                                                 mock_get_google_sub,
                                                 mock_gmail_api_get_message_size,
                                                 mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                 mock_cloud_loop_api_get_rock_block_id,
                                                 mock_cloud_loop_api_requests_get,
                                                 mock_gmail_get_top_inbox_message,
                                                 mock_gmail_api_get_gmail_message_by_id,
                                                 mock_write_gmail_message_to_file,
                                                 mock_google_api_get_whitelist):
        mock_get_google_sub.return_value = "test_sub"
        mock_gmail_api_get_message_size.return_value = 250
        mock_cloud_loop_api_get_cloud_loop_auth_token.return_value = "3"
        mock_cloud_loop_api_get_rock_block_id.return_value = "2003"
        mock_gmail_get_top_inbox_message.return_value = bob_skipped_email.email
        mock_gmail_api_get_gmail_message_by_id.return_value = ("test_sender@gmail.com", "full_emails", "new_email_text")
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Success'

    def test_bounce_duplicate_sub_email_ping_no_parts(self, client,
                                                      mock_get_google_sub,
                                                      mock_gmail_api_get_message_size,
                                                      mock_cloud_loop_api_requests_get,
                                                      mock_gmail_get_top_inbox_message,
                                                      mock_gmail_api_get_creds,
                                                      mock_gmail_api_google_api_get_message,
                                                      mock_write_gmail_message_to_file,
                                                      mock_google_api_get_whitelist,
                                                      mock_read_gmail_message_from_file):
        mock_get_google_sub.return_value = "test_sub"
        mock_gmail_api_get_message_size.return_value = 100
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_gmail_get_top_inbox_message.return_value = bob_skipped_email.email
        mock_gmail_api_google_api_get_message.return_value = bob_skipped_email.email
        mock_read_gmail_message_from_file.return_value = 'Really,\r\n\r\nSo there is no character limit for the sv ' \
                                                         'kiki 95 address?\r\n\r\nReally...Hawaii to ' \
                                                         'Samoa?\r\n\r\nTest Person\r\nTest Place, Test State ' \
                                                         '12345\r\ntest_sender@gmail.com\r\nH/O: ' \
                                                         '000-000-0000\r\nCell: 000-000-0000\r\n\r\n-----Original ' \
                                                         'Message-----\r\nFrom: test_recipient@gmai.com [' \
                                                         'mailto:test_recipient@gmai.com] \r\nSent: Friday, June 10, ' \
                                                         '2022 7:54 PM\r\nTo: test_sender@gmail.com\r\nSubject: Info ' \
                                                         '(1/1)\r\n\r\nCorrection on that last: from Hawaii to the ' \
                                                         'Samoan islands\r\n\r\n\r\n-- \r\nThis email has been ' \
                                                         'checked for viruses by AVG.\r\nhttps://www.avg.com\r\n\r\n'
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Bounced This One'

    # TODO: testing
    # def test_relay_valid_sub_email_ping(self, client, capfd,
    #                                     mock_read_gmail_message_from_file,
    #                                     mock_get_google_sub,
    #                                     mock_gmail_api_get_message_size,
    #                                     mock_cloud_loop_api_get_cloud_loop_auth_token,
    #                                     mock_cloud_loop_api_get_rock_block_id,
    #                                     mock_cloud_loop_api_requests_get,
    #                                     mock_gmail_get_top_inbox_message,
    #                                     mock_gmail_api_get_gmail_message_by_id,
    #                                     mock_write_gmail_message_to_file,
    #                                     mock_google_api_get_whitelist):
    #     mock_read_gmail_message_from_file.return_value = {"last_gmail_message": "Info"}
    #     mock_get_google_sub.return_value = "test_sub"
    #     mock_gmail_api_get_message_size.return_value = 250
    #     mock_cloud_loop_api_get_cloud_loop_auth_token.return_value = "3"
    #     mock_cloud_loop_api_get_rock_block_id.return_value = "2003"
    #     mock_gmail_api_get_gmail_message_by_id.return_value = [("test_sender@gmail.com",
    #                                                             "#fbc84a (1/2)", "Info"),
    #                                                            ("test_sender@gmail.com",
    #                                                             "#fbc84a (2/2)", "Testing text")]
    #     mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
    #     response = client.post('/', json={"subscription": "test_sub",
    #                                       "message":
    #                                           {"data": "test_data"}
    #                                       })
    #     captured = capfd.readouterr()
    #     assert captured.out == ""
    #     assert response.status_code == 200
    #     assert response.data == b'Success'
