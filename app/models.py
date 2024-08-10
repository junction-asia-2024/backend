from sqlite3 import Timestamp
from datetime import date
from sqlalchemy import Column, Integer, String, Date, Float

from . import schemas
from .database import Base


class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(500))
    latitude = Column(Float)
    longitude = Column(Float)
    classname = Column(String(10))
    phone = Column(String(11))
    image_link = Column(String(255))
    status = Column(String(10))
    description = Column(String(255))
    created_at = Column(Date, default=date.today)