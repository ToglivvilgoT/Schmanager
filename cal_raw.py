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