import json
import logging
import random
import threading
from datetime import datetime
from time import sleep

from confluent_kafka import Producer, KafkaError
from flask import Flask

from config import Config, PRODUCER_CONF
from model import SensorData, Device

app = Flask(__name__)

logger = logging.getLogger("Sensor Server: ")


@app.route('/api/v1/sensor/', methods=['GET', 'POST'])
def command():  # put application's code here
    return 'Hello World!'


device_1 = Device("Device 1", "localhost", 9001, type="sensor", location="calit2", status="active")
device_1.start()


def main():
    logger.info("Starting producer")
    app.run(port=9001)


if __name__ == '__main__':
    # produce_data()
    main()
