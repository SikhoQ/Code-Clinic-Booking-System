import booking_system.calendars.calendar_utilities as calendar_utilities
from datetime import timedelta, datetime
from InquirerPy import inquirer , validator
from InquirerPy.validator import EmptyInputValidator
from main import main
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

    

def time_handler():
    choices = []

    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)  # Get current UTC time
    local_now = utc_now.astimezone(pytz.timezone('Africa/Johannesburg'))  # Convert to Johannesburg time zone

    start_time = local_now
    end_time = start_time.replace(hour=17, minute=0, second=0, microsecond=0)
    interval = timedelta(minutes=30)

    if start_time.hour < 8 or start_time.hour >= 17:
        print("Closed!")

        book_next = inquirer.confirm(message="\nDo you wish to book a different date?").execute()

        if book_next:
            start_time = start_time.replace(hour=8, minute=0, second=0, microsecond=0)
            end_time = end_time.replace(hour=17, minute=0, second=0, microsecond=0)
            
        else:
            main()  # Returns to main if the user decides not to book

    if start_time.minute > 30:
        start_time = start_time.replace(minute=30, second=0, microsecond=0)
    else:
        start_time = start_time.replace(minute=0, second=0, microsecond=0)

    while start_time < end_time:
        choices.append(start_time.strftime("%H:%M"))
        start_time += interval

    return choices




def get_booking_info():
    choices = time_handler()

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

    time_choice = inquirer.select(
        message="Time:",
        choices=choices
    ).execute()


    return (date, time_choice, username + "@student.wethinkcode.co.za")


def is_slot_available(clinic_events, start_time, email, slot_type):
    end_time = start_time + timedelta(minutes=30)
    start_time = start_time.isoformat()+'+02:00'
    end_time = end_time.isoformat()+'+02:00'


    for event in clinic_events:
        event_start = event.get("start", {}).get("dateTime")
        event_end = event.get("end", {}).get("dateTime")

        if event_start and event_end:
          
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
