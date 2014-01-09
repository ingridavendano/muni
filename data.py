# --------------------------------------------------------------------------- #
# data.py                                                                     #
# Created by Ingrid Avendano 1/8/14.                                          #
# --------------------------------------------------------------------------- #
# Grab a transit stop data that matches each stop to a geolocation.           #
# --------------------------------------------------------------------------- #

import json
import requests
from StringIO import StringIO
import xml.etree.ElementTree as ET

# --------------------------------------------------------------------------- #

# grab API key from SF Bay Area transit site http://511.org/
config_file = open("./config.json")
config_data = json.load(config_file) 
config_file.close()

# variables from 511 transit data 
token = config_data["511_API_KEY"]
service = [
    "GetAgencies",
    "GetRoutesForAgencies",
    "GetRoutesForAgency",
    "GetStopsForRoute",
    "GetStopsForRoutes",
    "GetNextDeparturesByStopName",
    "GetNextDeparturesByStopCode"
    ]
agency = [
    "AC Transit",
    "BART",
    "Caltrain",
    "Dumbarton Express", 
    "SamTrans",
    "SF-MUNI",
    "VTA",
    "WESTCAT"
    ]

# convert variables to website friendly 
website = "http://services.my511.org/Transit2.0/"
token = "?token="+token
service = [service[i]+".aspx" for i in range(len(service))]
set_agency = ["&agencyName="+agency[i] for i in range(len(agency))]

# --------------------------------------------------------------------------- #

def sf_muni_stops(route_code):
    """ Provides the name and code for each stop on a route. """

    set_route = "&routeIDF=" + agency[5] + "~" + route_code + "~Inbound"
    response = requests.get(website + service[3] + token + set_route)
    xml = StringIO(response.text)

    rtt = ET.parse(xml).getroot()
    stops = rtt[0][0][0][0][0][0][0]

    for stop in stops:
        print stop.get("name"), stop.get("StopCode")


def sf_muni_routes():
    """ Grabs list of SF-MUNI routes with name and direction. """

    response = requests.get(website + service[2] + token + set_agency[5])
    xml = StringIO(response.text)

    # real time transit for SF-MUNI
    rtt = ET.parse(xml).getroot()
    routes = rtt[0][0][0]

    for route in routes:
        sf_muni_stops(route.get("Code"))


# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sf_muni_routes()
