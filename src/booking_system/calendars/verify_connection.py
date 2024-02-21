from googleapiclient.errors import HttpError


def verify_calendar_connection(service):
    try:
        print("Verifying connection to Google Calendar...\n")
        calendar = service.calendars().get(calendarId='primary').execute()
        print("Connection to Google Calendar successful")
        return True

    except HttpError as e:
        print(f"Error connecting to Google Calendar: {e}")
        return False
