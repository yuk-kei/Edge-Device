import json
import logging
import random
import threading
from datetime import datetime
from time import sleep

from confluent_kafka import Producer, KafkaError
from flask import Flask

from config import Config, PRODUCER_CONF
from model import SensorData, Sensor

app = Flask(__name__)

app_config = Config("sensor_01", capture_output=False, topic_name="test", rate=0.1)
logger = logging.getLogger(f"{app_config.device_id} Producer")


@app.route('/api/v1/sensor', methods=['GET', 'POST'])
def command():  # put application's code here
    return 'Hello World!'


def generate_value_arrays() -> dict[str, int]:
    """
    Generates a list of value arrays for every minute of the current date.
    """
    return {
        "value_a": random.randint(60, 90),
        "value_b": random.randint(70, 120),
    }


def gen_sensor_data() -> SensorData:
    """_summary_

    Returns:
        list[RawSensorData]: Generates the sensor data.
    """
    dt = datetime.now()
    timestamp = dt.strftime("%m/%d/%Y %H:%M:%S")

    return SensorData(timestamp, values=generate_value_arrays())


def produce_data() -> None:
    """
    Produces data to Kafka.
    """
    producer = Producer(PRODUCER_CONF)
    print("Producer started")
    sensor = Sensor("mock", "sensor_01")

    while True:
        try:
            if app_config.capture_output:
                print("Generating sensor data...")

            sensor_data = gen_sensor_data()
            sensor.set_sensor_data(sensor_data)
            key = app_config.device_id
            message = sensor.dump_data()
            value = json.dumps(message).encode('utf-8')

            producer.produce(app_config.topic_name, key=key, value=value)

            sleep(app_config.rate)

        except KafkaError as e:
            logger.error(f"Kafka error: {e}")


def main():
    logger.info("Starting producer")
    # produce_data()
    t1 = threading.Thread(target=produce_data)
    t1.start()
    app.run(port=9001)


if __name__ == '__main__':
    # produce_data()
    main()
