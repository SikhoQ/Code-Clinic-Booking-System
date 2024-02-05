import json
import os.path
import configuration
import calendars


TOKEN_FILE_PATH = os.path.expanduser("~/.google_calendar_token.json")
CREDS_FILE_PATH = os.path.expanduser("~/.google_calendar_credentials.json")
CONFIG_FILE_PATH = os.path.expanduser("~/.coding_clinics_config.json")

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def print_welcome():
    print("Welcome to the Coding Clinic Booking System!")


def configure_system(credentials, clinic_calendar):
    client_id = credentials.client_id
    client_secret = credentials.client_secret
    clinic_calendar_id = clinic_calendar["id"]

    config_data = {
        "google_calendar": {
            "credentials": {
                "client_id": client_id,
                "client_secret": client_secret,
                "token_file": TOKEN_FILE_PATH
            },
            "coding_clinic_calendar_id": clinic_calendar_id
        }
    }

    # Save the updated configuration
    configuration.write_config(config_data, CONFIG_FILE_PATH)
    print("Configuration updated successfully.")


def first_run_setup(credentials, clinic_calendar):
    # Check if configuration file exists
    try:
        config_data = configuration.read_config(CONFIG_FILE_PATH)
        print("Configuration already exists. No setup needed.")
    except FileNotFoundError:
        print("Starting configuration...")
        configure_system(credentials, clinic_calendar)


def load_client_credentials():
    with open(CREDS_FILE_PATH, "r") as credentials_file:
        credentials_data = json.load(credentials_file)
        client_id = credentials_data["installed"]["client_id"]
        client_secret = credentials_data["installed"]["client_secret"]
    return client_id, client_secret


def main():
    credentials, service = calendars.authorize_google_calendar(SCOPES, CREDS_FILE_PATH, TOKEN_FILE_PATH)
    clinic_calendar = calendars.create_coding_clinic_calendar(service)

    print_welcome()
    first_run_setup(credentials, clinic_calendar)


if __name__ == "__main__":
    main()
