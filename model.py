import os
from sqlalchemy import Column, String, DateTime, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()


def connect_db():
    return create_engine(os.environ['DATABASE_URL'], echo=False)


def init_db():
    # Create the database tables.
    engine = connect_db()
    Base.metadata.create_all(engine)


class Athlete(Base):
    __tablename__ = "athletes"

    id = Column(Integer, primary_key=True)
    access_token = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    profile_medium = Column(String)
    profile = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    sex = Column(String)
    email = Column(String)
    registered_on = Column(DateTime)

    def __init__(self, id, access_token, firstname,
                 lastname, profile_medium, profile, city, state,
                 country, sex, email, registered_on=func.now()):
        self.id = id
        self.access_token = access_token
        self.firstname = firstname
        self.lastname = lastname
        self.profile_medium = profile_medium
        self.profile = profile
        self.city = city
        self.state = state
        self.country = country
        self.sex = sex
        self.email = email
        self.registered_on = registered_on
