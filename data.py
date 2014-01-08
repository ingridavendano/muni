# --------------------------------------------------------------------------- #
# data.py                                                                     #
# Created by Ingrid Avendano 1/8/14.                                          #
# --------------------------------------------------------------------------- #
# Grab a transit stop data that matches each stop to a geolocation.           #
# --------------------------------------------------------------------------- #

import requests
from StringIO import StringIO
import xml.etree.ElementTree as ET

# --------------------------------------------------------------------------- #\
# variables for 511 transit data 

token = "4bba4c2d-55eb-4ee4-96fd-4f2743484605"
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

# --------------------------------------------------------------------------- #
# making all the variables website friendly 

website = "http://services.my511.org/Transit2.0/"
token = "?token="+token
service = [service[i]+".aspx" for i in range(len(service))]
agency = ["&agencyName="+agency[i] for i in range(len(agency))]

# --------------------------------------------------------------------------- #

def grab_sf_muni_data():
    response = requests.get(website + service[2] + token + agency[5])
    xml = StringIO(response.text)
    tree = ET.parse(xml)
    for child in tree.getroot()




# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    grab_sf_muni_data()
