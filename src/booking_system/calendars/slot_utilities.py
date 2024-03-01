# import booking_system.calendars.calendar_utilities as calendar_utilities
from datetime import timedelta, datetime
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
# from main import main
import pytz


def validate_date(value):
    try:
        date = datetime.strptime(value, "%Y-%m-%d").date()
        today = datetime.today().date()

        # Check if entered date is today or in the next 7 days
        if today <= date <= today + timedelta(days=6):
            return True

    except ValueError:
        return False

    return False


def time_handler(date_str):
    choices = []

    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)  # Get current UTC time
    local_now = utc_now.astimezone(pytz.timezone('Africa/Johannesburg'))  # Convert to Johannesburg time zone

    start_time = local_now
    date = datetime.strptime(date_str, '%Y-%m-%d')  # Convert date string to datetime object

    if date.date() > utc_now.date():
        start_time = start_time.replace(hour=7, minute=30, second=0, microsecond=0)
    end_time = start_time.replace(hour=17, minute=30, second=0, microsecond=0)
    interval = timedelta(minutes=30)

    # if start_time.hour < 8 or start_time.hour >= 17:
    #     print("Closed!")

    #     book_next = inquirer.confirm(message="\nDo you wish to book a different date?").execute()

    #     if book_next:
    #         start_time = start_time.replace(hour=8, minute=0, second=0, microsecond=0)
    #         end_time = end_time.replace(hour=17, minute=0, second=0, microsecond=0)

    #     else:
    #         main()  # Returns to main if the user decides not to book

    if start_time.minute > 30:
        start_time = start_time.replace(hour=start_time.hour + 1, minute=0, second=0, microsecond=0)
    else:
        start_time = start_time.replace(minute=30, second=0, microsecond=0)

    while start_time < end_time:
        choices.append(start_time.strftime("%H:%M"))
        start_time += interval

    return choices


def get_booking_info():
    # TODO: change to general name

    username = inquirer.text(
        message="Username:",
        validate=EmptyInputValidator,
        invalid_message="Username cannot be empty"
    ).execute()

    date = inquirer.text(
        message="Date (YYYY-MM-DD):",
        validate=validate_date,
        invalid_message="Invalid date format or date is not within the next 7 days. Please use YYYY-MM-DD."
    ).execute()

    choices = time_handler(date)

    time_choice = inquirer.select(
        message="Time:",
        choices=choices
    ).execute()

    return (date, time_choice, username + "@student.wethinkcode.co.za")


def is_slot_available(clinic_events, start_time, email, slot_type):
    end_time = start_time + timedelta(minutes=30)

    # Convert start_time and end_time to the local time zone
    local_timezone = pytz.timezone('Africa/Johannesburg')
    start_time_local = start_time.astimezone(local_timezone)
    end_time_local = end_time.astimezone(local_timezone)

    for event in clinic_events:
        event_start = event.get("start", {}).get("dateTime")
        event_end = event.get("end", {}).get("dateTime")

        if event_start and event_end:
            event_start = datetime.fromisoformat(event_start)
            event_end = datetime.fromisoformat(event_end)

            # Convert event start and end times to the local time zone
            event_start_local = event_start.astimezone(local_timezone)
            event_end_local = event_end.astimezone(local_timezone)

            if start_time_local == event_start_local and end_time_local == event_end_local:
                if slot_type == "booking":
                    if event.get("description", "").lower() == "volunteer slot" and \
                            email != event.get("creator", "").get("email"):
                        print("Slot available for booking")
                        return True
                    else:
                        print("You cannot book a slot you have volunteered for")
                        return False
                elif slot_type == "volunteering":
                    if email == event.get("creator", "").get("email"):
                        print("You have already volunteered for this slot")
                        return False
                    else:
                        print("Slot is not available for volunteering")
                        return False

    print("Slot is available for volunteering")
    return True


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


def is_volunteer_slot(event):
    return event.get("description", "").lower() == "volunteer slot"


def is_booked_slot(existing_event):
    return existing_event.get("description", "").lower() == "booked slot"
