from sqlalchemy.orm import Session

from . import models, schemas
from .enums import CLASSNAME
from .utils import Hasher
from datetime import date


# def get_user(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
#
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


def create_complaint(db: Session, complaint: schemas.ComplaintCreate):
    complaint = models.Complaint(
        location=complaint.location,
        latitude=complaint.latitude,
        longitude=complaint.longitude,
        classname=complaint.classname.value,
        phone=complaint.phone,
        image_link=complaint.image_link,
        status=complaint.status.value,
        description=complaint.description,
        created_at=date.today()
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return complaint


def get_complaints(classname: CLASSNAME, db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Complaint).filter(models.Complaint.classname == classname.value).offset(skip).limit(limit).all()


def get_complaint(complaint_id: int, db: Session):
    return db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()


def delete_complaint(complaint_id: int, db: Session):
    complaint = db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()
    db.delete(complaint)
    db.commit()
    return complaint

def get_nearby_complaint(db: Session):
    return [
        schemas.NearByComplaint(
            id=result.id,
            longitude=result.longitude,
            latitude=result.latitude,
            time=result.time,
            address=result.address,
            image_url=f"https://d1m84t8yekat2i.cloudfront.net/00000{result.id}"
        )
        for result in db.query(models.DetectImage).limit(10).all()
    ]
