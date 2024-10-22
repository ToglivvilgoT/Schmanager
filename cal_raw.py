from typing import Iterable
from abc import ABC, abstractmethod

from cal import Calendar, Event


class Time():
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute


class SrcCal(ABC):
    @abstractmethod
    def get_events(self) -> Iterable[Event]:
        pass


class Pattern(ABC):
    @abstractmethod
    def resolve(self, event: Event) -> bool:
        pass


class PatternAnd(Pattern):
    def __init__(self, patterns: Iterable[Pattern]):
        self.patterns = [pattern for pattern in patterns]

    def resolve(self, event: Event):
        return all([pattern.resolve(event) for patten in self.pattens])


class PatternOr(Pattern):
    def __init__(self, patterns: Iterable[Pattern]):
        self.patterns = [pattern for pattern in patterns]

    def resolve(self, event: Event):
        return any([pattern.resolve(event) for pattern in self.patterns])


class PatternNot(Pattern):
    def __init__(self, pattern: Pattern):
        self.pattern = pattern

    def resolve(self, event: Event):
        return not self.pattern(event)


class PatternHasText(Pattern):
    """ Pattern for checking if text is in a field (or in all fields) """
    def __init__(self, text: str, fields: Iterable[str]|None = None):
        """ text is the text to check for
        fields are the fields to check in, if None checks in all fields """
        self.text = text
        self.fields = fields

    def resolve(self, event: Event):
        """ checks pattern against event
        returns True if text is in the field of event
        returns False otherwise
        returns False if field is missing from Event """
        if self.fields == None:
            fields = event.get_fields()
        else:
            fields = self.fields

        for field in event.get_fields():
            if field in fields and self.text in event.get_field_text(field):
                return True

        return False


class PatternHasField(Pattern):
    pass


class PatternInTime(Pattern):
    pass


class Action(ABC):
    """ ABC for actions which are applied to events """
    @abstractmethod
    def resolve(self, event: Event) -> list[Event]:
        pass


class ActionMultiple(Action):
    """ Class for handling multiple actions in sequence """
    def __init__(self, actions: Iterable[Action]):
        self.actions = [action for action in actions]

    def resolve(self, event: Event):
        current_events = [event]
        next_events = []

        for action in self.actions:
            for event in current_events:
                for next_event in action.resolve(event):
                    next_events.append(next_event)

            current_events = next_events
            next_events = []

            

class Filter:
    """ Class for Event Filters """
    def __init__(self, pattern: Pattern, action: Action):
        self.pattern = pattern
        self.action = action

    def check(self, event: Event):
        if self.pattern.resolve(event):
            return self.action.resolve(event)
        else:
            return [event]


class UnbuiltCal:
    """ Class for Calendars before being built """
    def __init__(self, src_cals: Iterable[SrcCal], filters: Iterable[Filter]):
        self.src_cals = [src_cal for src_cal in src_cals]
        self.filters = [filtr for filtr in filters]

    def build(self):
        final_events = []

        for src_cal in self.src_cals:
            for event in src_cal.get_events():
                current_events = [event]
                next_events = []

                for filtr in self.filters:
                    for current_event in current_events:
                        for next_event in filtr.check(current_event):
                            next_events.append(next_event)

                    current_events = next_events
                    next_events = []

                final_events += current_events

        return Calendar(final_events)