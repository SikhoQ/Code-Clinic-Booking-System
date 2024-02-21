import os.path
import json
from datetime import datetime, timedelta  # Added import for datetime
import src.calendars.calendar_data as calendar_data

CALENDAR_FILE = os.path.expanduser("src/calendars/calendar_data.json")


def update_local_volunteer_data(date, time, event_id):
    # Implement logic to update the local volunteer data file
    # This could involve modifying a JSON file or another storage mechanism
    pass  # Replace with actual logic


def volunteer_for_slot(service, date, time):
    # Check if the slot is available
    if not calendar_data.is_slot_available(service, date, time):
        print("Slot not available. Please choose another slot.")
        return

    # Create event for volunteering
    start_time = f"{date}T{time}:00:00Z"
    end_time = (datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z') + timedelta(minutes=30)).isoformat()

    # Check if the volunteer is already booked for this slot
    if not calendar_data.is_slot_available(service, date, time):
        print("Volunteer is already booked for this slot. Please choose another slot.")
        return

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
