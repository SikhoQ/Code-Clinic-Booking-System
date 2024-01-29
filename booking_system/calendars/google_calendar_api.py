import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']


def authorize_and_authenticate():
    """
    Authorize and initialize the Google Calendar API.
    """
    credentials = None

    token_path = os.path.expanduser("~/.google_calendar_token.json")

    if os.path.exists(token_path):
        credentials = service = build('calendar', 'v3', credentials=None)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(credentials.to_json())

    service = build('calendar', 'v3', credentials=credentials)
    return service
