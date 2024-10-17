from typing import Iterable


class Event:
    """ Class for Calendar Events """
    def __init__(self, content: dict[str, str]):
        """ content keys should be fields and content values is the text of that field """
        self.content = content

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