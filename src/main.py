import json
import os.path
import configuration
import calendars
import calendar_api

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
    # If no config file found, assume 1st run
    if not os.path.exists(CONFIG_FILE):
        configuration.first_run_setup()

    credentials, service = calendar_api.authorise_google_calendar(SCOPES,
                                                                  CREDS_FILE,
                                                                  TOKEN_FILE)
    try:
        clinic_calendar = calendars.create_coding_clinic_calendar(service)
    except Exception as e:
        print(f"An error was encountered while creating calendar\n{e}")

    connection_successful = calendars.verify_calendar_connection(service)

    if not connection_successful:
        print("Connection to Google Calendar failed. Please try again.")


if __name__ == "__main__":
    main()
