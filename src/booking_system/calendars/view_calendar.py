from datetime import datetime, timedelta
import booking_system.calendars.calendar_utilities as calendar_utilities
import os
from prettytable import PrettyTable
import calendar


TOKEN_FILE = os.path.expanduser("~/.google_calendar_token.json")
CONFIG_FILE = os.path.expanduser("~/.coding_clinic_config.json")
CREDS_FILE = os.path.expanduser("~/.google_calendar_credentials.json")
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def format_data(event):
    start_time = datetime.fromisoformat(event['start']['dateTime']).strftime('%H:%M')
    end_time = datetime.fromisoformat(event['end']['dateTime']).strftime('%H:%M')
    date = datetime.fromisoformat(event['start']['dateTime'])
    summary = event['summary']
    return [summary, start_time, end_time, date]


def view_calendar(calendars):

    table = PrettyTable()
    table.field_names = ['Day', 'Date', 'Summary', 'Duration']

    slots = []
    calendar_data = calendar_utilities.read_calendar_data(calendars)["cohort 2023"]["events"]
    today = datetime.now()
    
    for event in calendar_data:
        
        formatted = format_data(event)
        
        slots.append(today.isoformat() + 'Z')
        today += timedelta(days=1)
        date = formatted[3]
        day = calendar.day_name[date.weekday()]
        table.add_row([day, date.strftime("%d-%m-%Y"), formatted[0], f'{formatted[1]} - {formatted[2]}'])
        table.align["Day"] = "l"

        
    print(table)

    return slots


if __name__ == '__main__':
    view_calendar()
    