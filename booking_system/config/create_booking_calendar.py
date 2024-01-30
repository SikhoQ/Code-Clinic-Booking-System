import google_calendar_api_config as api_config


def create_calendar():
    service = api_config.authorize_and_authenticate()

    # TODO: change to check calendar data file if calendar exists before creating
    calendar_list = service.calendarList().list().execute()
    calendar_exists = "Coding Clinic" in [calendar["summary"] for calendar in calendar_list["items"]]

    if not calendar_exists:
        print("Adding Coding Clinic calendar..\n")
        calendar_resource = {"summary": "Coding Clinic"}

        try:
            service.calendars().insert(body=calendar_resource).execute()
            print("Calendar successfully added")

        except api_config.HttpError as error:
            print(f"An error occurred: {error}")
