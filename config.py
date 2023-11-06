import os
from dotenv import load_dotenv

load_dotenv()
REGISTRATOR_URL = os.environ.get('REGISTRATOR_URL')
PRODUCER_CONF = {'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVERS')}
TOPIC_NAME = os.environ.get('TOPIC_NAME')
