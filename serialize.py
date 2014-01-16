# -----------------------------------------------------------------------------
# serialize.py 
# Created by Ingrid Avendano 1/12/14.
# -----------------------------------------------------------------------------
# Useful functions to write data into JSON.
# -----------------------------------------------------------------------------

import json
import deserialize
from math import *

# -----------------------------------------------------------------------------

class DepartureEncoder(json.JSONEncoder):
    """ Encode XML departure times to JSON. """

    def default(self, stop):

        def get_distance(stop):
            lat = radians(float(stop.lat))
            lng = radians(float(stop.lng))

            # calculate the distance in miles using Haversine formula
            distance = cos(LAT)*cos(lat)*cos(lng - LNG) + sin(LAT)*sin(lat)
            return 3959*acos(distance)

        def stop_data(route):
            return {
                'route': route.get("Name"),
                'direction': route[0][0].get("Name"),
                'times': [time.text for time in route[0][0][0][0][0]]
            }

        # get XML of departures leaving from stop 
        departures = deserialize.get_departures(stop.code)

        return {
            'id': stop.code,
            'name': stop.address,
            'lat': float(stop.lat),
            'lng': stop.lng, 
            'distance': get_distance(stop), 
            'departures': [
                stop_data(route) for route in departures
            ]
        }

# -----------------------------------------------------------------------------

def to_json(stops, latitude, longitude, debug=False):
    """ Converts data about a MUNI stop into JSON. """
    # stops_data = {'stops': stops}

    global LAT
    global LNG

    LAT = radians(float(latitude))
    LNG = radians(float(longitude))


    # stops_data = {'stops': stops}
    stop_id = stops[0].code
    print stop_id
    # if no departure data was given
    if stop_id is None: return None

    # get XML of departures leaving from stop 
    departures_at_stop = deserialize.get_departures(stop_id)

    # encode departure for MUNI stop data to JSON
    json_string = json.dumps(stops,
        cls=DepartureEncoder,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
        )

    # for pretty printing uncomment other attributes in json.dumps() above
    if debug: print json_string

    return json_string
