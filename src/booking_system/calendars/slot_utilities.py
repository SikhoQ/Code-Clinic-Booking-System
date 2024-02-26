import booking_system.calendars.calendar_utilities as calendar_utilities
import os


CALENDAR_FILE = os.path.expanduser("src/booking_system/data/calendar_data.json")


def is_available_to_book(events, start_time, end_time):
    # start_time is is the full date
    pass


def is_available_to_volunteer(events, start_time, end_time):
    # start_time is is the full date
    pass


def is_slot_available(calendars, start_time, end_time, slot_type):
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    # handle time range error in function calling this -> loop user prompt
    # handle raised exception in function calling this

    # to check if slot is available check events in data file (clinic calendar)
    clinic_events = calendar_data["code clinic"]["event"]

    calendar_data = calendar_utilities.read_calendar_data(calendars)
    clinic_events = calendar_data["code clinic"]["events"]

    if slot_type == "booking":
        return is_available_to_book(clinic_events, start_time, end_time)
    elif slot_type == "volunteer":
        return is_available_to_volunteer(clinic_events, start_time, end_time)
    else:
        raise ValueError("Invalid slot_type. Use 'booking' or 'volunteer'.")

    #     for volunteer:
    #         if event is present, return False
    #         only return True if there's no event for that specific time
    #     for booking:
    #         if event is not present, return False
    #         if event is present:
    #             if event description is volunteer:
    #                 if volunteer is the same as person making booking (check from creator field), return False
    #                 else return True
    #             else return False
