from datetime import *
import booking_system.calendars.calendar_utilities as calendar_utilities
import booking_system.calendars.calendar_api as api
import os
import csv
from prettytable import PrettyTable
import calendar


TOKEN_FILE = os.path.expanduser("~/.google_calendar_token.json")
CONFIG_FILE = os.path.expanduser("~/.coding_clinic_config.json")
CREDS_FILE = os.path.expanduser("~/.google_calendar_credentials.json")
SCOPES = ["https://www.googleapis.com/auth/calendar"]



def format_data(event):
    start_time = datetime.fromisoformat(event['start']['dateTime']).strftime('%H:%M')
    end_time = datetime.fromisoformat(event['end']['dateTime']).strftime('%H:%M')
    summary = event['summary']
        
    return [summary ,start_time , end_time]



def view_calendar():

    table = PrettyTable()
    table.field_names = ['Day', 'Date', 'Summary', 'Duration']

    slots = []
    calendar_data = calendar_utilities.read_calendar_data()["cohort 2023"]["items"]

    for event in calendar_data:
    
        formatted = format_data(event)
        day = calendar.day_name[today.weekday()]
        slots.append(today.isoformat() + 'Z')
        today += timedelta(days=1)
        table.add_row([day, (today - timedelta(days=1)).strftime("%d-%m-%Y"), formatted[0], f'{formatted[1]} - {formatted[2]}'])
        table.align["Day"] = "l"
        if not event:
            formatted[0] = 'No event'


    print("printing table")
    print(table)
    
    return slots

    
if __name__ == '__main__':
    view_calendar()
