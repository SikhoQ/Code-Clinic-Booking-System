from datetime import datetime, timedelta
import booking_system.calendars.calendar_utilities as calendar_utilities
from InquirerPy import inquirer
import booking_system.calendars.slot_utilities as slot_utilities
import pytz


def cancel_volunteering(service, calendars):
    (date, time_choice, email) = slot_utilities.get_booking_info()
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    clinic_events = calendar_data["code clinic"]["events"]
    calendar_id = calendar_data["code clinic"]["id"]

    event_id, existing_event = slot_utilities.find_existing_event(clinic_events, date, time_choice)

    if existing_event and slot_utilities.is_volunteer_slot(existing_event):
        try:
            service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            print("Volunteering cancellation successful!\n")

            calendar_utilities.update_calendar_data_file(service, calendars)
        except Exception:
            raise

        else:

            print("Cannot cancel a slot already booked by a student.")

    else:

        print("No volunteering slot found for cancellation.")
