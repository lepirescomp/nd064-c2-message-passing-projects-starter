# Setup Instructions

## Set the broker
In the root file, run
```
kubectl apply -f kafka.yml
```

## For each new service (location_api, location_consumer, location_producer, person_api)
Run:
```
cd modules/<service name>
docker build -t <your dockerhub username>/<service name>:latest
docker push <your dockerhub username>/<service name>:latest
kubectl apply -f deployment/ 
```

## Troubleshooting
To investigating possible issues:
```
kubectl get pods
```
Get the name of your pod or service
```
kubectl logs <pod name>
```