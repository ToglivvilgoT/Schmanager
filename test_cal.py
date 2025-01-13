import cal

import unittest


class TestTime(unittest.TestCase):
    def test_as_tuple(self):
        time = (2005, 2, 20, 12, 0)
        self.assertEqual(cal.Time(*time).as_tuple(), time)

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

    # Tests for method 'str2time'
    def test_parsing(self):
        """Tests normal case for str2time."""
        year = 2005
        month = 3
        day = 14
        hour = 9
        minute = 0
        second = 0
        time_str = f'{year:4}{month:2}{day:2}T{hour:2}{minute:2}{second:2}Z'
        time = cal.Time(year, month, day, hour, minute)
        self.assertEqual(cal.Time.str2time(time_str), time)

    def test_parsing_not_int(self):
        """Test for str2time where date numbers are not integers."""
        year = 2005
        month = 3
        day = 14
        hour = 9
        minute = 0
        second = 0
        time_str = f'{year:04}{month:02}{day:02}T{hour:02}{minute:02}{second:02}Z'
        for index, length in [
                (0, 4),
                (4, 2),
                (6, 2),
                (9, 2),
                (11, 2),
                (13, 2),
        ]:
            test_str = time_str[:index] + '?' * length + time_str[index + length:]
            self.assertRaises(ValueError, cal.Time.str2time, test_str)

    def test_parsing_not_literal(self):
        """Test for str2time where sting literals 'T' or 'Z' are missing from input str."""
        self.assertRaises(ValueError, cal.Time.str2time, '20250213?150300Z')
        self.assertRaises(ValueError, cal.Time.str2time, '20250213T150300?')


class TestEvent(unittest.TestCase):
    """Class for testing the Event class methods."""
    def test_has_field(self):
        """Tests the 'has_field' method."""
        # test with one field
        field = 'myFiled'
        missing_field = '????????'
        self.assertTrue(cal.Event({field: 'myValue'}).has_field(field))
        self.assertFalse(cal.Event({field: 'myValue'}).has_field(missing_field))
        
        # test with more fields
        content = {'1': 'one', '2': 'two', field: 'three', '4': 'four'}
        self.assertTrue(cal.Event(content).has_field(field))
        self.assertFalse(cal.Event(content).has_field(missing_field))

        # test with no fileds
        self.assertFalse(cal.Event({}).has_field(missing_field))
        self.assertFalse(cal.Event({}).has_field(''))

    def test_get_field_text(self):
        """Tests the 'get_field_test' method."""
        field = 'myField'
        value = 'myValue'
        missing_field = '?????????'
        event = cal.Event({field: value})
        self.assertEqual(event.get_field_text(field), value)
        self.assertRaises(KeyError, event.get_field_text, missing_field)

    def test_get_time(self):
        """Tests the 'get_start_time' and 'get_end_time' methods."""
        for field, method in (('DTSTART', cal.Event.get_start_time), ('DTEND', cal.Event.get_end_time)):
            wrong_field = 'FOO'
            time = '20250113T120000Z'
            wrong_time = 'BAR'
            
            self.assertEqual(method(cal.Event({field: time})), cal.Time.str2time(time))
            self.assertRaises(ValueError, method, cal.Event({wrong_field: time}))
            self.assertRaises(ValueError, method, cal.Event({field: wrong_time}))

    def fields_equal(self, event: cal.Event, fields: dict[str, str]):
        """Helper method that tests if event.get_fields() is the same as fields."""
        event_fields = event.get_fields()
        for field in event_fields:
            self.assertIn(field, fields)
        for field in fields:
            self.assertIn(field, event_fields)

    def test_get_fields(self):
        """Tests the 'get_fields' method."""
        for fields in ({}, {'a': '1'}, {'a': '1', 'b': '2', 'c': '3'}):
            self.fields_equal(cal.Event(fields), fields)

    def test_remove_field(self):
        """Tests the 'remove_field' method."""
        field = 'foo'
        event = cal.Event({field: 'bar'})
        event.remove_field(field)
        self.assertNotIn(field, event.get_fields())

        fields = {field: 'bar'}
        not_field = 'yahoo'
        event = cal.Event(fields)
        event.remove_field(not_field)
        self.fields_equal(event, fields)

    def test_write_field(self):
        """Tests the 'write_field' method."""
        key1 = 'foo'
        val1 = 'bar'
        key2 = 'its a me'
        val2 = 'mario'
        event = cal.Event({})

        # test with simple write
        event.write_field(key1, val1, True)
        self.fields_equal(event, {key1: val1})

        # test atempt to overwrite with overwrite set to False
        event.write_field(key1, val2, False)
        self.fields_equal(event, {key1: val1})

        # test atempt to overwrite with overwrite set to True
        event.write_field(key1, val2, True)
        self.fields_equal(event, {key1: val2})

        # test to write new field with overwrite set to False
        event.write_field(key2, val2, False)
        self.fields_equal(event, {key1: val2, key2: val2})

def test_visuals():
    """Function for testing the __str__ method for Time, Event and Cal."""
    time = cal.Time(2025, 1, 13, 12, 0)
    print(time)
    print(time.__str__(1))

    event1 = cal.Event({'First Field': 'First Value', 'its a me': 'mario', 'foo': 'bar'})
    print(event1)
    print(event1.__str__(1))
    event_empty = cal.Event({})
    print(event_empty)

    event2 = cal.Event({'Never': 'Gonna', 'Give': 'You up'})
    event3 = event_empty
    event4 = event2
    calendar = cal.Calendar((event1, event2, event3, event4))
    print(calendar)
    print(calendar.__str__(1))
    calendar_empty = cal.Calendar(())
    print(calendar_empty)


if __name__ == '__main__':
    test_visuals()
    unittest.main()