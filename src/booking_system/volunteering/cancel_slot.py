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


def find_existing_event(clinic_events, date, time_choice):
    start_time = f"{date}T{time_choice}:00"
    start_time_sast = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
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
                return event_id, event

    return event_id, event


def cancel_volunteering(service, calendars):
    (date, time_choice, email) = slot_utilities.get_booking_info()
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    clinic_events = calendar_data["code clinic"]["events"]
    calendar_id = calendar_data["code clinic"]["id"]

    event_id, existing_event = find_existing_event(clinic_events, date, time_choice)

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
