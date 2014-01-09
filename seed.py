# --------------------------------------------------------------------------- #
# seed.py                                                                     #
# Created by Ingrid Avendano 1/8/14.                                          #
# --------------------------------------------------------------------------- #
# Populate the transit.db with MUNI locations with latitudes and longitudes.  # 
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

def load_transit_stops():
    """ Adds stopcode, name, location by latitude and longitude. """

    with open("./data/stops.txt") as datafile:
        transit_stops = datafile.readlines()

        for stop in transit_stops:
            stop = stop.split(",")
            print stop[0], stop[1]


def sf_muni_stops(route_id, direction):
        """ Gets XML of name and code for each stop on a route from 511. """

        set_route = "&routeIDF=" + agency[5] + "~" + route_id + direction
        response = requests.get(website + service[3] + token + set_route)
        xml = StringIO(response.text)

        rtt = ET.parse(xml).getroot()
        stops = rtt[0][0][0][0][0][0][0]

        for stop in stops:
            code = stop.get("StopCode")
            name = stop.get("name")
            # print stop.get("StopCode"), stop.get("name")
            if code not in codes:
                codes.append(code)

            xml_locations[code] = name
            

def sf_muni_routes():
    """ Gets XML list of SF-MUNI routes with name and direction frmo 511. """

    response = requests.get(website + service[2] + token + set_agency[5])
    xml = StringIO(response.text)

    # real time transit for SF-MUNI
    rtt = ET.parse(xml).getroot()
    routes = rtt[0][0][0]

    for route in routes:
        route_id = route.get("Code")

        # grab inbound stops
        sf_muni_stops(route_id, "~Inbound")

        # grab outbound stops, but 81X and 80X don't have outbound stops
        if route.get("Code") != "81X" and route.get("Code") != "80X":
            sf_muni_stops(route_id, "~Outbound")
# --------------------------------------------------------------------------- #


if __name__ == "__main__":
    load_transit_stops()
