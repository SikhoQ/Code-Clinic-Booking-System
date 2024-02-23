import os.path
import json
from datetime import datetime, timedelta  # Added import for datetime
import booking_system.calendars.slot_utilities as slot_utils
import booking_system.calendars.calendar_utilities as calendar_utilities

CALENDAR_FILE = os.path.expanduser("src/calendars/calendar_data.json")


def update_local_volunteer_data(date, time, event_id):
    # this will use the write func in cal_utils
    pass


# for volunteering, to check if a slot is available use the data file to iterate through events
# event = cal_data["calendar name"]["events"]
# event["start"]["dateTime"]


def volunteer_for_slot(service, date, time, calendars):
    """    # Check if the slot is available
            # Only check code clinic calendar in data file
    """

    # if not slot_utils.is_slot_available(service, date, time):
    #     print("Slot not available. Please choose another slot.")
    #     return


    # Create event for volunteering

    calendar_data = calendar_utilities.read_calendar_data(calendars)

    calendar_id = calendar_data["code clinic"]["id"]

    start_time = f"{date}T{time}+02:00"
    end_time = (datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z') + timedelta(minutes=30)).isoformat()

    event = {
        'summary': 'Volunteering',
        'start': {'dateTime': start_time},
        'end': {'dateTime': end_time},
    }

    try:
        # Insert the event into the volunteer's personal Google Calendar
        event = service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()

        print(f"Volunteering successful. Event ID: {event['id']}")

        # Update local data file for the volunteer

        # update_local_volunteer_data(date, time, event['id'])

    except Exception as e:
        print(f"Error volunteering for slot: {e}")







# when a user volunteers, they need to supply date (full) - the volunteer's username will be extracted
# from login info - when tool is run, mainloop will determine program's lifetime, afterwhich login is required
# this will be through username input, checked against config file (if found), if user not found, prompt to register
        
