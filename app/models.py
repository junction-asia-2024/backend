from sqlite3 import Timestamp
from datetime import date
from sqlalchemy import Column, Integer, String, Date, Float, DateTime

from . import schemas
from .database import Base


class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(500))
    latitude = Column(String(255))
    longitude = Column(String(255))
    classname = Column(String(10))
    phone = Column(String(11))
    image_link = Column(String(255))
    status = Column(String(10))
    description = Column(String(255))
    created_at = Column(DateTime)

"""
koa=> create table detect_images (
koa(> id integer not null,
koa(> longitude numeric(10, 9) not null,
koa(> latitude numeric(10, 9) not null,
koa(> time timestamp not null default now(),
koa(> address text not null
koa(> );
"""
class DetectImage(Base):
    __tablename__ = "detect_images"
    id = Column(Integer, primary_key=True)
    longitude = Column(String(255))
    latitude = Column(String(255))
    time = Column(DateTime)
    address = Column(String(255))