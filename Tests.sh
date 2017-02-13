#!/bin/bash
# This script is to test concurrent requests to the web server and measure the access time.

URL="http://localhost/publicXMLFeed?command=agencyList"

for i in {1..500}
do
  curl -o /dev/null $URL -s -w %{time_connect}:%{time_starttransfer}:%{time_total}\\n
done


wait
