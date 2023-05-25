import json
import logging
import random
import threading
from dataclasses import dataclass
from datetime import date
from time import sleep

from confluent_kafka import Producer, Consumer, KafkaError
from flask import Flask

from sensorutils import gen_timestamps

app = Flask(__name__)


@dataclass
class Config:
    capture_output: bool
    sensor_id: str
    topic_name: str
    output_file: str = False
    rate: int = 0.1


@dataclass
class SensorData:
    timestamp: str
    values: list[int]


conf = {'bootstrap.servers': '128.195.151.182:9392'}

sensor_config = Config(capture_output=False, sensor_id="sensor1", topic_name="test")
logger = logging.getLogger(f"{sensor_config.sensor_id} Producer")


@app.route('/api/v1/sensor', methods=['GET', 'POST'])
def command():  # put application's code here
    return 'Hello World!'


def generate_value_arrays() -> list[int]:
    """
    Generates a list of value arrays for every minute of the current date.

    Returns:
        list: Value arrays for every minute of the current date.
    """
    l = [0, 0, 0, 0, 1, 0, 1, 0, 2, 3]
    c = random.choice(l)
    n = None
    if c == 0:
        n = random.randrange(60, 100)
    elif c == 1:
        n = random.randrange(10, 59)
    elif c == 2:
        n = random.randrange(101, 120)
    else:
        n = random.randrange(200, 500)
    return [random.randint(0, 100) for _ in range(60)]


def gen_sensor_data() -> SensorData:
    """_summary_

    Returns:
        list[RawSensorData]: Generates the sensor data.
    """
    timestamp = gen_timestamps()
    return SensorData(timestamp, values=generate_value_arrays())


def produce_data() -> None:
    """
    Produces data to Kafka.
    """
    producer = Producer(conf)
    print("Producer started")
    while True:
        try:
            record = gen_sensor_data()
            if sensor_config.capture_output:
                print("Generating sensor data...")

            key = sensor_config.sensor_id.encode('utf-8')
            message = {"timestamp": record.timestamp, "values": record.values}
            value = json.dumps(message).encode('utf-8')

            producer.produce(sensor_config.topic_name, key=key, value=value)

            sleep(sensor_config.rate)

        except KafkaError as e:
            logger.error(f"Kafka error: {e}")


def main():
    logger.info("Starting producer")

    t1 = threading.Thread(target=produce_data)
    t1.start()
    app.run(port=9001)


if __name__ == '__main__':
    # produce_data()
    main()
