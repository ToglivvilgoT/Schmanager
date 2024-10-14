from typing import Iterable


class Event:
    """ Class for Calendar Events """
    def __init__(self, content: dict[str, str]):
        """ content keys should be fields and content values is the text of that field """
        self.content = content


class Calendar:
    """ Class for Calendars """
    def __init__(self, events: Iterable[Event]):
        """ Initializes Calendar Object """
        self.events = [event for event in events]