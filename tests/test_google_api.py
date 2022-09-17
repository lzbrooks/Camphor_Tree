import json
import os

import pytest

from google.oauth2.credentials import Credentials

from apis.google_api_lib import GMailAPI, GMailAuth
from tests.data import bob_skipped_email, two_part_email, dummy_client_credentials, \
    dummy_expired_access_token, dummy_unexpired_access_token


class TestGMailAuth:

    def test_re_watch_assemble_valid_http(self, mocker, tmp_path,
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
        assert mock_gmail_auth_google_api_execute_request.called

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

    def test_refresh_with_browser_no_credential_file(self, tmp_path,
                                                     mock_gmail_api_get_google_topic,
                                                     mock_gmail_auth_google_api_execute_request,
                                                     mock_gmail_auth_google_api_refresh_access_token_local,
                                                     mock_gmail_auth_google_api_refresh_with_browser):
        test_gmail_auth = GMailAuth()
        with pytest.raises(FileNotFoundError, match=r"No such file or directory: 'credentials.json'"):
            test_gmail_auth.refresh_with_browser()

    def test_get_creds_assemble_valid_http(self, mocker, tmp_path,
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
        assert mock_gmail_auth_google_api_refresh_access_token_local.called

    def test_get_creds_no_token_file(self, mocker, tmp_path,
                                     mock_gmail_api_get_google_topic,
                                     mock_gmail_auth_google_api_refresh_access_token_local):
        tmp_token_file = tmp_path / 'token.json'
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        test_gmail_auth = GMailAuth()
        with pytest.raises(ValueError, match=r"No Valid Refresh Token"):
            test_gmail_auth._get_creds()

    def test_get_creds_expired_token_file(self, mocker, tmp_path,
                                          mock_gmail_api_get_google_topic,
                                          mock_gmail_auth_google_api_refresh_access_token_local):
        tmp_token_file = tmp_path / 'token.json'
        token_dict = dummy_expired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        test_gmail_auth = GMailAuth()
        test_gmail_auth._get_creds()
        assert mock_gmail_auth_google_api_refresh_access_token_local.called

    def test_get_creds_unexpired_token_file(self, mocker, tmp_path,
                                            mock_gmail_api_get_google_topic,
                                            mock_gmail_auth_google_api_refresh_access_token_local):
        tmp_token_file = tmp_path / 'token.json'
        token_dict = dummy_unexpired_access_token.token_dict
        with open(tmp_token_file, "w") as test_file_object:
            json.dump(token_dict, test_file_object)
        mocker.patch.dict(os.environ, {"CAMPHOR_TREE_ACCESS_TOKEN_FILE": tmp_token_file.as_posix()})
        test_gmail_auth = GMailAuth()
        test_gmail_auth._get_creds()
        assert not mock_gmail_auth_google_api_refresh_access_token_local.called


class TestGMailApi:
    def test__dissect_message__no_parts(self, mock_gmail_api_get_message_size,
                                        mock_google_api_get_whitelist):
        mock_gmail_api_get_message_size.return_value = '250'
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
        mock_gmail_api_get_message_size.return_value = '250'
        mock_google_api_get_whitelist.return_value = {"0": "test_sender@gmail.com"}
        sut = GMailAPI()
        message_from, message_subject, message_text = sut._dissect_message(two_part_email.email['payload'])
        assert message_from == "test_sender@gmail.com"
        assert message_subject == "full emails"
        assert message_text == "Yep, I've observed some pretty large emails going back and forth. I " \
                               "do\r\ndouble-check emails in cloudloop so if something gets lost I'll forward it," \
                               "\r\nbut so far the new integration has not failed to deliver anything\r\n"
