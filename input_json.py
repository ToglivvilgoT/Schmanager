import json
from typing import Iterable

from cal_raw import UnbuiltCal
import src_cal
import filter


class InputJSON():
    @staticmethod
    def _read_file(file_path: str) -> any:
        """ returns the parsed data from file at file_path
        file_path should be a path to a json file
        raises ValueError if file cant be opened or cant be parsed """
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except:
            raise ValueError(f'invalid file_name "{file_path}", wasnt able to read or parse')
        
    @staticmethod
    def _get_src_cals(data) -> Iterable[src_cal.SrcCal]:
        """ returns the src_cals from data
        data should be a parsed json file """
        src_cals = []
        src_cals_list = data['src_cals'].split()
        i = 0
        while i < len(src_cals_list):
            match src_cals_list[i]:
                case 'url':
                    src_cals.append(src_cal.SrcCalURL(src_cals_list[i+1]))
                    i += 3

        return src_cals
    
    @classmethod
    def _get_filters(cls, data) -> Iterable[filter.Filter]:
        """ returns the filters from data
        data should be a parsed json file """

    @classmethod
    def get_unbuilt_cal(cls, file_name: str) -> UnbuiltCal:
        data = cls._read_file(file_name)
        src_cals = cls._get_src_cals(data)
        filters = cls._get_filters(data)
        return UnbuiltCal(src_cals, filters)



if __name__ == '__main__':
    print(InputJSON('input_24HT1.json').get_unbuilt_cal())