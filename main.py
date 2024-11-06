import cal
import input_json
import output_week


if __name__ == '__main__':
    unbuilt_calendar = input_json.InputJSON().get_unbuilt_cal('input_24HT2.json')
    calendar = unbuilt_calendar.build()
    print(unbuilt_calendar)
    output_week.OutputWeek(
        [
            cal.Time(2024, 11, 4, 0, 0),
            cal.Time(2024, 11, 5, 0, 0),
            cal.Time(2024, 11, 6, 0, 0),
            cal.Time(2024, 11, 7, 0, 0),
            cal.Time(2024, 11, 8, 0, 0),
            cal.Time(2024, 11, 9, 0, 0),
            cal.Time(2024, 11, 10, 0, 0),
        ],
        calendar,
        'output_week.html'     
    ).write_to_file()