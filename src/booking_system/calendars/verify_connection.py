import booking_system.calendars.calendar_utilities as calendar_utilities
import time
import os


def verify_calendar_connection(service, calendars):
    user_calendars = calendar_utilities.read_calendar_data(calendars)

    try:
        for user_calendar in user_calendars:
            print(f"Verifying connection to {user_calendar.title()} Calendar...")
            calendar = service.calendars().get(calendarId=user_calendars[user_calendar]["id"]).execute()
            print("Connection verification successful\n")
            time.sleep(2)
            os.system("clear")
        return True

    except Exception as e:
        print(f"Error connecting to Google Calendar: {e}\n")
        return False
