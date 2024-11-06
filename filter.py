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
        
    def __str__(self, tabs: int = 0):
        name = '\t' * tabs + 'Filter:\n'
        name += '\t' * (tabs+1) + 'Pattern:\n' + self.pattern.__str__(tabs+2) + '\n'
        name += '\t' * (tabs+1) + 'Action:\n' + self.action.__str__(tabs+2)
        return name