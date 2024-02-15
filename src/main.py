import json
import os.path
import configure.configuration as configuration
import calendars.calendars as calendars
import calendars.calendar_api as calendar_interface
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
        configuration.first_run_setup()

    service = calendar_interface.authorise_google_calendar(SCOPES,
                                                           CREDS_FILE,
                                                           TOKEN_FILE)
    try:
        calendars.create_code_clinic_calendar(service)
    except Exception as e:
        print(f"An error was encountered while creating calendar\n{e}")
        try_again = inquirer.confirm(message="\nTry again?").execute()
        if try_again:
            main()

    # TODO: Implement main loop logic here

    #     start_date = datetime(2024, 2, 13, 0, 0, 0)  
    #     end_date = datetime(2024, 2, 14, 0, 0, 0)    
    #     calendar_data = download_calendar_data(start_date, end_date)
    #     display_calendar_data(calendar_data)

if __name__ == "__main__":
    main()
