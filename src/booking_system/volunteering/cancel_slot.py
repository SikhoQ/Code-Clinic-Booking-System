from datetime import datetime, timedelta
import booking_system.calendars.calendar_utilities as calendar_utilities
from InquirerPy import inquirer


def validate_date(value):
    try:

        datetime.strptime(value, "%Y-%m-%d")

        return True

    except ValueError:

        return False


def get_cancellation_info():

    date = inquirer.text(
        message="Date (YYYY-MM-DD):",
        validate=validate_date,
        invalid_message="Invalid date format. Please use YYYY-MM-DD."
    ).execute()
    time_choice = inquirer.select(
        message="Time:",
        choices=choices #a list containing the available time slots for volunteering. 

    ).execute()
    return f"{date}T{time_choice}:00+02:00"


def cancel_volunteering(calendars, service):

    # Get cancellation information from the user

    cancellation_time = get_cancellation_info()
    calendar_data = calendar_utilities.read_calendar_data(calendars)

    clinic_events = calendar_data["code clinic"]["events"]

    # Find the event to cancel based on the provided time

    event_id, existing_event = find_existing_event(clinic_events, cancellation_time)



    if existing_event and is_volunteer_slot(existing_event):

        # Check if the slot is not already booked by a student

        if not is_booked_slot(clinic_events, cancellation_time):

            # Cancel the volunteering slot

            # service.events().delete(calendarId=calendar_id, eventId=event_id).execute() # calendar_id
            service.events().delete(calendarId=id, eventId=event_id).execute()

            print("Volunteering cancellation successful!")

            # Update local data file

            update_local_data_file(cancellation_time, event_id, "volunteer", "canceled")

        else:

            print("Cannot cancel a slot already booked by a student.")

    else:

        print("No volunteering slot found for cancellation.")



def is_volunteer_slot(event):

    return event.get("description", "").lower() == "volunteer"



def is_booked_slot(clinic_events, cancellation_time):

    # Check if the slot is already booked by a student

    for event in clinic_events:

        if event.get("start").get("dateTime") == cancellation_time:

            return True

    return False



def update_local_data_file(cancellation_time, event_id, event_type, status):

    # Implement logic to update the local data file with cancellation information

    pass