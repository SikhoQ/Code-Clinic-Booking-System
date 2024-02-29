import booking_system.calendars.calendar_utilities as calendar_utilities
from prettytable import PrettyTable 
import booking_system.calendars.slot_utilities as slot_utilities
import booking_system.calendars.view_calendar as view_calendar
from datetime import datetime, timedelta
import calendar
import booking_system.calendars.calendar_api as api


def view_events(calendars):
     
    table = PrettyTable()
    table.field_names = ['Day', 'Date', 'Summary', 'Duration']

    slots = []
    calendar_data = calendar_utilities.read_calendar_data(calendars)["code clinic"]["events"]

    day = datetime.utcnow()
    day_str = day.strftime("%d-%m-%Y")
    # events_on_day = [event for event in calendar_data if day <= datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z') < day + timedelta(days=1)]

    
    for event in calendar_data:
        formatted = view_calendar.format_data(event)
        table.add_row([calendar.day_name[day.weekday()], day_str, formatted[0], f'{formatted[1]} - {formatted[2]}'])
        table.align["Day"] = "l"

    print(table)
    

def book_slot(service, date, time, description):
    pass


def update_local_data_file(date, time, event_id, description):
    # Implement logic to update the local data file with booking information


    pass


# def main():
#     service = api.authorise_google_calendar()
#     calendars = calendars = calendar_utilities.create_coding_clinic_calendar(service)
#     view_events(calendars)


# if __name__ == "__main__":
#     main()
    
