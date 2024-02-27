from datetime import datetime
import booking_system.calendars.calendar_utilities as calendar_utilities
import os
from prettytable import PrettyTable
import calendar
import pytz

TOKEN_FILE = os.path.expanduser("~/.google_calendar_token.json")
CONFIG_FILE = os.path.expanduser("~/.coding_clinic_config.json")
CREDS_FILE = os.path.expanduser("~/.google_calendar_credentials.json")
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def format_data(event):
    # Convert event times to South African Standard Time (SAST)
    start_time_utc = datetime.fromisoformat(event['start']['dateTime'])
    end_time_utc = datetime.fromisoformat(event['end']['dateTime'])

    sa_tz = pytz.timezone('Africa/Johannesburg')
    start_time_sast = start_time_utc.replace(tzinfo=pytz.utc).astimezone(sa_tz)
    end_time_sast = end_time_utc.replace(tzinfo=pytz.utc).astimezone(sa_tz)

    # Format times in SAST
    start_time = start_time_sast.strftime('%H:%M')
    end_time = end_time_sast.strftime('%H:%M')

    date = start_time_sast.strftime('%Y-%m-%d %H:%M:%S')

    summary = event['summary']
    return [summary, start_time, end_time, date]


def calendar_layout(calendars):
    table = PrettyTable()
    table.field_names = ['Day', 'Date', 'Summary', 'Duration']

    slots = []
    calendar_data = calendar_utilities.read_calendar_data(calendars)["code clinic"]["events"]

    for event in calendar_data:
        formatted = format_data(event)

        # Convert the 'date' string to a datetime object
        date = datetime.strptime(formatted[3], '%Y-%m-%d %H:%M:%S')

        day = calendar.day_name[date.weekday()]
        table.add_row([day, date.strftime("%d-%m-%Y"), formatted[0], f'{formatted[1]} - {formatted[2]}'])
        table.align["Day"] = "l"

    print(table)
    return slots
