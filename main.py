import cal
import cal_input
import pattern
import action
import cal_raw


if __name__ == '__main__':
    src_cals = [cal_input.SrcCalURL('https://cloud.timeedit.net/liu/web/schema/ri647QQQY80Zn1Q5368009Z8y6Z56.ics')]
    filters = [
        cal_raw.Filter(
            pattern.PatternNot(
                pattern.PatternInTime(
                    cal.Time(2024, 10, 21, 0, 0),
                    cal.Time(2024, 10, 28, 0, 0),
                )
            ),
            action.ActionRemoveEvent()
        )
    ]
    unbuilt_calendar = cal_raw.UnbuiltCal(src_cals, filters)
    calendar = unbuilt_calendar.build()
    print(calendar)