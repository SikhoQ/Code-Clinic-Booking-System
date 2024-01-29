from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def verify_google_calendar_connection(credentials_path):
    try:
        # Load stored credentials
        creds = Credentials.from_authorized_user_file(credentials_path)

        # Check if the credentials are valid; refresh if expired
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise Exception("Invalid credentials. Please reauthorize.")

        # Build the Google Calendar API service
        service = build('calendar', 'v3', credentials=creds)

        # Attempt to retrieve a list of the next 1 event from the primary calendar
        events = service.events().list(calendarId='primary', maxResults=1).execute()

        # If successful, print the event summary
        if events:
            print("Connection to Google Calendar successful.")

    except Exception as e:
        print(f"Error verifying Google Calendar connection: {e}")
