# -----------------------------------------------------------------------------
# serialize.py 
# Created by Ingrid Avendano 1/12/14.
# -----------------------------------------------------------------------------
# Useful functions to write data into JSON.
# -----------------------------------------------------------------------------

import json
import deserialize

class DepartureEncoder(json.JSONEncoder):
    """ Encode XML departure times to JSON. """

    def default(self, routes):

        def departure(route):
            return {
                'route': route.get("Name"),
                'direction': route[0][0].get("Name"),
                'times': [time.text for time in route[0][0][0][0][0]]
            }

        return {
            'name': deserialize.muni_stop(routes[0][0][0][0][0].get("name")),
            'code': routes[0][0][0][0][0].get("StopCode"),
            'departures': [
                departure(route) for route in routes
            ]
        }

# -----------------------------------------------------------------------------

def to_json(stop_id, debug=False):
    """ Converts data about a MUNI stop into JSON. """

    # if no departure data was given
    if stop_id is None: return None

    # get XML of departures leaving from stop 
    departures_at_stop = deserialize.get_departures(stop_id)

    # encode departure for MUNI stop data to JSON
    json_string = json.dumps(departures_at_stop,
        cls=DepartureEncoder,
        # sort_keys=True,
        # indent=4,
        # separators=(',', ': ')
        )

    # for pretty printing uncomment other attributes in json.dumps() above
    if debug: print json_string

    return json_string
