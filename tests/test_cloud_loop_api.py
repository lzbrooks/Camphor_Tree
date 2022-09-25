import re

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
                                                 mock_cloud_loop_api_requests_get):
        mock_cloud_loop_message_get_max_message_size.return_value = 250
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_cloud_loop_api_requests_get.return_value = "200 Success"
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Info",
                                                message_to_encode="testing hex encode")
        test_cloud_loop.send_cloud_loop_message()
        captured = capfd.readouterr()
        assert 'Message Encoding...\n' \
               'Number of Message Chunks: 2\n' \
               'Message Encoded\n' \
               'Sending CloudLoop Message\n' \
               'Sending part 1 of 2\n' \
               '200 Success\n' in captured.out
        assert 'Sent part 1 of 2\n' \
               'Sending CloudLoop Message\n' \
               'Sending part 2 of 2\n' \
               '200 Success\n' in captured.out
        assert 'Sent part 2 of 2\n' in captured.out
        assert test_cloud_loop.message_to_encode == 'testing hex encode'
        assert test_cloud_loop.message_chunk_list == ['Info', 'testing hex encode']
        assert re.findall(r"0,#[\da-fA-F]{6} \(1/2\),",
                          test_cloud_loop._assemble_payload_tagline(0))
        assert re.findall(r"0,#[\da-fA-F]{6} \(2/2\),",
                          test_cloud_loop._assemble_payload_tagline(1))
        assert mock_cloud_loop_api_requests_get.called

    def test_send_cloud_loop_message_multi_part(self, capfd,
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
        test_cloud_loop.send_cloud_loop_message()
        captured = capfd.readouterr()
        assert 'Message Encoding...\n' \
               'Number of Message Chunks: 3\n' \
               'Message Encoded\n' \
               'Sending CloudLoop Message\n' \
               'Sending part 1 of 3\n' \
               '200 Success\n' in captured.out
        assert 'Sent part 1 of 3\n' \
               'Sending CloudLoop Message\n' \
               'Sending part 2 of 3\n' \
               '200 Success\n' in captured.out
        assert 'Sent part 2 of 3\n' \
               'Sending CloudLoop Message\n' \
               'Sending part 3 of 3\n' \
               '200 Success\n' in captured.out
        assert 'Sent part 3 of 3\n' in captured.out
        assert test_cloud_loop.message_to_encode == 'testing hex encode extra extra extra extra long'
        assert test_cloud_loop.message_chunk_list == ['Info', 'testing hex encode extra ', 'extra extra extra long']
        assert re.findall(r"0,#[\da-fA-F]{6} \(1/3\),",
                          test_cloud_loop._assemble_payload_tagline(0))
        assert re.findall(r"0,#[\da-fA-F]{6} \(2/3\),",
                          test_cloud_loop._assemble_payload_tagline(1))
        assert re.findall(r"0,#[\da-fA-F]{6} \(3/3\),",
                          test_cloud_loop._assemble_payload_tagline(2))
        assert mock_cloud_loop_api_requests_get.called

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

    # TODO: testing
    def test_chunk_message(self, capfd,
                           mock_cloud_loop_api_get_cloud_loop_auth_token,
                           mock_cloud_loop_api_get_rock_block_id,
                           mock_cloud_loop_message_get_max_message_size,
                           mock_cloud_loop_message_get_whitelist,
                           mock_cloud_loop_api_requests_get):
        mock_cloud_loop_message_get_max_message_size.return_value = 25
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_cloud_loop_api_requests_get.return_value = "200 Success"
        test_cloud_loop = HexEncodeForCloudLoop(message_from="test_sender@gmail.com",
                                                message_subject="Test really really really long tagline",
                                                message_to_encode="testing hex encode short")
        test_cloud_loop._chunk_message()
        captured = capfd.readouterr()
        assert captured.out == 'Number of Message Chunks: 2\n'
        assert test_cloud_loop.hex_message_id
        assert test_cloud_loop.max_chunk_size == 25
        # TODO: add back in
        # assert test_cloud_loop.message_from == "0"
        assert test_cloud_loop.message_subject == 'Test really really really long tagline'
        assert test_cloud_loop.message_to_encode == 'testing hex encode short'
        assert test_cloud_loop.message_chunk_list == ['Test really really really',
                                                      'testing hex encode short']
        assert not mock_cloud_loop_api_requests_get.called
