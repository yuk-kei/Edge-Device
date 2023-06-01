from dataclasses import dataclass


@dataclass
class SensorData:
    timestamp: str
    values: dict[str, int]


class Sensor:
    def __init__(self, name, sensor_id):
        self.name = name
        self.sensor_id = sensor_id
        self.tags = {
            "owner": "CalPlug",
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
