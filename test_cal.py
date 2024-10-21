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

        # test equals
        self.assertEqual(cal.Time(*mid_times), cal.Time(*mid_times))
        self.assertNotEqual(cal.Time(*low_times), cal.Time(*high_times))

        # test less than
        # isolates the cases where:
        #    year1 < year2 or
        #    year1 == year2 and month1 < month2 or
        #    year1 == year2 and month1 == month2 and day1 < day2 or etc.
        for i in range(4):
            self.assertLess(cal.Time(*mid_times[:i], low_times[i], *high_times[i+1:]), cal.Time(*mid_times))
        
        # tests order of priority between time units i.e. if year1 < year2 it doesnt matter how the months compare etc.
        for i in range(1, 4):
            self.assertGreaterEqual(cal.Time(*mid_times[:i], high_times[i], *low_times[i+1:]), cal.Time(*mid_times))


if __name__ == '__main__':
    unittest.main()