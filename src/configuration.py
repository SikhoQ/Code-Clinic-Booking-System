"""Configuration Setup:

Initialize and set up the configuration files.
This might involve creating default configuration files if they don't exist or prompting the user to input initial configuration details.
OAuth 2.0 Authorization Flow:

If your tool interacts with Google Calendar API or any other external service that requires OAuth 2.0 authentication, the first run might involve initiating the OAuth 2.0 authorization flow.
This includes obtaining the necessary client ID, client secret, and API key.
User Consent:

If OAuth 2.0 is used, the user might need to grant consent for the tool to access their Google Calendar or other data.
This typically involves opening a browser window where the user logs in and provides consent.
Token Retrieval and Storage:

After the user grants consent, the tool needs to retrieve the access and refresh tokens and store them securely for future use.
This often involves saving the tokens to a token file.
Initial Data Setup:

If your tool relies on specific data or files, create or initialize them.
For example, if your tool uses a local database, tables might need to be created.
Provide Welcome Message or Instructions:

Display a welcome message or instructions to guide the user on how to use the tool."""

import json
import os


def read_config(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError


def write_config(config_data, file_path):
    with open(file_path, 'w') as f:
        json.dump(config_data, f, indent=2)
