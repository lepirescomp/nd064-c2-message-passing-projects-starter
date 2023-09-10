import time
from concurrent import futures

import grpc
import LocationEvent_pb2
import LocationEvent_pb2_grpc
import logging
import json
from os import environ
from kafka import KafkaProducer


kafka_url = environ["KAFKA_URL"]
kafka_topic = environ["KAFKA_TOPIC"]

class LocationEventServicer(LocationEvent_pb2_grpc.ItemServiceServicer):

        def Create(self, request, context):
            request_value = {
                 "personId": request.personId,
                 "latitude": request.latitude,
                 "longitude": request.longitude,
              }
            logging.info('processing entity ', request_value)

            producer = KafkaProducer(bootstrap_servers=kafka_url,api_version=(0, 10, 0),value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            future=producer.send(kafka_topic,request_value)
            producer.flush()
            return LocationEvent_pb2.LocationEventMessage(**request_value)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
LocationEvent_pb2_grpc.add_ItemServiceServicer_to_server(LocationEventServicer(), server)
server.add_insecure_port("[::]:5005")
server.start()


try:
    while True:
        time.sleep(400)
except KeyboardInterrupt:
    server.stop(0)