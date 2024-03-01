# import unittest
# from unittest.mock import MagicMock, patch
# from src.booking_system.calendars.calendar_api import authorise_google_calendar


# class TestGoogleCalendarAuthorization(unittest.TestCase):

#     @patch('os.path.exists', return_value=True)
#     @patch('google.oauth2.credentials.Credentials.from_authorized_user_file')
#     def test_existing_token_file(self, mock_from_authorized_user_file, mock_os_path_exists):
#         # Mock the return value of Credentials.from_authorized_user_file
#         mock_credentials = MagicMock()
#         mock_from_authorized_user_file.return_value = mock_credentials

#         # Call the function under test
#         service = authorise_google_calendar()

#         # Assertions
#         self.assertEqual(service, mock_credentials)

#         # Verify that Credentials.from_authorized_user_file was called with the correct arguments
#         mock_from_authorized_user_file.assert_called_once_with(filename='~/.google_calendar_token.json', scopes=['https://www.googleapis.com/auth/calendar'])

#     @patch('os.path.exists', return_value=False)
#     @patch('calendar_api.inquirer.confirm', return_value=MagicMock(execute=MagicMock(return_value=True)))
#     @patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file')
#     def test_new_token_file(self, mock_from_client_secrets_file, mock_confirm, mock_os_path_exists):
#         # Mock the return value of InstalledAppFlow.from_client_secrets_file
#         mock_flow = MagicMock()
#         mock_credentials = MagicMock()
#         mock_flow.run_local_server.return_value = mock_credentials
#         mock_from_client_secrets_file.return_value = mock_flow

#         # Call the function under test
#         service = authorise_google_calendar()

#         # Assertions
#         self.assertEqual(service, mock_credentials)

#         # Verify that InstalledAppFlow.from_client_secrets_file was called with the correct arguments
#         mock_from_client_secrets_file.assert_called_once_with(client_secrets_file='~/.google_calendar_credentials.json', scopes=['https://www.googleapis.com/auth/calendar'])

    

# if __name__ == '__main__':
#     unittest.main()
