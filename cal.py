from typing import Iterable, Sequence
from functools import total_ordering


@total_ordering
class Time:
    def __init__(year: int, month: int, day: int, hour: int, minute: int):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def __eq__(self, other: Time):
        if isinstance(other, Time):
            return self.year == other.year and
                self.month == other.month and
                self.day == other.day and
                self.hour == other.hour and
                self.minute == other.minute

    def __lt__(self, other: Time):
        def helper_comp(first: Sequence[int], second: Sequence[int]):
            if not first:
                return False
            else:
                return first[0] < second[0] or first[0] == second[0] and helper_comp(first[1:], second[1:])

        if isinstance(other, Time):
            return helper_comp([self.year, self.month, self.day, self.hour, self.minute],
                [other.year, other.month, other.day, other.hour, other.minute])
        
        else:
            raise ValueError("can only compare arguments of type Time, not Time and {type(other)}")


class Event:
    """ Class for Calendar Events """
    def __init__(self, content: dict[str, str]):
        """ content keys should be fields and content values is the text of that field """
        self.content = content

    def has_field(self, field_name: str):
        """ Returns True if Event has the field 'field_name' else False """
        return field_name in self.content.keys()

    def get_field_text(self, field_name: str):
        """ Returns the content of field 'field_name'
        raises KeyError if Event doesnt contain the field 'field_name' """

        try:
            return self.content[field_name]
        except KeyError:
            raise KeyError(f'Event does not have the field: {field_name}')

    def get_start_time(self):
        """ returns the start time of the Event
        raises ValueError if Event doesnt have start_time """

        try:
            return Time.str2time(self.content['DTSTART'])
        except KeyError:
            raise ValueError('Event does not have a start time')

    def get_end_time(self):
        """ retuns the end time of the Event
        raises ValueError if Event doesnt have end time """

        try:
            return time.str2time(self.content['DTEND'])
        except KeyError:
            raise ValueError('Event does not have an end time')

    def __str__(self, tabs:int=0):
        name = '\t' * tabs + 'Event:\n'
        for field, text in self.content.items():
            name += '\t' * (tabs+1) + field + ': ' + text + '\n'
        return name


class Calendar:
    """ Class for Calendars """
    def __init__(self, events: Iterable[Event]):
        """ Initializes Calendar Object """
        self.events = [event for event in events]

    def __str__(self, tabs:int=0):
        name = '\t' * tabs + 'Calendar:\n'
        for event in self.events:
            name += event.__str__(tabs=1)
        return name