import datetime
import json
from googleapiclient.errors import HttpError


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
    clinic_calendar = service.calendarList().list().execute()

    # Check if the calendar already exists
    try:
        calendars = service.calendarList().list().execute()
        for calendar in calendars['items']:
            if calendar['summary'] == "Coding Clinic":
                print("Coding Clinic Calendar already exists.")
                return calendar
        print("Coding Clinic Calendar not found. Creating...\n")
    except HttpError as e:
        if e.resp.status == 404:
            print("Coding Clinic Calendar not found. Creating...\n")
        else:
            # re-raise caught exception if its status code is not 404.
            raise

    # Create the calendar
    calendar = {
        "summary": "Coding Clinic",
        "description": "Calendar for Coding Clinics volunteering and bookings"
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    print("Coding Clinic Calendar created.")
    return created_calendar


def verify_calendar_connection(service):
    try:
        print("Verifying connection to Google Calendar...\n")
        calendar = service.calendars().get(calendarId='primary').execute()
        print("Connection to Google Calendar successful")
        return True

    except HttpError as error:
        print(f"Error connecting to Google Calendar: {error}")
        return False
