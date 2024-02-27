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


def is_slot_available(clinic_events, start_time, email, slot_type):
    end_time = start_time + timedelta(minutes=30)

    for event in clinic_events:
        event_start = event.get("start", {}).get("dateTime")
        event_end = event.get("end", {}).get("dateTime")

        if event_start and event_end:
            event_start = datetime.fromisoformat(event_start)
            event_end = datetime.fromisoformat(event_end)

            print(f"start time: {start_time}, event start {event_start}\nend time: {end_time} event end {event_end}")

            # Check if there's an overlap in time
            if start_time < event_end and end_time > event_start:
                if slot_type == "booking":
                    # Check if the event is a volunteer slot and not booked by the same volunteer
                    if event.get("description", "").lower() == "volunteer slot" and email != event.get("creator", {}).get("email"):
                        print("Slot available for booking")
                        return True
                elif slot_type == "volunteering":
                    # Check if the same volunteer has already volunteered for this slot
                    if email == event.get("creator", {}).get("email"):
                        print("You have already volunteered for this slot")
                        return False
                    else:
                        print("Slot is not available for volunteering")
                        return False

    print("Slot is available for volunteering")
    return True
