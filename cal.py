from typing import Iterable, Sequence
from functools import total_ordering


@total_ordering
class Time:
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def __eq__(self, other: 'Time'):
        if isinstance(other, Time):
            return self.year == other.year and \
                self.month == other.month and \
                self.day == other.day and \
                self.hour == other.hour and \
                self.minute == other.minute

    def __lt__(self, other: 'Time'):
        def helper_comp(first: Sequence[int], second: Sequence[int]):
            if not first:
                return False
            else:
                return first[0] < second[0] or first[0] == second[0] and helper_comp(first[1:], second[1:])

        if isinstance(other, Time):
            return helper_comp([self.year, self.month, self.day, self.hour, self.minute],
                [other.year, other.month, other.day, other.hour, other.minute])
        
        else:
            raise ValueError(f"can only compare arguments of type Time, not Time and {type(other)}")

    def str2time(time_str: str):
        """ returns a Time object given a time_str in format: yyyyMMddThhmmssZ where 'T' and 'Z' are string Literals
        raises ValueError if time_str can not be decoded """

        try:
            year = int(time_str[0:4])
            month = int(time_str[4:6])
            day = int(time_str[6:8])
            hour = int(time_str[9:11])
            minute = int(time_str[11:13])
        except:
            raise ValueError('time_str could not be interpreted, should be in format yyyyMMddThhmmssZ where "T" and "Z" are string Literals')
        
        return Time(year, month, day, hour, minute)


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
        except ValueError:
            raise ValueError('Event does not have a start time in correct format, should be in format yyyyMMddThhmmssZ')

    def get_end_time(self):
        """ retuns the end time of the Event
        raises ValueError if Event doesnt have end time """

        try:
            return Time.str2time(self.content['DTEND'])
        except KeyError:
            raise ValueError('Event does not have an end time')
        except ValueError:
            raise ValueError('Event does not have a start time in correct format, should be in format yyyyMMddThhmmssZ')

    def get_fields(self):
        """ returns all fields of the event """
        return self.content.keys()

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