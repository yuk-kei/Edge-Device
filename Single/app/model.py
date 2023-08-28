import json
import logging
import threading
from dataclasses import dataclass
from time import sleep

import requests
from confluent_kafka import Producer, KafkaError

from Single import config
from Single.config import PRODUCER_CONF, TOPIC_NAME

logger = logging.getLogger("Device Producer: ")


@dataclass
class SensorData:
    timestamp: str
    values: dict[str, int]


from .data_gen import generate_mock_values, gen_ts_data  # , gen_accelerometer_data


class Device(threading.Thread):
    def __init__(self, name, ip, port, device_id=None, type=None, category=None, location=None, status=None,
                 data_source=None, rate=1):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.producer = Producer(PRODUCER_CONF)
        self._stop_event = threading.Event()  # flag to stop the thread
        self._pause_event = threading.Event()  # flag to pause the thread
        self._pause_event.set()  # Set to True
        self.name = name
        self.category = category
        self.device_id = device_id
        self.type = type
        self.location = location
        self.status = status
        self.rate = rate
        self.topic_name = TOPIC_NAME

    def data_source(self):
        return generate_mock_values()

    def emit_data(self):

        # TODO: Overide this method to add real data here
        mock_data = self.data_source()

        ts_data = gen_ts_data(mock_data)

        key = self.name
        message = json.dumps(self.dump_to_infuxdb(ts_data)).encode('utf-8')

        try:
            self.producer.produce(
                self.topic_name,
                key=key,

                value=message,
                callback=self.delivery_report
            )
            print(f"Sent data: {message}")
        except KafkaError as e:
            logger.error(f"Kafka error: {e}")

    def delivery_report(self, err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
            pass

    def flush(self):
        self.producer.flush()

    def poll(self):
        self.producer.poll(0)

    def dump_to_infuxdb(self, ts_data):

        return {
            "device_name": self.name,
            "id": self.device_id,
            "time": ts_data.timestamp,
            "values": ts_data.values
        }

    def register(self):
        try:
            response = requests.post(url=config.REGISTRATOR_URL,
                                     json={"device_id": self.device_id, "name": self.name, "type": self.type,
                                           "location": self.location, "status": self.status, "ip_address": self.ip,
                                           "category": self.category, "port": self.port})
            if 200 <= response.status_code < 300:
                data = response.json()
                self.device_id = data.get("device_id")
                logger.info(f"Device registered with id: {self.device_id}")
            else:
                print(response.status_code)
                logger.error(f"Error registering device: {response.status_code}")
        except Exception as e:
            print(e)
            logger.error(f"Error registering device: {e}")

    def change_sampling_rate(self, rate):
        self.rate = rate

    def run(self):
        if self.device_id is None:
            self.register()
        self.status = "running"
        message_count = 0
        try:
            while not self._stop_event.is_set():  # check stop flag before sending data
                self.emit_data()  # add real data here
                message_count += 1
                print(f"Sent {message_count} messages")
                # self.flush()
                self.poll()
                sleep(self.rate)
                self._pause_event.wait()  # wait until resume is called
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            self._stop_event.set()

    def pause(self):
        self._pause_event.clear()
        self.status = "paused"

    def resume(self):
        self._pause_event.set()
        self.status = "running"

    def stop(self):
        self._stop_event.set()
        sleep(1)
        self.status = "stopped"
        self.flush()
        self.join()


"""------------Different types of devices------------"""


class Accelerometer(Device):

    def data_source(self):
        pass

    # def emit_data(self):
    #     acc_data = gen_accelerometer_data
    #     ts_data = gen_ts_data(acc_data)
    #     key = self.name
    #     message = json.dumps(self.dump_to_infuxdb(ts_data)).encode('utf-8')
    #
    #     try:
    #         self.producer.produce(
    #             self.topic_name,
    #             key=key,
    #             value=message,
    #         )
    #         print(f"Sent data: {message}")
    #     except KafkaError as e:
    #         logger.error(f"Kafka error: {e}")
