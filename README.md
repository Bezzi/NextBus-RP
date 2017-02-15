
# Python reverse proxy for NextBus API

This is a python3 implementation of a reverse proxy for the NextBus API using docker-compose, allowing multiple instances of the app to run at the same time.

By creating a web server the program receives GET requests from a user and forwards it - if the request is not already cached - to the NextBus API .


## Endpoints
/stats : Displays statistics of the requests stored in a Mongo database.

/?command= : Forwards GET request specified in NextBus API.

## Instructions
Install "docker-compose" in the system and run the following command:

 - ./Run.sh or bash Run.sh

To create more than one instance of the app, run the following command with the adequate quantity:

  - docker-compose scale nextbus="quantity" mongodb=1 haproxy=1

Alternatively the python script "revproxy.py" could be executed locally by installing the following dependencies and python3 libraries:

### Libraries:
- http.server: To create a web server.
- requests: For external http GET requests to NextBus API.
- requests_cache: To store requests in cache.
- pymongo: Driver to use Mongo database.
- json: To return data in json format.
- urllib: To parse query parameters.

### Python3 Dependecies:
- redis
- requests
- requests_cache
- pymongo
