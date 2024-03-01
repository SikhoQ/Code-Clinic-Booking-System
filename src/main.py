# HANDLE ALL EXCEPTIONS IN MAIN LOOP

# when tool is run, mainloop will determine program's lifetime, afterwhich login is required
# this will be through username input, checked against config file (if found), if user not found, prompt to register
import sys
import json
import os.path
import booking_system.volunteering.volunteer_slot as volunteer_slot
import booking_system.volunteering.cancel_slot as cancel_slot
import configure.configuration as configuration
import booking_system.calendars.calendar_utilities as calendar_utilities
import booking_system.calendars.verify_connection as verify_connection
import booking_system.calendars.view_calendar as view_calendar
import booking_system.calendars.calendar_api as api
from InquirerPy import inquirer
from InquirerPy.separator import Separator
import booking_system.bookings.make_booking as make_booking
import booking_system.bookings.cancel_booking as cancel_booking
import time

TOKEN_FILE = os.path.expanduser("~/.google_calendar_token.json")
CONFIG_FILE = os.path.expanduser("~/.coding_clinic_config.json")
CREDS_FILE = os.path.expanduser("~/.google_calendar_credentials.json")
CALENDAR_FILE = os.path.expanduser("src/booking_system/data/calendar_data.json")


def load_client_credentials():
    """
    Loads client credentials from the credentials file.

    Returns:
        tuple: A tuple containing client ID and client secret."""
    
    with open(CREDS_FILE, "r") as credentials_file:
        credentials_data = json.load(credentials_file)
        client_id = credentials_data.client_id
        client_secret = credentials_data.client_secret
    return client_id, client_secret


def print_welcome():
    """
    Prints a welcome message for the Coding Clinic Booking System."""

    print("\nWelcome to the Coding Clinic Booking System\n")
    time.sleep(2)
    os.system("clear")


def usage():
    pass


def menu_selection():
    menu = inquirer.select(
        message="Select",
        choices=['configure system', 'verify configuration',
                 Separator(),
                 'view calendar',
                 Separator(),
                 'volunteer', 'cancel volunteer slot',
                 Separator(),
                 'book session',
                 'cancel booking',
                 Separator(),
                 'help', 'quit',]
    ).execute()

    return (menu)


def main():
    """
    The main function for running the Code Clinics Booking System.
    """
    if not os.path.exists(CONFIG_FILE):
        print_welcome()

    # google calendar authentication and authorisation
    service = api.authorise_google_calendar()

    # creating the Coding Clinic calendar
    try:
        calendars = calendar_utilities.create_coding_clinic_calendar(service)

    except Exception as e:
        print(f"An error was encountered while creating calendar: {e}")
        try_again = inquirer.confirm(message="\nTry again?").execute()

        if try_again:
            main()
        else:
            sys.exit("Quitting...")

    # first run config step
    if not os.path.exists(CONFIG_FILE):
        configuration.first_run_setup()

    # assume file can only be created by program; fix later on
    # (can also be created manually with wrong format)
    try:
        calendar_utilities.read_calendar_data(calendars)
    except FileNotFoundError:
        calendar_utilities.create_calendar_data_file_template(calendars)

    calendar_utilities.update_calendar_data_file(service, calendars)

    (menu) = menu_selection()

    while True:
        if menu == 'configure system':
            configuration.do_configuration()

        elif menu == 'verify configuration':
            connection = verify_connection.verify_calendar_connection(service, calendars)
            while not connection:
                if inquirer.confirm(message="Retry?"):
                    connection = verify_connection.verify_calendar_connection(service, calendars)
                else:
                    sys.exit("Quitting...")

        elif menu == 'view calendar':
            print("Downloading calendars...\n")
            view_calendar.calendar_layout(calendars)

        elif menu == 'volunteer':
            try:
                volunteer_slot.do_volunteering(service, calendars)
            except Exception as e:
                print(f"Error encountered: {e}\n")
                if inquirer.confirm(message="Retry?"):
                    volunteer_slot.do_volunteering(service, calendars)

        elif menu == 'book session':
            try:
                make_booking.do_booking(service, calendars)
            except Exception as e:
                print(f"Error encountered: {e}\n")
                if inquirer.confirm(message="Retry?"):
                    volunteer_slot.do_volunteering(service, calendars)

        elif menu == 'help':
            pass
            usage()

        elif menu == 'cancel booking':
            try:
                cancel_booking.cancel_booking(service, calendars)
            except Exception as e:
                print(f"Error encountered: {e}\n")
                if inquirer.confirm(message="Retry?"):
                    volunteer_slot.do_volunteering(service, calendars)

        elif menu == 'cancel volunteer slot':
            try:
                cancel_slot.cancel_volunteering(service, calendars)
            except Exception as e:
                print(f"Error encountered: {e}\n")
                if inquirer.confirm(message="Retry?"):
                    volunteer_slot.do_volunteering(service, calendars)

        elif menu == 'quit':
            try_again = inquirer.confirm(message="\nAre you sure?").execute()

            if try_again:

                sys.exit("Quitting...")
            else:
                main()
        main()


if __name__ == "__main__":
    main()
