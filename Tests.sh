#!/bin/bash



URL="http://10.10.10.10/publicXMLFeed?command=agencyList"


for i in {1..500}
do
  curl -o /dev/null $URL -s -w %{time_connect}:%{time_starttransfer}:%{time_total}\\n
done
wait
