import requests

from cal import Calendar, Event
from cal_raw import SrcCal, Time


class SrcCalURL(SrcCal):
    def __init__(self, url: str):
        self.url = url
        self.cal = None

    @staticmethod
    def str_to_time(time: str):
        year = int(time[:4])
        month = int(time[4:6])
        day = int(time[6:8])
        hour = int(time[9:11])
        minute = int(time[11:13])
        return Time(year, month, day, hour, minute)

    def read_ics(self, file_raw: str):
        file_raw = file_raw.replace('\r\n ', '')
        calendars: list[Calendar]
        current_calendar_info: dict|None = None
        current_calendar_events: list[Event]|None = None
        current_event_info: dict|None = None
        started_cal = started_event = False
        
        for line in file_raw.split('\r\n'):
            if not line:
                continue

            field, content = line.split(':', 1)

            match field, content:
                case 'BEGIN', 'VCALENDAR':
                    current_calendar_events = []
                    current_calendar_info = {}
                    started_cal = True
                    break
                case 'BEGIN', 'VEVENT':
                    current_event_info = {}
                    started_event = True
                    break
                case 'END', 'VCALENDAR':
                    calendars.append(Calendar(current_calendar_events))
                    started_cal = False
                    break
                case 'END', 'VEVENT':
                    current_calendar_events.append(Event(current_event_info))
                    started_event = False
                    break
                case _:
                    if started_event:
                        current_event_info[field] = content
                    elif started_cal:
                        current_calendar_info[field] = content
            
    def fetch(self):
        """ loads in all content from the url """
        
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err}")  # Could be a 404 or 500 error, for example
        except requests.exceptions.ConnectionError as conn_err:
            raise Exception(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            raise Exception(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            raise Exception(f"An error occurred: {req_err}")

        file_raw = response.content.decode('utf-8')

        self.cal = self.read_ics(file_raw)

    def get_events():
        pass


if __name__ == '__main__':
    src_cal = SrcCalURL('https://cloud.timeedit.net/liu/web/schema/ri647QQQY80Zn1Q5368009Z8y6Z56.ics')
    src_cal.fetch()