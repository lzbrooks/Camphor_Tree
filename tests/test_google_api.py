import json
import os
import types
from base64 import urlsafe_b64decode

import pytest

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

from apis.google_api import GMailAPI, GMailAuth
from gmail_auth_flow import gmail_auth_flow
from tests.data import bob_skipped_email, two_part_email, dummy_client_credentials, \
    dummy_expired_access_token, dummy_unexpired_access_token


class TestGMailAuth:
    def test_re_watch_assemble_valid_http(self, mocker, tmp_path, capfd,
                                          mock_gmail_api_get_google_topic,
                                          mock_gmail_auth_google_api_execute_request,
                                          mock_gmail_auth_google_api_refresh_access_token_local):
        mock_gmail_api_get_google_topic.return_value = 'test_topic'
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        test_gmail_auth = GMailAuth()
        test_gmail_auth.re_watch()
        captured = capfd.readouterr()
        assert mock_gmail_auth_google_api_execute_request.called
        assert captured.out == 'Access Token File Found\nGmail Re-Watch Failure\n'

    def test_re_watch_assemble_valid_response(self, mocker, tmp_path, capfd,
                                              mock_gmail_api_get_google_topic,
                                              mock_gmail_auth_google_api_re_watch,
                                              mock_gmail_auth_google_api_execute_request,
                                              mock_gmail_auth_google_api_refresh_access_token_local):
        mock_gmail_api_get_google_topic.return_value = 'test_topic'
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        mock_gmail_auth_google_api_re_watch.return_value = {'historyId': '1512534'}
        test_gmail_auth = GMailAuth()
        test_gmail_auth.re_watch()
        captured = capfd.readouterr()
        assert mock_gmail_auth_google_api_re_watch.called
        assert captured.out == 'Access Token File Found\nGMail Re-Watch Success\n'

    def test_re_watch_valid_body_made(self,
                                      mock_gmail_api_get_google_topic,
                                      mock_gmail_auth_google_api_re_watch,
                                      mock_gmail_api_get_creds_local):
        mock_gmail_api_get_google_topic.return_value = 'test_topic'
        test_gmail_auth = GMailAuth()
        test_gmail_auth.re_watch()
        mock_gmail_auth_google_api_re_watch.assert_called_with({
            'labelIds': ['INBOX'],
            'labelFilterAction': 'include',
            'topicName': 'test_topic'
        })

    def test_refresh_with_browser_valid_creds(self, mocker, tmp_path,
                                              mock_gmail_api_get_google_topic,
                                              mock_gmail_auth_google_api_refresh_with_browser):
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_expired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        test_scopes = ['https://www.googleapis.com/auth/gmail.modify']
        mock_gmail_auth_google_api_refresh_with_browser.return_value = \
            Credentials.from_authorized_user_file(tmp_token_file.as_posix(), test_scopes)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        test_gmail_auth = GMailAuth()
        test_gmail_auth.refresh_with_browser()
        assert mock_gmail_auth_google_api_refresh_with_browser.called

    # TODO: testing
    def test_refresh_with_browser_no_credential_file(self, mocker, tmp_path,
                                                     mock_gmail_api_get_google_topic,
                                                     mock_gmail_auth_google_api_execute_request,
                                                     mock_gmail_auth_google_api_refresh_access_token_local,
                                                     mock_gmail_auth_google_api_refresh_with_browser):
        tmp_invalid_cred_file = tmp_path / 'credentials.json'
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_invalid_cred_file.as_posix()})
        test_gmail_auth = GMailAuth()
        assert test_gmail_auth.cred_file == tmp_invalid_cred_file.as_posix()
        with pytest.raises(FileNotFoundError, match=f"No such file or directory: '{tmp_invalid_cred_file.as_posix()}'"):
            test_gmail_auth.refresh_with_browser()

    def test_get_creds_assemble_valid_http(self, mocker, tmp_path, capfd,
                                           mock_gmail_api_get_google_topic,
                                           mock_gmail_auth_google_api_refresh_access_token_local):
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_expired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        test_gmail_auth = GMailAuth()
        test_gmail_auth._get_creds()
        captured = capfd.readouterr()
        assert mock_gmail_auth_google_api_refresh_access_token_local.called
        assert captured.out == ('Access Token File Found\n'
                                'Getting New GMail Access Token...\n'
                                'GMail Access Token Attained\n'
                                f'Token Written To {tmp_token_file.as_posix()}\n')

    def test_get_creds_no_token_file(self, mocker, tmp_path, capfd,
                                     mock_gmail_api_get_google_topic,
                                     mock_gmail_auth_google_api_refresh_access_token_local):
        tmp_token_file = tmp_path / 'token.json'
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        test_gmail_auth = GMailAuth()
        with pytest.raises(ValueError, match=r"No Valid Refresh Token"):
            test_gmail_auth._get_creds()
        captured = capfd.readouterr()
        assert captured.out == 'Access Token File Not Found\n'

    def test_get_creds_expired_token_file(self, mocker, tmp_path, capfd,
                                          mock_gmail_api_get_google_topic,
                                          mock_gmail_auth_google_api_refresh_access_token_local):
        tmp_token_file = tmp_path / 'token.json'
        token_dict = dummy_expired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        test_gmail_auth = GMailAuth()
        test_gmail_auth._get_creds()
        captured = capfd.readouterr()
        assert mock_gmail_auth_google_api_refresh_access_token_local.called
        assert captured.out == ('Access Token File Found\n'
                                'Getting New GMail Access Token...\n'
                                'GMail Access Token Attained\n'
                                f'Token Written To {tmp_token_file.as_posix()}\n')

    def test_get_creds_unexpired_token_file(self, mocker, tmp_path, capfd,
                                            mock_gmail_api_get_google_topic,
                                            mock_gmail_auth_google_api_refresh_access_token_local):
        tmp_token_file = tmp_path / 'token.json'
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        test_gmail_auth = GMailAuth()
        test_gmail_auth._get_creds()
        captured = capfd.readouterr()
        assert not mock_gmail_auth_google_api_refresh_access_token_local.called
        assert captured.out == 'Access Token File Found\n'

    def test_google_api_execute_request_error(self, mocker, capfd):
        test_api_http_request = "bogus_url"
        test_http_request_resp = types.SimpleNamespace()
        test_http_request_resp.status = "403"
        test_http_request_resp.reason = "placeholder"
        test_gmail_auth = GMailAuth()
        mocker.patch('apis.google_api.GMailAuth._google_api_execute_request_http_catch',
                     side_effect=HttpError(resp=test_http_request_resp,
                                           content=bytes("uh oh", "utf-8"),
                                           uri="http://localhost"))
        test_gmail_auth._google_api_execute_request(test_api_http_request)
        captured = capfd.readouterr()
        assert captured.out == "Error response status code : 403, reason : uh oh\n"

    def test_google_api_execute_request_no_error(self, capfd,
                                                 mock_gmail_auth_google_api_execute_request_http_catch):
        mock_gmail_auth_google_api_execute_request_http_catch.return_value = "200 Success"
        test_api_http_request = "bogus_url"
        test_gmail_auth = GMailAuth()
        test_response = test_gmail_auth._google_api_execute_request(test_api_http_request)
        captured = capfd.readouterr()
        assert not captured.out
        assert mock_gmail_auth_google_api_execute_request_http_catch.called
        assert test_response == "200 Success"


class TestGMailApi:
    def test_get_top_inbox_message_valid_message(self, mocker, tmp_path,
                                                 mock_gmail_api_google_api_refresh_access_token_local,
                                                 mock_gmail_api_google_api_execute_request):
        mock_gmail_api_google_api_execute_request.return_value = {"messages": [bob_skipped_email.email]}
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        test_gmail_api = GMailAPI()
        top_message = test_gmail_api.get_top_inbox_message()
        assert not mock_gmail_api_google_api_refresh_access_token_local.called
        assert mock_gmail_api_google_api_execute_request.called
        assert top_message == bob_skipped_email.email

    def test_get_top_inbox_message_no_message(self, mocker, tmp_path,
                                              mock_gmail_api_google_api_refresh_access_token_local,
                                              mock_gmail_api_google_api_execute_request):
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        test_gmail_api = GMailAPI()
        top_message = test_gmail_api.get_top_inbox_message()
        assert not mock_gmail_api_google_api_refresh_access_token_local.called
        assert mock_gmail_api_google_api_execute_request.called
        assert not top_message

    def test_get_gmail_message_by_id_valid_message(self, mocker, tmp_path,
                                                   mock_gmail_api_get_message_size,
                                                   mock_google_api_get_whitelist,
                                                   mock_gmail_api_google_api_refresh_access_token_local,
                                                   mock_gmail_api_google_api_execute_request):
        mock_gmail_api_get_message_size.return_value = 250
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_gmail_api_google_api_execute_request.return_value = bob_skipped_email.email
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        test_gmail_api = GMailAPI()
        message_from, message_subject, message_text = test_gmail_api.get_gmail_message_by_id(bob_skipped_email.email)
        assert not mock_gmail_api_google_api_refresh_access_token_local.called
        assert mock_gmail_api_google_api_execute_request.called
        assert message_from == "test_sender@gmail.com"
        assert message_subject == "RE: Info (1/1)"
        assert message_text == 'Really,\r\n\r\nSo there is no character limit for the sv kiki 95 ' \
                               'address?\r\n\r\nReally...Hawaii to Samoa?\r\n\r\nTest Person\r\nTest Place, ' \
                               'Test State 12345\r\ntest_sender@gmail.com\r\nH/O: 000-000-0000\r\nCell: ' \
                               '000-000-0000\r\n\r\n-----Original Message-----\r\nFrom: test_recipient@gmai.com [' \
                               'mailto:test_recipient@gmai.com] \r\nSent: Friday, June 10, 2022 7:54 PM\r\nTo: ' \
                               'test_sender@gmail.com\r\nSubject: Info (1/1)\r\n\r\nCorrection on that last: from ' \
                               'Hawaii to the Samoan islands\r\n\r\n\r\n-- \r\nThis email has been checked for ' \
                               'viruses by AVG.\r\nhttps://www.avg.com\r\n\r\n'

    def test_get_gmail_message_by_id_reject_draft(self, mocker, tmp_path,
                                                  mock_gmail_api_get_message_size,
                                                  mock_google_api_get_whitelist,
                                                  mock_gmail_api_google_api_refresh_access_token_local,
                                                  mock_gmail_api_google_api_execute_request,
                                                  mock_gmail_api_dissect_message_local):
        mock_gmail_api_get_message_size.return_value = '250'
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_gmail_api_google_api_execute_request.return_value = {'labelIds': ['DRAFT']}
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        test_gmail_api = GMailAPI()
        message_from, message_subject, message_text = test_gmail_api.get_gmail_message_by_id({"id": 42})
        assert not mock_gmail_api_google_api_refresh_access_token_local.called
        assert mock_gmail_api_google_api_execute_request.called
        assert not mock_gmail_api_dissect_message_local.called
        assert not message_from
        assert not message_subject
        assert not message_text

    def test_get_gmail_message_by_id_reject_sent(self, mocker, tmp_path,
                                                 mock_gmail_api_get_message_size,
                                                 mock_google_api_get_whitelist,
                                                 mock_gmail_api_google_api_refresh_access_token_local,
                                                 mock_gmail_api_google_api_execute_request,
                                                 mock_gmail_api_dissect_message_local):
        mock_gmail_api_get_message_size.return_value = '250'
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_gmail_api_google_api_execute_request.return_value = {'labelIds': ['SENT']}
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        test_gmail_api = GMailAPI()
        message_from, message_subject, message_text = test_gmail_api.get_gmail_message_by_id({"id": 42})
        assert not mock_gmail_api_google_api_refresh_access_token_local.called
        assert mock_gmail_api_google_api_execute_request.called
        assert not mock_gmail_api_dissect_message_local.called
        assert not message_from
        assert not message_subject
        assert not message_text

    def test_get_gmail_message_by_id_accept_inbox(self, mocker, tmp_path,
                                                  mock_gmail_api_get_message_size,
                                                  mock_google_api_get_whitelist,
                                                  mock_gmail_api_google_api_refresh_access_token_local,
                                                  mock_gmail_api_google_api_execute_request,
                                                  mock_gmail_api_dissect_message_local):
        mock_gmail_api_get_message_size.return_value = '250'
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        mock_gmail_api_google_api_execute_request.return_value = {'labelIds': ['INBOX'], 'payload': "test_payload"}
        mock_gmail_api_dissect_message_local.return_value = ("test_from", "test_subject", "test_text")
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        test_gmail_api = GMailAPI()
        message_from, message_subject, message_text = test_gmail_api.get_gmail_message_by_id({"id": 42})
        assert not mock_gmail_api_google_api_refresh_access_token_local.called
        assert mock_gmail_api_google_api_execute_request.called
        assert mock_gmail_api_dissect_message_local.called
        assert message_from == "test_from"
        assert message_subject == "test_subject"
        assert message_text == "test_text"

    def test_get_gmail_message_by_id_no_message_for_id(self, mocker, tmp_path,
                                                       mock_gmail_api_google_api_refresh_access_token_local,
                                                       mock_gmail_api_google_api_execute_request):
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        test_gmail_api = GMailAPI()
        message_from, message_subject, message_text = test_gmail_api.get_gmail_message_by_id(bob_skipped_email.email)
        assert not mock_gmail_api_google_api_refresh_access_token_local.called
        assert mock_gmail_api_google_api_execute_request.called
        assert not message_from
        assert not message_subject
        assert not message_text

    def test_send_gmail_message_to_valid_address(self, mocker, tmp_path,
                                                 mock_gmail_api_get_message_size,
                                                 mock_google_api_get_whitelist,
                                                 mock_gmail_api_google_api_refresh_access_token_local,
                                                 mock_gmail_api_google_api_execute_request):
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_EMAIL": "test_sender@gmail.com"})
        test_gmail_api = GMailAPI(message_to=["test_receiver@gmail.com"],
                                  message_from=None,
                                  message_subject="RE: Info (1/1)",
                                  message_text="test_text")
        test_gmail_api.send_gmail_message()
        assert not mock_gmail_api_google_api_refresh_access_token_local.called
        assert mock_gmail_api_google_api_execute_request.called
        print(urlsafe_b64decode(test_gmail_api.gmail_message['raw']))
        sent_message = urlsafe_b64decode(test_gmail_api.gmail_message['raw']).decode()
        assert "To: test_receiver@gmail.com\n" in sent_message
        assert "From: test_sender@gmail.com\n" in sent_message
        assert "Subject: RE: Info (1/1)\n" in sent_message
        assert 'Content-Type: text/plain; charset="utf-8"\nContent-Transfer-Encoding: 7bit\nMIME-Version: ' \
               '1.0\n\ntest_text\n' in sent_message

    def test_send_gmail_message_no_message(self, mocker, tmp_path,
                                           mock_gmail_api_get_message_size,
                                           mock_google_api_get_whitelist,
                                           mock_gmail_api_google_api_refresh_access_token_local,
                                           mock_gmail_api_google_api_execute_request):
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_EMAIL": "test_sender@gmail.com"})
        test_gmail_api = GMailAPI(message_to=None,
                                  message_from=None,
                                  message_subject=None,
                                  message_text=None)
        test_gmail_api.send_gmail_message()
        assert not mock_gmail_api_google_api_refresh_access_token_local.called
        assert not mock_gmail_api_google_api_execute_request.called
        assert not test_gmail_api.gmail_message

    def test__dissect_message__no_parts(self, mock_gmail_api_get_message_size,
                                        mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = 250
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        sut = GMailAPI()
        message_from, message_subject, message_text = sut._dissect_message(bob_skipped_email.email['payload'])
        assert message_from == 'test_sender@gmail.com'
        assert message_subject == 'RE: Info (1/1)'
        assert message_text == 'Really,\r\n\r\nSo there is no character limit for the sv kiki 95 ' \
                               'address?\r\n\r\nReally...Hawaii to Samoa?\r\n\r\nTest Person\r\nTest Place, ' \
                               'Test State 12345\r\ntest_sender@gmail.com\r\nH/O: 000-000-0000\r\nCell: ' \
                               '000-000-0000\r\n\r\n-----Original Message-----\r\nFrom: test_recipient@gmai.com [' \
                               'mailto:test_recipient@gmai.com] \r\nSent: Friday, June 10, 2022 7:54 PM\r\nTo: ' \
                               'test_sender@gmail.com\r\nSubject: Info (1/1)\r\n\r\nCorrection on that last: from ' \
                               'Hawaii to the Samoan islands\r\n\r\n\r\n-- \r\nThis email has been checked for ' \
                               'viruses by AVG.\r\nhttps://www.avg.com\r\n\r\n'

    def test__dissect_message__two_parts(self, mock_gmail_api_get_message_size,
                                         mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = 250
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        sut = GMailAPI()
        message_from, message_subject, message_text = sut._dissect_message(two_part_email.email['payload'])
        assert message_from == "test_sender@gmail.com"
        assert message_subject == "full emails"
        assert message_text == "Yep, I've observed some pretty large emails going back and forth. I " \
                               "do\r\ndouble-check emails in cloudloop so if something gets lost I'll forward it," \
                               "\r\nbut so far the new integration has not failed to deliver anything\r\n"

    def test__dissect_message_parts_valid_payload(self, mock_gmail_api_get_message_size,
                                                  mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = 250
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        sut = GMailAPI()
        message_text = sut._dissect_message_parts("test_sender@gmail.com", two_part_email.email['payload'])
        assert message_text == "Yep, I've observed some pretty large emails going back and forth. I " \
                               "do\r\ndouble-check emails in cloudloop so if something gets lost I'll forward it," \
                               "\r\nbut so far the new integration has not failed to deliver anything\r\n"

    def test__dissect_message_parts_stripped_valid_message(self, mock_gmail_api_get_message_size,
                                                           mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = 250
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_message_part = {"mimeType": "text/plain",
                             "body": {"size": 216,
                                      "data": "WWVwLCBJJ3ZlIG9ic2VydmVkIHNvbWUgcHJldHR5IGxhcmdlIGVtYWlscyBnb2luZy"
                                              "BiYWNrIGFuZCBmb3J0aC4gSSBkbw0KZG91YmxlLWNoZWNrIGVtYWlscyBpbiBjbG91Z"
                                              "Gxvb3Agc28gaWYgc29tZXRoaW5nIGdldHMgbG9zdCBJJ2xsIGZvcndhcmQgaXQsDQpi"
                                              "dXQgc28gZmFyIHRoZSBuZXcgaW50ZWdyYXRpb24gaGFzIG5vdCBmYWlsZWQgdG8gZGV"
                                              "saXZlciBhbnl0aGluZw0K"
                                      }}
        test_message_payload = {'parts': [test_message_part]}
        sut = GMailAPI()
        message_text = sut._dissect_message_parts("test_sender@gmail.com", test_message_payload)
        assert message_text == "Yep, I've observed some pretty large emails going back and forth. I " \
                               "do\r\ndouble-check emails in cloudloop so if something gets lost I'll forward it," \
                               "\r\nbut so far the new integration has not failed to deliver anything\r\n"

    def test__dissect_message_parts_no_parts(self, mock_gmail_api_get_message_size,
                                             mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = '250'
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_message_payload = {'parts': []}
        sut = GMailAPI()
        message_text = sut._dissect_message_parts("test_sender@gmail.com", test_message_payload)
        assert not message_text

    def test__dissect_message_parts_invalid_mime_type(self, mock_gmail_api_get_message_size,
                                                      mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = '250'
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_message_part = {"mimeType": "text/html",
                             "body": {"size": 216,
                                      "data": "WWVwLCBJJ3ZlIG9ic2VydmVkIHNvbWUgcHJldHR5IGxhcmdlIGVtYWlscyBnb2luZy"
                                              "BiYWNrIGFuZCBmb3J0aC4gSSBkbw0KZG91YmxlLWNoZWNrIGVtYWlscyBpbiBjbG91Z"
                                              "Gxvb3Agc28gaWYgc29tZXRoaW5nIGdldHMgbG9zdCBJJ2xsIGZvcndhcmQgaXQsDQpi"
                                              "dXQgc28gZmFyIHRoZSBuZXcgaW50ZWdyYXRpb24gaGFzIG5vdCBmYWlsZWQgdG8gZGV"
                                              "saXZlciBhbnl0aGluZw0K"
                                      }}
        test_message_payload = {'parts': [test_message_part]}
        sut = GMailAPI()
        message_text = sut._dissect_message_parts("test_sender@gmail.com", test_message_payload)
        assert not message_text

    def test__dissect_message_parts_no_mime_type(self, mock_gmail_api_get_message_size,
                                                 mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = '250'
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_message_part = {"body": {"size": 216,
                                      "data": "WWVwLCBJJ3ZlIG9ic2VydmVkIHNvbWUgcHJldHR5IGxhcmdlIGVtYWlscyBnb2luZy"
                                              "BiYWNrIGFuZCBmb3J0aC4gSSBkbw0KZG91YmxlLWNoZWNrIGVtYWlscyBpbiBjbG91Z"
                                              "Gxvb3Agc28gaWYgc29tZXRoaW5nIGdldHMgbG9zdCBJJ2xsIGZvcndhcmQgaXQsDQpi"
                                              "dXQgc28gZmFyIHRoZSBuZXcgaW50ZWdyYXRpb24gaGFzIG5vdCBmYWlsZWQgdG8gZGV"
                                              "saXZlciBhbnl0aGluZw0K"
                                      }}
        test_message_payload = {'parts': [test_message_part]}
        sut = GMailAPI()
        message_text = sut._dissect_message_parts("test_sender@gmail.com", test_message_payload)
        assert not message_text

    def test__dissect_message_parts_no_size(self, mock_gmail_api_get_message_size,
                                            mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = '250'
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_message_part = {"mimeType": "text/plain",
                             "body": {"data": "WWVwLCBJJ3ZlIG9ic2VydmVkIHNvbWUgcHJldHR5IGxhcmdlIGVtYWlscyBnb2luZy"
                                              "BiYWNrIGFuZCBmb3J0aC4gSSBkbw0KZG91YmxlLWNoZWNrIGVtYWlscyBpbiBjbG91Z"
                                              "Gxvb3Agc28gaWYgc29tZXRoaW5nIGdldHMgbG9zdCBJJ2xsIGZvcndhcmQgaXQsDQpi"
                                              "dXQgc28gZmFyIHRoZSBuZXcgaW50ZWdyYXRpb24gaGFzIG5vdCBmYWlsZWQgdG8gZGV"
                                              "saXZlciBhbnl0aGluZw0K"
                                      }}
        test_message_payload = {'parts': [test_message_part]}
        sut = GMailAPI()
        message_text = sut._dissect_message_parts("test_sender@gmail.com", test_message_payload)
        assert not message_text

    def test__dissect_message_parts_no_data(self, mock_gmail_api_get_message_size,
                                            mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = '250'
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_message_part = {"mimeType": "text/plain",
                             "body": {"size": 0}}
        test_message_payload = {'parts': [test_message_part]}
        sut = GMailAPI()
        message_text = sut._dissect_message_parts("test_sender@gmail.com", test_message_payload)
        assert not message_text

    def test__dissect_message_parts_small_size_not_whitelisted(self, mock_gmail_api_get_message_size,
                                                               mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = 250
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_message_part = {"mimeType": "text/plain",
                             "body": {"size": 216,
                                      "data": "WWVwLCBJJ3ZlIG9ic2VydmVkIHNvbWUgcHJldHR5IGxhcmdlIGVtYWlscyBnb2luZy"
                                              "BiYWNrIGFuZCBmb3J0aC4gSSBkbw0KZG91YmxlLWNoZWNrIGVtYWlscyBpbiBjbG91Z"
                                              "Gxvb3Agc28gaWYgc29tZXRoaW5nIGdldHMgbG9zdCBJJ2xsIGZvcndhcmQgaXQsDQpi"
                                              "dXQgc28gZmFyIHRoZSBuZXcgaW50ZWdyYXRpb24gaGFzIG5vdCBmYWlsZWQgdG8gZGV"
                                              "saXZlciBhbnl0aGluZw0K"
                                      }}
        test_message_payload = {'parts': [test_message_part]}
        sut = GMailAPI()
        message_text = sut._dissect_message_parts("test_not_whitelisted@gmail.com", test_message_payload)
        assert message_text == "Yep, I've observed some pretty large emails going back and forth. I " \
                               "do\r\ndouble-check emails in cloudloop so if something gets lost I'll forward it," \
                               "\r\nbut so far the new integration has not failed to deliver anything\r\n"

    def test__dissect_message_parts_large_size_not_whitelisted(self, mock_gmail_api_get_message_size,
                                                               mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = 250
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_message_part = {"mimeType": "text/plain",
                             "body": {"size": 300,
                                      "data": "WWVwLCBJJ3ZlIG9ic2VydmVkIHNvbWUgcHJldHR5IGxhcmdlIGVtYWlscyBnb2luZy"
                                              "BiYWNrIGFuZCBmb3J0aC4gSSBkbw0KZG91YmxlLWNoZWNrIGVtYWlscyBpbiBjbG91Z"
                                              "Gxvb3Agc28gaWYgc29tZXRoaW5nIGdldHMgbG9zdCBJJ2xsIGZvcndhcmQgaXQsDQpi"
                                              "dXQgc28gZmFyIHRoZSBuZXcgaW50ZWdyYXRpb24gaGFzIG5vdCBmYWlsZWQgdG8gZGV"
                                              "saXZlciBhbnl0aGluZw0K"
                                      }}
        test_message_payload = {'parts': [test_message_part]}
        sut = GMailAPI()
        message_text = sut._dissect_message_parts("test_not_whitelisted@gmail.com", test_message_payload)
        assert not message_text

    def test__dissect_message_parts_large_size_whitelisted(self, mock_gmail_api_get_message_size,
                                                           mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = 250
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        test_message_part = {"mimeType": "text/plain",
                             "body": {"size": 300,
                                      "data": "WWVwLCBJJ3ZlIG9ic2VydmVkIHNvbWUgcHJldHR5IGxhcmdlIGVtYWlscyBnb2luZy"
                                              "BiYWNrIGFuZCBmb3J0aC4gSSBkbw0KZG91YmxlLWNoZWNrIGVtYWlscyBpbiBjbG91Z"
                                              "Gxvb3Agc28gaWYgc29tZXRoaW5nIGdldHMgbG9zdCBJJ2xsIGZvcndhcmQgaXQsDQpi"
                                              "dXQgc28gZmFyIHRoZSBuZXcgaW50ZWdyYXRpb24gaGFzIG5vdCBmYWlsZWQgdG8gZGV"
                                              "saXZlciBhbnl0aGluZw0K"
                                      }}
        test_message_payload = {'parts': [test_message_part]}
        sut = GMailAPI()
        message_text = sut._dissect_message_parts("test_sender@gmail.com", test_message_payload)
        assert message_text == "Yep, I've observed some pretty large emails going back and forth. I " \
                               "do\r\ndouble-check emails in cloudloop so if something gets lost I'll forward it," \
                               "\r\nbut so far the new integration has not failed to deliver anything\r\n"

    def test_dissect_message_headers_valid_message(self):
        sut = GMailAPI()
        message_from, message_subject = sut._dissect_message_headers(two_part_email.email['payload'])
        assert message_from == "test_sender@gmail.com"
        assert message_subject == "full emails"

    def test_dissect_message_headers_valid_from(self):
        test_headers = {'headers': [{'name': 'From',
                                     'value': 'Test Person \u003ctest_sender@gmail.com\u003e'}]}
        sut = GMailAPI()
        message_from, message_subject = sut._dissect_message_headers(test_headers)
        assert message_from == 'test_sender@gmail.com'
        assert not message_subject

    def test_dissect_message_headers_invalid_from(self):
        test_headers = {'headers': [{'name': 'From',
                                     'value': 'invalid_address'}]}
        sut = GMailAPI()
        message_from, message_subject = sut._dissect_message_headers(test_headers)
        assert not message_from
        assert not message_subject

    def test_dissect_message_headers_valid_subject(self):
        test_headers = {'headers': [{'name': 'Subject',
                                     'value': 'testing...'}]}
        sut = GMailAPI()
        message_from, message_subject = sut._dissect_message_headers(test_headers)
        assert not message_from
        assert message_subject == 'testing...'

    def test_dissect_message_headers_no_from_value(self):
        test_headers = {'headers': [{'name': 'From',
                                     'value': ''}]}
        sut = GMailAPI()
        message_from, message_subject = sut._dissect_message_headers(test_headers)
        assert not message_from
        assert not message_subject

    def test_dissect_message_headers_no_subject_value(self):
        test_headers = {'headers': [{'name': 'Subject',
                                     'value': ''}]}
        sut = GMailAPI()
        message_from, message_subject = sut._dissect_message_headers(test_headers)
        assert not message_from
        assert not message_subject

    def test_dissect_message_headers_no_headers(self):
        test_headers = {'headers': []}
        sut = GMailAPI()
        message_from, message_subject = sut._dissect_message_headers(test_headers)
        assert not message_from
        assert not message_subject


class TestGmailAuthFlow:
    def test_gmail_auth_flow_re_watch_assemble_valid_http(self, mocker, tmp_path, capfd,
                                                          mock_gmail_api_get_google_topic,
                                                          mock_gmail_auth_google_api_execute_request,
                                                          mock_gmail_auth_google_api_refresh_access_token_local):
        mock_gmail_api_get_google_topic.return_value = 'test_topic'
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        gmail_auth_flow(["./gmail_auth_flow.py", "re_watch"])
        captured = capfd.readouterr()
        assert mock_gmail_auth_google_api_execute_request.called
        assert captured.out == 'Access Token File Found\nGmail Re-Watch Failure\n'

    def test_gmail_auth_flow_re_watch_assemble_valid_response(self, mocker, tmp_path, capfd,
                                                              mock_gmail_api_get_google_topic,
                                                              mock_gmail_auth_google_api_re_watch,
                                                              mock_gmail_auth_google_api_execute_request,
                                                              mock_gmail_auth_google_api_refresh_access_token_local):
        mock_gmail_api_get_google_topic.return_value = 'test_topic'
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        mock_gmail_auth_google_api_re_watch.return_value = {'historyId': '1512534'}
        gmail_auth_flow(["./gmail_auth_flow.py", "re_watch"])
        captured = capfd.readouterr()
        assert mock_gmail_auth_google_api_re_watch.called
        assert captured.out == 'Access Token File Found\nGMail Re-Watch Success\n'

    def test_gmail_auth_flow_re_watch_valid_body_made(self,
                                                      mock_gmail_api_get_google_topic,
                                                      mock_gmail_auth_google_api_re_watch,
                                                      mock_gmail_api_get_creds_local):
        mock_gmail_api_get_google_topic.return_value = 'test_topic'
        gmail_auth_flow(["./gmail_auth_flow.py", "re_watch"])
        mock_gmail_auth_google_api_re_watch.assert_called_with({
            'labelIds': ['INBOX'],
            'labelFilterAction': 'include',
            'topicName': 'test_topic'
        })

    def test_gmail_auth_flow_refresh_valid_creds(self, mocker, tmp_path,
                                                 mock_gmail_api_get_google_topic,
                                                 mock_gmail_auth_google_api_refresh_with_browser):
        tmp_cred_file = tmp_path / 'credentials.json'
        tmp_token_file = tmp_path / 'token.json'
        credentials_dict = dummy_client_credentials.credentials_dict
        with open(tmp_cred_file, "w") as test_file_object:
            json.dump(credentials_dict, test_file_object)
        token_dict = dummy_expired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        test_scopes = ['https://www.googleapis.com/auth/gmail.modify']
        mock_gmail_auth_google_api_refresh_with_browser.return_value = \
            Credentials.from_authorized_user_file(tmp_token_file.as_posix(), test_scopes)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_cred_file.as_posix()})
        gmail_auth_flow(["./gmail_auth_flow.py", "refresh"])
        assert mock_gmail_auth_google_api_refresh_with_browser.called

    # TODO: testing
    def test_gmail_auth_flow_refresh_no_credential_file(self, mocker, tmp_path,
                                                        mock_gmail_api_get_google_topic,
                                                        mock_gmail_auth_google_api_execute_request,
                                                        mock_gmail_auth_google_api_refresh_access_token_local,
                                                        mock_gmail_auth_google_api_refresh_with_browser):
        tmp_invalid_cred_file = tmp_path / 'credentials.json'
        tmp_invalid_token_file = tmp_path / 'token.json'
        mocker.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": tmp_invalid_cred_file.as_posix()})
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_invalid_token_file.as_posix()})
        with pytest.raises(FileNotFoundError,
                           match=f"No such file or directory: '{tmp_invalid_cred_file.as_posix()}'"):
            gmail_auth_flow(["./gmail_auth_flow.py", "refresh"])

    # TODO: stub test
    def test_gmail_auth_flow_refresh_error_response(self):
        test_case = """
                    Access Token File Found
                    Error response status code : 400, reason : [{'message': 'Invalid topicName does not match projects/camphor-tree-server/topics/*', 'domain': 'global', 'reason': 'invalidArgument'}]
                    Traceback (most recent call last):
                    File "/home/satsuki/Camphor_Tree/gmail_auth_flow.py", line 40, in <module>
                    gmail_auth_flow(sys.argv)
                    File "/home/satsuki/Camphor_Tree/gmail_auth_flow.py", line 12, in gmail_auth_flow
                    gmail_auth.re_watch()
                    File "/home/satsuki/Camphor_Tree/apis/google_api.py", line 37, in re_watch
                    response_json = self._google_api_re_watch(request)
                    File "/home/satsuki/Camphor_Tree/apis/google_api.py", line 75, in _google_api_re_watch
                    return self._google_api_execute_request(re_watch_http_request).json()
                    AttributeError: 'NoneType' object has no attribute 'json' 
                    """
        print(test_case)
        pass

    def test_gmail_auth_flow_invalid_option(self, tmp_path, capfd,
                                            mock_gmail_api_get_google_topic,
                                            mock_gmail_auth_google_api_execute_request,
                                            mock_gmail_auth_google_api_refresh_access_token_local,
                                            mock_gmail_auth_google_api_refresh_with_browser):
        gmail_auth_flow(["./gmail_auth_flow.py", "invalid"])
        captured = capfd.readouterr()
        assert captured.out == ("Argument 'invalid' given is not valid\n"
                                "Valid arguments are either 're_watch' or 'refresh'\n"
                                '\n'
                                'Environment Variables needed are:\n'
                                "GOOGLE_APPLICATION_CREDENTIALS: 'credentials.json' client credentials file "
                                'path\n'
                                "CAMPHOR_TREE_ACCESS_TOKEN_FILE: 'token.json' refresh token file path\n"
                                '\n'
                                're_watch specific environment variable needed is:\n'
                                'CAMPHOR_TREE_TOPIC: google pub/sub topic string\n')

    def test_gmail_auth_flow_no_option(self, tmp_path, capfd,
                                            mock_gmail_api_get_google_topic,
                                            mock_gmail_auth_google_api_execute_request,
                                            mock_gmail_auth_google_api_refresh_access_token_local,
                                            mock_gmail_auth_google_api_refresh_with_browser):
        gmail_auth_flow(["./gmail_auth_flow.py"])
        captured = capfd.readouterr()
        assert captured.out == ("Argument 'None' given is not valid\n"
                                "Valid arguments are either 're_watch' or 'refresh'\n"
                                '\n'
                                'Environment Variables needed are:\n'
                                "GOOGLE_APPLICATION_CREDENTIALS: 'credentials.json' client credentials file "
                                'path\n'
                                "CAMPHOR_TREE_ACCESS_TOKEN_FILE: 'token.json' refresh token file path\n"
                                '\n'
                                're_watch specific environment variable needed is:\n'
                                'CAMPHOR_TREE_TOPIC: google pub/sub topic string\n')
