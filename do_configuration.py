from booking_system.config.config_manager import configure_system
from booking_system.calendars.google_calendar_api import authorize_and_authenticate


service = authorize_and_authenticate()
configure_system(service)
