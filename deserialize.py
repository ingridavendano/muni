# -----------------------------------------------------------------------------
# deserialize.py 
# Created by Ingrid Avendano 1/12/14.
# -----------------------------------------------------------------------------
# Useful funcitons to interpret XML data.
# -----------------------------------------------------------------------------

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

def departures_by_stop(code):
    """ Gets list of departure times from XML from 511. """
    response = requests.get(website + service[6] + token + "&stopcode=" + code)
    xml = StringIO(response.text)

    rtt = ET.parse(xml).getroot()
    routes = rtt[0][0][0]

    for route in routes:
        print "#"*80
        print route.get("Name")
        print route[0][0].get("Name")
        times = [time.text for time in route[0][0][0][0][0]]
        print times



def stops_by_route(route, all_stops):
    pass

def routes_by_agency(agency):
    pass



