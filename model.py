import json
import logging
import os
import threading
from dataclasses import dataclass

import requests
from confluent_kafka import Producer, KafkaError

from config import PRODUCER_CONF

logger = logging.getLogger("Device Producer: ")


@dataclass
class SensorData:
    timestamp: str
    values: dict[str, int]


from sensorutils import generate_mock_values, gen_ts_data


class Sensor:
    def __init__(self, name, sensor_id):
        self.name = name
        self.sensor_id = sensor_id
        self.tags = {
            "owner": "Calit2",
            "machine_id": "None",
        }
        self.data = None

    def set_sensor_data(self, data: SensorData):
        self.data = data

    def set_tags(self, tags):
        self.tags = tags

    def dump_data(self):
        return {
            "sensor_name": self.name,
            "sensor_id": self.sensor_id,
            "tags": self.tags,
            "time": self.data.timestamp,
            "fields": self.data.values
        }


class Device(threading.Thread):
    def __init__(self, name, ip, port, device_id=None, type=None, location=None, status=None, sleep_time=5):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sleep_time = sleep_time
        self.producer = Producer(PRODUCER_CONF)
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self.name = name
        self.device_id = device_id
        self.type = type
        self.location = location
        self.status = status
        self.rate = 0.1
        self.topic_name = "test"

    def emit_data(self, mode="mock", ts_data=None):

        if ts_data is None and mode == "mock":
            mock_data = generate_mock_values()
            ts_data = gen_ts_data(mock_data)

        key = self.name
        message = json.dumps(self.dump_to_infuxdb(ts_data)).encode('utf-8')

        try:
            self.producer.produce(
                self.topic_name,
                key=key,
                value=message,
            )
        except KafkaError as e:
            logger.error(f"Kafka error: {e}")

    def flush(self):
        self.producer.flush()

    def dump_to_infuxdb(self, ts_data):

        info = {
            "type": self.type,
            "id": self.device_id,
            "status": self.status,
        }
        return {
            "device_name": self.name,
            "info": info,
            "time": ts_data.timestamp,
            "values": ts_data.values
        }

    def run(self):
        # if self.device_id is None:
        #     self.register()

        try:
            while not self._stop_event.is_set() and not self._pause_event.is_set():
                self.emit_data()
                self.flush()
                self._pause_event.wait(self.rate)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            self._stop_event.set()

    def register(self):
        url = os.environ.get("REGISTRATOR_URL")
        try:
            response = requests.post(url, json={"device_id": self.device_id, "name": self.name, "type": self.type,
                                                "location": self.location, "status": self.status, "ip_address": self.ip,
                                                "port": self.port})
            if response.status_code == 200:  # Assuming a successful response with status code 200
                data = response.json()
                self.device_id = data.get("device_id")
                logger.info(f"Device registered with id: {self.device_id}")
            else:
                logger.error(f"Error registering device: {response.status_code}")
        except Exception as e:
            print(e)

    def stop(self):
        self._stop_event.set()

    def pause(self):
        self._pause_event.set()

    def resume(self):
        self._pause_event.clear()
