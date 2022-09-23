from apis.cloud_loop_api import HexEncodeForCloudLoop


class TestHexEncodeForCloudLoop:
    def test_set_up_message_to_hex_encode_no_message(self,
                                                     mock_cloud_loop_api_get_cloud_loop_auth_token,
                                                     mock_cloud_loop_api_get_rock_block_id):
        test_cloud_loop = HexEncodeForCloudLoop()
        assert not test_cloud_loop.message_from
        assert not test_cloud_loop.message_to_encode
        assert not test_cloud_loop.message_subject
