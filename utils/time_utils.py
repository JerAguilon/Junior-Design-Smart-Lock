import datetime

import pytz


def get_current_datetime(timezone: pytz.timezone = None):
    if timezone:
        return datetime.datetime.now(timezone)
    else:
        return datetime.datetime.utcnow()


def get_current_time_ms():
    return int(get_current_datetime().strftime("%s")) * 1000


def get_current_day(timezone=pytz.timezone("US/Eastern")):
    local_dt = get_current_datetime(timezone)
    return local_dt.strftime("%A").upper()
