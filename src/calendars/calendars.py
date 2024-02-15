import json
from InquirerPy import inquirer
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


def create_code_clinic_calendar(service):
    clinic_calendar = service.calendarList().list().execute()

    # Check if the calendar already exists
    try:
        calendars = service.calendarList().list().execute()
        for calendar in calendars['items']:
            if calendar['summary'] == "Code Clinic":
                return calendar
        # TODO: add blinking ellipses
        print("\n\nCode Clinic Calendar not found. Creating...\n")

    except HttpError as e:
        if e.resp.status == 404:
            # TODO: add blinking ellipses
            print("\n\nCode Clinic Calendar not found. Creating...\n")
        else:
            # re-raise caught exception if its status code is not 404.
            raise

    # Create the calendar
    calendar = {
        "summary": "Code Clinic",
        "description": "Calendar for Code Clinic bookings"
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    print("Code Clinic Calendar created.")
    return created_calendar
