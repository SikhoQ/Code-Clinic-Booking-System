import time
import json
import os
import sys
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
import booking_system.calendars.calendar_utilities as calendar_utilities

TOKEN_FILE = os.path.expanduser("~/.google_calendar_token.json")
CONFIG_FILE = os.path.expanduser("~/.coding_clinic_config.json")
CREDS_FILE = os.path.expanduser("~/.google_calendar_credentials.json")
CALENDAR_FILE = os.path.expanduser("src/booking_system/data/calendar_data.json")


def print_config_message():
    """
    Prints a message indicating the absence of a config file and prompts the user for input.
    """
    print("You do not appear to have a config file defined, so let me ask you some questions\n")


def write_config(config_data):
    """
    Writes configuration data to the config file.

    Args:
        config_data (dict): Configuration data to be written to the file."""

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=2)


def get_student_info(): 
    """
    Prompts the user to enter student information.

    Returns:
        tuple: A tuple containing first name, last name, campus, and student email.
    """
    first_name = inquirer.text(
        message="First name:",
        validate=EmptyInputValidator("Name should not be empty")
        ).execute()
    last_name = inquirer.text(
        message="Last name:",
        validate=EmptyInputValidator("Last name should not be empty")
        ).execute()
    campus = inquirer.select(
        message="Select your campus:",
        choices=["CPT", "DBN", "JHB"]
        ).execute()
    student_email = inquirer.text(
        message="username:",
        validate=EmptyInputValidator("Username should not be empty")
        ).execute()

    student_email += "@student.wethinkcode.co.za"

    return (first_name, last_name, campus, student_email)


def do_configuration():
    """Performs the initial configuration.
    """
    print("Starting configuration...\n")
    time.sleep(2)
    try:
        with open(CREDS_FILE, 'r') as creds_file:
            file_data = json.load(creds_file)
            client_id = file_data["installed"]["client_id"]
            client_secret = file_data["installed"]["client_secret"]
    except FileNotFoundError:
        print("Error: Google Calendar API credentials not found.\nQuitting...")
        sys.exit()

    first_name, last_name, campus, student_email = get_student_info()

    config_data = {
        "student_info": {
            "first_name": first_name.title(),
            "last_name": last_name.title(),
            "campus": campus,
            "student_email": student_email
        },

        "google_calendar_api": {
            "credentials": {
                "client_id": client_id,
                "client_secret": client_secret,
                "token_file": TOKEN_FILE
                }
            }
    }

    write_config(config_data)
    print("Configuration completed.\n")


def first_run_setup():
    """Performs the setup for the first run of the application.
    """
    print_config_message()
    do_configuration()
