import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def volunteer_for_slot(service, date, time):
    # Create event for volunteering
    start_time = f"{date}T{time}:00:00Z"
    end_time = (datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z') + timedelta(minutes=30)).isoformat()

    event = {
        'summary': 'Volunteering',
        'start': {'dateTime': start_time, 'timeZone': 'UTC'},
        'end': {'dateTime': end_time, 'timeZone': 'UTC'},
    }

    try:
        # Insert the event into the volunteer's personal Google Calendar
        event = service.events().insert(
            calendarId='primary',  # Change to your calendar ID if not using the primary calendar
            body=event
        ).execute()

        print(f"Volunteering successful. Event ID: {event['id']}")

        # Update local data file for the volunteer
        update_local_volunteer_data(date, time, event['id'])

    except Exception as e:
        print(f"Error volunteering for slot: {e}")

def update_local_volunteer_data(date, time, event_id):
    # Implement logic to update the local volunteer data file
    # This could involve modifying a JSON file or another storage mechanism
    pass  # Replace with actual logic

def main():
    config = load_config()

    if not config or 'google_calendar_api_key' not in config:
        print("Configuration incomplete. Run the configuration tool first.")
        return

    credentials = Credentials.from_authorized_user_info(
        config['google_calendar_api_key'],
        scopes=['https://www.googleapis.com/auth/calendar']
    )

    service = build('calendar', 'v3', credentials=credentials)

    # Replace '2024-02-01', '09:00:00' with the desired date and time for volunteering
    volunteer_for_slot(service, '2024-02-01', '09:00:00')

if __name__ == "__main__":
    main()
