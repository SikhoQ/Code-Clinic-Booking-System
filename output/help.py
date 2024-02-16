
from InquirerPy import inquirer

def print_help():
    print("")
    print(f""" 
    book                   :  book a time slot with a tutor
    cancel booking         :  cancel a booking
    cancel volunteering    :  cancel the free-time slot you offered as a tutor
    view_event             :  view details of a specific slot
    view_calendar          :  view slots for the whole week
    volunteer              :  volunteer your time as a tutor
    logout                 :  log out of the code_clinic"""
    )
print_help()


def option():
    options = inquirer.select(
    message="Select What You Want To Do:",
    choices=["book", "volunteer cancelation", "cancel_booking", "view event", "view calendar ", "volunteer", "logout"]
    ).execute()
    return options

option()