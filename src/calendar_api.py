from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os


def authorize_google_calendar(scopes, credentials_file, token_file):
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
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'w') as token_file:
            token_file.write(credentials.to_json())

    service = build('calendar', 'v3', credentials=credentials)

    return credentials, service
