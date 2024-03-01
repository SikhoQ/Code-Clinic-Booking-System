from datetime import datetime, timedelta
import booking_system.calendars.calendar_utilities as calendar_utilities
from InquirerPy import inquirer
import booking_system.calendars.slot_utilities as slot_utilities
import pytz


def is_volunteer_slot(event):

    return event.get("description", "").lower() == "volunteer slot"


def is_booked_slot(existing_event):

    # Check if the slot is already booked by a student

    if existing_event.get("attendees", []):
        return True

    return False


def cancel_volunteering(service, calendars):
    (date, time_choice, email) = slot_utilities.get_booking_info()
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    clinic_events = calendar_data["code clinic"]["events"]
    calendar_id = calendar_data["code clinic"]["id"]

    event_id, existing_event = slot_utilities.find_existing_event(clinic_events, date, time_choice)

    if existing_event and is_volunteer_slot(existing_event):

        if not is_booked_slot(existing_event):

            # Cancel the volunteering slot

            # service.events().delete(calendarId=calendar_id, eventId=event_id).execute() # calendar_id
            try:
                service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
                print("Volunteering cancellation successful!\n")
                # Update local data file
                calendar_utilities.update_calendar_data_file(service, calendars)
            except Exception:
                raise

        else:

            print("Cannot cancel a slot already booked by a student.")

    else:

        print("No volunteering slot found for cancellation.")
