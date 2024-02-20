import json
import os.path
from datetime import datetime
import configure.configuration as configuration
import calendars.calendar_interface as calendar_interface
import calendars.calendar_api as api
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
    service = api.authorise_google_calendar(SCOPES,
                                            CREDS_FILE,
                                            TOKEN_FILE)

    if not os.path.exists(CONFIG_FILE):
        configuration.first_run_setup(service)

    try:
        clinic_calendar = calendar_interface.create_coding_clinic_calendar(service)
        # add calendar id to calendar data file
        with open("src/calendars/calendar_data.json", 'w') as file_handle:
            data = {
                "calendar_id": clinic_calendar["id"] 
            }
            json.dump(data, file_handle, indent=2)
    except Exception as e:
        print(f"An error was encountered while creating calendar\n{e}")
        try_again = inquirer.confirm(message="\nTry again?").execute()
        if try_again:
            main()


if __name__ == "__main__":
    main()
