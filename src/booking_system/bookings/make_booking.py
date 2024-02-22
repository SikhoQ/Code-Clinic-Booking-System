from InquirerPy import inquirer
from InquirerPy.validator import *
from datetime import datetime, timedelta
# import src.booking_system.calendars.calendar_utilities as calendar_utilities
        
def validate_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_booking_info(): 

    time = datetime.now()
    print(time)

    end_time = time.replace(hour=20, minute=00, second=0, microsecond=0)

    interval = timedelta(minutes=30)

    if time.minute % 30 != 0:
        time += interval - timedelta(minutes=time.minute % 30)

    choices = []

    while time < end_time:
        choices.append(time.strftime("%H:%M"))
        time += interval

    date = inquirer.text(
        message = "Date (YYYY-MM-DD):",
        validate=validate_date,
        invalid_message="Invalid date format. Please use YYYY-MM-DD."
    ).execute()

    time_choice = inquirer.select(
        message="Time:",
        choices=choices
    ).execute()
    
    return [date, time_choice]

    
    



def book_slot(calendars,service, date, time, description):
    # TODO: Check if the slot is available
    #       Create event for booking
    #       Insert the event into the user's calendar
    #       Update local data file with the booking information (leave this out for now)
    calendar_info = calendar_utilities.calendar_data(calendars)

    # Assuming you have information like calendar_id, event_id, etc. in the returned dictionary
    calendar_id = calendar_info.get('calendar_id')
    event_id = calendar_info.get('event_id')

    # Retrieve the existing event
    try:
        existing_event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    except Exception as e:
        print(f'Error retrieving existing event: {e}')
        return

    # Add new attendees to the existing event
    if 'attendees' not in existing_event:
        existing_event['attendees'] = []

        existing_event['attendees'].extend(new_attendees)

    # Update the event in the user's calendar
    try:
        updated_event = service.events().update(calendarId=calendar_id, eventId=event_id, body=existing_event).execute()
        print(f'Event updated with new attendees: {updated_event.get("htmlLink")}')
    except Exception as e:
        print(f'Error updating event: {e}')



def update_local_data_file(date, time, event_id, description):
    # Implement logic to update the local data file with booking information


    pass


def main():
    pass


if __name__ == "__main__":
    # main()
    get_booking_info()