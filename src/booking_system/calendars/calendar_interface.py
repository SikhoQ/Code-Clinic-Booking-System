import json
import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import *
from InquirerPy import inquirer

CALENDAR_FILE = os.path.expanduser("src/booking_system/data/calendar_data.json")


def download_calendars(service):
    try:
        calendars = service.calendarList().list().execute()
        return calendars.get('items', [])
    except Exception as e:
        print(f"Error downloading calendars: {e}")
        try_again = inquirer.confirm(message="\nTry again?").execute()

        if try_again:
            download_calendars(service)
        else:
            sys.exit()


def get_calendar_ids(calendars):
    # Extract calendar IDs based on calendar summary (name)
    clinic_calendar_id = None
    primary_calendar_id = None

    for calendar in calendars:
        summary = calendar.get('summary', '').lower()

        if 'coding clinic' in summary:
            clinic_calendar_id = calendar['id']
        elif 'primary' in summary:
            primary_calendar_id = calendar['id']

    return clinic_calendar_id, primary_calendar_id


def create_calendar_data_file_template(service):
    calendars = download_calendars(service)

    clinic_calendar_id, primary_calendar_id = get_calendar_ids(calendars)

    template = {
        "etag": None,
        "primary": {
            "events": [],
            "calendar_id": primary_calendar_id
        },
        "code clinic": {
            "events": [],
            "calendar_id": clinic_calendar_id
        }
    }

    with open(CALENDAR_FILE, "w") as file:
        json.dump(template, file, indent=2)


def is_calendar_data_outdated(service):
    # Use the etag to check if the data is outdated, from all 3 calendars

    calendar_id = 'your_calendar_id'
    service = build('calendar', 'v3', credentials=get_credentials())

    try:
        calendar = service.calendars().get(calendarId=calendar_id).execute()
        server_etag = calendar.get('etag', '')

        return etag != server_etag

    except Exception as e:
        # return True whether or not outdated if check fails
        print(f"Error checking etag: {e}")
        return True


def update_calendar_data_file(service):
    if is_calendar_data_outdated(service):
        calendar_data = download_calendars(service)

        with open(CALENDAR_FILE, 'w') as file:
            json.dump(calendar_data, file, indent=2)


def read_calendar_data(service):
    try:
        # Load the local calendar data
        with open(CALENDAR_FILE, "r") as file:
            calendar_data = json.load(file)

        return calendar_data

    except FileNotFoundError:
        update_calendar_data_file(service)
        read_calendar_data(service)


def create_coding_clinic_calendar(service):
    try:
        calendars = service.calendarList().list().execute()
        for calendar in calendars['items']:
            if calendar['summary'] == "Coding Clinic":
                return calendar
        print("Coding Clinic Calendar not found. Creating...\n")
    except HttpError as e:
        if e.resp.status == 404:
            print("Coding Clinic Calendar not found. Creating...\n")
        else:
            print("Error connecting to Google Calendar.\n\nQuitting...")
            sys.exit()

    calendar = {
        "summary": "Coding Clinic",
        "description": "Calendar for Coding Clinics volunteering and bookings"
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    print("Coding Clinic Calendar created.")
    return created_calendar
