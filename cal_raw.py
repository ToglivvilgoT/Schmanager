from typing import Iterable


class Pattern:
    pass


class Action:
    pass


class SrcCal:
    pass


class Filter:
    pass


class UnbuiltCal:
    """ Class for Calendars before being built """
    def __init__(self, src_cals: Iterable[SrcCal], filters: Iterable[Filter]):
        self.src_cals = set([src_cal for src_cal in src_cals])
        self.filters = [filtr for filtr in filters]
