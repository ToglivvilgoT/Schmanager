import pattern
import cal

import unittest


class TestPatternHasText(unittest.TestCase):
    def setUp(self):
        self.event_fields = ['FIELD1', 'FIELD2', 'FIELD3']
        self.event_texts = ['VAL1', 'VAL2', 'VAL3']
        self.event_content = {field: val for field, val in
            zip(self.event_fields, self.event_texts)}

        self.event = cal.Event(self.event_content)

    def test_one(self):
        """ tests for text in one field """
        pat = pattern.PatternHasText(self.event_texts[0], [self.event_fields[0]])
        self.assertTrue(pat.resolve(self.event))
        pat = pattern.PatternHasText(self.event_texts[1], [self.event_fields[2]])
        self.assertFalse(pat.resolve(self.event))

    def test_multiple(self):
        """ tests for text in two fields """
        pat = pattern.PatternHasText(self.event_texts[0], [self.event_fields[0], self.event_fields[1]])
        self.assertTrue(pat.resolve(self.event))
        pat = pattern.PatternHasText(self.event_texts[1], [self.event_fields[2], self.event_fields[0]])
        self.assertFalse(pat.resolve(self.event))

    def test_all(self):
        """ tests for text in one field """
        pat = pattern.PatternHasText(self.event_texts[0])
        self.assertTrue(pat.resolve(self.event))
        pat = pattern.PatternHasText('NOT_A_TEXT')
        self.assertFalse(pat.resolve(self.event))

    def test_none(self):
        """ test for text in no field """
        pat = pattern.PatternHasText(self.event_texts[0], [])
        self.assertFalse(pat.resolve(self.event))


class TestPatternInTime(unittest.TestCase):
    def setUp(self):
        self.time1 = '20020202T120000Z'
        self.time2 = '20030303T130000Z'
        self.time3 = '20040404T140000Z'
        self.time4 = '20050505T150000Z'

    def run_test(self, event_start: str, event_end: str, timeframe_start: str, timeframe_end: str, expected_result: bool):
        event = cal.Event({'DTSTART': event_start, 'DTEND': event_end})
        pat = pattern.PatternInTime(
            cal.Time.str2time(timeframe_start),
            cal.Time.str2time(timeframe_end)
        )

        if expected_result == True:
            self.assertTrue(pat.resolve(event))
        else:
            self.assertFalse(pat.resolve(event))

    def test_wholey(self):
        """ tests when event is wholey inside and outside time frame """
        self.run_test(self.time2, self.time3, self.time1, self.time4, True)
        self.run_test(self.time1, self.time2, self.time3, self.time4, False)
        self.run_test(self.time3, self.time4, self.time1, self.time2, False)

    def test_partially(self):
        """ tests when event is partially inside and partially outside time frame """
        self.run_test(self.time1, self.time3, self.time2, self.time4, True)
        self.run_test(self.time2, self.time4, self.time1, self.time3, True)

    def test_on_under(self):
        """ tests when event ends/starts at the same time as the time frame starts/ends """
        self.run_test(self.time1, self.time2, self.time2, self.time3, False)
        self.run_test(self.time2, self.time3, self.time1, self.time2, False)

    def test_invalid(self):
        """ tests when event is missing or has invalid DTSTART and DTEND fields """
        pat = pattern.PatternInTime(
            cal.Time.str2time(self.time1),
            cal.Time.str2time(self.time4)
        )
        event = cal.Event({'DTSTART': self.time2})
        self.assertFalse(pat.resolve(event))
        event = cal.Event({'DTEND': self.time3})
        self.assertFalse(pat.resolve(event))
        event = cal.Event({'DTSTART': 'NaN', 'DTEND': self.time3})
        self.assertFalse(pat.resolve(event))
        event = cal.Event({'DTSTART': self.time2, 'DTEND': 'NaN'})
        self.assertFalse(pat.resolve(event))


if __name__ == '__main__':
    unittest.main()