#!/usr/bin/env python
import requests
import requests_cache
from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
import pymongo

# TODO: VER ESTOO


import json

# Specifies the time - in seconds - in which cached data will expire.
CACHE_TIMEOUT = 300

# Specifies the threshold time - in seconds - for queries.
THRESHOLD = 0.2

# Configuration for request caching
requests_cache.install_cache('redis_cache', backend='redis', expire_after=CACHE_TIMEOUT)
requests_cache.clear()

# Database connection and collections
client = MongoClient()
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

        if self.path == "/stats":
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send response data
            self.wfile.write(bytes(json.dumps(self.find_stats()), "utf8"))
        else:
            # Forward the request to the API
            URL = "http://webservices.nextbus.com/service{0}".format(self.path)
            headers = {'Accept-Encoding': 'gzip, deflate'}
            r = requests.get(URL, headers=headers)
            r_seconds = r.elapsed.total_seconds()

            # Update stats
            queries.update_one({"path": self.path},{"$inc": {"count":1}},upsert=True)

            if r_seconds > THRESHOLD :
                # TODO: VER SI ES MAS GRANDE QUE EL QUE ESTA ANTES DE PISARLO!!!
                slow_requests.update_one({"path": self.path},{"$set": {"seconds":r_seconds}},upsert=True)

            if r.from_cache:
                print('Cached answer: '+ str(r_seconds))
            else:
                print('Non cached answer: '+ str(r_seconds))

            # Send response data
            self.wfile.write(bytes(r.text, "utf8"))

        return

def run():

  # Server settings
  server_address = ('10.10.10.10', 80)
  httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
  print('Running server')
  httpd.serve_forever()

run()
