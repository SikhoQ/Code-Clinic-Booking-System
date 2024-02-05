import config
import calendar
import json
import os.path


TOKEN_PATH = os.path.expanduser("~/.google_calendar_token.json")
CREDS_PATH = os.path.expanduser("~/.google_calendar_credentials.json")
CONFIG_FILE_PATH = "~/.coding_clinics_config.json"

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def print_welcome():
    print("Welcome to the Coding Clinic Booking System!")


def configure_system():
    credentials, service = calendar.authorize_google_calendar(SCOPES, CREDS_PATH, TOKEN_PATH)

    # TODO: get info for fields in config.json from api module

    clinic_calendar = calendar.create_coding_clinic_calendar(service)

    client_id = credentials["installed"]["client_id"]
    client_secret = credentials["installed"]["client_secret"]
    clinic_calendar_id = clinic_calendar["id"]
    print(clinic_calendar_id)
    input()

    # Save the updated configuration
    config.write_config(config_data, CONFIG_FILE_PATH)
    print("Configuration updated successfully.")


def first_run_setup():
    # Check if configuration file exists
    try:
        config_data = config.read_config(CONFIG_FILE_PATH)
        print("Configuration already exists. No setup needed.")
    except FileNotFoundError:
        print("Starting configuration...")
        configure_system()


def load_client_credentials():
    with open(CREDS_PATH, "r") as credentials_file:
        credentials_data = json.load(credentials_file)
        client_id = credentials_data["installed"]["client_id"]
        client_secret = credentials_data["installed"]["client_secret"]
    return client_id, client_secret


def main():
    print_welcome()
    first_run_setup()


if __name__ == "__main__":
    main()
