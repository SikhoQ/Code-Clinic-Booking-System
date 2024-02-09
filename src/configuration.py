import json
import os

TOKEN_FILE = os.path.expanduser("~/.google_calendar_token.json")
CONFIG_FILE = os.path.expanduser("~/.coding_clinic_config.json")



def load_config():
    try:
        with open('config/config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Configuration file not found.")
        return None

def save_config(config):
    with open('config/config.json', 'w') as f:
        json.dump(config, f, indent=2)




def read_config(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError


def write_config(config_data, file_path):
    with open(file_path, 'w') as f:
        json.dump(config_data, f, indent=2)


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
                "token_file": TOKEN_FILE
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
    write_config(config_data, CONFIG_FILE)
    print("Configuration updated successfully.")




###############################################################
###############################################################


import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def load_config():
    try:
        with open('config/config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Configuration file not found.")
        return None

def save_config(config):
    with open('config/config.json', 'w') as f:
        json.dump(config, f, indent=2)

def configure_system():
    # Load existing configuration
    config = load_config() or {}

    # Google Calendar API setup
    flow = InstalledAppFlow.from_client_secrets_file(
        'path/to/client_secret.json',  # Path to your client_secret.json file
        ['https://www.googleapis.com/auth/calendar']
    )

    credentials = flow.run_local_server(port=0)
    config['google_calendar_api_key'] = credentials.token
    config['google_calendar_id'] = 'primary'  # Assuming the clinic calendar is added to the user's primary calendar

    # Save configuration
    save_config(config)
    print("Configuration completed successfully.")

if __name__ == "__main__":
    configure_system()
