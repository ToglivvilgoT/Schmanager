from pattern import Pattern
from cal import Event

from typing import Iterable
from abc import ABC, abstractmethod


class Action(ABC):
    """ ABC for actions which are applied to events """
    @abstractmethod
    def resolve(self, event: Event) -> list[Event]:
        pass

    def __str__(self, tabs: int = 0):
        return '\t' * tabs + 'Baseclass Action Object'


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

        return current_events
    
    def __str__(self, tabs: int = 0):
        name = '\t' * tabs + 'Action Multiple:\n'
        for act in self.actions:
            name += act.__str__(tabs+1) + '\n'

        return name.rstrip()


class ActionRemoveField(Action):
    """ Class for removing field from event """
    def __init__(self, field: str):
        self.field = field

    def resolve(self, event: Event):
        event.remove_field(self.field)
        return [event]
    
    def __str__(self, tabs: int = 0):
        return '\t' * tabs + f'Action Remove Field: {self.field}'


class ActionWriteField(Action):
    """ Class for writing text to a field of event """
    def __init__(self, field: str, text: str, overwrite: bool = True):
        self.field = field
        self.text = text
        self.overwrite = overwrite

    def resolve(self, event: Event):
        """ writes text to field as long as overwrite is True or event doesnt have field """
        event.write_field(self.field, self.text, self.overwrite)
        return [event]
    
    def __str__(self, tabs: int = 0):
        name = '\t' * tabs + 'Action Write Field:\n'
        name += '\t' * (tabs+1) + f'Field: {self.field}\n'
        name += '\t' * (tabs+1) + f'Text: {self.text}\n'
        name += '\t' * (tabs+1) + f'Overwrite: {self.overwrite}\n'
        return name.rstrip()



class ActionRemoveEvent(Action):
    """ Class for removing events """
    def resolve(self, event: Event):
        return []
    
    def __str__(self, tabs: int = 0):
        return '\t' * tabs + 'Action Remove Event'
    

class ActionAddEvent(Action):
    """ Class for adding new events """
    def __init__(self, event: Event):
        self.event_to_add = event

    def resolve(self, event: Event):
        return [event, self.event_to_add]
    
    def __str__(self, tabs: int = 0):
        return '\t' * tabs + 'Action Add Event:\n' + self.event_to_add.__str__(tabs+1)