from datetime import datetime, timedelta
import json
import os
import sys
from InquirerPy import inquirer
import pytz
import time

CALENDAR_FILE = os.path.expanduser("src/booking_system/data/calendar_data.json")
CONFIG_FILE = os.path.expanduser("~/.coding_clinic_config.json")


def download_calendars(service):
    # print("Downloading calendars...\n")
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


def read_calendar_data(calendars):
    try:
        # Load the local calendar data
        with open(CALENDAR_FILE, "r") as file:
            calendar_data = json.load(file)

        return calendar_data

    except FileNotFoundError:
        create_calendar_data_file_template()
        return read_calendar_data(calendars)


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


def create_calendar_data_file_template():
    # use calendars to get id's
    # use id's from data file when checking if data is outdated

    template = {
        "primary": {
            "etag": "~",
            "events": [],
            "id": "~"

        },
        "code clinic": {
            "etag": "~",
            "events": [],
            "id": "~"
        },
        "cohort 2023": {
            "etag": "~",
            "events": [],
            "id": "~"
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
    if len(local_etags) != len(server_etags):
        return True

    for key in keys:
        if local_etags[key] != server_etags[key]:
            return True

    return True


def get_email():
    with open(CONFIG_FILE, 'r') as file:
        config_data = json.load(file)

    email = config_data["student_info"]["student_email"]

    return email


def get_server_data(service, calendars, days=7):
    user_email = get_email()

    # need to change data file primary calendar key to general, rest remain same
    calendar_keys = {user_email: "primary", "Code Clinic": "code clinic",
                     "Cohort 2023": "cohort 2023"}
    calendar_data = dict()

    for calendar in calendars:
        if calendar["summary"] in calendar_keys:
            calendar_data[calendar_keys[calendar["summary"]]] = calendar

    calendar_ids = {
        "primary": calendar_data["primary"]["id"],
        "code clinic": calendar_data["code clinic"]["id"],
        "cohort 2023": calendar_data["cohort 2023"]["id"]
    }

    server_data = dict()

    # Get the current UTC time
    now = datetime.utcnow()

    # Get the timezone object for South Africa Standard Time (SAST)
    sast_tz = pytz.timezone('Africa/Johannesburg')

    now = now.replace(tzinfo=pytz.utc).astimezone(sast_tz)

    end_date = now + timedelta(days=days - 1)

    # Convert UTC time to the calendar time zone
    formatted_now = now.isoformat()
    formatted_end_date = end_date.isoformat()

    for key in calendar_ids:
        try:
            server_data[key] = service.events().list(
                calendarId=calendar_ids[key],
                timeMin=formatted_now,
                timeMax=formatted_end_date,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
        except Exception:
            raise
    return server_data, calendar_ids


def update_calendar_data_file(service, calendars):
    # "UPDATE FUNCTIONALITY WORKS BUT OUTDATED CHECK DOESN'T"
    calendar_data = read_calendar_data(calendars)
    try:
        print("Getting server data...\n")
        server_data, calendar_ids = get_server_data(service, calendars)
        os.system("clear")
    except Exception:
        if inquirer.confirm(message="An error was encountered, try again?").execute():
            os.system("clear")
            update_calendar_data_file(service, calendars)
        else:
            sys.exit("Quitting...")

    if is_calendar_data_outdated(calendar_data, server_data):
        print("Updating Calendar Data...\n")
        time.sleep(2)
        new_data = {
            "primary": {
                "etag": server_data["primary"]["etag"],
                "events": server_data["primary"]["items"],
                "id": calendar_ids["primary"]
            },
            "code clinic": {
                "etag": server_data["code clinic"]["etag"],
                "events": server_data["code clinic"]["items"],
                "id": calendar_ids["code clinic"]
            },
            "cohort 2023": {
                "etag": server_data["cohort 2023"]["etag"],
                "events": server_data["cohort 2023"]["items"],
                "id": calendar_ids["cohort 2023"]
            }
        }

        write_calendar_data(new_data)

        os.system("clear")

        print("Calendar Data Updated.\n")

    else:
        print("Calendar Data is up to date.\n")

    time.sleep(2)
    os.system("clear")


def create_coding_clinic_calendar(service):
    try:
        calendars = download_calendars(service)
        for calendar in calendars:
            if calendar['summary'] == "Code Clinic":
                return calendars

    except Exception as e:
        print(f"There was an error while connecting to Google Calendar: {e}\n")
        if inquirer.confirm(message="Try again?\n").execute():
            return create_coding_clinic_calendar(service)
        else:
            sys.exit("Quitting...")

    print("Coding Clinic Calendar not found. Creating...\n")

    calendar = {
        "summary": "Code Clinic",
        "description": "Calendar for Coding Clinic volunteering and bookings"
    }

    service.calendars().insert(body=calendar).execute()

    os.system("clear")

    input("Coding Clinic Calendar created. Press any key to continue")

    os.system("clear")

    # after creating calendars, call this func again to return updated calendar list
    return create_coding_clinic_calendar(service)
