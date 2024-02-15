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
        with open("data/clinic_calendar.json", 'w') as file_handle:
            data = {
                "calendar_id": clinic_calendar["id"] 
            }
            json.dump(data, file_handle, indent=2)
    except Exception as e:
        print(f"An error was encountered while creating calendar\n{e}")
        try_again = inquirer.confirm(message="\nTry again?").execute()
        if try_again:
            main()

    start_date = datetime(2024, 2, 14, 0, 0, 0)
    end_date = datetime(2024, 5, 16, 0, 0, 0)
    start_date = start_date.isoformat() + 'Z'
    end_date = end_date.isoformat() + 'Z'

    calendar_data = calendar_interface.download_calendar_data(service, start_date, end_date)
    calendar_interface.display_calendar_data(calendar_data)

if __name__ == "__main__":
    main()
