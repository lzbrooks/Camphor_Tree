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
def mock_cloud_loop_message_get_max_message_size(mocker):
    return mocker.patch("apis.cloud_loop_api.Config.get_max_message_size")


@pytest.fixture
def mock_cloud_loop_message_get_whitelist(mocker):
    return mocker.patch("apis.cloud_loop_api.Config.get_whitelist")


@pytest.fixture
def mock_cloud_loop_message_send_cloud_loop_message(mocker):
    return mocker.patch("apis.camphor_tree_api.HexEncodeForCloudLoop.send_cloud_loop_message")


@pytest.fixture
def mock_cloud_loop_message_get_payload(mocker):
    return mocker.patch("apis.camphor_tree_api.HexEncodeForCloudLoop.get_payload")


@pytest.fixture
def mock_cloud_loop_api_get_cloud_loop_auth_token(mocker):
    return mocker.patch("apis.cloud_loop_api.Config.get_cloud_loop_auth_token")


@pytest.fixture
def mock_cloud_loop_api_get_rock_block_id(mocker):
    return mocker.patch("apis.cloud_loop_api.Config.get_rock_block_id")


@pytest.fixture
def mock_cloud_loop_api_get_cloud_loop_payload_url(mocker):
    return mocker.patch("apis.cloud_loop_api.HexEncodeForCloudLoop._get_cloud_loop_payload_url")


@pytest.fixture
def mock_cloud_loop_api_requests_get(mocker):
    return mocker.patch("apis.cloud_loop_api.requests.get")

#
# Rock Block API Mocks
#


@pytest.fixture
def mock_rock_block_api_set_up_uart(mocker):
    return mocker.patch("apis.camphor_tree_api.RockBlockAPI._set_up_uart")


@pytest.fixture
def mock_rock_block_api_send_data_out(mocker):
    return mocker.patch("apis.camphor_tree_api.RockBlockAPI.send_data_out")


@pytest.fixture
def mock_rock_block_api_get_satellite_transfer(mocker):
    return mocker.patch("apis.rock_block_api.RockBlockAPI._get_satellite_transfer")


@pytest.fixture
def mock_rock_block_api_set_data_out(mocker):
    return mocker.patch("apis.rock_block_api.RockBlockAPI._set_data_out")


@pytest.fixture
def mock_rock_block_api_time_sleep(mocker):
    return mocker.patch("apis.rock_block_api.time.sleep")

#
# GMail API Mocks
#


@pytest.fixture
def mock_gmail_api_get_google_client_id(mocker):
    return mocker.patch("apis.google_api_lib.Config.get_google_id")


@pytest.fixture
def mock_gmail_api_get_google_client_secret(mocker):
    return mocker.patch("apis.google_api_lib.Config.get_google_secret")


@pytest.fixture
def mock_gmail_api_get_refresh_token(mocker):
    return mocker.patch("apis.google_api_lib.Config.get_google_refresh_token")


@pytest.fixture
def mock_gmail_api_get_google_topic(mocker):
    return mocker.patch("apis.google_api_lib.Config.get_google_topic")


@pytest.fixture
def mock_gmail_api_get_email(mocker):
    return mocker.patch("apis.google_api_lib.Config.get_email")


@pytest.fixture
def mock_gmail_api_get_message_size(mocker):
    return mocker.patch("apis.google_api_lib.Config.get_max_message_size")


@pytest.fixture
def mock_google_api_get_whitelist(mocker):
    return mocker.patch("apis.google_api_lib.Config.get_whitelist")


@pytest.fixture
def mock_google_api_get_whitelist(mocker):
    return mocker.patch("apis.google_api_lib.Config.get_whitelist")


@pytest.fixture
def mock_gmail_get_top_inbox_message(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailAPI.get_top_inbox_message")


@pytest.fixture
def mock_gmail_api_get_gmail_message_by_id(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailAPI.get_gmail_message_by_id")


@pytest.fixture
def mock_gmail_api_send_gmail_message(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailAPI.send_gmail_message")


@pytest.fixture
def mock_gmail_api_get_creds(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailAPI._get_creds")


@pytest.fixture
def mock_gmail_api_google_api_get_top_inbox_message(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailAPI._google_api_get_top_inbox_message")


@pytest.fixture
def mock_gmail_api_google_api_send_message(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailAPI._google_api_send_message")


@pytest.fixture
def mock_gmail_api_google_api_get_message(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailAPI._google_api_get_message")


@pytest.fixture
def mock_gmail_auth_google_api_refresh_access_token(mocker):
    return mocker.patch("apis.camphor_tree_api.GMailAPI._google_api_refresh_access_token")

#
# GMail API Mocks LOCAL
#


@pytest.fixture
def mock_gmail_api_get_creds_local(mocker):
    return mocker.patch("apis.google_api_lib.GMailAPI._get_creds")


@pytest.fixture
def mock_gmail_api_dissect_message_local(mocker):
    return mocker.patch("apis.google_api_lib.GMailAPI._dissect_message")


@pytest.fixture
def mock_gmail_api_google_api_execute_request(mocker):
    return mocker.patch("apis.google_api_lib.GMailAPI._google_api_execute_request")


@pytest.fixture
def mock_gmail_api_google_api_refresh_access_token_local(mocker):
    return mocker.patch("apis.google_api_lib.GMailAPI._google_api_refresh_access_token")

#
# GMail Auth Mocks LOCAL
#


@pytest.fixture
def mock_gmail_api_get_creds_local(mocker):
    return mocker.patch("apis.google_api_lib.GMailAuth._get_creds")


@pytest.fixture
def mock_gmail_auth_google_api_execute_request(mocker):
    return mocker.patch("apis.google_api_lib.GMailAuth._google_api_execute_request")


@pytest.fixture
def mock_gmail_auth_google_api_execute_request_http_catch(mocker):
    return mocker.patch("apis.google_api_lib.GMailAuth._google_api_execute_request_http_catch")


@pytest.fixture
def mock_gmail_auth_google_api_re_watch(mocker):
    return mocker.patch("apis.google_api_lib.GMailAuth._google_api_re_watch")


@pytest.fixture
def mock_gmail_auth_google_api_refresh_with_browser(mocker):
    return mocker.patch("apis.google_api_lib.GMailAuth._google_api_refresh_with_browser")


@pytest.fixture
def mock_gmail_auth_google_api_refresh_access_token_local(mocker):
    return mocker.patch("apis.google_api_lib.GMailAuth._google_api_refresh_access_token")


#
# Other Function Mocks
#
