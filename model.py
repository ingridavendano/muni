# -----------------------------------------------------------------------------
# model.py 
# Created by Ingrid Avendano 1/6/14.
# -----------------------------------------------------------------------------
# Grabs data needed for webapp from database.                                 
# -----------------------------------------------------------------------------

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session

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
    lat = Column(Integer, nullable=False)
    lng = Column(Integer, nullable=False)

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
