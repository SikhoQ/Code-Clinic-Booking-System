import json
import os
import sys
from InquirerPy import inquirer

TOKEN_FILE = os.path.expanduser("~/.google_calendar_token.json")
CONFIG_FILE = os.path.expanduser("~/.coding_clinic_config.json")
CREDS_FILE = os.path.expanduser("~/.google_calendar_credentials.json")


def print_welcome():
    print("\nWelcome to the Coding Clinic Booking System")
    print("You do not appear to have a config file defined, so let me ask you some questions\n")


def read_config(CONFIG_FILE):
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError


def write_config(config_data, CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=2)


def get_student_info():
    first_name = inquirer.text(message="First name: ").execute()
    last_name = inquirer.text(message="Last name: ").execute()
    campus = inquirer.select(message="Select your campus:",
                             choices=["CPT", "DBN", "JHB"]).execute()
    student_email = inquirer.text(message="username: ").execute()

    return (first_name, last_name, campus, student_email)


def do_configuration():
    try:
        with open(CREDS_FILE, 'r') as creds_file:
            file_data = json.load(creds_file)
            client_id = file_data["installed"]["client_id"]
            client_secret = file_data["installed"]["client_secret"]
    except FileNotFoundError:
        print("Google Calendar API credentials not found. Please run authorisation flow.")

    first_name, last_name, campus, student_email = get_student_info()


def first_run_setup():
    print_welcome()

    do_configuration()

    config_data = {
        "student_info": {
            "first_name": first_name.title(),
            "last_name": last_name.title(),
            "campus": campus,
            "student_email": student_email
        }
    }

    write_config(config_data, CONFIG_FILE)


def main():
    pass


if __name__ == "__main__":
    main()
























# "google_calendar": {
#             "credentials": {
#                 "client_id": client_id,
#                 "client_secret": client_secret,
#                 "token_file": TOKEN_FILE
#             }
#         }