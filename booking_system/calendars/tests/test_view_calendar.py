import os
import unittest
import view_calendar
from unittest.mock import patch

class TestViewCalendar(unittest.TestCase):

    def test_file_exists(self):
        folder_path = '../calender API'
        file_name = 'dates.csv'
        file_path = os.path.join(folder_path, file_name)

    
        self.assertTrue(os.path.exists(file_path))

    def test_output(self):
        pass

if __name__ == '__main__':
    unittest.main()
