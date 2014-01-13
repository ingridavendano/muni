# -----------------------------------------------------------------------------
# seed.py 
# Created by Ingrid Avendano 1/8/14. 
# -----------------------------------------------------------------------------
# Populate the muni.db with geo-locations of every MUNI stop.
# -----------------------------------------------------------------------------

import re
import model
import json
import requests
from StringIO import StringIO
import xml.etree.ElementTree as ET

# -----------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------

def read_xml_of_stops(route_id, direction, locations):
    """ Gets XML of name and code for each stop on a route from 511. """

    set_route = "&routeIDF=" + agency[5] + "~" + route_id + direction
    response = requests.get(website + service[3] + token + set_route)
    xml = StringIO(response.text)

    rtt = ET.parse(xml).getroot()
    stops = rtt[0][0][0][0][0][0][0]

    for stop in stops:
        code = stop.get("StopCode")

        # cleaning up the data of the names for each stop
        name = stop.get("name")
        name = re.sub("  and  ", " & ", name)
        name = re.sub("Street", "St", name)
        name = re.sub(" Of ", " of ", name)
        name = re.sub("C Chavez", "Cesar Chavez", name)

        locations[code] = name

    return locations


def read_xml_of_routes():
    """ Gets XML list of SF-MUNI routes with name and direction frmo 511. """
    response = requests.get(website + service[2] + token + set_agency[5])
    xml = StringIO(response.text)

    # real time transit for SF-MUNI
    rtt = ET.parse(xml).getroot()
    routes = rtt[0][0][0]

    locations = {}

    for route in routes:
        route_id = route.get("Code")

        # grab inbound stops
        locations = read_xml_of_stops(route_id, "~Inbound", locations)

        # grab outbound stops, but 81X and 80X don't have outbound stops
        if route_id != "81X" and route_id != "80X":
            locations = read_xml_of_stops(route_id, "~Outbound", locations)

    return locations


def read_txt_of_stops():
    """ Get stops with tuples of latitude and longitudefrom from txt file. """
    locations = {}

    with open("./data/stops.txt") as stopdata:
        stops = stopdata.readlines()

        for stop in stops:
            stop = stop.split(",")
            try: 
                stop_id = int(stop[0])
                locations[stop_id] = (stop[3], stop[4])
            except ValueError:
                pass

    return locations


def load_stops(db_session, debug=False):
    """ Loads information about each MUNI stop into the database. """
    locations = read_txt_of_stops()
    stops = read_xml_of_routes()

    for code in stops.keys(): 
        stop_id = int(code[-4:])

        if debug: 
            print code, stops[code], locations[stop_id]

        new_stop = model.Stop(
            code=code, 
            address=stops[code], 
            lat=locations[stop_id][0], 
            lng=locations[stop_id][1]
            )
        db_session.add(new_stop)

    return db_session

# -----------------------------------------------------------------------------

def main():
    db_session = model.connect()
    db_session = load_stops(db_session)
    db_session.commit()


if __name__ == "__main__":
    main()
    