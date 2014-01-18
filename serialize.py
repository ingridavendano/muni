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

def get_distance(stop):
    """ Calculate the distance in miles using Haversine formula. """
    lat = radians(float(stop.lat))
    lng = radians(float(stop.lng))

    distance = cos(LAT)*cos(lat)*cos(lng - LNG) + sin(LAT)*sin(lat)
    return 3959*acos(distance)

def add_distance(routes):
    """ Calculate the distance in miles for user to view. """
    largest_distance = 0.0
  
    for courses in routes.values():
        for course in courses:
            if largest_distance < course['dist']:
                largest_distance = course['dist']

    return '%.2f'%largest_distance


def add_course(stop, route):
    """ Each stop has multiple routes departuring referred to as a course. """
    return {
        'course': route[0][0].get("Name"), 
        'times': [time.text for time in route[0][0][0][0][0]], 
        'lat': stop.lat, 
        'lng': stop.lng, 
        'dist': get_distance(stop)
    }

def sort_routes(routes):
    """ Reorganize routes listed in order of soonest time to appear. """
    organize_by_times = []

    for route in routes:
        if len(route['times']) == 0:
            route['times'].append("N/A")
        organize_by_times.append(route['times'][0])

    organize_by_times.sort()

    for route in routes:
        i = organize_by_times.index(route['times'][0])
        organize_by_times[i] = route

    return organize_by_times


def sort_stops(stops):
    """ Get routes for bus stops to show up in ascending order. """ 
    tmp_stops = []
    organize_by_distances = []

    # organize the stops with their routes into a list
    for name, routes in stops.iteritems():
        distance = add_distance(routes)
        tmp_stops.append({
            'name': name, 
            'routes': [
            {'line':n, 'transit':sort_routes(d)} for n, d in routes.iteritems()
            ], 
            'distance': distance
            })
        organize_by_distances.append(distance)

    organize_by_distances.sort()

    # organize stops by disance:
    for stop in tmp_stops:
        i = organize_by_distances.index(stop['distance'])
        organize_by_distances[i] = stop

    return organize_by_distances


def organize_stops(stops, latitude, longitude):
    """ Reorganize stops into an updated list. """
    update = {} 

    # cannot use JSONEncoder because it doesn't parse properly
    for stop in stops:
        update[stop.address] = {}

    # go through all the stops 
    for stop in stops:
        location = stop.address
        departures = deserialize.get_departures(stop.code)

        # check the departures for this stop
        for route in departures:
            name = route.get("Name")

            # add new course to existing route
            if name in update[location].keys():
                update[location][name].append(add_course(stop, route))
            else:
                 update[location][name] = [add_course(stop, route)]

    organize_by_distances = sort_stops(update)

    return organize_by_distances

# -----------------------------------------------------------------------------

class DepartureEncoder(json.JSONEncoder):
    """ Encode XML departure times to JSON. """

    def default(self, stop):
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

    updated_stops = organize_stops(stops, latitude, longitude)

    # if no departure data was given
    if stops is None: return None

    # # encode departure for MUNI stop data to JSON
    # json_string = json.dumps(stops,
    #     cls=DepartureEncoder,
    #     sort_keys=True,
    #     indent=4,
    #     separators=(',', ': ')
    #     )

    # organized stops, above code also works too
    json_string = json.dumps(updated_stops,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
        )

    if debug: print json_string
    
    return json_string
