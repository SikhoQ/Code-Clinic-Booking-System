from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import sys
from InquirerPy import inquirer


TOKEN_FILE = os.path.expanduser("~/.google_calendar_token.json")
CREDS_FILE = os.path.expanduser("~/.google_calendar_credentials.json")
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authorise_google_calendar(scopes, credentials_file, token_file):
    credentials = None

    # Check if token file exists and contains valid credentials
    if os.path.exists(token_file):
        # credentials = json.loads(open(token_file, 'r').read())
        credentials = Credentials.from_authorized_user_file(token_file, scopes)

    # If there are no (valid) credentials available, let the user log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # Save the original standard output
            original_stdout = sys.stdout
            # Redirect standard output to a null device (a place where output is discarded)
            # This is to remove the "please visit this URL..." output while running program
            with open(os.devnull, 'w') as null_device:
                sys.stdout = null_device
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
                credentials = flow.run_local_server(port=0)
            sys.stdout = original_stdout

        # Save the credentials for the next run
        with open(token_file, 'w') as token_file:
            token_file.write(credentials.to_json())

    service = build('calendar', 'v3', credentials=credentials)

    return credentials, service
