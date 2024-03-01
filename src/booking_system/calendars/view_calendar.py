from datetime import datetime, timedelta
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
    """
    Formats event data for display in South African Standard Time (SAST) .

    Args:
        event (dict): Event details.

    Returns:
        list: Formatted event data.

    """
    
    start_time_utc = datetime.fromisoformat(event['start']['dateTime'])
    end_time_utc = datetime.fromisoformat(event['end']['dateTime'])

    sa_tz = pytz.timezone('Africa/Johannesburg')
    start_time_sast = start_time_utc.replace(tzinfo=pytz.utc).astimezone(sa_tz)
    end_time_sast = end_time_utc.replace(tzinfo=pytz.utc).astimezone(sa_tz)

    start_time = start_time_sast.strftime('%H:%M')
    end_time = end_time_sast.strftime('%H:%M')

    date = start_time_sast.strftime('%Y-%m-%d %H:%M:%S')

    summary = event['summary']
    return [summary, start_time, end_time, date]


def get_next_7_days():
    """
    Gets the list of the next 7 days starting from today.

    Returns:
        list: List of datetime objects representing the next 7 days.

    """
    today = datetime.now(pytz.timezone('Africa/Johannesburg')).replace(hour=0, minute=0, second=0, microsecond=0)
    next_7_days = [today + timedelta(days=i) for i in range(7)]
    return next_7_days


def calendar_layout(calendars):
    """
    Displays calendar data in a tabular layout.

    Args:
        calendars (dict): Dictionary containing calendar names and their corresponding IDs.

    Returns:
        list: List of slots.

    """
    table = PrettyTable()
    table.field_names = ['Day', 'Date', 'Summary', 'Duration', 'Status']

    slots = []
    calendar_data = calendar_utilities.read_calendar_data(calendars)["code clinic"]["events"]

    next_7_days = get_next_7_days()

    for day in next_7_days:
        day_str = day.strftime("%d-%m-%Y")
        events_on_day = [event for event in calendar_data if day <= datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z') < day + timedelta(days=1)]

        if not events_on_day:
            # If no events on this day, display "No events" and "N/A"
            table.add_row([calendar.day_name[day.weekday()], day_str, 'No events', 'N/A', 'N/A'])
        else:
            for event in events_on_day:
                formatted = format_data(event)
                table.add_row([calendar.day_name[day.weekday()], day_str, formatted[0], f'{formatted[1]} - {formatted[2]}', event["description"]])
                table.align["Day"] = "l"

    print(table)
    return slots

def primary_calendar(calendars):
    table = PrettyTable()
    table.field_names = ['Day', 'Date', 'Summary', 'Duration', 'Status']

    slots = []
    calendar_data = calendar_utilities.read_calendar_data(calendars)["primary"]["events"]

    next_7_days = get_next_7_days()

    for day in next_7_days:
        day_str = day.strftime("%d-%m-%Y")
        events_on_day = [event for event in calendar_data if day <= datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z') < day + timedelta(days=1)]

        if not events_on_day:
            # If no events on this day, display "No events" and "N/A"
            table.add_row([calendar.day_name[day.weekday()], day_str, 'No events', 'N/A', 'N/A'])
        else:
            for event in events_on_day:
                formatted = format_data(event)
                table.add_row([calendar.day_name[day.weekday()], day_str, formatted[0], f'{formatted[1]} - {formatted[2]}', event["description"]])
                table.align["Day"] = "l"

    print(table)
    return slots