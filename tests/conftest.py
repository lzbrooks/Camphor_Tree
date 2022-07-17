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
def mock_get_gmail_push_id(mocker):
    return mocker.patch("app.get_gmail_push_id")


@pytest.fixture
def mock_push_id_is_new(mocker):
    return mocker.patch("app.push_id_is_new")


@pytest.fixture
def mock_relay_email_message_to_cloud_loop(mocker):
    return mocker.patch("app.relay_email_message_to_cloud_loop")

#
# Camphor Tree API Mocks
#

#
# Cloud Loop API Mocks
#


@pytest.fixture
def mock_cloud_loop_message_set_up_hex_encoded_message(mocker):
    return mocker.patch("apis.camphor_tree_api.CloudLoopMessage.set_up_hex_encoded_message")


@pytest.fixture
def mock_cloud_loop_message_set_up_message_to_hex_encode(mocker):
    return mocker.patch("apis.camphor_tree_api.CloudLoopMessage.set_up_message_to_hex_encode")


@pytest.fixture
def mock_cloud_loop_message_send_cloud_loop_message(mocker):
    return mocker.patch("apis.camphor_tree_api.CloudLoopMessage.send_cloud_loop_message")

#
# Rock Block API Mocks
#


@pytest.fixture
def mock_rock_block_api_set_up_uart(mocker):
    return mocker.patch("apis.camphor_tree_api.RockBlockAPI.set_up_uart")


@pytest.fixture
def mock_rock_block_api_send_data_out(mocker):
    return mocker.patch("apis.camphor_tree_api.RockBlockAPI.send_data_out")

#
# GMail API Mocks
#


@pytest.fixture
def mock_gmail_api_set_up_google_client_id(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessage.set_up_google_client_id")


@pytest.fixture
def mock_gmail_api_set_up_set_up_google_client_secret(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessage.set_up_google_client_secret")


@pytest.fixture
def mock_gmail_api_set_up_set_up_refresh_token(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessage.set_up_refresh_token")


@pytest.fixture
def mock_gmail_api_set_up_set_up_google_topic(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessage.set_up_google_topic")


@pytest.fixture
def mock_gmail_api_set_up_set_up_email_recipient(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessage.set_up_email_recipient")


@pytest.fixture
def mock_gmail_api_set_up_set_up_email_sender(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessage.set_up_email_sender")


@pytest.fixture
def mock_gmail_api_set_up_set_up_message_size(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessage.set_up_message_size")


@pytest.fixture
def mock_gmail_api_gmail_get_messages_from_push(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessage.gmail_get_messages_from_push")


@pytest.fixture
def mock_gmail_api_get_new_gmail_messages(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessage.get_new_gmail_messages")


@pytest.fixture
def mock_gmail_api_gmail_get_message_by_id(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessage.gmail_get_message_by_id")


@pytest.fixture
def mock_gmail_api_send_gmail_message(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailMessage.send_gmail_message")

#
# Other Function Mocks
#


@pytest.fixture
def mock_open(mocker):
    return mocker.patch("apis.camphor_tree_api.open")


@pytest.fixture
def mock_get_gmail_push_id_from_config(mocker):
    return mocker.patch("apis.camphor_tree_api.get_gmail_push_id_from_config")


@pytest.fixture
def mock_save_gmail_push_id_to_file(mocker):
    return mocker.patch("apis.camphor_tree_api.save_gmail_push_id_to_file")
