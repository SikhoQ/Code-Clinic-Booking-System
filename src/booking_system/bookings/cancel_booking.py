import booking_system.calendars.calendar_utilities as calendar_utilities
from prettytable import PrettyTable 
import booking_system.calendars.slot_utilities as slot_utilities
import booking_system.calendars.view_calendar as view_calendar
from datetime import datetime, timedelta
import calendar
import booking_system.calendars.calendar_api as api
from InquirerPy import inquirer
from main import main


def cancel_booking(service, calendars):
    (date, time_choice, email) = slot_utilities.get_booking_info()
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    clinic_events = calendar_data["code clinic"]["events"]
    calendar_id = calendar_data["code clinic"]["id"]

    event_id, existing_event = slot_utilities.find_existing_event(clinic_events, date, time_choice)

    if existing_event and slot_utilities.is_booked_slot(existing_event):
        try:
            del existing_event["attendees"]
            existing_event["description"] = "Volunteer Slot"
            existing_event = service.events().update(calendarId=calendar_id, eventId=event_id, body=existing_event).execute()
            print("Booking cancellation successful!\n")

            calendar_utilities.update_calendar_data_file(service, calendars)
        except Exception:
            raise
    else:
        if not existing_event:
            print("No volunteer slot for given time.", end=" ")
        else:
            print("No booking found for volunteer slot.")
        if inquirer.confirm(message="Select another slot?"):
            cancel_booking(service, calendars)


# def view_events(calendars):
#     table = PrettyTable()
#     table.field_names = ['Day', 'Date', 'Summary', 'Duration']

#     calendar_data = calendar_utilities.read_calendar_data(calendars)["code clinic"]["events"]

#     day = datetime.utcnow()
#     day_str = day.strftime("%d-%m-%Y")
#     # events_on_day = [event for event in calendar_data if day <= datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z') < day + timedelta(days=1)]

#     for event in calendar_data:
#         formatted = view_calendar.format_data(event)
#         table.add_row([calendar.day_name[day.weekday()], day_str, formatted[0], f'{formatted[1]} - {formatted[2]}'])
#         table.align["Day"] = "l"

#     print(table)
