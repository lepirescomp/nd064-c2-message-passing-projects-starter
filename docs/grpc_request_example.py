import grpc
import LocationEvent_pb2
import LocationEvent_pb2_grpc

channel = grpc.insecure_channel("localhost:30003")
stub = LocationEvent_pb2_grpc.ItemServiceStub(channel)

#payload
location = LocationEvent_pb2.LocationEventMessage(
    personId=1,
    latitude=1,
    longitude=1
   
)

response = stub.Create(location)