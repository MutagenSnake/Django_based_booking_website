import re
import pytz
from datetime import datetime, date
from collections import namedtuple

def form_to_datetime(date):
    time_listed = re.findall(r"\d+", date)
    print(f'Time_listed {time_listed}')
    datetime_format = datetime(int(time_listed[0]), int(time_listed[1]), int(time_listed[2]),
                                        int(time_listed[3]), int(time_listed[4]))
    aware_datetime_format = pytz.utc.localize(datetime_format)

    print(f'returning daterime {aware_datetime_format}')
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

def past_checker(date):
    time_now = datetime.now()
    time_now_aware = pytz.utc.localize(time_now)
    print(f'From pas checker{date}')
    if time_now_aware > date:
        return True
    else:
        return False

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))