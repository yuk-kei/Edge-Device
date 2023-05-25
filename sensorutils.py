from datetime import datetime, date
from random import randint


def gen_timestamps() -> str:
    """
    Generates a list of timestamps for every minute of the current date.

    Returns:
        list: Unix epoch formatted timestamps for every minute of the current date.
    """
    month = datetime.now().month
    day = datetime.now().day
    year = datetime.now().year
    hour = datetime.now().hour
    minute = datetime.now().minute
    second = datetime.now().second
    microsecond = datetime.now().microsecond
    current_time_str = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(
        second) + "." + str(microsecond)
    # current_time = datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S.%f")
    # current_time_str_in_ms = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    # timestamp_unix = int(datetime.strptime(current_time_str_in_ms, "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000)

    return current_time_str
