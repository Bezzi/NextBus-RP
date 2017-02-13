"""

#import xml.etree.ElementTree as ET

  # Root element of XML tree
  #root = ET.fromstring(requests.get(r.text))


  if root.find('Error'):
      if root.find('Error').attrib['shouldRetry']:
          print('Retry request in a few seconds')
      else:
          print('Invalid request')
  """

import requests
import xml.etree.ElementTree as ET

IP = 10.10.10.10

# Request stats
curl "http://{0}/stats".format(IP)

#######################################
####### Configuration Requests ########
#######################################

agency_list = []

#######  Command "agencyList" #######
# Requests to list agencies - responses should be cached starting at the second request.
for i in range 1,10:
    root = ET.fromstring(requests.get("http://{0}/publicXMLFeed?command=agencyList".format(IP)))
    agency_list = root.find('agency').tag()

# Request stats
curl "http://{0}/stats".format(IP)

#######  Command "routeList" #######
for i in range 1,10:
    curl "http://{0}/publicXMLFeed?command=routeList&a={1}".format(IP,agency_list[i])


#######  Command "routeConfig" #######
# To obtain a list of routes for an agency
for i in range 1,10:
    curl "http://{0}/publicXMLFeed?command=routeConfig&a={1}&r={2}".format(IP,agency_list[i],route_tag[i])


#######################################
######## Prediction Requests ##########
#######################################

## Command "predictionsForMultiStops" #



##### Command Command "schedule" ######




#######################################
########## Message Requests ###########
#######################################

######### Command "messages" #########




#######################################
###### Vehicle Location Requests ######
#######################################

###### Command "vehicleLocations" ######


#######################################
############ BAD Requests #############
#######################################
# Bad Requests -  responses should be cached starting at the second request.
#for i in range 1,10:
    #curl "http://{0}/publicXMLFeed?command=Error".format(IP)
