from datetime import datetime, timedelta
import json
import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import *
from InquirerPy import inquirer

CALENDAR_FILE = os.path.expanduser("src/booking_system/data/calendar_data.json")


def download_calendars(service):
    print("Downloading calendars...\n")
    try:
        calendars = service.calendarList().list().execute()
        return calendars.get('items', [])
    except Exception as e:
        print(f"Error downloading calendars: {e}")
        try_again = inquirer.confirm(message="\nTry again?").execute()

        if try_again:
            return download_calendars(service)
        else:
            sys.exit()


def read_calendar_data():
    try:
        # Load the local calendar data
        with open(CALENDAR_FILE, "r") as file:
            calendar_data = json.load(file)

        return calendar_data

    except FileNotFoundError:
        create_calendar_data_file_template()

        return read_calendar_data()


def write_calendar_data(calendar_data):
    with open(CALENDAR_FILE, 'w') as file:
        json.dump(calendar_data, file, indent=2)


def get_calendar_info(calendars):
    # Extract calendar IDs based on calendar summary (name)
    clinic_calendar = None
    primary_calendar = None
    cohort_calendar = None

    for calendar in calendars:
        summary = calendar.get("summary", '').lower()

        if calendar.get("primary", False):
            primary_calendar = calendar

        elif 'coding clinic' in summary:
            clinic_calendar = calendar

        elif 'cohort 2023' in summary:
            cohort_calendar = calendar

    return cohort_calendar, clinic_calendar, primary_calendar


def create_calendar_data_file_template(calendars):
    # use calendars to get id's
    # use id's from data file when checking if data is outdated

    cohort_calendar, clinic_calendar, primary_calendar = get_calendar_info(calendars)

    template = {
        "primary": {
            "etag": primary_calendar["etag"],
            "events": [],
            "id": primary_calendar["id"]
        },
        "code clinic": {
            "etag": clinic_calendar["etag"],
            "events": [],
            "id": clinic_calendar["id"]
        },
        "cohort 2023": {
            "etag": cohort_calendar["etag"],
            "events": [],
            "id": cohort_calendar["id"]
        }
    }

    write_calendar_data(template)


def is_calendar_data_outdated(calendar_data, server_data):
    # Use the etag to check if the data is outdated, from all 3 calendars
    # needs calendar id's to get server etags for all calendars and compare

    keys = ["primary", "code clinic", "cohort 2023"]
    # use list to shorten
    local_etags = {
        "primary": calendar_data["primary"]["etag"],
        "cohort 2023": calendar_data["cohort 2023"]["etag"],
        "code clinic": calendar_data["code clinic"]["etag"]
    }

    server_etags = {
        "primary": server_data["primary"]["etag"],
        "cohort 2023": server_data["cohort 2023"]["etag"],
        "code clinic": server_data["code clinic"]["etag"]
    }

    for key in keys:
        if local_etags[key] != server_etags[key]:
            return True

    return False


def get_server_data(service, days=7):
    # days could be redundant
    calendar_data = read_calendar_data()
    calendar_ids = {
        "primary": calendar_data["primary"]["id"],
        "code clinic": calendar_data["code clinic"]["id"],
        "cohort 2023": calendar_data["cohort 2023"]["id"]
    }

    server_data = dict()

    now = datetime.utcnow()
    end_date = now + timedelta(days=days)

    for key in calendar_ids:
        # catch possible exception here
        server_data[key] = service.events().list(
            calendarId=calendar_ids[key],
            timeMin=now.isoformat() + 'Z',
            timeMax=end_date.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

    return server_data


def update_calendar_data_file(service):
    # output to user that this is happening
    # ouput should be before API requests -> get_server_data

    calendar_data = read_calendar_data()
    server_data = get_server_data(service)

    if is_calendar_data_outdated(calendar_data, server_data):
        new_data = {
            "primary": {
                "etag": server_data["primary"]["etag"],
                "events": server_data["primary"]["items"]
                "id": 
            },
            "code clinic": {
                "etag": server_data["code clinic"]["etag"],
                "events": server_data["code clinic"]["items"]
            },
            "cohort 2023": {
                "etag": server_data["cohort 2023"]["etag"],
                "events": server_data["cohort 2023"]["items"]
            }
        }

        write_calendar_data(new_data)


def create_coding_clinic_calendar(service):
    try:
        calendars = download_calendars(service)
        for calendar in calendars:
            if calendar['summary'] == "Coding Clinic":
                return calendars

    except Exception as e:
        print(f"There was an error while connecting to Google Calendar: {e}\n")
        if inquirer.confirm(message="Try again?\n"):
            return create_coding_clinic_calendar(service)
        else:
            sys.exit("Quitting...")

    print("Coding Clinic Calendar not found. Creating...\n")

    calendar = {
        "summary": "Coding Clinic",
        "description": "Calendar for Coding Clinic volunteering and bookings"
    }

    service.calendars().insert(body=calendar).execute()

    input("Coding Clinic Calendar created. Press any key to continue")

    # after creating calendars, call this func again to return updated calendar list
    return create_coding_clinic_calendar(service)
