import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from src.booking_system.volunteering.volunteer_slot import volunteer_for_slot, do_volunteering

class TestVolunteering(unittest.TestCase):

    @patch('src.booking_system.volunteering.volunteer_slot.calendar_utilities.read_calendar_data')
    @patch('src.booking_system.volunteering.volunteer_slot.slot_utilities.get_booking_info')
    @patch('src.booking_system.volunteering.volunteer_slot.calendar_utilities.update_calendar_data_file')
    @patch('src.booking_system.volunteering.volunteer_slot.service.events')
    def test_successful_volunteering(self, mock_events, mock_update_calendar, mock_get_booking_info, mock_read_calendar_data):
        mock_events.return_value.insert.return_value.execute.return_value = {'id': 'event_id'}
        mock_update_calendar.return_value = None
        mock_get_booking_info.return_value = ('2024-03-01', '10:00', 'test@student.wethinkcode.com')
        mock_read_calendar_data.return_value = {
            'code clinic': {'id': 'clinic_id', 'events': []},
            'primary': {'id': 'primary_id', 'events': []}
        }

        service_mock = MagicMock()
        calendars_mock = MagicMock()

        start_datetime = datetime(2024, 3, 1, 10, 0)
        volunteer_for_slot(service_mock, start_datetime, calendars_mock, 'test@example.com')

        mock_events.return_value.insert.assert_called_once()
        mock_update_calendar.assert_called_once()
        mock_get_booking_info.assert_called_once()
        mock_read_calendar_data.assert_called_once()

    

if __name__ == '__main__':
    unittest.main()
