from pydantic import BaseModel
import datetime

from app.enums import CLASSNAME, STATUS


# class ComplaintBase(BaseModel):
#     location: str
#     classname: CLASSNAME
#     phone: str
#     image_link: str
#     status: STATUS
#     created_at: datetime.date
#
#
# class ComplaintCreate(ComplaintBase):
#     location: str
#     classname: CLASSNAME
#     phone: str
#     image_link: str
#     status: STATUS
#     created_at: datetime.date
class ComplaintCreate(BaseModel):
    location: str
    latitude: str
    longitude: str
    classname: CLASSNAME
    phone: str
    image_link: str
    status: STATUS
    description: str

    class Config:
        from_attributes = True


class ComplaintGet(ComplaintCreate):
    id: int  # ID 필드를 추가합니다.
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class NearByComplaint(BaseModel):
    id: int
    longitude: str
    latitude: str
    time: datetime.datetime
    address: str
    file_name: str

    class Config:
        from_attributes = True