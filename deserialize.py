# -----------------------------------------------------------------------------
# deserialize.py 
# Created by Ingrid Avendano 1/12/14.
# -----------------------------------------------------------------------------
# Useful funcitons to interpret XML data.
# -----------------------------------------------------------------------------

import re
import json
import requests
from StringIO import StringIO
import xml.etree.ElementTree as ET

# -----------------------------------------------------------------------------

# convert variables to website friendly 
website = "http://services.my511.org/Transit2.0/"
token = "?token="

# grab API key from SF Bay Area transit site http://511.org/
with open("./config.json") as api_key:
    token += json.load(api_key)["511"]

service = [
    "GetAgencies.aspx",
    "GetRoutesForAgencies.aspx",
    "GetRoutesForAgency.aspx",
    "GetStopsForRoute.aspx",
    "GetStopsForRoutes.aspx",
    "GetNextDeparturesByStopName.aspx",
    "GetNextDeparturesByStopCode.aspx"
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

direction = ["~Inbound", "~Outbound"]

# -----------------------------------------------------------------------------

def get_xml(url):
    """ Parse XML of real time transit (RTT) data from http://511.org/. """
    response = requests.get(url)
    xml = StringIO(response.text)
    return ET.parse(xml).getroot()


def get_departures(stop_id):
    """ Gets XML of a list of departure times based on a stop's code. """
    rtt = get_xml(website + service[6] + token + "&stopcode=" + stop_id)
    return rtt[0][0][0]


def get_stops(route_id, direction):
    """ Get XML of list of stops for each route. """
    route = "&routeIDF=" + agency[5] + "~" + route_id + direction
    rtt = get_xml(website + service[3] + token + route)
    return rtt[0][0][0][0][0][0][0]


def get_routes(agency):
    """ Get XML of routes from a specific agency. """ 
    rtt = get_xml(website + service[2] + token + "&agencyName=" + agency)
    return rtt[0][0][0]

# -----------------------------------------------------------------------------
# SF-MUNI specific functions below.
# -----------------------------------------------------------------------------

def muni_times(route):
    """ Gets XML of departure times at SF-MUNI stop for specific route. """
    times = [time.text for time in route[0][0][0][0][0]]
    return times


def muni_departures(stop_id):
    """ Gets XML of routes that departure at specific SF-MUNI stops. """
    routes = {}

    for route in get_departures(stop_id):
        name = route.get("Name")
        direction = route[0][0].get("Name")
        times = muni_times(route)

        # store the route info at MUNI stop 
        routes[name] = (direction, times)

    return routes


def muni_stop(name):
    """ Normalize SF-MUNI stop name with regex. """
    name = re.sub("  and  ", " & ", name)
    name = re.sub("Street", "St", name)
    name = re.sub(" Of ", " of ", name)
    name = re.sub("C Chavez", "Cesar Chavez", name)
    return name


def muni_stops(route_id, direction, stops):
    """ Get XML of SF-MUNI list of stops for each route. """
    for stop in get_stops(route_id, direction):
        stop_id = stop.get("StopCode")

        # store each stop in dictionary
        stops[stop_id] = muni_stop(stop.get("name"))

    return stops


def muni_routes(agency, stops):
    """ Get XML of SF-MUNI stops from all the routes for specific agency. """ 
    for route in get_routes(agency):
        route_id = route.get("Code")

        # grab inbound stops
        stops = muni_stops(route_id, direction[0], stops)

        # grab outbound stops, except 81X and 80X don't have outbound stops
        if route_id != "81X" and route_id != "80X":
            stops = muni_stops(route_id, direction[1], stops)

    return stops


def muni():
    """ Get SF-MUNI data on stops for all of the routes. """
    return muni_routes(agency[5], {})
