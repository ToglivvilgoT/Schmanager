from cal import Event
from pattern import Pattern
from action import Action


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