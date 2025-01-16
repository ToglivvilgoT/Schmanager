import json
from typing import Iterable

from cal_raw import UnbuiltCal
import cal
import src_cal
import filter
import pattern
import action


class InputJSON():
    @staticmethod
    def _read_file(file_path: str) -> any:
        """ returns the parsed data from file at file_path
        file_path should be a path to a json file
        raises ValueError if file cant be opened or cant be parsed """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            raise ValueError(f'invalid file_name "{file_path}", wasnt able to read or parse')
        
    @staticmethod
    def _get_src_cals(data) -> Iterable[src_cal.SrcCal]:
        """ returns the src_cals from data
        data should be a parsed json file """
        src_cals = []
        src_cals_list = data['src_cals']
        i = 0
        while i < len(src_cals_list):
            match src_cals_list[i]:
                case 'url':
                    src_cals.append(src_cal.SrcCalURL(src_cals_list[i+1]))
                    i += 3

        return src_cals
    
    @staticmethod
    def _parse_pattern(pat: list[str]) -> pattern.Pattern:
        """ parses a pattern list of strings and returns the parsed pattern """
        def parse_strings(patrn: list[str], index: int) -> tuple[list[str], int]:
            """Returns all strings from patern at index until next '/' prefixed keyword appears.
            Also returns the index dirrectly after the '/' prefixed keyword.
            """
            words = []
            while index < len(patrn):
                if patrn[index][0] == '/':
                    return words, index + 1
                else:
                    words.append(patrn[index])
                    index += 1
            raise ValueError('No "/" prefixed keyword was found in patrn')

        def parse_recursive(patrn: list[str], index: int) -> tuple[Iterable[pattern.Pattern], int]:
            """ parses all patterns from index until end of patrn or
            until '/' indexed keyword without beginning keyword is found 
            returns parsed patterns and index after last parsed keyword """
            patrns = []
            while index < len(patrn):
                match patrn[index]:
                    case 'or':
                        or_patrns, index = parse_recursive(patrn, index + 1)
                        patrns.append(pattern.PatternOr(or_patrns))
                        index += 1

                    case 'and':
                        and_patrns, index = parse_recursive(patrn, index + 1)
                        patrns.append(pattern.PatternAnd(and_patrns))
                        index += 1

                    case 'not':
                        not_patrns, index = parse_recursive(patrn, index + 1)
                        patrns.append(pattern.PatternNot(not_patrns[0]))
                        index += 1

                    case 'has_text':
                        text = patrn[index + 1]
                        fields, index = parse_strings(patrn, index + 2)
                        if fields == []:
                            fields = None
                        patrns.append(pattern.PatternHasText(text, fields))

                    case 'in_time':
                        patrns.append(pattern.PatternInTime(
                            *map(cal.Time.str2time, patrn[index+1:index+3])
                        ))
                        index += 3

                    case _:
                        break

            return patrns, index
        
        return parse_recursive(pat, 0)[0][0]
        
    @staticmethod
    def _parse_action(act: list[str]):
        """ returns the parsed act """
        def parse_recursive(acts: list[str], index: int) -> tuple[list[action.Action], int]:
            """ returns a list of all parsed actions in act from index 
            to end of act or until not opened closed tag 
            also returns the index after the last parsed action """
            actions = []
            while index < len(acts):
                match acts[index]:
                    case 'add_event':
                        actions.append(action.ActionAddEvent(cal.Event(acts[index+1])))
                        index += 2
                    case 'remove_event':
                        actions.append(action.ActionRemoveEvent())
                        index += 1
                    case 'remove_field':
                        actions.append(action.ActionRemoveField(acts[index+1]))
                        index += 2
                    case 'write_field':
                        actions.append(action.ActionWriteField(acts[index+1], acts[index+2]))
                        index += 3
                    case 'multiple':
                        new_acts, index = parse_recursive(acts, index+1)
                        actions.append(action.ActionMultiple(new_acts))
                    case '/multiple':
                        return actions, index + 1
                    
            return actions, index
        
        return parse_recursive(act, 0)[0][0]
                
        
    
    @classmethod
    def _get_filters(cls, data) -> Iterable[filter.Filter]:
        """ returns the filters from data
        data should be a parsed json file """
        filters = []
        for fltr in data['filters']:
            pat = cls._parse_pattern(fltr['pattern'])
            act = cls._parse_action(fltr['action'])
            filters.append(filter.Filter(pat, act))

        return filters

    @classmethod
    def get_unbuilt_cal(cls, file_name: str) -> UnbuiltCal:
        data = cls._read_file(file_name)
        src_cals = cls._get_src_cals(data)
        filters = cls._get_filters(data)
        return UnbuiltCal(src_cals, filters)


if __name__ == '__main__':
    unbuilt_cal = InputJSON().get_unbuilt_cal('input_24HT2.json')
    print(unbuilt_cal)
    #print(unbuilt_cal.build())