import cal

import unittest


class TestTime(unittest.TestCase):
    def test_comparisons(self):
        low_year, mid_year, high_year = 2004, 2005, 2006
        low_month, mid_month, high_month = 5, 6, 7
        low_day, mid_day, high_day = 15, 16, 17
        low_hour, mid_hour, high_hour = 11, 12, 13
        low_minute, mid_minute, high_minute = 29, 30, 31

        low_times = [low_year, low_month, low_day, low_hour, low_minute]
        mid_times = [mid_year, mid_month, mid_day, mid_hour, mid_minute]
        high_times = [high_year, high_month, high_day, high_hour, high_minute]

        self.assertEqual(cal.Time(*mid_times), cal.Time(*mid_times))
        self.assertNotEqual(cal.Time(*low_times), cal.Time(*high_times))


if __name__ == '__main__':
    unittest.main()