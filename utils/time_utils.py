import datetime

<<<<<<< HEAD
import pytz


def get_current_datetime(timezone: pytz.timezone = None):
    if timezone:
        return datetime.datetime.now(timezone)
    else:
        return datetime.datetime.utcnow()
=======
from pytz import timezone


def get_current_datetime():
    return datetime.datetime.utcnow()
>>>>>>> 0f15754c8d897d4b88c90e712a0ce1d970fd842c


def get_current_time_ms():
    return int(get_current_datetime().strftime("%s")) * 1000


<<<<<<< HEAD
def get_current_day(timezone=pytz.timezone("US/Eastern")):
    local_dt = get_current_datetime(timezone)
=======
def get_current_day(timezone=timezone("US/Eastern")):
    local_dt = timezone.localize(
        get_current_datetime()
    )
>>>>>>> 0f15754c8d897d4b88c90e712a0ce1d970fd842c
    return local_dt.strftime("%A").upper()
