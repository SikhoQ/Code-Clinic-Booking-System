from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
import sys
from InquirerPy import inquirer


TOKEN_FILE = os.path.expanduser("~/.google_calendar_token.json")
CREDS_FILE = os.path.expanduser("~/.google_calendar_credentials.json")
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authorise_google_calendar(scopes, credentials_file, token_file):
    credentials = None

    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, scopes)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            original_stdout = sys.stdout
            # Redirect standard output to a null device (a place where output is discarded)
            # This is to remove the "please visit this URL..." output while running program
            if inquirer.confirm(message="Continue to Google OAuth 2.0 authentication flow?").execute():
                with open(os.devnull, 'w') as null_device:
                    sys.stdout = null_device
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
                    credentials = flow.run_local_server(port=0)
                sys.stdout = original_stdout

        with open(token_file, 'w') as token_file:
            token_file.write(credentials.to_json())

    service = build('calendar', 'v3', credentials=credentials)

    return service
