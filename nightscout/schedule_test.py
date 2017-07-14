import unittest
from models import *
from datetime import datetime, timedelta
import pytz
from dateutil import tz

class ScheduleTestCase(unittest.TestCase):
    def test_schedule_conversion_to_absolute_time(self):
        # Schedule should be fixed offset, to match the pump's date math
        schedule_tz = tz.tzoffset(None, -(5*60*60)) # UTC-5
        schedule = Schedule([
            ScheduleEntry(timedelta(hours=0), 1),
            ScheduleEntry(timedelta(hours=6), 0.7),
            ScheduleEntry(timedelta(hours=12), 0.8),
            ScheduleEntry(timedelta(hours=22), 0.9),
        ], schedule_tz)
        # Queries against the schedule are typically in utc
        items = schedule.between(datetime(2017,7,7,20,tzinfo=pytz.utc), datetime(2017,7,8,6,tzinfo=pytz.utc))

        expected = [
            AbsoluteScheduleEntry(datetime(2017,7,7,12,tzinfo=schedule_tz), 0.8),
            AbsoluteScheduleEntry(datetime(2017,7,7,22,tzinfo=schedule_tz), 0.9),
            AbsoluteScheduleEntry(datetime(2017,7,8,0,tzinfo=schedule_tz), 1),
        ]

        self.assertEqual(len(items), len(expected))

        for item, expected_item in zip(items, expected):
            self.assertEqual(item.start_date, expected_item.start_date)
            self.assertEqual(item.value, expected_item.value)
