from InquirerPy import inquirer
from InquirerPy.validator import *
from datetime import datetime, timedelta
import src.booking_system.calendars.calendar_utilities as calendar_utilities

        
def validate_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_booking_info(): 

    time = datetime.now()
    # print(time)validate_date

    end_time = time.replace(hour=17, minute=00, second=0, microsecond=0)

    interval = timedelta(minutes=30)

    if time.minute % 30 != 0:
        time += interval - timedelta(minutes=time.minute % 30)

    choices = []

    while time < end_time:
        choices.append(time.strftime("%H:%M:%S"))
        time += interval

    username = inquirer.text(
        message = f"Username:",
        validate=EmptyInputValidator,
        invalid_message="Invalid date format. Please use YYYY-MM-DD."
    ).execute()

    date = inquirer.text(
        message = "Date (YYYY-MM-DD):",
        validate=validate_date,
        invalid_message="Invalid date format. Please use YYYY-MM-DD."
    ).execute()

    time_choice = inquirer.select(
        message="Time:",
        choices=choices
    ).execute()
    
    return (date, time_choice, username+"@student.wethinkcode.co.za")

    
    



def book_slot(calendars,service):
    # TODO: Check if the slot is available
    #       Create event for booking
    #       Insert the event into the user's calendar
    #       Update local data file with the booking information (leave this out for now)
    
    (date, time_choice, email) = get_booking_info()

    calendar_data = calendar_utilities.read_calendar_data(calendars)

    calendar_id = calendar_data["cohort 2023"]["id"]
    
    start_time = f"{date}T{time_choice}+02:00"

    event = dict()
    for each_event in calendar_data.get("cohort 2023").get("events"):
        if each_event.get("start").get("dateTime") == start_time:
            event_id = each_event.get("id")
            event = each_event
            break

    event["attendees"] = email

    service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()


def update_local_data_file(date, time, event_id, description):
    # Implement logic to update the local data file with booking information


    pass


def main():
    pass


# if __name__ == "__main__":
#     # main()
#     book_slot()
    