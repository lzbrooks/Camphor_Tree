import re

import pytest

from apis.cloud_loop_api import HexEncodeForCloudLoop, DecodeCloudLoopMessage


class TestHexEncodeForCloudLoop:
    def test_init_valid_message(self,
                                mock_cloud_loop_api_get_cloud_loop_auth_token,
                                mock_cloud_loop_api_get_rock_block_id):
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Info (1/1",
                                                message_to_encode="testing hex encode")
        assert test_cloud_loop.message_from == ["test_sender@gmail.com"]
        assert test_cloud_loop.message_to_encode == "testing hex encode"
        assert test_cloud_loop.message_subject == "Info (1/1"

    def test_init_non_list_message_from(self,
                                        mock_cloud_loop_api_get_cloud_loop_auth_token,
                                        mock_cloud_loop_api_get_rock_block_id):
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com")
        assert test_cloud_loop.message_from == ["test_sender@gmail.com"]
        assert not test_cloud_loop.message_to_encode
        assert not test_cloud_loop.message_subject

    def test_init_list_message_from(self,
                                    mock_cloud_loop_api_get_cloud_loop_auth_token,
                                    mock_cloud_loop_api_get_rock_block_id):
        test_cloud_loop = HexEncodeForCloudLoop(message_from=["test_sender@gmail.com"])
        assert test_cloud_loop.message_from == ["test_sender@gmail.com"]
        assert not test_cloud_loop.message_to_encode
        assert not test_cloud_loop.message_subject

    def test_init_no_message(self,
                             mock_cloud_loop_api_get_cloud_loop_auth_token,
                             mock_cloud_loop_api_get_rock_block_id):
        test_cloud_loop = HexEncodeForCloudLoop()
        assert not test_cloud_loop.message_from
        assert not test_cloud_loop.message_to_encode
        assert not test_cloud_loop.message_subject

    def test_send_cloud_loop_message_no_message(self, capfd,
                                                mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                mock_cloud_loop_api_get_rock_block_id,
                                                mock_cloud_loop_api_requests_get):
        test_cloud_loop = HexEncodeForCloudLoop()
        test_cloud_loop.send_cloud_loop_message()
        captured = capfd.readouterr()
        assert captured.out == "No CloudLoop Message to Send\n"
        assert not test_cloud_loop.message_to_encode
        assert not mock_cloud_loop_api_requests_get.called

    def test_send_cloud_loop_message_single_part(self, capfd,
                                                 mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                 mock_cloud_loop_api_get_rock_block_id,
                                                 mock_cloud_loop_message_get_max_message_size,
                                                 mock_cloud_loop_message_get_whitelist,
                                                 mock_cloud_loop_message_assemble_hex_message_id_local,
                                                 mock_cloud_loop_api_requests_get):
        mock_cloud_loop_message_get_max_message_size.return_value = 250
        mock_cloud_loop_message_assemble_hex_message_id_local.return_value = "#fbc84a"
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_cloud_loop_api_requests_get.return_value = "200 Success"
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Info",
                                                message_to_encode="testing hex encode")
        test_cloud_loop.send_cloud_loop_message()
        captured = capfd.readouterr()
        assert captured.out == ('Message Encoding...\n'
                                'Number of Message Chunks: 2\n'
                                'Message Encoded\n'
                                'Sending CloudLoop Message\n'
                                'Sending part 1 of 2\n'
                                '200 Success\n'
                                '0,#fbc84a (1/2),Info\n'
                                'Sent part 1 of 2\n'
                                'Sending CloudLoop Message\n'
                                'Sending part 2 of 2\n'
                                '200 Success\n'
                                '0,#fbc84a (2/2),testing hex encode\n'
                                'Sent part 2 of 2\n')
        assert test_cloud_loop.message_to_encode == 'testing hex encode'
        assert test_cloud_loop.message_chunk_list == ['Info', 'testing hex encode']
        assert test_cloud_loop._assemble_payload_tagline(0) == "0,#fbc84a (1/2),"
        assert test_cloud_loop._assemble_payload_tagline(1) == "0,#fbc84a (2/2),"
        assert mock_cloud_loop_api_requests_get.called

    def test_send_cloud_loop_message_multi_part(self, capfd,
                                                mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                mock_cloud_loop_api_get_rock_block_id,
                                                mock_cloud_loop_message_get_max_message_size,
                                                mock_cloud_loop_message_get_whitelist,
                                                mock_cloud_loop_message_assemble_hex_message_id_local,
                                                mock_cloud_loop_api_requests_get):
        mock_cloud_loop_message_get_max_message_size.return_value = 25
        mock_cloud_loop_message_assemble_hex_message_id_local.return_value = "#fbc84a"
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_cloud_loop_api_requests_get.return_value = "200 Success"
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Info",
                                                message_to_encode="testing hex encode extra extra extra extra long")
        test_cloud_loop.send_cloud_loop_message()
        captured = capfd.readouterr()
        assert captured.out == ('Message Encoding...\n'
                                'Number of Message Chunks: 3\n'
                                'Message Encoded\n'
                                'Sending CloudLoop Message\n'
                                'Sending part 1 of 3\n'
                                '200 Success\n'
                                '0,#fbc84a (1/3),Info\n'
                                'Sent part 1 of 3\n'
                                'Sending CloudLoop Message\n'
                                'Sending part 2 of 3\n'
                                '200 Success\n'
                                '0,#fbc84a (2/3),testing hex encode extra \n'
                                'Sent part 2 of 3\n'
                                'Sending CloudLoop Message\n'
                                'Sending part 3 of 3\n'
                                '200 Success\n'
                                '0,#fbc84a (3/3),extra extra extra long\n'
                                'Sent part 3 of 3\n')
        assert test_cloud_loop.message_to_encode == 'testing hex encode extra extra extra extra long'
        assert test_cloud_loop.message_chunk_list == ['Info', 'testing hex encode extra ', 'extra extra extra long']
        assert test_cloud_loop._assemble_payload_tagline(0) == "0,#fbc84a (1/3),"
        assert test_cloud_loop._assemble_payload_tagline(1) == "0,#fbc84a (2/3),"
        assert test_cloud_loop._assemble_payload_tagline(2) == "0,#fbc84a (3/3),"
        assert mock_cloud_loop_api_requests_get.called

    def test_get_payload_no_message(self, mock_cloud_loop_api_requests_get):
        test_cloud_loop = HexEncodeForCloudLoop()
        with pytest.raises(TypeError, match=r"'NoneType' object is not iterable"):
            test_cloud_loop.get_payload()

    def test_get_payload_valid_message_with_newlines(self, capfd,
                                                     mock_cloud_loop_message_get_max_message_size,
                                                     mock_cloud_loop_message_get_whitelist,
                                                     mock_cloud_loop_message_assemble_hex_message_id_local,
                                                     mock_cloud_loop_api_requests_get):
        mock_cloud_loop_message_get_max_message_size.return_value = 25
        mock_cloud_loop_message_assemble_hex_message_id_local.return_value = "#fbc84a"
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Info",
                                                message_to_encode="Testing message text\r\n")
        payload_list = test_cloud_loop.get_payload()
        captured = capfd.readouterr()
        assert captured.out == 'Message Encoding...\nNumber of Message Chunks: 2\nMessage Encoded\n'
        assert test_cloud_loop.message_from == ["0"]
        assert test_cloud_loop.message_chunk_list == ['Info', 'Testing message text\r\n']
        assert payload_list == ['0,#fbc84a (1/2),Info', '0,#fbc84a (2/2),Testing message text']

    def test_send_payload_part_valid_message(self, capfd,
                                             mock_cloud_loop_api_get_cloud_loop_auth_token,
                                             mock_cloud_loop_api_get_rock_block_id,
                                             mock_cloud_loop_message_get_max_message_size,
                                             mock_cloud_loop_message_get_whitelist,
                                             mock_cloud_loop_message_assemble_hex_message_id_local,
                                             mock_cloud_loop_api_requests_get):
        mock_cloud_loop_message_get_max_message_size.return_value = 25
        mock_cloud_loop_api_get_rock_block_id.return_value = "2003"
        mock_cloud_loop_api_get_cloud_loop_auth_token.return_value = "3"
        mock_cloud_loop_message_assemble_hex_message_id_local.return_value = "#fbc84a"
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_cloud_loop_api_requests_get.return_value = "200 Success"
        test_payload = '0,#fbc84a (1/2),Info'
        test_payload_list = [test_payload]
        test_payload_part_number = 0
        test_cloud_loop = HexEncodeForCloudLoop()
        test_cloud_loop._send_payload_part(test_payload,
                                           test_payload_list,
                                           test_payload_part_number)
        captured = capfd.readouterr()
        mock_cloud_loop_api_requests_get.assert_called_with(
            "https://api.cloudloop.com/DataMt/DoSendMessage?hardware=2003&payload"
            "=302c236662633834612028312f32292c496e666f&token=3",
            headers={'Accept': 'application/json'})
        assert captured.out == ('Sending CloudLoop Message\n'
                                'Sending part 1 of 1\n'
                                '200 Success\n'
                                '0,#fbc84a (1/2),Info\n'
                                'Sent part 1 of 1\n')

    def test_chunk_message_multi_part_message(self, capfd,
                                              mock_cloud_loop_api_get_cloud_loop_auth_token,
                                              mock_cloud_loop_api_get_rock_block_id,
                                              mock_cloud_loop_message_get_max_message_size,
                                              mock_cloud_loop_message_get_whitelist,
                                              mock_cloud_loop_api_requests_get):
        mock_cloud_loop_message_get_max_message_size.return_value = 25
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_cloud_loop_api_requests_get.return_value = "200 Success"
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Info",
                                                message_to_encode="testing hex encode extra extra extra extra long")
        test_cloud_loop._chunk_message()
        captured = capfd.readouterr()
        assert captured.out == 'Number of Message Chunks: 3\n'
        assert test_cloud_loop.hex_message_id
        assert test_cloud_loop.max_chunk_size == 25
        assert test_cloud_loop.message_from == ["test_sender@gmail.com"]
        assert test_cloud_loop.message_subject == "Info"
        assert test_cloud_loop.message_to_encode == 'testing hex encode extra extra extra extra long'
        assert test_cloud_loop.message_chunk_list == ['Info',
                                                      'testing hex encode extra ',
                                                      'extra extra extra long']
        assert not mock_cloud_loop_api_requests_get.called

    def test_chunk_message_single_part_message(self, capfd,
                                               mock_cloud_loop_api_get_cloud_loop_auth_token,
                                               mock_cloud_loop_api_get_rock_block_id,
                                               mock_cloud_loop_message_get_max_message_size,
                                               mock_cloud_loop_message_get_whitelist,
                                               mock_cloud_loop_api_requests_get):
        mock_cloud_loop_message_get_max_message_size.return_value = 25
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_cloud_loop_api_requests_get.return_value = "200 Success"
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Info",
                                                message_to_encode="testing hex encode short")
        test_cloud_loop._chunk_message()
        captured = capfd.readouterr()
        assert captured.out == 'Number of Message Chunks: 2\n'
        assert test_cloud_loop.hex_message_id
        assert test_cloud_loop.max_chunk_size == 25
        assert test_cloud_loop.message_from == ["test_sender@gmail.com"]
        assert test_cloud_loop.message_subject == "Info"
        assert test_cloud_loop.message_to_encode == 'testing hex encode short'
        assert test_cloud_loop.message_chunk_list == ['Info',
                                                      'testing hex encode short']
        assert not mock_cloud_loop_api_requests_get.called

    def test__assemble_payload_part_valid_message(self,
                                                  mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                  mock_cloud_loop_api_get_rock_block_id,
                                                  mock_cloud_loop_message_get_max_message_size,
                                                  mock_cloud_loop_message_get_whitelist,
                                                  mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_assemble_hex_message_id_local.return_value = "#fbc84a"
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Info",
                                                message_to_encode="Testing payload")
        payload_part = test_cloud_loop._assemble_payload_part("Testing payload", 1)
        assert payload_part == "test_sender@gmail.com,#fbc84a (2/0),Testing payload"

    def test__assemble_payload_part_with_newlines(self,
                                                  mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                  mock_cloud_loop_api_get_rock_block_id,
                                                  mock_cloud_loop_message_get_max_message_size,
                                                  mock_cloud_loop_message_get_whitelist,
                                                  mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_assemble_hex_message_id_local.return_value = "#fbc84a"
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._assemble_payload_part("Testing payload\r\n", 1)
        assert payload_part == "test_sender@gmail.com,#fbc84a (2/0),Testing payload"

    def test__assemble_payload_part_no_message(self,
                                               mock_cloud_loop_api_get_cloud_loop_auth_token,
                                               mock_cloud_loop_api_get_rock_block_id,
                                               mock_cloud_loop_message_get_max_message_size,
                                               mock_cloud_loop_message_get_whitelist):
        test_cloud_loop = HexEncodeForCloudLoop()
        with pytest.raises(TypeError, match=r"'NoneType' object is not iterable"):
            test_cloud_loop._assemble_payload_part(None, None)

    def test__assemble_payload_tagline_single_sender(self,
                                                     mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                     mock_cloud_loop_api_get_rock_block_id,
                                                     mock_cloud_loop_message_get_max_message_size,
                                                     mock_cloud_loop_message_get_whitelist,
                                                     mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_assemble_hex_message_id_local.return_value = "#fbc84a"
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._assemble_payload_tagline(1)
        assert payload_part == "test_sender@gmail.com,#fbc84a (2/0),"

    def test__assemble_payload_tagline_multiple_senders(self,
                                                        mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                        mock_cloud_loop_api_get_rock_block_id,
                                                        mock_cloud_loop_message_get_max_message_size,
                                                        mock_cloud_loop_message_get_whitelist,
                                                        mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_assemble_hex_message_id_local.return_value = "#fbc84a"
        test_cloud_loop = HexEncodeForCloudLoop(message_from=["test_sender_1@gmail.com",
                                                              "test_sender_2@gmail.com"],
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._assemble_payload_tagline(1)
        assert payload_part == "test_sender_1@gmail.com,test_sender_2@gmail.com,#fbc84a (2/0),"

    def test__assemble_payload_tagline_int_contacts(self,
                                                    mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                    mock_cloud_loop_api_get_rock_block_id,
                                                    mock_cloud_loop_message_get_max_message_size,
                                                    mock_cloud_loop_message_get_whitelist,
                                                    mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_assemble_hex_message_id_local.return_value = "#fbc84a"
        test_cloud_loop = HexEncodeForCloudLoop(message_from=["0",
                                                              "13"],
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._assemble_payload_tagline(1)
        assert payload_part == "0,13,#fbc84a (2/0),"

    def test__email_to_contact_number_no_emails(self,
                                                mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                mock_cloud_loop_api_get_rock_block_id,
                                                mock_cloud_loop_message_get_max_message_size,
                                                mock_cloud_loop_message_get_whitelist,
                                                mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_cloud_loop = HexEncodeForCloudLoop(message_from=["0",
                                                              "13"],
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._email_to_contact_number([])
        assert not payload_part

    def test__email_to_contact_number_whitelisted_email(self,
                                                        mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                        mock_cloud_loop_api_get_rock_block_id,
                                                        mock_cloud_loop_message_get_max_message_size,
                                                        mock_cloud_loop_message_get_whitelist,
                                                        mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_cloud_loop = HexEncodeForCloudLoop(message_from=["0",
                                                              "13"],
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._email_to_contact_number(["test_sender@gmail.com"])
        assert payload_part == ['0']

    def test__email_to_contact_number_not_whitelisted(self,
                                                      mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                      mock_cloud_loop_api_get_rock_block_id,
                                                      mock_cloud_loop_message_get_max_message_size,
                                                      mock_cloud_loop_message_get_whitelist,
                                                      mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_cloud_loop = HexEncodeForCloudLoop(message_from=["0",
                                                              "13"],
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._email_to_contact_number(["test_sender_nope@gmail.com"])
        assert payload_part == ['test_sender_nope@gmail.com']

    def test__email_to_contact_number_multiple_whitelisted(self,
                                                           mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                           mock_cloud_loop_api_get_rock_block_id,
                                                           mock_cloud_loop_message_get_max_message_size,
                                                           mock_cloud_loop_message_get_whitelist,
                                                           mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_cloud_loop = HexEncodeForCloudLoop(message_from=["0",
                                                              "13"],
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._email_to_contact_number(["test_sender_1@gmail.com",
                                                                 "test_sender_2@gmail.com"])
        assert payload_part == ['0', '1']

    def test__email_to_contact_number_multiple_not_whitelisted(self,
                                                               mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                               mock_cloud_loop_api_get_rock_block_id,
                                                               mock_cloud_loop_message_get_max_message_size,
                                                               mock_cloud_loop_message_get_whitelist,
                                                               mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_cloud_loop = HexEncodeForCloudLoop(message_from=["0",
                                                              "13"],
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._email_to_contact_number(["test_sender_3@gmail.com",
                                                                 "test_sender_4@gmail.com"])
        assert payload_part == ['test_sender_3@gmail.com', 'test_sender_4@gmail.com']

    def test__email_to_contact_number_whitelisted_and_not(self,
                                                          mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                          mock_cloud_loop_api_get_rock_block_id,
                                                          mock_cloud_loop_message_get_max_message_size,
                                                          mock_cloud_loop_message_get_whitelist,
                                                          mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_cloud_loop = HexEncodeForCloudLoop(message_from=["0",
                                                              "13"],
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._email_to_contact_number(["test_sender_1@gmail.com",
                                                                 "test_sender_4@gmail.com"])
        assert payload_part == ['0', 'test_sender_4@gmail.com']

    def test__get_contact_number_for_email_whitelisted(self,
                                                       mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                       mock_cloud_loop_api_get_rock_block_id,
                                                       mock_cloud_loop_message_get_max_message_size,
                                                       mock_cloud_loop_message_get_whitelist,
                                                       mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_cloud_loop = HexEncodeForCloudLoop(message_from=["0",
                                                              "13"],
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._get_contact_number_for_email("test_sender_1@gmail.com")
        assert payload_part == '0'

    def test__get_contact_number_for_email_not_whitelisted(self,
                                                           mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                           mock_cloud_loop_api_get_rock_block_id,
                                                           mock_cloud_loop_message_get_max_message_size,
                                                           mock_cloud_loop_message_get_whitelist,
                                                           mock_cloud_loop_message_assemble_hex_message_id_local):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_cloud_loop = HexEncodeForCloudLoop(message_from=["0",
                                                              "13"],
                                                message_subject="Info",
                                                message_to_encode="Testing payload\r\n")
        payload_part = test_cloud_loop._get_contact_number_for_email("test_sender_3@gmail.com")
        assert not payload_part

    def test__get_cloud_loop_payload_url_valid_params(self,
                                                      mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                      mock_cloud_loop_api_get_rock_block_id,
                                                      mock_cloud_loop_message_get_max_message_size,
                                                      mock_cloud_loop_message_get_whitelist):
        test_hardware_id = "2003"
        test_auth_token = "3"
        mock_cloud_loop_api_get_rock_block_id.return_value = test_hardware_id
        mock_cloud_loop_api_get_cloud_loop_auth_token.return_value = test_auth_token
        test_payload = '0,#fbc84a (1/2),Info'
        test_encoded_payload = test_payload.encode().hex()
        test_url = f"https://api.cloudloop.com/DataMt/DoSendMessage?hardware={test_hardware_id}" \
                   f"&payload={test_encoded_payload}&token={test_auth_token}"
        test_cloud_loop = HexEncodeForCloudLoop()
        returned_url = test_cloud_loop._get_cloud_loop_payload_url(test_payload)
        assert returned_url == test_url

    def test__assemble_hex_message_id(self):
        returned_hex_id = HexEncodeForCloudLoop()._assemble_hex_message_id()
        assert re.findall(r"#[a-fA-F\d]{6}", returned_hex_id)


class TestDecodeCloudLoopMessage:
    def test_decode_hex_message(self, capfd):
        test_hex_string = "test_sender@gmail.com,#fbc84a (2/2),Testing payload".encode().hex()
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop.decode_hex_message()
        captured = capfd.readouterr()
        assert captured.out == ('Hex Message Processing...\n'
                                'Changing Hex to Bytes\n'
                                "['test_sender@gmail.com']\n"
                                '#fbc84a (2/2)\n'
                                'Testing payload\n'
                                'Hex Message Processed\n')
        assert test_cloud_loop.decoded_message == "test_sender@gmail.com,#fbc84a (2/2),Testing payload"
        assert test_cloud_loop.recipient_list == ["test_sender@gmail.com"]
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"
        assert test_cloud_loop.message_text == "Testing payload"

    def test_decode_hex_message_no_message(self):
        test_cloud_loop = DecodeCloudLoopMessage()
        with pytest.raises(TypeError, match=r"fromhex\(\) argument must be str, not None"):
            test_cloud_loop.decode_hex_message()
        assert not test_cloud_loop.recipient_list
        assert not test_cloud_loop.message_subject
        assert not test_cloud_loop.message_text

    def test__decode_message_from_hex_string(self, capfd):
        test_hex_string = "test_sender@gmail.com,#fbc84a (2/2),Testing payload".encode().hex()
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._decode_message_from_hex()
        captured = capfd.readouterr()
        assert captured.out == "Changing Hex to Bytes\n"
        assert test_cloud_loop.decoded_message == "test_sender@gmail.com,#fbc84a (2/2),Testing payload"

    def test__decode_message_from_hex_bytes(self, capfd):
        test_hex_string = bytes.fromhex("test_sender@gmail.com,#fbc84a (2/2),Testing payload".encode().hex())
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._decode_message_from_hex()
        captured = capfd.readouterr()
        assert not captured.out
        assert test_cloud_loop.decoded_message == "test_sender@gmail.com,#fbc84a (2/2),Testing payload"

    def test__decode_message_from_hex_no_message(self):
        test_cloud_loop = DecodeCloudLoopMessage()
        with pytest.raises(TypeError, match=r"fromhex\(\) argument must be str, not None"):
            test_cloud_loop._decode_message_from_hex()
        assert not test_cloud_loop.decoded_message

    def test__extract_all_message_parts_not_whitelisted(self, capfd):
        test_hex_string = "test_sender@gmail.com,#fbc84a (2/2),Testing payload".encode().hex()
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._decode_message_from_hex()
        test_cloud_loop._extract_all_message_parts()
        captured = capfd.readouterr()
        assert captured.out == ('Changing Hex to Bytes\n'
                                "['test_sender@gmail.com']\n"
                                '#fbc84a (2/2)\n'
                                'Testing payload\n')
        assert test_cloud_loop.decoded_message == "test_sender@gmail.com,#fbc84a (2/2),Testing payload"
        assert test_cloud_loop.recipient_list == ["test_sender@gmail.com"]
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"
        assert test_cloud_loop.message_text == "Testing payload"

    def test__extract_all_message_parts_whitelisted(self, capfd, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_hex_string = "0,#fbc84a (2/2),Testing payload".encode().hex()
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._decode_message_from_hex()
        test_cloud_loop._extract_all_message_parts()
        captured = capfd.readouterr()
        assert captured.out == ('Changing Hex to Bytes\n'
                                "['test_sender_1@gmail.com']\n"
                                '#fbc84a (2/2)\n'
                                'Testing payload\n')
        assert test_cloud_loop.decoded_message == '0,#fbc84a (2/2),Testing payload'
        assert test_cloud_loop.recipient_list == ["test_sender_1@gmail.com"]
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"
        assert test_cloud_loop.message_text == "Testing payload"

    def test__extract_all_message_parts_no_subject(self, capfd, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_hex_string = "0,No Subject,Testing payload".encode().hex()
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._decode_message_from_hex()
        test_cloud_loop._extract_all_message_parts()
        captured = capfd.readouterr()
        assert captured.out == ('Changing Hex to Bytes\n'
                                "['test_sender_1@gmail.com']\n"
                                '\n'
                                '0No SubjectTesting payload\n')
        assert test_cloud_loop.decoded_message == '0,No Subject,Testing payload'
        assert test_cloud_loop.recipient_list == ["test_sender_1@gmail.com"]
        assert not test_cloud_loop.message_subject
        assert test_cloud_loop.message_text == '0No SubjectTesting payload'

    def test__extract_all_message_parts_no_message(self, capfd, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_cloud_loop = DecodeCloudLoopMessage()
        with pytest.raises(AttributeError, match=r"'NoneType' object has no attribute 'split'"):
            test_cloud_loop._extract_all_message_parts()
        captured = capfd.readouterr()
        assert not captured.out
        assert not test_cloud_loop.decoded_message
        assert test_cloud_loop.recipient_list == []
        assert not test_cloud_loop.message_subject
        assert not test_cloud_loop.message_text

    def test__extract_message_subject_not_whitelisted(self):
        test_string = "test_sender@gmail.com,#fbc84a (2/2),Testing payload"
        test_hex_string = test_string.encode().hex()
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._decode_message_from_hex()
        test_cloud_loop._extract_message_subject(test_string.split(","))
        assert test_cloud_loop.decoded_message == test_string
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"

    def test__extract_message_subject_whitelisted(self):
        test_string = "0,#fbc84a (2/2),Testing payload"
        test_hex_string = test_string.encode().hex()
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._decode_message_from_hex()
        test_cloud_loop._extract_message_subject(test_string.split(","))
        assert test_cloud_loop.decoded_message == test_string
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"

    def test__extract_message_subject_no_subject(self):
        test_string = "0,No Subject,Testing payload"
        test_hex_string = test_string.encode().hex()
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._decode_message_from_hex()
        with pytest.raises(TypeError, match=r"'NoneType' object is not iterable"):
            test_cloud_loop._extract_message_subject(None)
        assert test_cloud_loop.decoded_message == test_string
        assert not test_cloud_loop.message_subject

    def test__extract_message_subject_no_message(self):
        test_string = "0,#fbc84a (2/2),Testing payload"
        test_hex_string = test_string.encode().hex()
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._decode_message_from_hex()
        with pytest.raises(TypeError, match=r"'NoneType' object is not iterable"):
            test_cloud_loop._extract_message_subject(None)
        assert test_cloud_loop.decoded_message == test_string
        assert not test_cloud_loop.message_subject

    def test__split_on_subject_not_whitelisted(self):
        test_string = "test_sender@gmail.com,#fbc84a (2/2),Testing payload"
        test_hex_string = test_string.encode().hex()
        test_split_string = test_string.split(",")
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._extract_message_subject(test_split_string)
        test_cloud_loop._split_on_subject(test_split_string)
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"
        assert test_cloud_loop.recipient_list == ["test_sender@gmail.com"]
        assert test_cloud_loop._message_text_list == ["Testing payload"]

    def test__split_on_subject_whitelisted(self):
        test_string = "0,#fbc84a (2/2),Testing payload"
        test_hex_string = test_string.encode().hex()
        test_split_string = test_string.split(",")
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._extract_message_subject(test_split_string)
        test_cloud_loop._split_on_subject(test_split_string)
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"
        assert test_cloud_loop.recipient_list == ["0"]
        assert test_cloud_loop._message_text_list == ["Testing payload"]

    def test__split_on_subject_multiple_recipients(self):
        test_string = "0,test_sender@gmail.com,#fbc84a (2/2),Testing payload"
        test_hex_string = test_string.encode().hex()
        test_split_string = test_string.split(",")
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._extract_message_subject(test_split_string)
        test_cloud_loop._split_on_subject(test_split_string)
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"
        assert test_cloud_loop.recipient_list == ["0", "test_sender@gmail.com"]
        assert test_cloud_loop._message_text_list == ["Testing payload"]

    def test__split_on_subject_multiple_text_parts(self):
        test_string = "0,#fbc84a (2/2),Testing payload, second part of sentence"
        test_hex_string = test_string.encode().hex()
        test_split_string = test_string.split(",")
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._extract_message_subject(test_split_string)
        test_cloud_loop._split_on_subject(test_split_string)
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"
        assert test_cloud_loop.recipient_list == ["0"]
        assert test_cloud_loop._message_text_list == ["Testing payload", " second part of sentence"]

    def test__split_on_subject_no_subject(self):
        test_string = "0,No Subject,Testing payload"
        test_hex_string = test_string.encode().hex()
        test_split_string = test_string.split(",")
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._extract_message_subject(test_split_string)
        test_cloud_loop._split_on_subject(test_split_string)
        assert not test_cloud_loop.message_subject
        assert test_cloud_loop.recipient_list == test_split_string
        assert test_cloud_loop._message_text_list == test_split_string

    def test__split_on_subject_no_message(self):
        test_string = "0,#fbc84a (2/2),Testing payload"
        test_hex_string = test_string.encode().hex()
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._split_on_subject(None)
        assert not test_cloud_loop.message_subject
        assert not test_cloud_loop.recipient_list
        assert not test_cloud_loop._message_text_list

    def test__assemble_message_recipient_list_not_whitelisted(self, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_string = "test_sender@gmail.com,#fbc84a (2/2),Testing payload"
        test_hex_string = test_string.encode().hex()
        test_split_string = test_string.split(",")
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._extract_message_subject(test_split_string)
        test_cloud_loop._split_on_subject(test_split_string)
        test_cloud_loop._assemble_message_recipient_list()
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"
        assert test_cloud_loop.recipient_list == ["test_sender@gmail.com"]
        assert test_cloud_loop._message_text_list == ["Testing payload"]

    def test__assemble_message_recipient_list_whitelisted(self, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_string = "0,#fbc84a (2/2),Testing payload"
        test_hex_string = test_string.encode().hex()
        test_split_string = test_string.split(",")
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._extract_message_subject(test_split_string)
        test_cloud_loop._split_on_subject(test_split_string)
        test_cloud_loop._assemble_message_recipient_list()
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"
        assert test_cloud_loop.recipient_list == ["test_sender_1@gmail.com"]
        assert test_cloud_loop._message_text_list == ["Testing payload"]

    def test__assemble_message_recipient_list_multiple_recipients(self, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_string = "0,test_sender@gmail.com,#fbc84a (2/2),Testing payload"
        test_hex_string = test_string.encode().hex()
        test_split_string = test_string.split(",")
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._extract_message_subject(test_split_string)
        test_cloud_loop._split_on_subject(test_split_string)
        test_cloud_loop._assemble_message_recipient_list()
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"
        assert test_cloud_loop.recipient_list == ["test_sender_1@gmail.com", "test_sender@gmail.com"]
        assert test_cloud_loop._message_text_list == ["Testing payload"]

    def test__assemble_message_recipient_list_multiple_text_parts(self, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_string = "0,#fbc84a (2/2),Testing payload, second part of sentence"
        test_hex_string = test_string.encode().hex()
        test_split_string = test_string.split(",")
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._extract_message_subject(test_split_string)
        test_cloud_loop._split_on_subject(test_split_string)
        test_cloud_loop._assemble_message_recipient_list()
        assert test_cloud_loop.message_subject == "#fbc84a (2/2)"
        assert test_cloud_loop.recipient_list == ["test_sender_1@gmail.com"]
        assert test_cloud_loop._message_text_list == ["Testing payload", " second part of sentence"]

    def test__assemble_message_recipient_list_no_subject(self, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_string = "0,No Subject,Testing payload"
        test_hex_string = test_string.encode().hex()
        test_split_string = test_string.split(",")
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._extract_message_subject(test_split_string)
        test_cloud_loop._split_on_subject(test_split_string)
        test_cloud_loop._assemble_message_recipient_list()
        assert not test_cloud_loop.message_subject
        assert test_cloud_loop.recipient_list == ["test_sender_1@gmail.com"]
        assert test_cloud_loop._message_text_list == test_split_string

    def test__assemble_message_recipient_list_no_message(self, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_string = "0,#fbc84a (2/2),Testing payload"
        test_hex_string = test_string.encode().hex()
        test_cloud_loop = DecodeCloudLoopMessage(test_hex_string)
        test_cloud_loop._assemble_message_recipient_list()
        assert not test_cloud_loop.message_subject
        assert not test_cloud_loop.recipient_list
        assert not test_cloud_loop._message_text_list

    def test__get_recipient_list_whitelisted(self):
        test_string = "0,No Subject,Testing payload"
        test_split_string = test_string.split(",")
        returned_recipient_list = DecodeCloudLoopMessage()._get_recipient_list(test_split_string)
        assert returned_recipient_list == ["0"]

    def test__get_recipient_list_not_whitelisted(self):
        test_string = "test_sender@gmail.com,No Subject,Testing payload"
        test_split_string = test_string.split(",")
        returned_recipient_list = DecodeCloudLoopMessage()._get_recipient_list(test_split_string)
        assert returned_recipient_list == ["test_sender@gmail.com"]

    def test__get_recipient_list_not_whitelisted_multiple(self):
        test_string = "test_sender_1@gmail.com,test_sender_2@gmail.com,No Subject,Testing payload"
        test_split_string = test_string.split(",")
        returned_recipient_list = DecodeCloudLoopMessage()._get_recipient_list(test_split_string)
        assert returned_recipient_list == ["test_sender_1@gmail.com", "test_sender_2@gmail.com"]

    def test__get_recipient_list_no_recipients(self):
        test_string = ""
        test_split_string = test_string.split(",")
        returned_recipient_list = DecodeCloudLoopMessage()._get_recipient_list(test_split_string)
        assert returned_recipient_list == []

    def test__contact_number_to_email_whitelisted(self, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_emails = ["0"]
        test_cloud_loop = DecodeCloudLoopMessage()
        returned_email_list = test_cloud_loop._contact_number_to_email(test_emails)
        assert returned_email_list == ["test_sender_1@gmail.com"]

    def test__contact_number_to_email_not_whitelisted(self, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_emails = ["test_sender@gmail.com"]
        test_cloud_loop = DecodeCloudLoopMessage()
        returned_email_list = test_cloud_loop._contact_number_to_email(test_emails)
        assert returned_email_list == ["test_sender@gmail.com"]

    def test__contact_number_to_email_whitelisted_multiple(self, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_emails = ["1", "0"]
        test_cloud_loop = DecodeCloudLoopMessage()
        returned_email_list = test_cloud_loop._contact_number_to_email(test_emails)
        assert returned_email_list == ["test_sender_2@gmail.com", "test_sender_1@gmail.com"]

    def test__contact_number_to_email_no_emails(self, mock_cloud_loop_message_get_whitelist):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_emails = []
        test_cloud_loop = DecodeCloudLoopMessage()
        returned_email_list = test_cloud_loop._contact_number_to_email(test_emails)
        assert returned_email_list == []
