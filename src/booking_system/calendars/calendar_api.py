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


def authorise_google_calendar():
    """ Authorizes access to Google Calendar API.

    Returns:
        service:  Google Calendar service object. 
    """
    credentials = None

    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(filename=TOKEN_FILE, scopes=SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        elif inquirer.confirm(message="Continue to Google OAuth 2.0 authentication flow?\n").execute():
            # Redirect standard output to a null device (a place where output is discarded)
            # This is to remove the "please visit this URL..." output while running program

            original_stdout = sys.stdout
            with open(os.devnull, 'w') as null_device:
                sys.stdout = null_device
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file=CREDS_FILE, scopes=SCOPES)
                    credentials = flow.run_local_server(port=0)

                # if user denies access, quit program
                except Exception as e:
                    os.system("clear")
                    sys.exit(f"There was an error during authentication: {e}\n\nQuitting...")

                sys.stdout = original_stdout

        with open(TOKEN_FILE, 'w') as token_file:
            token_file.write(credentials.to_json())

    service = build('calendar', 'v3', credentials=credentials)

    return service
