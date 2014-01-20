# -----------------------------------------------------------------------------
# model.py 
# Created by Ingrid Avendano 1/6/14.
# -----------------------------------------------------------------------------
# Grabs data needed for webapp from database.                                 
# -----------------------------------------------------------------------------

import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, scoped_session
import serialize
import deserialize
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

# -----------------------------------------------------------------------------
# Connection function that is useful to seed.py to populate database.
# -----------------------------------------------------------------------------

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
    Base.query = Session.query_property()

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
    lat = Column(Float(precision=10), nullable=False)
    lng = Column(Float(precision=10), nullable=False)
    lat_str = Column(String(20), nullable=False)
    lng_str = Column(String(20), nullable=False)

# -----------------------------------------------------------------------------

def create_stop(code, name, latitude, longitude):
    """ Creates new MUNI stop in database. """
    new_stop = Stop(
        code=code, 
        address=name, 
        lat=latitude, 
        lng=longitude,
        lat_str=str(latitude), 
        lng_str=str(longitude),
        )
    db_session.add(new_stop)
    db_session.commit()
    return


def get_stop(code):
    """ Return stop based on stopcode. """
    stop = db_session.query(Stop).filter(Stop.code == code).one()
    return stop


def geo_fence(latitude, longitude, radius, limit=8):
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
        equation, " < ", str(radius), " ORDER BY ",
        equation, " LIMIT 0 , ", str(limit)
    ])

    # grab all stops and returns JSON string of the data
    stops = db_session.query(Stop).from_statement(search).all()
    json_string = serialize.to_json(stops, latitude, longitude, debug=True)

    return json_string
