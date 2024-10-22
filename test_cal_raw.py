import cal_raw
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
        pattern = cal_raw.PatternHasText(self.event_texts[0], [self.event_fields[0]])
        self.assertTrue(pattern.resolve(self.event))
        pattern = cal_raw.PatternHasText(self.event_texts[1], [self.event_fields[2]])
        self.assertFalse(pattern.resolve(self.event))

    def test_multiple(self):
        """ tests for text in two fields """
        pattern = cal_raw.PatternHasText(self.event_texts[0], [self.event_fields[0], self.event_fields[1]])
        self.assertTrue(pattern.resolve(self.event))
        pattern = cal_raw.PatternHasText(self.event_texts[1], [self.event_fields[2], self.event_fields[0]])
        self.assertFalse(pattern.resolve(self.event))

    def test_all(self):
        """ tests for text in one field """
        pattern = cal_raw.PatternHasText(self.event_texts[0])
        self.assertTrue(pattern.resolve(self.event))
        pattern = cal_raw.PatternHasText('NOT_A_TEXT')
        self.assertFalse(pattern.resolve(self.event))

    def test_none(self):
        """ test for text in no field """
        pattern = cal_raw.PatternHasText(self.event_texts[0], [])
        self.assertFalse(pattern.resolve(self.event))


if __name__ == '__main__':
    unittest.main()