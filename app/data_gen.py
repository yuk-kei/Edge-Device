import random
from datetime import datetime, timezone
from .model import SensorData

"""
Data generation utilities for device.

This module allows to write real data generation logic for the device.

Functions:
---------
generate_data() -> None:
    A placeholder for real data generation logic.
gen_ts_data(values: dict) -> SensorData:
    Generate timestamped data.
generate_mock_values() -> dict[str, int]:
    Produce mock sensor readings.
"""


def generate_data():
    """
    Your data generation logic goes here.
    """
    return generate_mock_values()


def gen_ts_data(values=None):
    """
    Generate timestamped data.

    :param values: A dictionary of sensor values.
    :return: A SensorData DTO.
    """
    dt = datetime.now(timezone.utc)
    timestamp = dt.strftime("%m/%d/%Y %H:%M:%S.%f")

    return SensorData(timestamp, values)


def generate_mock_values() -> dict[str, int]:
    """
    Generates a list of value arrays for every minute of the current date.
    """
    return {
        "value_a": random.randint(60, 90),
        "value_b": random.randint(70, 120),
    }
