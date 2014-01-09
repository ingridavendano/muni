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
xml_locations = {}
codes = []

if __name__ == "__main__":
    f = open("muni_transit_stops.txt", "w")



    def sf_muni_stops(route_code, direction):
        """ Provides the name and code for each stop on a route. """

        set_route = "&routeIDF=" + agency[5] + "~" + route_code + direction
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
            
            # print locations[stop.get("StopCode")]




    def sf_muni_routes():
        """ Grabs list of SF-MUNI routes with name and direction. """

        response = requests.get(website + service[2] + token + set_agency[5])
        xml = StringIO(response.text)

        # real time transit for SF-MUNI
        rtt = ET.parse(xml).getroot()
        routes = rtt[0][0][0]

        for route in routes:
            print route.get("Code")
            sf_muni_stops(route.get("Code"), "~Inbound")
            if route.get("Code") != "81X" and route.get("Code") != "80X":
                sf_muni_stops(route.get("Code"), "~Outbound")


        # print "from xml:", len(xml_locations)

        # count = 0
        # txt_locations = []

        # print xml_locations["15617"]
        # with open("./data/stops.txt") as datafile:
        #     transit_stops = datafile.readlines()

        #     print "from txt:", len(transit_stops)
        #     for stop in transit_stops:
        #         stop = stop.split(",")
        #         code = "1"+stop[0]
        #         txt_locations[code] = stop[1]

        #         # if code not in locations.keys():
        #         #     count += 1
        #         # print stop[0], stop[1]

        #     print "not found:", count

        # for key in xml_locations.keys():
        #     if key not in txt_locations.keys():
        #         print xml_locations[key]


# --------------------------------------------------------------------------- #

    sf_muni_routes()

    codes = sorted(codes)

    for c in codes:
        n = xml_locations[c]

        line = c + ", " + n + "\n"
        f.write(line)

    f.close()





