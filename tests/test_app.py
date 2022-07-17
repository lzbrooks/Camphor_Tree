class TestAppConsoleFlow:
    def test_login_page_default_load(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'submit-password' in response.data
        assert b'Satsuki Console' in response.data

    def test_login_page_default_login(self, client):
        response = client.post('/', data={"password": "satsuki",
                                          "submit-password": "Login"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data
        assert b'Console' in response.data

    def test_login_page_invalid_login(self, client):
        response = client.post('/', data={"password": "nope",
                                          "submit-password": "Login"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'submit-password' in response.data
        assert b'Satsuki Console' in response.data

    def test_email_page_valid_email(self, client, mock_send_satellite_message):
        mock_send_satellite_message.return_value = "Send Success"
        response = client.post('/', data={"email": "satsuki@mocker.com",
                                          "info_level": "Info",
                                          "message_body": "Testing",
                                          "submit-email": "Send Email"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data
        assert b'Send Success' in response.data

    def test_email_page_short_invalid_email(self, client):
        response = client.post('/', data={"email": "nope",
                                          "info_level": "Info",
                                          "message_body": "Testing",
                                          "submit-email": "Send Email"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data

        assert b'Field must be between 6 and 35 characters long.' in response.data
        assert b'Invalid email address.' in response.data

        assert b'Send Failure' in response.data

    def test_email_page_long_invalid_email(self, client):
        response = client.post('/', data={"email": "invalid",
                                          "info_level": "Info",
                                          "message_body": "Testing",
                                          "submit-email": "Send Email"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'Email Address' in response.data
        assert b'Info Level' in response.data
        assert b'Emergency' in response.data
        assert b'Urgent' in response.data
        assert b'value="Info"' in response.data
        assert b'Message Body' in response.data
        assert b'Send Email' in response.data

        assert b'Field must be between 6 and 35 characters long.' not in response.data
        assert b'Invalid email address.' in response.data

        assert b'Send Failure' in response.data

    def test_relay_valid_cloud_loop_message(self, client, mock_get_imei, mock_relay_cloud_loop_message_to_email):
        mock_get_imei.return_value = "2000"
        assert mock_get_imei() == "2000"
        response = client.post('/', json={"imei": "2000"})
        assert response.status_code == 200
        assert response.data == b'Success'

    def test_relay_invalid_cloud_loop_message(self, client, mock_get_imei, mock_relay_cloud_loop_message_to_email):
        mock_get_imei.return_value = "2000"
        assert mock_get_imei() == "2000"
        response = client.post('/', json={"imei": "3000"})
        assert response.status_code == 200
        assert b'Satsuki - Camphor Tree' in response.data
        assert b'submit-password' in response.data
        assert b'Satsuki Console' in response.data

    def test_relay_valid_sub_email_ping(self, client,
                                                 mock_get_google_sub,
                                                 mock_get_gmail_push_id,
                                                 mock_push_id_is_new,
                                                 mock_relay_email_message_to_cloud_loop):
        mock_get_google_sub.return_value = "test_sub"
        mock_get_gmail_push_id.return_value = "13"
        mock_push_id_is_new.return_value = True
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Success'

    def test_relay_duplicate_sub_email_ping(self, client,
                                                     mock_get_google_sub,
                                                     mock_get_gmail_push_id,
                                                     mock_push_id_is_new,
                                                     mock_relay_email_message_to_cloud_loop):
        mock_get_google_sub.return_value = "test_sub"
        mock_get_gmail_push_id.return_value = "13"
        mock_push_id_is_new.return_value = False
        response = client.post('/', json={"subscription": "test_sub",
                                          "message":
                                              {"data": "test_data"}
                                          })
        assert response.status_code == 200
        assert response.data == b'Bounced This One'
