import booking_system.calendars.calendar_utilities as calendar_utilities
import booking_system.calendars.slot_utilities as slot_utilities

CODE_CLINIC_CALENDAR = "code clinic"


def book_slot(service, date, time, calendars, email):
    calendar_data = calendar_utilities.read_calendar_data(calendars)

    # change these to use .get
    calendar_id = calendar_data[CODE_CLINIC_CALENDAR]["id"]

    start_time = f"{date}T{time}:00Z"

    event = dict()
    event_id = str()
    for each_event in calendar_data.get(CODE_CLINIC_CALENDAR).get("events", []):
        print(each_event.get("start").get("dateTime"), start_time, sep="***\n***\n\n")
        input("events")
        if each_event.get("start").get("dateTime") == start_time:
            event_id = each_event.get("id")
            event = each_event
            break

    event["attendees"] = [{"email": email}]
    print(event)
    input("PAUSED")

    event = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
    print(event)


def do_booking(service, calendars):
    try:
        (date, time_choice, volunteer_email) = slot_utilities.get_booking_info()
        book_slot(service, date, time_choice, calendars, volunteer_email)

    except Exception:
        raise
