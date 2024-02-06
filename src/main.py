import json
import os.path
import configuration
import calendars


TOKEN_FILE_PATH = os.path.expanduser("~/.google_calendar_token.json")
CREDS_FILE_PATH = os.path.expanduser("~/.google_calendar_credentials.json")
CONFIG_FILE_PATH = os.path.expanduser("~/.coding_clinic_config.json")

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def print_welcome():
    print("\nWelcome to the Coding Clinic Booking System")
    input("Press [ENTER] to complete authorization\n")


def get_student_info():
    first_name = input("First name: ").title()
    last_name = input("Last name: ").title()
    campus = input("Campus [CPT/DBN/JHB]: ").upper()
    student_email = input("Email: ").lower()

    return (first_name, last_name, campus, student_email)


def configure_system(credentials, clinic_calendar):
    client_id = credentials.client_id
    client_secret = credentials.client_secret
    clinic_calendar_id = clinic_calendar["id"]

    first_name, last_name, campus, student_email = get_student_info()

    config_data = {
        "google_calendar": {
            "credentials": {
                "client_id": client_id,
                "client_secret": client_secret,
                "token_file": TOKEN_FILE_PATH
            },
            "coding_clinic_calendar_id": clinic_calendar_id
        },
        "student_info": {
            "first_name": first_name,
            "last_name": last_name,
            "campus": campus,
            "student_email": student_email
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
        print("Configuration file not found. Starting configuration...")
        configure_system(credentials, clinic_calendar)


def load_client_credentials():
    with open(CREDS_FILE_PATH, "r") as credentials_file:
        credentials_data = json.load(credentials_file)
        client_id = credentials_data.client_id
        client_secret = credentials_data.client_secret
    return client_id, client_secret


def main():
    print_welcome()

    credentials, service = calendars.authorize_google_calendar(SCOPES, CREDS_FILE_PATH, TOKEN_FILE_PATH)

    # TODO: properly handle exception in function below
    #       and change something about calendar creation,
    #       for when it already exists
    clinic_calendar = calendars.create_coding_clinic_calendar(service)

    connection_successful = calendars.verify_google_calendar_connection(service)

    if not connection_successful:
        print("Connection to Google Calendar failed. Please try again.")

    first_run_setup(credentials, clinic_calendar)


if __name__ == "__main__":
    main()

# TODO: download creds file from API
