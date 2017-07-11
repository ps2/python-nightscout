import unittest
from models import *
from datetime import datetime, timedelta

class ScheduleTestCase(unittest.TestCase):
    def test_schedule_conversion_to_absolute_time(self):
        schedule = Schedule([
            ScheduleEntry(timedelta(hours=0), 1),
            ScheduleEntry(timedelta(hours=6), 0.7),
            ScheduleEntry(timedelta(hours=12), 0.8),
            ScheduleEntry(timedelta(hours=22), 0.9),
        ])
        items = schedule.between(datetime(2017,7,7,20), datetime(2017,7,8,4))

        expected = [
            AbsoluteScheduleEntry(datetime(2017,7,7,12), 0.8),
            AbsoluteScheduleEntry(datetime(2017,7,7,22), 0.9),
            AbsoluteScheduleEntry(datetime(2017,7,8,0), 1),
        ]

        for item, expected_item in zip(items, expected):
            self.assertEqual(item.start_date, expected_item.start_date)
            self.assertEqual(item.value, expected_item.value)
