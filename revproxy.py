#!/usr/bin/env python
import requests
import requests_cache
from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
import json

# Specifies the time - in seconds - in which cached data will expire.
CACHE_TIMEOUT = 300

# Specifies the threshold time - in seconds - for queries.
THRESHOLD = 0.5

# Block unwanted browser requests
BLACKLIST = ['/service/favicon.ico','/favicon.ico']

# Configuration for request caching
requests_cache.install_cache('redis_cache', backend='redis', expire_after=CACHE_TIMEOUT)
requests_cache.clear()

# Database connection and collections
client = MongoClient('mongodb', 27017)
db = client['statistics']
queries = db['queries']
slow_requests = db['slow_requests']


# HTTPRequestHandler class
class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # Method to retrieve statistics from the database
    def find_stats(self):
        data = {"queries":{},"slow_requests":{}}

        q = queries.find()
        sr = slow_requests.find()

        for item in sr:
            del item["_id"]
            data['slow_requests'][item['path']] = str(item['seconds'])+"s"
        for item in q:
            del item["_id"]
            data['queries'][item['path']] = item['count']

        return data

    # GET Method
    def do_GET(self):
        if self.path in BLACKLIST:
            return

        if self.path == "/stats":
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','application/json')
            self.end_headers()
            # Send response data
            self.wfile.write(bytes(json.dumps(self.find_stats()), "utf8"))

        else:
            # Forward the request to the API
            URL = "http://webservices.nextbus.com/service{0}".format(self.path)
            headers = {'Accept-Encoding': 'gzip, deflate'}
            r = requests.get(URL, headers=headers)
            r_seconds = r.elapsed.total_seconds()

            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','text/xml')
            self.end_headers()

            # Update stats
            queries.update_one({"path": self.path},{"$inc": {"count":1}},upsert=True)

            if r_seconds > THRESHOLD :
                data = db.slow_requests.find_one({"path": self.path})
                if data:
                    if r_seconds > data['seconds']:
                        slow_requests.update_one({"path": self.path},{"$set": {"seconds":r_seconds}})
                else:
                    slow_requests.update_one({"path": self.path},{"$set": {"seconds":r_seconds}},upsert=True)

            # Send response data
            self.wfile.write(bytes(r.text, "utf8"))

def run():
  # Server settings
  server_address = ('0.0.0.0', 80)
  httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
  httpd.serve_forever()

run()
