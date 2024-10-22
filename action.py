from pattern import Pattern
from cal import Event

from typing import Iterable
from abc import ABC, abstractmethod


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