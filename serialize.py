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

def organize_course(name):
    """ Remove inbound and outbound details to a course. """
    if 'Outbound ' in name: return ('outbound', name[9:])
    if 'Inbound ' in name: return ('inbound', name[8:])
    return ('no direction', name)


def add_course(stop, route):
    """ Each stop has multiple routes departuring referred to as a course. """
    times = [time.text for time in route[0][0][0][0][0]]
    route_direction = organize_course(route[0][0].get("Name"))

    # don't bother adding muni route if no muni is coming
    if len(times) == 0: return None
    
    return {
        'direction': route_direction[0],
        'destination': route_direction[1], 
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


def remove_lat_lng(routes):
    """ Get rid of repetitive latitude/longitude data. """
    lat = lng = 0

    for route in routes:
        for stop in route['departures']:
            lat = stop['lat']
            del stop['lat']
            lng = stop['lng']
            del stop['lng']
            del stop['dist']

    return (routes, lat, lng)


def organize_route_name(name):
    """ Provide proper dash in how name is represented. """
    name = name.split('-')
    return name[0] + ' - ' + name[1]


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
                {
                'line': organize_route_name(name[0]), 
                'code': name[1], 
                'departures': sort_routes(departures)} 
                    for name, departures in routes.iteritems()
                ], 
            'distance': distance
            })
        organize_by_distances.append(distance)

    organize_by_distances.sort()

    # organize stops by disance:
    for stop in tmp_stops:
        clean_up_routes = remove_lat_lng(stop['routes'])
        stop['routes'] = clean_up_routes[0]
        stop['lat'] = clean_up_routes[1]
        stop['lng'] = clean_up_routes[2]

        i = organize_by_distances.index(stop['distance'])

        organize_by_distances[i] = stop

    return organize_by_distances


def organize_name(stop_name):
    """ Return name that is easy to organize routes by stop. """
    cross_streets = sorted(stop_name.split(' & '))

    # if cross streets can be reoganized return it
    if len(cross_streets) == 2:
        return cross_streets[0] + ' & ' + cross_streets[1]

    return stop_name 


def organize_stops(stops, latitude, longitude):
    """ Reorganize stops into an updated list. """
    update = {} 

    # cannot use JSONEncoder because it doesn't parse properly
    for stop in stops:
        update[organize_name(stop.address)] = {}

    # go through all the stops 
    for stop in stops:
        location = organize_name(stop.address)
        departures = deserialize.get_departures(stop.code)

        # check the departures for this stop
        for route in departures:
            name = route.get("Name")
            code = route.get("Code")
            course = add_course(stop, route)

            if course is not None: 
                # add new course to existing route
                if (name,code) in update[location].keys():
                    update[location][(name,code)].append(course)
                else:
                     update[location][(name,code)] = [course]

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
    if stops is None: return None

    global LAT
    global LNG

    LAT = radians(float(latitude))
    LNG = radians(float(longitude))

    # # encode departure for MUNI stop data to JSON
    # json_string = json.dumps(stops,
    #     cls=DepartureEncoder,
    #     sort_keys=True,
    #     indent=4,
    #     separators=(',', ': ')
    #     )

    updated_stops = organize_stops(stops, latitude, longitude)

    # organized stops, above code also works too
    json_string = json.dumps(updated_stops,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
        )

    # for debugging purposes to be able to look back at muni data gathered
    if debug: 
        print json_string

        with open('./muni.json', 'w') as json_output_file:
            json.dump(json_string, json_output_file)

    
    return json_string
