import sys
import json
import os.path
import configure.configuration as configuration
import booking_system.calendars.calendar_interface as calendar_interface
import booking_system.calendars.calendar_api as api
from InquirerPy import inquirer

TOKEN_FILE = os.path.expanduser("~/.google_calendar_token.json")
CONFIG_FILE = os.path.expanduser("~/.coding_clinic_config.json")
CREDS_FILE = os.path.expanduser("~/.google_calendar_credentials.json")
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def load_client_credentials():
    with open(CREDS_FILE, "r") as credentials_file:
        credentials_data = json.load(credentials_file)
        client_id = credentials_data.client_id
        client_secret = credentials_data.client_secret
    return client_id, client_secret


def main():
    if not os.path.exists(CONFIG_FILE):
        print("\nWelcome to the Coding Clinic Booking System")

        # google calendar authentication and authorisation
        service = api.authorise_google_calendar(SCOPES,
                                                CREDS_FILE,
                                                TOKEN_FILE)

    # creating the Coding Clinic calendar
    try:
        clinic_calendar = calendar_interface.create_coding_clinic_calendar(service)
        # after this step, somewhere, calendar id's should be stored to data file
    except Exception as e:
        print(f"An error was encountered while creating calendar\n{e}")
        try_again = inquirer.confirm(message="\nTry again?").execute()

        if try_again:
            main()
        else:
            sys.exit()

    # first run config step
    if not os.path.exists(CONFIG_FILE):
        configuration.first_run_setup(service)

    calendar_interface.create_calendar_data_file_template(service)

    # after config step, update the calendar data file (data dates checked inside func def)
    calendar_interface.update_calendar_data_file(service)


if __name__ == "__main__":
    main()
