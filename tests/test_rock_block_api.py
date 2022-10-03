import json
import re

from apis.rock_block_api import RockBlockAPI, CheckMail


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


class TestCheckMail:
    def test_check_mailbox_success(self, capfd, tmp_path,
                                   mock_rock_block_api_serial,
                                   mock_rock_block_api_adafruit_rockblock,
                                   mock_rock_block_api_time_sleep,
                                   mock_rock_block_api_get_satellite_transfer,
                                   mock_rock_block_api_get_data_in,
                                   mock_cloud_loop_message_get_whitelist,
                                   mock_rock_block_api__assemble_complete_message_file_path):
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        mock_rock_block_api_get_satellite_transfer.side_effect = [(0, 3, 1, 0, 100, 0)]
        test_payload = '0,#fbc84a (1/2),Info'
        test_encoded_payload = test_payload.encode().hex()
        mock_rock_block_api_get_data_in.return_value = test_encoded_payload
        test_message_file_path = tmp_path / "2022_09_26__19_47_10.txt"
        mock_rock_block_api__assemble_complete_message_file_path.return_value = test_message_file_path.as_posix()
        test_rock_block = CheckMail()
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

    # TODO: testing
    def test__save_rock_block_hex_data_to_file_last_part(self, capfd, tmp_path,
                                                         mock_rock_block_api_serial,
                                                         mock_rock_block_api_adafruit_rockblock,
                                                         mock_rock_block_api_get_data_in,
                                                         mock_cloud_loop_message_get_whitelist,
                                                         mock_rock_block_api__assemble_complete_message_file_path,
                                                         mock_rock_block_api__assemble_collating_message_file_path):
        test_payload = '0,#fbc84a (3/3),final part'
        test_encoded_payload = test_payload.encode().hex()
        mock_rock_block_api_get_data_in.return_value = test_encoded_payload
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_complete_message_file_path = tmp_path / "2022_09_26__19_47_10.txt"
        test_collating_message_file_path = tmp_path / "#fbc84a.txt"
        mock_rock_block_api__assemble_complete_message_file_path.return_value = \
            test_complete_message_file_path.as_posix()
        test_collating_message_dict = {"#fbc84a": ["Info", "first part"]}
        mock_rock_block_api__assemble_collating_message_file_path.return_value = \
            test_collating_message_file_path.as_posix()
        with open(test_complete_message_file_path, "w") as test_message_file_object:
            json.dump(test_collating_message_dict, test_message_file_object)
        test_rock_block = CheckMail()
        test_rock_block._save_rock_block_hex_data_to_file()
        captured = capfd.readouterr()
        with open(test_complete_message_file_path) as f:
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
                                'Saved Message "Info"\n'
                                'To '
                                f'{test_complete_message_file_path.as_posix()}\n')
        assert test_written_content == "test_sender_1@gmail.com\n#fbc84a (1/2)\nInfo\n"

    # TODO: testing
    def test__save_rock_block_hex_data_to_file_middle_part(self, capfd, tmp_path,
                                                           mock_rock_block_api_serial,
                                                           mock_rock_block_api_adafruit_rockblock,
                                                           mock_rock_block_api_get_data_in,
                                                           mock_cloud_loop_message_get_whitelist,
                                                           mock_rock_block_api__assemble_complete_message_file_path,
                                                           mock_rock_block_api__assemble_collating_message_file_path):
        test_payload = '0,#fbc84a (2/3),part 2'
        test_encoded_payload = test_payload.encode().hex()
        mock_rock_block_api_get_data_in.return_value = test_encoded_payload
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_complete_message_file_path = tmp_path / "2022_09_26__19_47_10.txt"
        test_collating_message_file_path = tmp_path / "#fbc84a.txt"
        mock_rock_block_api__assemble_complete_message_file_path.return_value = \
            test_complete_message_file_path.as_posix()
        test_collating_message_dict = {"#fbc84a": ["Info", "part1"]}
        mock_rock_block_api__assemble_collating_message_file_path.return_value = \
            test_collating_message_file_path.as_posix()
        with open(test_complete_message_file_path, "w") as test_message_file_object:
            json.dump(test_collating_message_dict, test_message_file_object)
        test_rock_block = CheckMail()
        test_rock_block._save_rock_block_hex_data_to_file()
        captured = capfd.readouterr()
        with open(test_complete_message_file_path) as f:
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
                                'Saved Message "Info"\n'
                                'To '
                                f'{test_collating_message_file_path.as_posix()}\n')
        assert test_written_content == "test_sender_1@gmail.com\n#fbc84a (1/2)\nInfo\n"

    # TODO: testing
    def test__save_rock_block_hex_data_to_file_first_part(self, capfd, tmp_path,
                                                          mock_rock_block_api_serial,
                                                          mock_rock_block_api_adafruit_rockblock,
                                                          mock_rock_block_api_get_data_in,
                                                          mock_cloud_loop_message_get_whitelist,
                                                          mock_rock_block_api__assemble_complete_message_file_path,
                                                          mock_rock_block_api__assemble_collating_message_file_path):
        test_payload = '0,#fbc84a (1/2),Info'
        test_encoded_payload = test_payload.encode().hex()
        mock_rock_block_api_get_data_in.return_value = test_encoded_payload
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_complete_message_file_path = tmp_path / "2022_09_26__19_47_10.txt"
        test_collating_message_file_path = tmp_path / "#fbc84a.txt"
        mock_rock_block_api__assemble_complete_message_file_path.return_value = \
            test_complete_message_file_path.as_posix()
        test_collating_message_dict = {}
        mock_rock_block_api__assemble_collating_message_file_path.return_value = \
            test_collating_message_file_path.as_posix()
        with open(test_complete_message_file_path, "w") as test_message_file_object:
            json.dump(test_collating_message_dict, test_message_file_object)
        test_rock_block = CheckMail()
        test_rock_block._save_rock_block_hex_data_to_file()
        captured = capfd.readouterr()
        with open(test_complete_message_file_path) as f:
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
                                'Saved Message "Info"\n'
                                'To '
                                f'{test_collating_message_file_path.as_posix()}\n')
        assert test_written_content == "test_sender_1@gmail.com\n#fbc84a (1/2)\nInfo\n"

    def test__save_rock_block_hex_data_to_file_no_hex_data(self, capfd, tmp_path,
                                                           mock_rock_block_api_serial,
                                                           mock_rock_block_api_adafruit_rockblock,
                                                           mock_rock_block_api_get_data_in,
                                                           mock_cloud_loop_message_get_whitelist,
                                                           mock_rock_block_api__assemble_complete_message_file_path):
        mock_rock_block_api_get_data_in.return_value = None
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_message_file_path = tmp_path / "2022_09_26__19_47_10.txt"
        mock_rock_block_api__assemble_complete_message_file_path.return_value = test_message_file_path.as_posix()
        test_rock_block = CheckMail()
        test_rock_block._save_rock_block_hex_data_to_file()
        captured = capfd.readouterr()
        assert captured.out == "RockBLOCK Processing...\nRockBLOCK Processed\nNone\n"

    # TODO: testing
    def test__collate_cloud_loop_message_last_part(self, capfd, tmp_path,
                                                   mock_rock_block_api_serial,
                                                   mock_rock_block_api_adafruit_rockblock,
                                                   mock_rock_block_api_get_data_in,
                                                   mock_cloud_loop_message_get_whitelist):
        test_payload = '0,#fbc84a (3/3),final part'
        test_encoded_payload = test_payload.encode().hex()
        mock_rock_block_api_get_data_in.return_value = test_encoded_payload
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_complete_message_file_path = tmp_path / "2022_09_26__19_47_10.txt"
        test_collating_message_file_path = tmp_path / "#fbc84a.txt"
        test_collating_message_dict = {"#fbc84a": ["Info", "first part", None]}
        with open(test_collating_message_file_path, "w") as test_message_file_object:
            json.dump(test_collating_message_dict, test_message_file_object)
        test_rock_block = CheckMail(recipient_list="test_sender_1@gmail.com",
                                    message_hash_id="#fbc84a",
                                    message_part_number='3',
                                    parts_total='3',
                                    message_text="final part",
                                    collating_message_file_path=test_collating_message_file_path.as_posix(),
                                    complete_message_file_path=test_complete_message_file_path.as_posix())
        test_complete_message = test_rock_block._collate_cloud_loop_message()
        captured = capfd.readouterr()
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                "{'#fbc84a': ['Info', 'first part', None]}\n"
                                'Collation of Message #fbc84a Complete At 3/3\n'
                                'Removed #fbc84a From '
                                f'{test_collating_message_file_path.as_posix()}\n')
        # TODO: test collating file is gone
        assert test_complete_message == {'Body': 'first partfinal part',
                                         'From': 'test_sender_1@gmail.com',
                                         'Subject': 'Info'}

    # TODO: testing
    def test__collate_cloud_loop_message_middle_part(self, capfd, tmp_path,
                                                     mock_rock_block_api_serial,
                                                     mock_rock_block_api_adafruit_rockblock,
                                                     mock_rock_block_api_get_data_in,
                                                     mock_cloud_loop_message_get_whitelist):
        test_payload = '0,#fbc84a (2/3),part 2'
        test_encoded_payload = test_payload.encode().hex()
        mock_rock_block_api_get_data_in.return_value = test_encoded_payload
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_complete_message_file_path = tmp_path / "2022_09_26__19_47_10.txt"
        test_collating_message_file_path = tmp_path / "#fbc84a.txt"
        test_collating_message_dict = {"#fbc84a": ["Info", None, "part3"]}
        with open(test_collating_message_file_path, "w") as test_message_file_object:
            json.dump(test_collating_message_dict, test_message_file_object)
        test_rock_block = CheckMail(recipient_list="test_sender_1@gmail.com",
                                    message_hash_id="#fbc84a",
                                    message_part_number='2',
                                    parts_total='3',
                                    message_text="part 2",
                                    collating_message_file_path=test_collating_message_file_path,
                                    complete_message_file_path=test_complete_message_file_path)
        test_complete_message = test_rock_block._collate_cloud_loop_message()
        captured = capfd.readouterr()
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                "{'#fbc84a': ['Info', None, 'part3']}\n"
                                'Removed #fbc84a From '
                                f'{test_collating_message_file_path.as_posix()}\n')
        # TODO: test collating file contents
        # with open(test_complete_message_file_path) as f:
        #     test_written_content = f.read()
        assert test_complete_message == {'Body': 'part 2part3', 'From': 'test_sender_1@gmail.com', 'Subject': 'Info'}

    # TODO: testing
    def test__collate_cloud_loop_message_first_part(self, capfd, tmp_path,
                                                    mock_rock_block_api_serial,
                                                    mock_rock_block_api_adafruit_rockblock,
                                                    mock_rock_block_api_get_data_in,
                                                    mock_cloud_loop_message_get_whitelist):
        test_payload = '0,#fbc84a (1/2),Info'
        test_encoded_payload = test_payload.encode().hex()
        mock_rock_block_api_get_data_in.return_value = test_encoded_payload
        mock_cloud_loop_message_get_whitelist.return_value = {"0": "test_sender_1@gmail.com",
                                                              "1": "test_sender_2@gmail.com"}
        test_complete_message_file_path = tmp_path / "2022_09_26__19_47_10.txt"
        test_collating_message_file_path = tmp_path / "#fbc84a.txt"
        test_rock_block = CheckMail(recipient_list="test_sender_1@gmail.com",
                                    message_hash_id="#fbc84a",
                                    message_part_number='1',
                                    parts_total='2',
                                    message_text="Info",
                                    collating_message_file_path=test_collating_message_file_path,
                                    complete_message_file_path=test_complete_message_file_path)
        test_complete_message = test_rock_block._collate_cloud_loop_message()
        captured = capfd.readouterr()
        assert captured.out == ('RockBLOCK Processing...\n'
                                'RockBLOCK Processed\n'
                                'Saved Message "Info"\n'
                                'To '
                                f'{test_collating_message_file_path.as_posix()}\n')
        # TODO: test collating file content
        # with open(test_complete_message_file_path) as f:
        #     test_written_content = f.read()
        assert test_complete_message == "test_sender_1@gmail.com\n#fbc84a (1/2)\nInfo\n"

    def test__assemble_complete_message_file_name(self,
                                                  mock_rock_block_api_serial,
                                                  mock_rock_block_api_adafruit_rockblock):
        test_file_name = CheckMail()._assemble_complete_message_file_path()
        assert re.findall(r"Inbox/\d{4}_\d{2}_\d{2}__\d{2}_\d{2}_\d{2}.txt", test_file_name)
