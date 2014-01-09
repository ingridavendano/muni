# --------------------------------------------------------------------------- #
# model.py                                                                    #
# Created by Ingrid Avendano 1/6/14.                                          #
# --------------------------------------------------------------------------- #
# Grabs all the data needed from database.                                    #
# --------------------------------------------------------------------------- #

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session

# --------------------------------------------------------------------------- #
# setup of database

# ENGINE = create_engine("sqlite:///muni.db", echo=False)
# db_session = scoped_session(sessionmaker(
#     bind=ENGINE, 
#     autocommit=False, 
#     autoflush=False
#     ))
# Base = declarative_base()
# Base.query = db_session.query_property()

# --------------------------------------------------------------------------- #

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///muni.db", echo=False)
    db_session = scoped_session(sessionmaker(
        bind=ENGINE, 
        autocommit=False, 
        autoflush=False
        ))
    Base = declarative_base()
    Base.query = db_session.query_property()

    # if recreating the db, then uncomment below
    Base.metadata.create_all(ENGINE)

    return Session()

# --------------------------------------------------------------------------- #
# class declarations for table in database

class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True)
    code = Column(String(6), nullable=False)
    location = Column(String(40), nullable=False)
    latitude = Column(Integer, nullable=False)
    longitude = Column(Integer, nullable=False)

# --------------------------------------------------------------------------- #
# creating new instances in the database and querying 

def create_stop(code, name, lat, long):
    new_stop = Stop(code=code, name=name, latitude=lat, longitude=lon)
    db_session.add(new_stop)
    db_session.commit()
    return

def get_stop(code):
    """ Return stop based on stopcode. """
    stop = db_session.query(Stop).filter(Stop.code == code).one()
    return stop

# --------------------------------------------------------------------------- #

def main(): 
    pass

if __name__ == "__main__":
    main()
