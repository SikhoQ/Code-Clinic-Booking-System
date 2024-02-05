# src/calendar.py

import datetime
import os
import json

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def authorize_google_calendar(scopes, credentials_file, token_file):
    credentials = None

    # Check if token file exists and contains valid credentials
    if os.path.exists(token_file):
        credentials = json.loads(open(token_file, 'r').read())

    # If there are no (valid) credentials available, let the user log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            # REPLACE WITH FOLLOWING after taking values for config file
            # token.write(credentials.to_json())
            token.write(json.dumps({
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'id_token': credentials.id_token,
                'scopes': credentials.scopes,
                'expiry': credentials.expiry.strftime("%Y-%m-%d %H:%M:%S")
            }, indent=2))

    service = build('calendar', 'v3', credentials=credentials)

    return credentials, service


def download_calendar_data(api_key, calendar_id, start_date, end_date):
    # Implement code to fetch calendar data using Google Calendar API
    pass


def display_calendar_data(data):
    # Implement code to display calendar data on the command line
    pass


def update_local_data_file(file_path, new_data):
    # Implement code to update the local data file with new data
    pass


def create_coding_clinic_calendar(service):
    calendar = {
        "summary": "Coding Clinics"
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    print(f'Coding Clinics Calendar created: {created_calendar["id"]}')

    return created_calendar
