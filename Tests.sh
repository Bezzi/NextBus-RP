#!/bin/bash
# This script is to test concurrent requests to the web server and measure the access time.

BASEURL="http://10.10.10.10/"
PARAMS="?command=agencyList"

for i in {1..500}
do
  curl -o /dev/null $BASEURL$PARAMS -s -w %{time_connect}:%{time_starttransfer}:%{time_total}\\n
done

# Request another endpoint
PARAMS="?command=routeList&a=sf-muni"
for i in {1..250}
do
  curl -o /dev/null $BASEURL$PARAMS -s -w %{time_connect}:%{time_starttransfer}:%{time_total}\\n
done

# Request an invalid endpoint
PARAMS="?command=null"
for i in {1..125}
do
  curl -o /dev/null $BASEURL$PARAMS -s -w %{time_connect}:%{time_starttransfer}:%{time_total}\\n
done


wait
