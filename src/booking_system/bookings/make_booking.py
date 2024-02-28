import booking_system.calendars.calendar_utilities as calendar_utilities
import booking_system.calendars.slot_utilities as slot_utilities
from datetime import datetime, timedelta
import pytz


CODE_CLINIC_CALENDAR = "code clinic"


def book_slot(service, date, time, calendars, email):
    calendar_data = calendar_utilities.read_calendar_data(calendars)

    # change these to use .get
    calendar_id = calendar_data[CODE_CLINIC_CALENDAR]["id"]

    start_time = f"{date}T{time}:00"
    # start_time = start_time.astimezone(pytz.timezone('Africa/Johannesburg'))

    event = dict()
    event_id = str()
    for each_event in calendar_data.get(CODE_CLINIC_CALENDAR).get("events", []):
        event_start_time = each_event.get("start").get("dateTime")
        event_start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)
        print(f"event start time: {event_start_time}***\n***\n\nstart time: {start_time}")
        input("events")
        if each_event.get("start").get("dateTime") == start_time:
            event_id = each_event.get("id")
            event = each_event
            break

    event["attendees"] = [{"email": email}]
    # print(event)
    # input("PAUSED")

    event = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
    print(event)


def do_booking(service, calendars):
    try:
        (date, time_choice, volunteer_email) = slot_utilities.get_booking_info()
        book_slot(service, date, time_choice, calendars, volunteer_email)

    except Exception:
        raise
