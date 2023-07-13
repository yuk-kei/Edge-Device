from dataclasses import dataclass


@dataclass
class Config:
    device_id: str
    capture_output: bool
    topic_name: str
    output_file: str = False
    rate: float = 0.1


PRODUCER_CONF = {'bootstrap.servers': '128.195.151.182:9392'}
TOPIC_NAME = "test"