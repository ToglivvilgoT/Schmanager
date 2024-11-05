import cal
import input_json
import output_week


if __name__ == '__main__':
    unbuilt_calendar = input_json.InputJSON().get_unbuilt_cal('input_24HT2.json')
    calendar = unbuilt_calendar.build()
    output_week.OutputWeek(
        [
            cal.Time(2024, 11, 11, 0, 0),
            cal.Time(2024, 11, 12, 0, 0),
            cal.Time(2024, 11, 13, 0, 0),
            cal.Time(2024, 11, 14, 0, 0),
            cal.Time(2024, 11, 15, 0, 0),
            cal.Time(2024, 11, 16, 0, 0),
            cal.Time(2024, 11, 17, 0, 0),
        ],
        calendar,
        'output_week.html'     
    ).write_to_file()