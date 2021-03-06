import pytest
from app import app


@pytest.fixture()
def test_app():
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture()
def client(test_app):
    return app.test_client()

#
# App Mocks
#


@pytest.fixture
def mock_send_satellite_message(mocker):
    return mocker.patch("app.send_satellite_message")


@pytest.fixture
def mock_relay_cloud_loop_message_to_email(mocker):
    return mocker.patch("app.relay_cloud_loop_message_to_email")


@pytest.fixture
def mock_get_imei(mocker):
    return mocker.patch("app.Config.get_imei")


@pytest.fixture
def mock_get_google_sub(mocker):
    return mocker.patch("app.Config.get_google_sub")


@pytest.fixture
def mock_relay_email_message_to_cloud_loop(mocker):
    return mocker.patch("app.relay_email_message_to_cloud_loop")


@pytest.fixture
def mock_get_latest_gmail_message_text(mocker):
    return mocker.patch("app.get_latest_gmail_message_text")


@pytest.fixture
def mock_message_text_is_new(mocker):
    return mocker.patch("app.message_text_is_new")


@pytest.fixture
def mock_get_sister(mocker):
    return mocker.patch("app.Config.get_sister")


@pytest.fixture
def mock_get_relay_switch(mocker):
    return mocker.patch("app.Config.get_relay_switch")


#
# Camphor Tree API Mocks
#


@pytest.fixture
def mock_read_gmail_message_from_file(mocker):
    return mocker.patch("apis.camphor_tree_api.read_gmail_message_from_file")


@pytest.fixture
def mock_save_gmail_message_to_file(mocker):
    return mocker.patch("apis.camphor_tree_api.save_gmail_message_to_file")


@pytest.fixture
def mock_write_gmail_message_to_file(mocker):
    return mocker.patch("apis.camphor_tree_api.write_gmail_message_to_file")

#
# Cloud Loop API Mocks
#


@pytest.fixture
def mock_cloud_loop_message_set_up_hex_encoded_message(mocker):
    return mocker.patch("apis.camphor_tree_api.DecodeCloudLoopMessage.set_up_hex_encoded_message")


@pytest.fixture
def mock_cloud_loop_message_set_up_message_to_hex_encode(mocker):
    return mocker.patch("apis.camphor_tree_api.HexEncodeForCloudLoop.set_up_message_to_hex_encode")


@pytest.fixture
def mock_cloud_loop_message_get_max_message_size(mocker):
    return mocker.patch("apis.cloud_loop_api.Config.get_max_message_size")


@pytest.fixture
def mock_cloud_loop_message_get_whitelist(mocker):
    return mocker.patch("apis.cloud_loop_api.Config.get_whitelist")


@pytest.fixture
def mock_cloud_loop_message_send_cloud_loop_message(mocker):
    return mocker.patch("apis.camphor_tree_api.HexEncodeForCloudLoop.send_cloud_loop_message")


@pytest.fixture
def mock_cloud_loop_api_get_cloud_loop_auth_token(mocker):
    return mocker.patch("apis.cloud_loop_api.Config.get_cloud_loop_auth_token")


@pytest.fixture
def mock_cloud_loop_api_get_rock_block_id(mocker):
    return mocker.patch("apis.cloud_loop_api.Config.get_rock_block_id")


@pytest.fixture
def mock_cloud_loop_api_get_cloud_loop_payload_url(mocker):
    return mocker.patch("apis.cloud_loop_api.HexEncodeForCloudLoop.get_cloud_loop_payload_url")


@pytest.fixture
def mock_cloud_loop_api_requests_get(mocker):
    return mocker.patch("apis.cloud_loop_api.requests.get")

#
# Rock Block API Mocks
#


@pytest.fixture
def mock_rock_block_api_set_up_uart(mocker):
    return mocker.patch("apis.camphor_tree_api.RockBlockAPI.set_up_uart")


@pytest.fixture
def mock_rock_block_api_send_data_out(mocker):
    return mocker.patch("apis.camphor_tree_api.RockBlockAPI.send_data_out")


@pytest.fixture
def mock_rock_block_api_get_satellite_transfer(mocker):
    return mocker.patch("apis.rock_block_api.RockBlockAPI.get_satellite_transfer")


@pytest.fixture
def mock_rock_block_api_set_data_out(mocker):
    return mocker.patch("apis.rock_block_api.RockBlockAPI.set_data_out")


@pytest.fixture
def mock_rock_block_api_time_sleep(mocker):
    return mocker.patch("apis.rock_block_api.time.sleep")

#
# GMail API Mocks
#


@pytest.fixture
def mock_gmail_api_set_up_google_client_id(mocker):
    return mocker.patch("apis.google_api.Config.get_google_id")


@pytest.fixture
def mock_gmail_api_set_up_set_up_google_client_secret(mocker):
    return mocker.patch("apis.google_api.Config.get_google_secret")


@pytest.fixture
def mock_gmail_api_set_up_set_up_refresh_token(mocker):
    return mocker.patch("apis.google_api.Config.get_google_refresh_token")


@pytest.fixture
def mock_gmail_api_set_up_set_up_google_topic(mocker):
    return mocker.patch("apis.google_api.Config.get_google_topic")


@pytest.fixture
def mock_gmail_api_set_up_set_up_email(mocker):
    return mocker.patch("apis.google_api.Config.get_email")


@pytest.fixture
def mock_gmail_api_set_up_set_up_message_size(mocker):
    return mocker.patch("apis.google_api.Config.get_max_message_size")


@pytest.fixture
def gmail_get_first_message_from_push(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessageGet.gmail_get_first_message_from_push")


@pytest.fixture
def mock_gmail_api_get_new_gmail_message(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessageGet.get_new_gmail_message")


@pytest.fixture
def mock_gmail_api_gmail_get_message_by_id(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessageGet.gmail_get_message_by_id")


@pytest.fixture
def mock_gmail_api_get_message_from_gmail_endpoint(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessageGet.get_message_from_gmail_endpoint")


@pytest.fixture
def mock_google_api_get_whitelist(mocker):
    return mocker.patch("apis.google_api.Config.get_whitelist")


@pytest.fixture
def mock_gmail_api_send_gmail_message(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessageSend.send_gmail_message")


@pytest.fixture
def mock_google_api_requests_get(mocker):
    return mocker.patch("apis.google_api.requests.get")


@pytest.fixture
def mock_google_api_requests_post(mocker):
    return mocker.patch("apis.google_api.requests.post")

#
# Other Function Mocks
#
