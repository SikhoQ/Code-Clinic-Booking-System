import booking_system.calendars.calendar_utilities as calendar_utilities
from prettytable import PrettyTable 
import booking_system.calendars.slot_utilities as slot_utilities
from InquirerPy import inquirer


CODE_CLINIC_CALENDAR = "code clinic"
PRIMARY_CALENDAR = "primary"


def cancel_booking(service, calendars):
    """Cancels a booking.

    Args:
        service: The Google Calendar service object.
        calendars (dict): Dictionary containing calendar data.
        """

    (date, time_choice, email) = slot_utilities.get_booking_info()
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    clinic_events = calendar_data[CODE_CLINIC_CALENDAR]["events"]

    clinic_id = calendar_data[CODE_CLINIC_CALENDAR]["id"]
    primary_id = calendar_data[PRIMARY_CALENDAR]["id"]

    id_list = [clinic_id, primary_id]

    event_id, existing_event = slot_utilities.find_existing_event(clinic_events, date, time_choice)

    if existing_event and slot_utilities.is_booked_slot(existing_event):
        for calendar_id in id_list:
            try:
                del existing_event["attendees"]
                existing_event["description"] = "Volunteer Slot"
                existing_event = service.events().update(calendarId=calendar_id, eventId=event_id, body=existing_event).execute()
                print("Booking cancellation successful!\n")
                calendar_utilities.update_calendar_data_file(service, calendars)
            except Exception:
                raise
    else:
        if not existing_event:
            print("No volunteer slot for given time.", end=" ")
        else:
            print("No booking found for volunteer slot.")
        if inquirer.confirm(message="Select another slot?"):
            cancel_booking(service, calendars)