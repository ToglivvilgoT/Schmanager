"""Module with three main classes:
Time class for representing time.
Event class for representing a calendar event.
Calendar class for representing a calendar.
"""
from typing import Iterable
from functools import total_ordering


@total_ordering
class Time:
    """Class for representing time."""
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def as_tuple(self) -> tuple[int, int, int, int, int]:
        """Return time as a tuple: (year, month, day, hour, minute)."""
        return (self.year, self.month, self.day, self.hour, self.minute)

    def __eq__(self, other: 'Time') -> bool:
        """Check if two Times are equal.
        If other is not of type Time, raise ValueError.
        """
        if isinstance(other, Time):
            return self.as_tuple() == other.as_tuple()
        else:
            raise ValueError(f'can only compare arguments of type Time, not Time and {type(other)}')

    def __lt__(self, other: 'Time') -> bool:
        """Check if self comes before other.
        If other is not of type time, raise ValueError.
        """
        if isinstance(other, Time):
            return self.as_tuple() < other.as_tuple()
        else:
            raise ValueError(f'can only compare arguments of type Time, not Time and {type(other)}')

    @staticmethod
    def str2time(time_str: str) -> 'Time':
        """Returns a Time object given a time_str in format: yyyyMMddThhmmssZ where 'T' and 'Z' are string Literals
        raises ValueError if time_str can not be decoded.
        """
        try:
            year = int(time_str[0:4])
            month = int(time_str[4:6])
            day = int(time_str[6:8])
            assert time_str[8] == 'T'
            hour = int(time_str[9:11])
            minute = int(time_str[11:13])
            int(time_str[14:15])
            assert time_str[15] == 'Z'
        except:
            raise ValueError('time_str could not be interpreted, should be in format yyyyMMddThhmmssZ where "T" and "Z" are string Literals')

        return Time(year, month, day, hour, minute)

    def as_str(self) -> str:
        """returns time as a stirng on format yyyyMMddThhmmssZ where 'T' and 'Z' are string literals."""
        return f'{self.year:04}{self.month:02}{self.day:02}T{self.hour:02}{self.minute:02}00Z'

    def __str__(self, tabs: int=0) -> str:
        return '\t' * tabs + f'Time: {self.year:04}/{self.month:02}/{self.day:02} {self.hour:02}:{self.minute:02}'


class Event:
    """Class for Calendar Events."""
    def __init__(self, content: dict[str, str]):
        """Content keys should be fields and content values is the text of that field."""
        self.content = content

    def has_field(self, field_name: str) -> bool:
        """Returns True if Event has the field 'field_name' else False."""
        return field_name in self.content

    def get_field_text(self, field_name: str) -> str:
        """Returns the content of field 'field_name'
        raises KeyError if Event doesnt contain the field 'field_name'.
        """
        try:
            return self.content[field_name]
        except KeyError:
            raise KeyError(f'Event does not have the field: {field_name}')

    def get_start_time(self) -> Time:
        """Returns the start time of the Event.
        Event must have a field called 'DTSTART' and its value must be in format yyyyMMddThhmmssZ where 'T' and 'Z' are string literals.
        raises ValueError if Event doesnt have start_time or start_time is in the wrong format.
        """
        try:
            return Time.str2time(self.get_field_text('DTSTART'))
        except KeyError:
            raise ValueError('Event does not have a start time')
        except ValueError:
            raise ValueError('Event does not have a start time in correct format, should be in format yyyyMMddThhmmssZ')

    def get_end_time(self) -> Time:
        """Retuns the end time of the Event
        Event must have a field called 'DTEND' and its value must be in format yyyyMMddThhmmssZ where 'T' and 'Z' are string literals.
        raises ValueError if Event doesnt have end time or if it is in the wrong format.
        """
        try:
            return Time.str2time(self.get_field_text('DTEND'))
        except KeyError:
            raise ValueError('Event does not have an end time')
        except ValueError:
            raise ValueError('Event does not have a start time in correct format, should be in format yyyyMMddThhmmssZ')

    def get_fields(self) -> Iterable[str]:
        """Returns all fields of the event."""
        return self.content.keys()
    
    def remove_field(self, field: str) -> None:
        """Removes field from event, if field doesnt exist, nothing happens."""
        try:
            del self.content[field]
        except KeyError:
            pass

    def write_field(self, field: str, text: str, overwrite: bool = True) -> None:
        """Writes text to field
        if event doesnt have field, field is added
        if event has field and overwrite = True, the previous text is discarded
        if event has field and overwrite is False, nothing happens.
        """
        if overwrite or not self.has_field(field):
            self.content[field] = text

    def __str__(self, tabs: int=0) -> str:
        name = '\t' * tabs + 'Event:'
        for field, text in self.content.items():
            name += '\n' + '\t' * (tabs+1) + field + ': ' + text
        return name


class Calendar:
    """Class for Calendars."""
    def __init__(self, events: Iterable[Event]):
        """Initializes Calendar Object."""
        self.events = list(events)

    def __str__(self, tabs: int=0) -> str:
        name = '\t' * tabs + 'Calendar:'
        for event in self.events:
            name += '\n' + event.__str__(tabs=tabs + 1)
        return name