import random
from datetime import datetime, timezone
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX
from adafruit_lsm6ds import Rate

from model import SensorData

# print(qwiic.list_devices())
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = ISM330DHCX(i2c, 0x6b)
sensor.accelerometer_data_rate = Rate.RATE_833_HZ


def gen_accelerometer_data():
    data1 = sensor.acceleration
    data2 = sensor.gyro

    return {
        "acc_x": data1[0],
        "acc_y": data1[1],
        "acc_z": data1[2],
        "gyro_x": data2[0],
        "gyro_y": data2[1],
        "gyro_z": data2[2],
    }


def gen_ts_data(values=None):
    dt = datetime.now(timezone.utc)
    timestamp = dt.strftime("%m/%d/%Y %H:%M:%S.%f")

    return SensorData(timestamp, values)


def gen_mock_temperature():
    return {
        "temperature": random.randint(20, 30),
    }


def generate_mock_values() -> dict[str, int]:
    """
    Generates a list of value arrays for every minute of the current date.
    """
    return {
        "value_a": random.randint(60, 90),
        "value_b": random.randint(70, 120),
    }
