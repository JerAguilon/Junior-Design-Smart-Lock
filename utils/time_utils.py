import datetime

import pytz


def get_current_datetime(timezone: pytz.timezone = None) -> datetime.datetime:
    if timezone:
        return datetime.datetime.now(timezone)
    else:
        return datetime.datetime.utcnow()


def get_current_time_ms() -> int:
    return int(get_current_datetime().strftime("%s")) * 1000


def get_current_day(timezone=pytz.timezone("US/Eastern")) -> str:
    local_dt = get_current_datetime(timezone)
    return local_dt.strftime("%A").upper()


def get_current_time(timezone=pytz.timezone("US/Eastern")) -> datetime.time:
    return get_current_datetime(timezone).time()


def is_time_between(
        begin_time,
        end_time,
        timezone=pytz.timezone("US/Eastern")):
    # If check time is not given, default to current UTC time
    check_time = get_current_time(timezone)
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time
