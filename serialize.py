# -----------------------------------------------------------------------------
# serialize.py 
# Created by Ingrid Avendano 1/12/14.
# -----------------------------------------------------------------------------
# Useful functions to write data into JSON.
# -----------------------------------------------------------------------------

import json

class DepartureEncoder(json.JSONEncoder):
    """ Encode XML departure times to JSON. """

    def default(self, rtt, name):

        def stop_data(stop):
            return {
                'route': stop.get("Name"),
                'direction': stop[0][0].get('Name'), 
                'times': [time.text for time in stop[0][0][0][0][0]]
            }

        return {
            'stop': [stop_data(stop) for stop in rtt[0][0][0]]
        }

# -----------------------------------------------------------------------------

def to_json(name, rtt, debug=False):
    """ Converts data about a MUNI stop into JSON. """

    # if no XML stop exists 
    if name is None: return None

    # encode XML  
    json_string = json.dumps(rtt, cls=DepartureEncoder)

    if debug: print json_string
    return json_string
