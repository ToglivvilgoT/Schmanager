from typing import Literal
import json

from cal_raw import UnbuiltCal
from src_cal import SrcCalURL
from filter import Filter
from pattern import Pattern, PatternAnd, PatternOr, PatternNot, PatternHasText, PatternInTime
from action import Action, ActionAddEvent, ActionMultiple, ActionRemoveEvent, ActionRemoveField, ActionWriteField


class OutputJSON():
    """Class for outputing UnbuiltCals to a JSON file."""

    JSONSrcCals = list[str]
    @classmethod
    def _get_src_cals(cls, src_cals: list[SrcCalURL]) -> JSONSrcCals:
        """Formats src_cals as a list of strings.
        Acceptable src_cals are: SrcCalURL.
        Other src_cals will raise TypeError.
        """
        json_list = []
        for src_cal in src_cals:
            if isinstance(src_cal, SrcCalURL):
                json_list.extend(('url', src_cal.url, '/url'))
            else:
                raise TypeError(f'source calendar of wrong type {type(src_cal)}, should be SrcCalURL.')
        return json_list

    JSONPattern = list[str]
    @classmethod
    def _get_pattern(cls, pattern: Pattern) -> JSONPattern:
        """returns a JSON representation of pattern."""
        if isinstance(pattern, PatternInTime):
            return ['in_time', pattern.time_start.as_str(), pattern.time_end.as_str()]
        elif isinstance(pattern, PatternHasText):
            if pattern.fields is None:
                return ['has_text', pattern.text]

            json_patterns = []
            for field in pattern.fields:
                json_patterns += ['has_text', pattern.text, field]
            return json_patterns
        elif isinstance(pattern, PatternNot):
            return ['not'] + cls._get_pattern(pattern.pattern) + ['/not']
        elif isinstance(pattern, PatternAnd):
            json_patterns = ['and']
            for and_pattern in pattern.patterns:
                json_patterns += cls._get_pattern(and_pattern)
            json_patterns.append('/and')
            return json_patterns
        elif isinstance(pattern, PatternOr):
            json_patterns = ['or']
            for or_pattern in pattern.patterns:
                json_patterns += cls._get_pattern(or_pattern)
            json_patterns.append('/or')
            return json_patterns
        else:
            raise TypeError(f'Unsuported Pattern type {type(pattern)}.')

    JSONAction = list[str]
    @classmethod
    def _get_action(cls, action: Action) -> JSONAction:
        """returns a JSON representation of action."""
        if isinstance(action, ActionWriteField):
            return ['write_field', action.field, action.text]
        elif isinstance(action, ActionAddEvent):
            json_action = ['add_event']
            for field in action.event_to_add.get_fields():
                json_action.append(field)
                json_action.append(action.event_to_add.get_field_text(field))
            json_action.append('/add_event')
            return json_action
        elif isinstance(action, ActionRemoveEvent):
            return ['remove_event']
        elif isinstance(action, ActionRemoveField):
            return ['remove_field', action.field]
        elif isinstance(action, ActionMultiple):
            json_action = ['multiple']
            for child_action in action.actions:
                json_action += cls._get_action(child_action)
            json_action.append('/multiple')
            return json_action
        else:
            raise TypeError(f'action is of unsuported type {type(action)}')

    JSONFilter = dict[Literal['pattern'] | Literal['action'], JSONPattern | JSONAction]
    JSONFilters = list[JSONFilter]
    @classmethod
    def _get_filters(cls, filters: list[Filter]) -> JSONFilters:
        json_filters = []
        for filter in filters:
            json_filter = {}
            json_filter['pattern'] = cls._get_pattern(filter.pattern)
            json_filter['action'] = cls._get_action(filter.action)
            json_filters.append(json_filter)
        return json_filters

    @classmethod
    def output_unbuild_cal(cls, cal: UnbuiltCal, file_path: str) -> None:
        """Outputs an unbuilt calendar to file at file_path as a json object."""
        json_obj = {}
        json_obj['src_cals'] = cls._get_src_cals(cal.src_cals)
        json_obj['filters'] = cls._get_filters(cal.filters)

        with open(file_path, 'w') as file:
            json.dump(json_obj, file, indent=4)


if __name__ == '__main__':
    from input_json import InputJSON
    unbuilt = InputJSON.get_unbuilt_cal('input_24HT2.json')
    OutputJSON.output_unbuild_cal(unbuilt, 'output_24HT2.json')