import cal
import cal_raw
import src_cal
import input_json
import output_week


if __name__ == '__main__':
    unbuilt_school_calendar = input_json.InputJSON().get_unbuilt_cal('input_24HT2.json')
    unbuild_private_calendar = input_json.InputJSON().get_unbuilt_cal('input_private_calendar.json')
    school_calendar = unbuilt_school_calendar.build()
    private_calendar = unbuild_private_calendar.build()
    src_school_calendar = src_cal.SrcCalCalendar(school_calendar)
    src_private_calendar = src_cal.SrcCalCalendar(private_calendar)

    unbuilt_calendar = cal_raw.UnbuiltCal((src_school_calendar, src_private_calendar), [])
    calendar = unbuilt_calendar.build()

    output_week.OutputWeek(
        [
            cal.Time(2024, 11, 25, 0, 0),
            cal.Time(2024, 11, 26, 0, 0),
            cal.Time(2024, 11, 27, 0, 0),
            cal.Time(2024, 11, 28, 0, 0),
            cal.Time(2024, 11, 29, 0, 0),
            cal.Time(2024, 11, 30, 0, 0),
            cal.Time(2024, 12, 1, 0, 0),
        ],
        calendar,
        'output_week.html'     
    ).write_to_file()