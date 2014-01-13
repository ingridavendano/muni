# -----------------------------------------------------------------------------
# model.py 
# Created by Ingrid Avendano 1/6/14.
# -----------------------------------------------------------------------------
# Grabs data needed for webapp from database.                                 
# -----------------------------------------------------------------------------

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, scoped_session
import json
import requests
from StringIO import StringIO
import xml.etree.ElementTree as ET

# -----------------------------------------------------------------------------
# To create a new database, first follow the steps below in the console:
#
# python -i model.py
# >>> engine = create_engine("mysql://root@localhost/stops", echo=True)
# >>> Base.metadata.create_all(engine)
# 
# Then run seed.py file to populate the database with stop geolocations.
# -----------------------------------------------------------------------------

ENGINE = create_engine("mysql://root@localhost/stops", echo=False)
db_session = scoped_session(sessionmaker(
    bind=ENGINE, 
    autocommit=False, 
    autoflush=False
    ))
Base = declarative_base()
Base.query = db_session.query_property()


def connect():
    """ Use this function to connect to database for seed.py file. """
    global ENGINE
    global Session

    ENGINE = create_engine("mysql://root@localhost/stops", echo=False)
    Session = scoped_session(sessionmaker(
        bind=ENGINE, 
        autocommit=False, 
        autoflush=False
        ))
    Base = declarative_base()
    Base.query = db_session.query_property()

    # if recreating the db, then uncomment below
    Base.metadata.create_all(ENGINE)

    return Session()

# -----------------------------------------------------------------------------
# Class declarations for table of stops in database.
# -----------------------------------------------------------------------------

class Stop(Base):
    __tablename__ = "muni"

    id = Column(Integer, primary_key=True)
    code = Column(String(6), nullable=False)
    address = Column(String(40), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

# -----------------------------------------------------------------------------

def create_stop(code, name, latitude, longitude):
    """ Creates new MUNI stop in database. """
    new_stop = Stop(code=code, address=name, lat=latitude, lng=longitude)
    db_session.add(new_stop)
    db_session.commit()
    return


def get_stop(code):
    """ Return stop based on stopcode. """
    stop = db_session.query(Stop).filter(Stop.code == code).one()
    return stop


def get_stop_departure_times(code):
    """ Gets list of departure times from XML from 511. """

    # grab API key from SF Bay Area transit site http://511.org/
    config_file = open("./config.json")
    config_data = json.load(config_file) 
    config_file.close()

    website = "http://services.my511.org/Transit2.0/"
    token = "?token="+config_data["511_API_KEY"]
    service = "GetNextDeparturesByStopCode.aspx"
    stop = "&stopcode=" + code

    response = requests.get(website + service + token + stop)
    xml = StringIO(response.text)

    rtt = ET.parse(xml).getroot()
    routes = rtt[0][0][0]

    for route in routes:
        print "#"*80
        print route.get("Name")
        print route[0][0].get("Name")
        times = [time.text for time in route[0][0][0][0][0]]
        print times




def geo_fencing_for_nearest_stops(latitude, longitude):
    """ Finds closest MUNI stop in database by a user's geolocation. """
    equation = "".join(["( 3959 * acos( cos( radians(",
        latitude,
        ") ) * cos( radians( lat ) ) * cos( radians( lng ) - radians(",
        longitude,
        ") ) + sin( radians(",
        latitude,
        ") ) * sin( radians( lat ) ) ) )"
    ])

    # equation based on Haversine formula
    search = "".join(["SELECT * FROM muni WHERE ",
        equation, 
        " < 5 ORDER BY ",
        equation,
        " LIMIT 0 , 4"
    ])


    
    stops = db_session.query(Stop).from_statement(search).all()

    get_stop_departure_times(stops[0].code)

    return stops
