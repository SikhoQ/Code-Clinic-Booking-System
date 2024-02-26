import booking_system.calendars.calendar_utilities as calendar_utilities
from datetime import timedelta, datetime
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator


def validate_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_booking_info():

    time = datetime.now()
    # print(time)validate_date

    end_time = time.replace(hour=20, minute=00, second=0, microsecond=0)

    interval = timedelta(minutes=30)

    if time.minute % 30 != 0:
        time += interval - timedelta(minutes=time.minute % 30)

    choices = []

    while time < end_time:
        choices.append(time.strftime("%H:%M"))
        time += interval

    username = inquirer.text(
        message="Username:",
        validate=EmptyInputValidator,
        invalid_message="Invalid date format. Please use YYYY-MM-DD."
    ).execute()

    date = inquirer.text(
        message="Date (YYYY-MM-DD):",
        validate=validate_date,
        invalid_message="Invalid date format. Please use YYYY-MM-DD."
    ).execute()

    time_choice = inquirer.select(
        message="Time:",
        choices=choices
    ).execute()

    return (date, time_choice, username+"@student.wethinkcode.co.za")


def is_available_to_volunteer(clinic_events, start_time, end_time):
    for event in clinic_events:
        event_start = event["start"]
        event_end = event["end"]
        if start_time >= event_start and start_time < event_end:
            # Slot is already booked for volunteer
            return False
    # Slot is available for volunteering
    return True


def is_available_to_book(clinic_events, start_time, end_time):
    for event in clinic_events:
        event_start = event["start"]["dateTime"]
        event_end = event["end"]["dateTime"]
        if start_time >= event_start and start_time < event_end:
            if event["description"].lower() == "volunteer":
                # Slot is booked by a volunteer
                return False
            else:
                # Slot is already booked for a non-volunteer event
                return False
    # Slot is available for booking
    return True


def is_slot_available(calendars, start_time, end_time, slot_type):
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    clinic_events = calendar_data["code clinic"]["events"]

    if slot_type == "booking":
        return is_available_to_book(clinic_events, start_time, end_time)
    elif slot_type == "volunteer":
        return is_available_to_volunteer(clinic_events, start_time, end_time)
    else:
        raise ValueError("Invalid slot_type. Use 'booking' or 'volunteer'.")
