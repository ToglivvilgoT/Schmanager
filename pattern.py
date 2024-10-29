from typing import Iterable
from abc import ABC, abstractmethod

from cal import Event, Time


class Pattern(ABC):
    @abstractmethod
    def resolve(self, event: Event) -> bool:
        pass

    @abstractmethod
    def __str__(self, tabs: int = 0):
        return 'Pattern Object'


class PatternAnd(Pattern):
    def __init__(self, patterns: Iterable[Pattern]):
        self.patterns = [pattern for pattern in patterns]

    def resolve(self, event: Event):
        return all([pattern.resolve(event) for pattern in self.patterns])
    
    def __str__(self, tabs: int = 0):
        name = tabs * '\t' + 'Pattern And:\n'
        for pattern in self.patterns:
            name += pattern.__str__(tabs+1) + '\n'
        
        name = name.removesuffix('\n')
        return name
    

class PatternOr(Pattern):
    def __init__(self, patterns: Iterable[Pattern]):
        self.patterns = [pattern for pattern in patterns]

    def resolve(self, event: Event):
        return any([pattern.resolve(event) for pattern in self.patterns])
    
    def __str__(self, tabs: int = 0):
        name = tabs * '\t' + 'Pattern Or:\n'
        for pattern in self.patterns:
            name += pattern.__str__(tabs+1) + '\n'
        
        name = name.removesuffix('\n')
        return name


class PatternNot(Pattern):
    def __init__(self, pattern: Pattern):
        self.pattern = pattern

    def resolve(self, event: Event):
        return not self.pattern.resolve(event)
    
    def __str__(self, tabs: int = 0):
        return tabs * '\t' + 'Pattern Not:\n' + self.pattern.__str__(tabs+1)


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
    
    def __str__(self, tabs: int = 0):
        name = tabs * '\t' + 'Pattern Has Text:\n'
        name += tabs * '\t' + '\tText: ' + str(self.text) + '\n'
        name += tabs * '\t' + '\tFields: ' + str(self.fields)
        return name


class PatternInTime(Pattern):
    """ Pattern for checking if Event is partialy inside a given timeframe """
    def __init__(self, time_start: Time, time_end: Time):
        """ time_start chould be earlier than time_end """
        self.time_start = time_start
        self.time_end = time_end

    def resolve(self, event: Event):
        """ checks pattern against event
        returns true if event is partially or wholey inside timeframe, false otherwise
        returns false if event starts/ends at the exact same time as timeframe ends/starts
        returns false if event is missing/has invalid DTSTART or DTEND fields """
        try:
            event_start = event.get_start_time()
            event_end = event.get_end_time()
            return event_start < self.time_end and event_end > self.time_start
        except ValueError:
            return False
        
    def __str__(self, tabs: int = 0):
        name = tabs * '\t' + 'Pattern in Time:\n'
        name += tabs * '\t' + '\tStart: ' + str(self.time_start) + '\n'
        name += tabs * '\t' + '\tEnd: ' + str(self.time_end)
        return name