import os
import sys
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from datetime import *


def download_calendar_data(service, start_date, end_date):
    try:
        events = service.events().list(
            calendarId='primary',
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        for event in events['items']:
            print(event['summary'])

    except HttpError as e:
        print(f"An error occurred: {e}")


def display_calendar_data(data):
    """
    Display calendar data on the command line.
    Args:
        data: Calendar data to display.
    """
    if not data:
        print("No events to display.")
        return

    print("Calendar Events:")
    for event in data:
        print(f"- {event['summary']} ({event['start']['dateTime']})")

def update_local_data_file(file_path, new_data):
    """
    Update the local data file with new data.
    Args:
        file_path (str): Path to the local data file.
        new_data: New data to be added to the file.
    """
    try:
        with open(file_path, 'a') as file:
            for event in new_data:
                file.write(f"{event['summary']} ({event['start']['dateTime']})\n")
        print("Local data file updated successfully.")
    except Exception as e:
        print(f"An error occurred while updating the local data file: {e}")

def create_coding_clinic_calendar(service):
    clinic_calendar = service.calendarList().list().execute()

    try:
        calendars = service.calendarList().list().execute()
        for calendar in calendars['items']:
            if calendar['summary'] == "Coding Clinic":
                return calendar
        print("Coding Clinic Calendar not found. Creating...\n")
    except HttpError as e:
        if e.resp.status == 404:
            print("Coding Clinic Calendar not found. Creating...\n")
        else:
            print("Error connecting to Google Calendar.\n\nQuitting...")
            sys.exit()

    calendar = {
        "summary": "Coding Clinic",
        "description": "Calendar for Coding Clinics volunteering and bookings"
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    print("Coding Clinic Calendar created.")
    return created_calendar


# if __name__ == '__main__':
#     start_date = datetime(2024, 2, 13, 0, 0, 0)  
#     end_date = datetime(2024, 2, 14, 0, 0, 0)    

#     calendar_data = download_calendar_data(start_date, end_date)

#     display_calendar_data(calendar_data)

#     local_data_file_path = "path/to/your/local_data_file.txt"
#     update_local_data_file(local_data_file_path, calendar_data)