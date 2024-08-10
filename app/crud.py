from sqlalchemy.orm import Session

from . import models, schemas
from .enums import TYPE
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
        type=complaint.type.value,
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


def get_complaints(type: TYPE, db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Complaint).filter(models.Complaint.type == type.value).offset(skip).limit(limit).all()


def get_complaint(complaint_id: int, db: Session):
    return db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()


def delete_complaint(complaint_id: int, db: Session):
    complaint = db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()
    db.delete(complaint)
    db.commit()
    return complaint
