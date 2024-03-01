from datetime import datetime, timedelta
import booking_system.calendars.calendar_utilities as calendar_utilities
# from InquirerPy import inquirer
import booking_system.calendars.slot_utilities as slot_utilities
import pytz

CODE_CLINIC_CALENDAR = "code clinic"
PRIMARY_CALENDAR = "primary"

def is_volunteer_slot(event):
    """Check if the event is a volunteer slot.

    Args:
        event (dict): The event dictionary containing information about the event.

    Returns:
        bool: True if the event is a volunteer slot, False otherwise.
    """

    return event.get("description", "").lower() == "volunteer slot"


def is_booked_slot(existing_event):
    """Check if the slot is already booked by a student.

    Args:
        existing_event (dict): The existing event dictionary containing information about the event.

    Returns:
        bool: True if the slot is already booked by a student, False otherwise.
    """

    if existing_event.get("attendees", []):
        return True

    return False


def find_existing_event(clinic_events, date, time_choice):
    """Find an existing event matching the given date and time_choice.

    Args:
        clinic_events (list): List of events in the clinic calendar.
        date (str): Date of the event in 'YYYY-MM-DD' format.
        time_choice (str): Time of the event in 'HH:MM' format.

    Returns:
        tuple: A tuple containing event_id and event dictionary if found, otherwise empty values.
    """

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
    """Cancel a volunteering slot if it's not booked by a student.

    Args:
        service: The Google Calendar service object.
        calendars (dict): Dictionary containing calendar data.
    """
    (date, time_choice, email) = slot_utilities.get_booking_info()
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    clinic_events = calendar_data["code clinic"]["events"]

    clinic_id = calendar_data[CODE_CLINIC_CALENDAR]["id"]
    primary_id = calendar_data[PRIMARY_CALENDAR]["id"]

    id_list = [clinic_id, primary_id]

    event_id, existing_event = slot_utilities.find_existing_event(clinic_events, date, time_choice)

    if existing_event and is_volunteer_slot(existing_event):
        if not is_booked_slot(existing_event):
            # Cancel the volunteering slot
            # service.events().delete(calendarId=calendar_id, eventId=event_id).execute() # calendar_id
            for calendar_id in id_list:
                try:
                    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
                    # Update local data file
                    calendar_utilities.update_calendar_data_file(service, calendars)
                except Exception:
                    raise 
            print("Volunteering cancellation successful!\n")
        else:
            print("Cannot cancel a slot already booked by a student.")
    else:
        print("No volunteering slot found for cancellation.")
# fixes?
# canceling someone elses booking
# if len(email) == 1 and email[0].get("email") == email:
# service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
# current time is showing for upcoming days? for all events
# volonteer slot accepts mult bookings for the same time
# book session?
#summary ?