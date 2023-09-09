
from datetime import datetime
from json import loads, dumps
from kafka import KafkaConsumer
from os import environ
from requests import post
from urllib.parse import urljoin
from logging import getLogger, INFO, StreamHandler


KAFKA_TOPIC = environ["KAFKA_TOPIC"]
KAFKA_URL = environ["KAFKA_URL"]
UDACONNECT_API_URL = environ["UDACONNECT_API_URL"]

logger = getLogger(__name__)
logger.setLevel(INFO)
logger.addHandler(StreamHandler())

logger.info(f"Starting consumer with {KAFKA_URL}, subscribing to {KAFKA_URL}")
consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_URL])

while True:
    for location in consumer:
        message = location.value.decode('utf-8')
        logger.info(f"{message}")
        try:
            url = urljoin(UDACONNECT_API_URL, "api/locations")
            message_dict = loads(message)
            post_message = {
                "person_id": message_dict["person_id"],
                "longitude": f'{message_dict["longitude"]:.7f}',
                "latitude": f'{message_dict["latitude"]:.7f}',
                "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            result = post(url, json=post_message)
        except Exception as e:
            logger.error(f"Post of location failed with error: {e}")