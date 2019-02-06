import datetime

from pytz import timezone


def get_current_datetime():
    return datetime.datetime.utcnow()


def get_current_time_ms():
    return int(get_current_datetime().strftime("%s")) * 1000


def get_current_day(timezone=timezone("US/Eastern")):
    local_dt = timezone.localize(
        get_current_datetime()
    )
    return local_dt.strftime("%A").upper()
