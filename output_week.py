import cal
import cal_raw
import filter
import pattern
import action
import src_cal


class OutputWeek:
    def __init__(self, week_range: list[cal.Time], calendar: cal.Calendar, file_name: str = 'output_week.html'):
        self.week_range = week_range

        patrn = pattern.PatternNot(pattern.PatternInTime(week_range[0], week_range[-1]))
        act = action.ActionRemoveEvent()
        filtr = filter.Filter(patrn, act)
        src_calendar = src_cal.SrcCalCalendar(calendar)
        self.calendar = cal_raw.UnbuiltCal([src_calendar], [filtr]).build()

        self.file_name = file_name

    def _clear_file(self) -> None:
        """ clears the file of any content, if file doesnt exist, file is created. """
        with open(self.file_name, 'w') as file:
            file.write('')

    def _write(self, text: str, tabs: int = 0, new_line: bool = False) -> None:
        """ writes text to file \n
        writes tabs amount of tabs before text \n
        if new_line, then writes a \\n at end of text """
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write('\t' * tabs + text + '\n' * new_line)

    def _write_tag(
            self, 
            tag_name: str, 
            properties: dict[str, str] = {}, 
            closed = False, 
            tabs: int = 0, 
            new_line: bool = False
        ) -> None:
        """ writes html tag to file \n
        tag_name is the html tag eg. 'div', 'p', 'h3', etc. \n
        properties are key-value pairs inside the tag like {'style': 'width: 10px;', 'class'='my-class'} \n
        if closed is True, a slash '/' is writen before tag_name to close the element \n
        writes tabs amount of tabs before tag \n
        if new_line, then writes a \\n at end of tag """
        tag = '<'
        if closed:
            tag += '/'
        tag += tag_name
        for key, val in properties.items():
            tag += ' ' + key + '="' + val + '"'
        tag += '>'

        self._write(tag, tabs, new_line)

    def _write_open_closed_tag(
            self, 
            tag_name: str, 
            properties: dict[str, str] = {}, 
            content: str = '', 
            tabs: int = 0,
            new_line: bool = True
        ) -> None:
        """ writes html open tag, then content and finally a closing tag on one line \n
        tag_name is the html tag eg. 'div', 'p', 'h3', etc. \n
        properties are key-value pairs inside the tag like {'style': 'width: 10px;', 'class'='my-class'} \n
        content is the text writen between opening and closing tags \n
        writes tabs amount of tabs before tags \n
        if new_line, then writes a \\n at end of tags """
        self._write_tag(tag_name, properties, tabs=tabs)
        self._write(content)
        self._write_tag(tag_name, closed=True, new_line=new_line)

    def _write_header(self) -> None:
        """ writes the Doctype and opening html tags """
        self._write_tag('!Doctype html', new_line=True)
        self._write_tag('html', {'lang': 'sv'}, new_line=True)

    def _write_head(self, title: str|None = None, style_sheets: list[str] = []) -> None:
        """ writes the head of the html document \n
        title is the title inbetween the title tags \n
        style_sheets is a list of all style sheets that should be linked to the document """
        self._write_tag('head', new_line=True)
        self._write_tag('meta', {'charset': 'UTF-8'}, tabs=1, new_line=True)
        self._write_open_closed_tag('title', content=title, tabs=1)

        for style_sheet in style_sheets:
            self._write_open_closed_tag('link', {'rel': 'stylesheet', 'href': style_sheet}, tabs=1)

        self._write_tag('head', closed=True, new_line=True)

    def _write_day_headers(
            self,
            properties = {'class': 'day-header'},
            contents = ('Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lördag', 'Söndag'),
            tabs: int = 0,
        ) -> None:
        """ writes out 7 divs with content from contents and properties = properties """
        for content in contents:
            self._write_open_closed_tag('h2', properties, content, tabs)

    def _write_time_sidebar(
            self,
            container_properties = {'class': 'time-sidebar-left'},
            time_properties = {'class': 'time'},
            hour_range = (0, 24),
            tabs: int = 0,
    ) -> None:
        self._write_tag('div', container_properties, tabs=tabs, new_line=True)
        tabs += 1
        for hour in range(*hour_range):
            self._write_open_closed_tag('p', time_properties, f'{"0" * (hour < 10)}{hour}:00', tabs)
        tabs -= 1
        self._write_tag('div', closed=True, tabs=tabs, new_line=True)

    def _write_before_events(self) -> None:
        """ writes all html that goes before calendar events 
        returns how many tabs are on the last line """
        self._clear_file()

        self._write_header()
        self._write_head('Schema', ['output_week.css'])

        tabs = 0

        self._write_tag('body', tabs=tabs, new_line=True)
        tabs += 1
        
        self._write_tag('div', {'class': 'schedule'}, tabs=tabs, new_line=True)
        tabs += 1
        
        self._write_tag('div', {'class': 'week'}, tabs=tabs, new_line=True)
        tabs += 1
        
        # write day headers
        self._write_open_closed_tag('div', tabs=tabs)
        self._write('', tabs=tabs, new_line=True)
        self._write_day_headers(tabs=tabs)
        self._write('', tabs=tabs, new_line=True)
        self._write_open_closed_tag('div', tabs=tabs)
        self._write('', tabs=tabs, new_line=True)

        # write left timebar
        self._write_time_sidebar(tabs=tabs)
        self._write('', tabs=tabs, new_line=True)

        return tabs
    
    def _get_sorted_events(self) -> dict[int, list[cal.Event]]:
        """ returns a dict with the day as key and all events taking place that day as the value """
        sorted_events = {time.day: [] for time in self.week_range}
        for event in self.calendar.events:
            try:
                sorted_events[event.get_start_time().day].append(event)
            except KeyError:
                pass

        return sorted_events            

    def _get_event_offset(self, start_time: cal.Time):
        return 100 * ((start_time.hour + (start_time.minute / 60)) / 24)

    def _get_event_height(self, start_time: cal.Time, end_time: cal.Time):
        start = start_time.hour + (start_time.minute / 60)
        end = end_time.hour + (end_time.minute / 60)
        return 100 * ((end - start) / 24)
    
    def _write_one_day_events(self, events: list[cal.Event], tabs: int = 0):
        """ writes out all events taking place during one day """
        self._write_tag('div', {'class': 'event-container'}, tabs=tabs, new_line=True)
        tabs += 1

        for event in events:
            start_time = event.get_start_time()
            start_time_str = f'{"0" * (start_time.hour < 10)}{start_time.hour}:{"0" * (start_time.minute < 10)}{start_time.minute}'
            end_time = event.get_end_time()
            end_time_str = f'{"0" * (end_time.hour < 10)}{end_time.hour}:{"0" * (end_time.minute < 10)}{end_time.minute}'

            offset = self._get_event_offset(start_time)
            height = self._get_event_height(start_time, end_time)

            self._write_tag(
                'div', 
                {'class': 'event', 'style': f'top: {offset}%; height: {height}%;'}, 
                tabs=tabs, 
                new_line=True
            )
            tabs += 1

            try:
                self._write_open_closed_tag(
                    'h3', 
                    {'class': 'event-header'}, 
                    event.get_field_text('SUMMARY'), 
                    tabs
                )
            except KeyError:
                pass
            try:
                self._write_open_closed_tag(
                    'p', 
                    {'class': 'event-time'},
                    f'{start_time_str}-{end_time_str}',
                    tabs
                )
            except:
                pass
            try:
                self._write_open_closed_tag(
                    'p',
                    {'class': 'event-location'},
                    event.get_field_text('LOCATION'),
                    tabs
                )
            except KeyError:
                pass
            try:
                self._write_open_closed_tag(
                    'p',
                    {'class': 'event-description'},
                    event.get_field_text('DESCRIPTION'),
                    tabs
                )
            except KeyError:
                pass

            tabs -= 1
            self._write_tag('div', closed=True, tabs=tabs, new_line=True)

        tabs -= 1
        self._write_tag('div', closed=True, tabs=tabs, new_line=True)
    
    def _write_events(self, tabs: int):
        sorted_events = self._get_sorted_events()
        for events in sorted_events.values():
            self._write_one_day_events(events, tabs)
    
    def _write_after_events(self, tabs: int):
        tabs -= 1
        self._write_tag('div', closed=True, tabs=tabs, new_line=True)

        tabs -= 1
        self._write_tag('div', closed=True, tabs=tabs, new_line=True)

        tabs -= 1
        self._write_tag('body', closed=True, new_line=True)

        return tabs


    def write_to_file(self) -> None:
        """ writes out the week of events to the html file """
        tabs = self._write_before_events()

        self._write_events(tabs)

        tabs = self._write_after_events(tabs)

        if tabs != 0:
            if tabs > 0:
                print('you forgot to close a tag')
            else:
                print('you closed one too many tags')


if __name__ == '__main__':
    output = OutputWeek(None, None, None)
    output.write_to_file()