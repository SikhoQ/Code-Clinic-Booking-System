from datetime import datetime, timedelta
from booking_system.calendars import calendar_utilities, slot_utilities

CODE_CLINIC_CALENDAR = "code clinic"


def volunteer_for_slot(service, date, time, calendars, volunteer_email):
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    calendar_info = calendar_data.get(CODE_CLINIC_CALENDAR, {})

    calendar_id = calendar_info.get("id")
    clinic_events = calendar_info.get("events")

    start_time = f"{date}T{time}:00Z"

    start_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
    end_datetime = start_datetime + timedelta(minutes=30)

    start_datetime_str = start_datetime.isoformat()
    end_datetime_str = end_datetime.isoformat()

    print(start_datetime, end_datetime, sep="***\n***\n\n")
    input("eventss")

    if slot_utilities.is_slot_available(clinic_events, start_datetime, volunteer_email, "volunteering"):
        event = {
            'summary': 'Code Clinic',
            'description': 'Volunteer Slot',
            'start': {'dateTime': start_datetime_str, 'timeZone': 'Africa/Johannesburg'},
            'end': {'dateTime': end_datetime_str, 'timeZone': 'Africa/Johannesburg'},
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
    try:
        (date, time_choice, volunteer_email) = slot_utilities.get_booking_info()
        volunteer_for_slot(service, date, time_choice, calendars, volunteer_email)

    except Exception:
        raise


# when tool is run, mainloop will determine program's lifetime, afterwhich login is required
# this will be through username input, checked against config file (if found), if user not found, prompt to register
