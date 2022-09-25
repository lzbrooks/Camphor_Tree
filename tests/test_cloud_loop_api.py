import pytest

from apis.cloud_loop_api import HexEncodeForCloudLoop


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

    # TODO: testing
    def test_get_payload(self, capfd,
                         mock_cloud_loop_message_get_max_message_size,
                         mock_cloud_loop_message_get_whitelist,
                         mock_cloud_loop_api_requests_get):
        mock_cloud_loop_message_get_max_message_size.return_value = 25
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Info",
                                                message_to_encode="Testing message text")
        test_cloud_loop.get_payload()
        captured = capfd.readouterr()
        assert captured == ""


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
        # TODO: add back in
        # assert test_cloud_loop.message_from == "0"
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
        # TODO: add back in
        # assert test_cloud_loop.message_from == "0"
        assert test_cloud_loop.message_subject == "Info"
        assert test_cloud_loop.message_to_encode == 'testing hex encode short'
        assert test_cloud_loop.message_chunk_list == ['Info',
                                                      'testing hex encode short']
        assert not mock_cloud_loop_api_requests_get.called
