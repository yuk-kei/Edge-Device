import os
from dotenv import load_dotenv

load_dotenv()
REGISTRATOR_URL = os.environ.get('REGISTRATOR_URL', "http://128.195.151.182:9002/api/devices/register")
PRODUCER_CONF = {'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVERS')}
TOPIC_NAME = os.environ.get('TOPIC_NAME')
