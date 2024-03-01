from googleapiclient.errors import HttpError
import booking_system.calendars.calendar_utilities as calendar_utilities


def verify_calendar_connection(service, calendars):
    user_calendars = calendar_utilities.read_calendar_data(calendars)

    try:
        for user_calendar in user_calendars:
            print(f"Verifying connection to {user_calendar.title()} Calendar...")
            calendar = service.calendars().get(calendarId=user_calendars[user_calendar]["id"]).execute()
            print("Connection verification successful\n")
        return True

    except HttpError as e:
        print(f"Error connecting to Google Calendar: {e}\n")
        return False
