import booking_system.calendars.calendar_utilities as calendar_utilities
import booking_system.calendars.slot_utilities as slot_utilities
from datetime import datetime, timedelta
import pytz


CODE_CLINIC_CALENDAR = "code clinic"


def book_slot(service, start_datetime, calendars, email):
    calendar_data = calendar_utilities.read_calendar_data(calendars)

    # Change these to use .get
    calendar_id = calendar_data[CODE_CLINIC_CALENDAR]["id"]
    clinic_events = calendar_data[CODE_CLINIC_CALENDAR]["events"]

    # Assuming start_time is in Africa/Johannesburg timezone
    start_time_sast = datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S')
    start_time_sast = pytz.timezone('Africa/Johannesburg').localize(start_time_sast)

    event = dict()
    event_id = str()
    for each_event in clinic_events:
        event_start_time = each_event.get("start").get("dateTime")
        event_start_time_utc = datetime.strptime(event_start_time, '%Y-%m-%dT%H:%M:%S%z')  # Parse event start time with timezone
        event_start_time_utc = event_start_time_utc.replace(tzinfo=pytz.utc)  # Make it aware of UTC timezone
        event_start_time_sast = event_start_time_utc.astimezone(pytz.timezone('Africa/Johannesburg'))  # Convert to SAST

        if event_start_time_sast == start_time_sast:
            event_id = each_event.get("id")
            event = each_event
            break

    if slot_utilities.is_slot_available(clinic_events, start_datetime, email, "volunteering"):
        event["attendees"] = [{"email": email}]
        event = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()


def do_booking(service, calendars):
    try:
        (date, time_choice, volunteer_email) = slot_utilities.get_booking_info()
        start_datetime = f"{date} {time_choice}"
        start_datetime_str = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M")
        book_slot(service, start_datetime, calendars, volunteer_email)

    except Exception:
        raise
