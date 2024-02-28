from datetime import datetime, timedelta
from booking_system.calendars import calendar_utilities, slot_utilities
import pytz

CODE_CLINIC_CALENDAR = "code clinic"


def volunteer_for_slot(service, date, start_datetime, calendars, volunteer_email):
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    calendar_info = calendar_data.get(CODE_CLINIC_CALENDAR, {})

    calendar_id = calendar_info.get("id")
    clinic_events = calendar_info.get("events")

    end_datetime = start_datetime + timedelta(minutes=30)

    start_datetime_str = start_datetime.isoformat()
    end_datetime_str = end_datetime.isoformat()

    if slot_utilities.is_slot_available(clinic_events, start_datetime, volunteer_email, "volunteering"):
        event = {
            'summary': 'Code Clinic',
            'description': 'Volunteer Slot',
            'start': {'dateTime': start_datetime_str, 'timeZone': 'Africa/Johannesburg'},
            'end': {'dateTime': end_datetime_str, 'timeZone': 'Africa/Johannesburg'}
        }

        try:
            event = service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()

            calendar_utilities.update_calendar_data_file(service, calendars)
            print(f"Volunteering successful. Event ID: {event['id']}")

        except Exception:
            raise


def do_volunteering(service, calendars):
    try:
        (date, time_choice, volunteer_email) = slot_utilities.get_booking_info()
        start_datetime = f"{date} {time_choice}"
        start_datetime_str = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M")
        volunteer_for_slot(service, date, start_datetime_str, calendars, volunteer_email)

    except Exception:
        raise


# when tool is run, mainloop will determine program's lifetime, afterwhich login is required
# this will be through username input, checked against config file (if found), if user not found, prompt to register
