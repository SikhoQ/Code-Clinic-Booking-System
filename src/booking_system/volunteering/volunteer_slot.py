from datetime import datetime, timedelta
from booking_system.calendars import calendar_utilities, slot_utilities
import pytz

CODE_CLINIC_CALENDAR = "code clinic"


def volunteer_for_slot(service, start_datetime, calendars, email):
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    calendar_info = calendar_data.get(CODE_CLINIC_CALENDAR, {})

    calendar_id = calendar_info.get("id")
    clinic_events = calendar_info.get("events")

    end_datetime = start_datetime + timedelta(minutes=30)

    start_datetime_str = start_datetime.isoformat()+'+02:00'
    end_datetime_str = end_datetime.isoformat()+'+02:00'
    if slot_utilities.is_slot_available(clinic_events, start_datetime, email, "volunteering"):
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
        (date, time_choice, email) = slot_utilities.get_booking_info()
        start_datetime = f"{date} {time_choice}"
        start_datetime_str = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M")
        volunteer_for_slot(service, start_datetime_str, calendars, email)

    except Exception:
        raise


