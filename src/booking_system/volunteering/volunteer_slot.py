import os.path
from datetime import datetime, timedelta
import booking_system.calendars.slot_utilities as slot_utilities
import booking_system.calendars.calendar_utilities as calendar_utilities

CALENDAR_FILE = os.path.expanduser("src/calendars/calendar_data.json")


def volunteer_for_slot(service, date, time, calendars):
    """    # Check if the slot is available
            # Only check code clinic calendar in data file
    """

    calendar_data = calendar_utilities.read_calendar_data(calendars)

    calendar_id = calendar_data["code clinic"]["id"]

    start_time = f"{date}T{time}Z"
    end_time = (datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z') + timedelta(minutes=30)).isoformat()

    event = {
        'summary': 'Code Clinic',
        'description': 'Volunteer 2',
        'start': {'dateTime': start_time},
        'end': {'dateTime': end_time}
    }

    try:
        event = service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()

        print(f"Volunteering successful. Event ID: {event['id']}")

        calendar_utilities.update_calendar_data_file(service, calendars)

    except Exception:
        raise


def do_volunteering(service, calendars):
    (date, time_choice, email) = slot_utilities.get_booking_info()

    try:
        volunteer_for_slot(service, date, time_choice, calendars)

    except Exception:
        raise






# when a user volunteers, they need to supply date (full) - the volunteer's username will be extracted
# from login info - when tool is run, mainloop will determine program's lifetime, afterwhich login is required
# this will be through username input, checked against config file (if found), if user not found, prompt to register
        
