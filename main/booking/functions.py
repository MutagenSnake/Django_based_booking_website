import re
import pytz
from datetime import datetime
from collections import namedtuple

def form_to_datetime(date):
    time_listed = re.findall(r"\d+", date)
    datetime_format = datetime(int(time_listed[0]), int(time_listed[1]), int(time_listed[2]),
                                        int(time_listed[3]), int(time_listed[4]))
    aware_datetime_format = pytz.utc.localize(datetime_format)

    return aware_datetime_format

def overlap_checker(date1_start, date1_end, date2_start, date2_end):
    Range = namedtuple('Range', ['start', 'end'])

    range1 = Range(start=date1_start, end=date1_end)
    range2 = Range(start=date2_start, end=date2_end)

    latest_start = max(range1.start, range2.start)
    earliest_end = min(range1.end, range2.end)

    delta = (earliest_end - latest_start).total_seconds()

    overlapping_seconds = max(0, delta)

    if overlapping_seconds > 0:
        return True
    else:
        return False