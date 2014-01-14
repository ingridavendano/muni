# -----------------------------------------------------------------------------
# seed.py 
# Created by Ingrid Avendano 1/8/14. 
# -----------------------------------------------------------------------------
# Populate MySQL database with SF-MUNI stop latitude/longitude data.
# -----------------------------------------------------------------------------

import model
import deserialize

# -----------------------------------------------------------------------------

def get_geolocations():
    """ Map stop_id to geolocations of every SF-MUNI stop from text file. """
    coordinates = {}

    with open("./data/stops.txt") as data:
        stops = data.readlines()

        for stop in stops:
            stop = stop.split(",")
            try: 
                stop_id = int(stop[0])
                latitude = stop[3]
                longitude = stop[4]

                # map each stop_id to its geolocation
                coordinates[stop_id] = (latitude, longitude)
            except ValueError:
                pass

    return coordinates


def load_muni_stops(db_session, debug=False):
    """ Loads information about each SF-MUNI stop into the database. """
    coordinates = get_geolocations()
    muni = deserialize.muni()

    for stop in muni.keys(): 
        stop_id = int(stop[-4:])

        if debug: print stop, muni[stop], coordinates[stop_id]

        new_stop = model.Stop(
            code=stop, 
            address=muni[stop], 
            lat=coordinates[stop_id][0], 
            lng=coordinates[stop_id][1]
            )
        db_session.add(new_stop)

    return db_session

    
# -----------------------------------------------------------------------------

def main():
    db_session = model.connect()
    db_session = load_muni_stops(db_session)
    db_session.commit()


if __name__ == "__main__":
    main()
    