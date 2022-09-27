import re

from apis.rock_block_api import RockBlockAPI


class TestRockBlockAPI:
    def test_init(self,
                  mock_rock_block_api_serial,
                  mock_rock_block_api_adafruit_rockblock):
        test_rock_block = RockBlockAPI()
        assert test_rock_block.rock_block
        assert mock_rock_block_api_serial.called
        assert mock_rock_block_api_adafruit_rockblock.called

    def test_send_data_out_success(self, capfd,
                                   mock_rock_block_api_serial,
                                   mock_rock_block_api_adafruit_rockblock,
                                   mock_rock_block_api_time_sleep,
                                   mock_rock_block_api_get_satellite_transfer):
        payload_list = ['0,#fbc84a (1/2),Info', '0,#fbc84a (2/2),Testing message text']
        mock_rock_block_api_get_satellite_transfer.side_effect = [(0, 3, 1, 0, 100, 0),
                                                                  (0, 3, 1, 0, 100, 0)]
        test_rock_block = RockBlockAPI()
        test_rock_block.send_data_out(payload_list)
        captured = capfd.readouterr()
        assert mock_rock_block_api_get_satellite_transfer.call_count == 2
        assert test_rock_block.rock_block.data_out == b'0,#fbc84a (2/2),Testing message text'
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                'Talking to satellite...\n'
                                '(0, 3, 1, 0, 100, 0)\n'
                                '\n'
                                'DONE.\n'
                                'Talking to satellite...\n'
                                '(0, 3, 1, 0, 100, 0)\n'
                                '\n'
                                'DONE.\n')

    def test_send_data_out_single_failure(self, capfd,
                                          mock_rock_block_api_serial,
                                          mock_rock_block_api_adafruit_rockblock,
                                          mock_rock_block_api_time_sleep,
                                          mock_rock_block_api_get_satellite_transfer):
        payload_list = ['0,#fbc84a (1/2),Info', '0,#fbc84a (2/2),Testing message text']
        mock_rock_block_api_get_satellite_transfer.side_effect = [(10, 3, 1, 0, 100, 0),
                                                                  (0, 3, 1, 0, 100, 0),
                                                                  (0, 3, 1, 0, 100, 0)]
        test_rock_block = RockBlockAPI()
        test_rock_block.send_data_out(payload_list)
        captured = capfd.readouterr()
        assert mock_rock_block_api_get_satellite_transfer.call_count == 3
        assert test_rock_block.rock_block.data_out == b'0,#fbc84a (2/2),Testing message text'
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                'Talking to satellite...\n'
                                '(10, 3, 1, 0, 100, 0)\n'
                                '(0, 3, 1, 0, 100, 0)\n'
                                '\n'
                                'DONE.\n'
                                'Talking to satellite...\n'
                                '(0, 3, 1, 0, 100, 0)\n'
                                '\n'
                                'DONE.\n')

    def test_check_mailbox_success(self, capfd, tmp_path,
                                   mock_rock_block_api_serial,
                                   mock_rock_block_api_adafruit_rockblock,
                                   mock_rock_block_api_time_sleep,
                                   mock_rock_block_api_get_satellite_transfer,
                                   mock_rock_block_api_get_data_in,
                                   mock_cloud_loop_message_get_whitelist,
                                   mock_rock_block_api_assemble_message_file_name):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        mock_rock_block_api_get_satellite_transfer.side_effect = [(0, 3, 1, 0, 100, 0)]
        test_payload = '0,#fbc84a (1/2),Info'
        test_encoded_payload = test_payload.encode().hex()
        mock_rock_block_api_get_data_in.return_value = test_encoded_payload
        test_message_file_path = tmp_path / "2022_09_26__19_47_10.txt"
        mock_rock_block_api_assemble_message_file_name.return_value = test_message_file_path.as_posix()
        test_rock_block = RockBlockAPI()
        test_rock_block.check_mailbox()
        captured = capfd.readouterr()
        assert mock_rock_block_api_get_satellite_transfer.call_count == 1
        assert test_rock_block.status_of_mailbox == (0, 3, 1, 0, 100, 0)
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                'Talking to satellite...\n'
                                '(0, 3, 1, 0, 100, 0)\n'
                                '\n'
                                'DONE.\n'
                                '(0, 3, 1, 0, 100, 0)\n'
                                'Message Received\n'
                                'Size in bytes of message: 100\n'
                                'Number of Messages in Queue: 0\n'
                                '302c236662633834612028312f32292c496e666f\n'
                                'Hex Message Processing...\n'
                                'Changing Hex to Bytes\n'
                                "['test_sender_1@gmail.com']\n"
                                '#fbc84a (1/2)\n'
                                'Info\n'
                                'Hex Message Processed\n'
                                'Message Witten To: '
                                f'{test_message_file_path.as_posix()}\n')

    def test__talk_to_rock_block_success(self, capfd,
                                         mock_rock_block_api_serial,
                                         mock_rock_block_api_adafruit_rockblock,
                                         mock_rock_block_api_time_sleep,
                                         mock_rock_block_api_get_satellite_transfer):
        mock_rock_block_api_get_satellite_transfer.side_effect = [(0, 3, 1, 0, 100, 0)]
        test_rock_block = RockBlockAPI()
        test_rock_block._talk_to_rock_block()
        captured = capfd.readouterr()
        assert mock_rock_block_api_get_satellite_transfer.call_count == 1
        assert test_rock_block.status_of_mailbox == (0, 3, 1, 0, 100, 0)
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                'Talking to satellite...\n'
                                '(0, 3, 1, 0, 100, 0)\n'
                                '\n'
                                'DONE.\n')

    def test__talk_to_rock_block_single_failure(self, capfd,
                                                mock_rock_block_api_serial,
                                                mock_rock_block_api_adafruit_rockblock,
                                                mock_rock_block_api_time_sleep,
                                                mock_rock_block_api_get_satellite_transfer):
        mock_rock_block_api_get_satellite_transfer.side_effect = [(10, 3, 1, 0, 100, 0),
                                                                  (0, 3, 1, 0, 100, 0)]
        test_rock_block = RockBlockAPI()
        test_rock_block._talk_to_rock_block()
        captured = capfd.readouterr()
        assert mock_rock_block_api_get_satellite_transfer.call_count == 2
        assert test_rock_block.status_of_mailbox == (0, 3, 1, 0, 100, 0)
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                'Talking to satellite...\n'
                                '(10, 3, 1, 0, 100, 0)\n'
                                '(0, 3, 1, 0, 100, 0)\n'
                                '\n'
                                'DONE.\n')

    def test__process_rock_block_status_received(self, capfd,
                                                 mock_rock_block_api_serial,
                                                 mock_rock_block_api_adafruit_rockblock):
        test_status = (0, 3, 1, 0, 100, 0)
        test_rock_block = RockBlockAPI(status_of_mailbox=test_status)
        test_rock_block._process_rock_block_status()
        captured = capfd.readouterr()
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                '(0, 3, 1, 0, 100, 0)\n'
                                'Message Received\n'
                                'Size in bytes of message: 100\n'
                                'Number of Messages in Queue: 0\n')

    def test__process_rock_block_status_no_waiting(self, capfd,
                                                   mock_rock_block_api_serial,
                                                   mock_rock_block_api_adafruit_rockblock):
        test_status = (0, 3, 0, 0, 100, 0)
        test_rock_block = RockBlockAPI(status_of_mailbox=test_status)
        test_rock_block._process_rock_block_status()
        captured = capfd.readouterr()
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                '(0, 3, 0, 0, 100, 0)\n'
                                'No Messages Waiting\n'
                                'Size in bytes of message: 100\n'
                                'Number of Messages in Queue: 0\n')

    def test__process_rock_block_status_messages_in_queue(self, capfd,
                                                          mock_rock_block_api_serial,
                                                          mock_rock_block_api_adafruit_rockblock):
        test_status = (0, 3, 1, 0, 100, 3)
        test_rock_block = RockBlockAPI(status_of_mailbox=test_status)
        test_rock_block._process_rock_block_status()
        captured = capfd.readouterr()
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                '(0, 3, 1, 0, 100, 3)\n'
                                'Message Received\n'
                                'Size in bytes of message: 100\n'
                                'Number of Messages in Queue: 3\n')

    def test__save_rock_block_hex_data_to_file(self, capfd, tmp_path,
                                               mock_rock_block_api_serial,
                                               mock_rock_block_api_adafruit_rockblock,
                                               mock_rock_block_api_get_data_in,
                                               mock_cloud_loop_message_get_whitelist,
                                               mock_rock_block_api_assemble_message_file_name):
        test_payload = '0,#fbc84a (1/2),Info'
        test_encoded_payload = test_payload.encode().hex()
        mock_rock_block_api_get_data_in.return_value = test_encoded_payload
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_message_file_path = tmp_path / "2022_09_26__19_47_10.txt"
        mock_rock_block_api_assemble_message_file_name.return_value = test_message_file_path.as_posix()
        test_rock_block = RockBlockAPI()
        test_rock_block._save_rock_block_hex_data_to_file()
        captured = capfd.readouterr()
        with open(test_message_file_path) as f:
            test_written_content = f.read()
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                '302c236662633834612028312f32292c496e666f\n'
                                'Hex Message Processing...\n'
                                'Changing Hex to Bytes\n'
                                "['test_sender_1@gmail.com']\n"
                                '#fbc84a (1/2)\n'
                                'Info\n'
                                'Hex Message Processed\n'
                                'Message Witten To: '
                                f'{test_message_file_path.as_posix()}\n')
        assert test_written_content == "test_sender_1@gmail.com\n#fbc84a (1/2)\nInfo\n"

    def test__save_rock_block_hex_data_to_file_no_hex_data(self, capfd, tmp_path,
                                                           mock_rock_block_api_serial,
                                                           mock_rock_block_api_adafruit_rockblock,
                                                           mock_rock_block_api_get_data_in,
                                                           mock_cloud_loop_message_get_whitelist,
                                                           mock_rock_block_api_assemble_message_file_name):
        mock_rock_block_api_get_data_in.return_value = None
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_message_file_path = tmp_path / "2022_09_26__19_47_10.txt"
        mock_rock_block_api_assemble_message_file_name.return_value = test_message_file_path.as_posix()
        test_rock_block = RockBlockAPI()
        test_rock_block._save_rock_block_hex_data_to_file()
        captured = capfd.readouterr()
        assert captured.out == "RockBLOCK Processing...\nRockBLOCK Processed\nNone\n"

    def test__assemble_message_file_name(self,
                                         mock_rock_block_api_serial,
                                         mock_rock_block_api_adafruit_rockblock):
        test_file_name = RockBlockAPI()._assemble_message_file_name()
        assert re.findall(r"Inbox/\d{4}_\d{2}_\d{2}__\d{2}_\d{2}_\d{2}.txt", test_file_name)
