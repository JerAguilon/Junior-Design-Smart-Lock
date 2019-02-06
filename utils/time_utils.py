import datetime


def get_current_datetime():
    return datetime.datetime.now()


def get_current_time_ms():
    return int(get_current_datetime().strftime("%s")) * 1000
