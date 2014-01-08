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

def grab_sf_muni_data():
    response = requests.get(website + service[2] + token + set_agency[5])
    xml = StringIO(response.text)

    # real time transit for SF-MUNI
    rtt = ET.parse(xml).getroot()
    routes = rtt[0][0][0]

    for route in routes:
        print route.get("Name"), route.get("Code")



# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    grab_sf_muni_data()
