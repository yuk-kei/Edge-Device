import random
from datetime import datetime, date
from random import randint

from model import SensorData


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


def generate_mock_values() -> dict[str, int]:
    """
    Generates a list of value arrays for every minute of the current date.
    """
    return {
        "value_a": random.randint(60, 90),
        "value_b": random.randint(70, 120),
    }


def gen_ts_data(values=None):
    dt = datetime.now()
    timestamp = dt.strftime("%m/%d/%Y %H:%M:%S")

    return SensorData(timestamp, values)
