# TODO: CONFIG VERIFICATION
# Verifying that the tool is configured correctly involves checking various aspects of the configuration to ensure that the required settings are present and accurate. Here are some general steps you can take to verify the configuration of your tool:

# Configuration File Check:
#   Ensure that the configuration file (where you store your settings, e.g., ~/.booking_system_config.json) exists in the specified location.

# Configuration Parameters:
#   Verify that all the necessary configuration parameters are present in the configuration file. This may include information such as API keys, calendar IDs, user emails, etc., depending on your specific tool's requirements.

# Configuration Values:
#   Check that the values of the configuration parameters are accurate and up-to-date. For example, if your tool connects to a Google Calendar, ensure that the calendar ID is valid and corresponds to the desired calendar.

# Authentication:
#   If your tool involves authentication with external services (e.g., Google Calendar API), verify that the authentication tokens or credentials stored in the configuration are valid.

# Connection to External Services:
#   Test the connection to external services using the configured settings. For instance, if your tool connects to Google Calendar, attempt to retrieve some calendar data to ensure that the connection is established.

# Error Handling:
#   Implement proper error handling in your tool to provide meaningful error messages in case of configuration issues. This helps users understand what might be wrong with the configuration.

# Logging:
#   Integrate logging into your tool to capture relevant information during the configuration process. Log messages can provide insights into whether the tool is encountering any issues during configuration.

# Configuration Validation:
#   Implement a validation mechanism within your tool that checks the correctness of the configuration settings. This can include checking the format of email addresses, verifying the existence of required files or directories, etc.

# User Feedback:
#   If your tool has a user interface or command-line interface, provide clear feedback to users about the configuration status. Inform users if the configuration is successful or if there are issues that need attention.

# Documentation:
#   Ensure that your tool's documentation includes clear instructions on how to configure the system. This documentation should guide users through the configuration process, explaining each parameter and providing examples.


import json
import os
import requests

CONFIG_FILE_PATH = os.path.expanduser("~/.booking_system_config.json")


def read_config():
    config = {}
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as file:
            config = json.load(file)
    return config


def write_config(config):
    with open(CONFIG_FILE_PATH, 'w') as file:
        json.dump(config, file, indent=2)


def invalid_email(user_email):
    return "023@student.wethinkcode.co.za" in user_email


def verify_config(config):
    if not config['clinic_calendar_id']:
        return False, "Configuration failed. Invalid Clinic Calendar ID."
    if invalid_email(config['user_email']):
        return False, "Configuration failed. Invalid user email."

    print("Checking connection to Google Calendar..")
    response = requests.get("https://calendar.google.com")

    if response.status_code == 200:
        return True, """Connection to Google Calendar successful.
"Configuration completed successfully."""

    # TODO: do something about failed connection
    return False, "Connection to Google Calendar failed."


def print_welcome_message(config):
    message_1 = "Welcome to the Coding Clinic Booking System Configuration."
    message_2 = """You do not appear to have a config file defined,\
 so let me ask you some questions""" if config else ''

    print(message_1 + message_2)


def get_user_input():
    user_email = input("Enter your WeThinkCode_ email: ").lower()
    clinic_cal_id = input("Enter Coding Clinic Google Calendar ID: ").lower()

    return user_email, clinic_cal_id


def update_config_file(config, user_email, clinic_calendar_id):
    config['user_email'] = user_email
    config['clinic_calendar_id'] = clinic_calendar_id

    return config


def configure_system():
    # TODO: add more functionality:
    # set up the initial environment,
    # connect to external services,
    # ensure app has required settings.

    config = read_config()

    print_welcome_message(config)

    # Get user input for configuration settings
    user_email, clinic_calendar_id = get_user_input()

    # Update the configuration
    config = update_config_file(config, user_email, clinic_calendar_id)

    # Additional configuration settings can be added based on project's needs

    # Verify the updated configuration -> validate input, check cal connection
    config_successful, config_message = verify_config(config)

    # Write the updated configuration to the file
    if config_successful:
        write_config(config)

    print(config_message)


if __name__ == "__main__":
    configure_system()
