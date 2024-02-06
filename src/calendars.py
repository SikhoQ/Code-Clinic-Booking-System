# src/calendar.py

import datetime
import os
import json

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request


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


def download_calendar_data(start_date, end_date):
    # Implement code to fetch calendar data using Google Calendar API
    pass


def display_calendar_data(data):
    # Implement code to display calendar data on the command line
    pass


def update_local_data_file(file_path, new_data):
    # Implement code to update the local data file with new data
    pass


def create_coding_clinic_calendar(service):
    # Check if the calendar already exists
    try:
        clinic_calendar = service.calendarList().get(calendarId="Coding Clinic").execute()
        print("Coding Clinic Calendar already exists.")
        return clinic_calendar
    except HttpError as e:
        if e.resp.status == 404:
            print("Coding Clinic Calendar not found. Creating...\n")
        else:
            raise

    # Create the calendar
    calendar = {
        "summary": "Coding Clinic"
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    print("Coding Clinic Calendar created.")
    return created_calendar


def verify_google_calendar_connection(service):
    try:
        print("Verifying connection to Google Calendar...\n")
        calendar = service.calendars().get(calendarId='primary').execute()
        print("Connection to Google Calendar successful")
        return True

    except HttpError as error:
        print(f"Error connecting to Google Calendar: {error}")
        return False
