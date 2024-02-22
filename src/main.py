import sys
import json
import os.path
import configure.configuration as configuration
import booking_system.calendars.calendar_utilities as calendar_utilities
import booking_system.calendars.view_calendar as view_calendar
import booking_system.calendars.calendar_api as api
from InquirerPy import inquirer

TOKEN_FILE = os.path.expanduser("~/.google_calendar_token.json")
CONFIG_FILE = os.path.expanduser("~/.coding_clinic_config.json")
CREDS_FILE = os.path.expanduser("~/.google_calendar_credentials.json")
CALENDAR_FILE = os.path.expanduser("src/booking_system/data/calendar_data.json")


def load_client_credentials():
    with open(CREDS_FILE, "r") as credentials_file:
        credentials_data = json.load(credentials_file)
        client_id = credentials_data.client_id
        client_secret = credentials_data.client_secret
    return client_id, client_secret


def print_welcome():
    print("\nWelcome to the Coding Clinic Booking System\n")


def main():
    if not os.path.exists(CONFIG_FILE):
        print_welcome()

    # google calendar authentication and authorisation
    service = api.authorise_google_calendar()

    # creating the Coding Clinic calendar
    try:
        calendars = calendar_utilities.create_coding_clinic_calendar(service)

    except Exception as e:
        print(f"An error was encountered while creating calendar: {e}")
        try_again = inquirer.confirm(message="\nTry again?").execute()

        if try_again:
            main()
        else:
            sys.exit("Quitting...")

    # first run config step
    if not os.path.exists(CONFIG_FILE):
        configuration.first_run_setup(service, calendars)

    # assume file can only be created by program; fix later on
    # (can also be created manually with wrong format)
    try:
        calendar_utilities.read_calendar_data(calendars)
    except FileNotFoundError:
        calendar_utilities.create_calendar_data_file_template(calendars)

    # after config step, update the calendar data file (data dates checked inside func def)
    calendar_utilities.update_calendar_data_file(service, calendars)

    view_calendar.calender_layout(calendars)


if __name__ == "__main__":
    main()
