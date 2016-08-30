import sys

from sqlalchemy import Column,ForeignKey,Integer,String,Float,DateTime
from sqlalchemy.ext.declarative  import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = "shelter"
    name= Column(String(80),nullable=False)
    city = Column(String(40), nullable=False)
    address = Column(String(100), nullable=False)
    state  = Column(String(40),nullable=False)
    zipCode = Column(String(10),nullable=False)
    website = Column(String(80),nullable=False)
    id=Column(Integer,primary_key=True)

class Puppy(Base):
    __tablename__ = "puppy"
    name=Column(String(80), nullable=False)
    dob =Column(DateTime, nullable=False)
    gender = Column(String(10), nullable=False)
    weight=Column(Float,nullable=False)
    id=Column(Integer,primary_key=True)
    shelter_id=Column(Integer, ForeignKey('shelter.id'))
    puppy = relationship(Shelter)





engine=create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)