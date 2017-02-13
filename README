
# Python reverse proxy for NextBus API

This is a python3 implementation of a reverse proxy for the NextBus API using docker-compose.

By creating a web server the program receives GET requests from a user and forwards it - if the request is not already cached - to the NextBus API .


## Endpoints
/stats : Displays statistics of the requests stored in a Mongo database.

/publicXMLFeed?command= : Forwards command specified in NextBus API.

## Instructions
#### Run the following commands:
 1.  cd /project_path
 2. docker-compose build
 3. docker-compose up
 4. Make the request to "http:localhost" with the corresponding endpoint.


### Libraries:
- http.server: To create a web server.
- requests: For external http GET requests to NextBus API.
- requests_cache: To store requests in cache.
- Pymongo: Driver to use Mongo database.
- json: To return data in json format.

### Python3 Dependecies:
- redis
- requests
- requests_cache
- pymongo
