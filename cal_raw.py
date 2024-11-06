from typing import Iterable

from cal import Calendar
from src_cal import SrcCal
from filter import Filter


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
    
    def __str__(self, tabs: int = 0):
        name = '\t' * tabs + 'Unbuilt Calendar:\n'
        
        name += '\t' * (tabs+1) + 'Source Calendars:\n'
        for src_cal in self.src_cals:
            name += src_cal.__str__(tabs+2) + '\n'
        
        name += '\t' * (tabs+1) + 'Filters:\n'
        for filter in self.filters:
            name += filter.__str__(tabs+2) + '\n'

        return name
