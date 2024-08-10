import math

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Session
from geoalchemy2 import WKTElement
from . import models, schemas
from .enums import CLASSNAME
from datetime import date, datetime, timedelta

from . import s3_bucket


def create_complaint(db: Session, complaint: schemas.ComplaintCreate):
    complaint = models.Complaint(
        location=complaint.location,
        latitude=complaint.latitude,
        longitude=complaint.longitude,
        classname=complaint.classname.value,
        phone=None
        image_link=complaint.image_link,
        status=complaint.status.value,
        description=None
        created_at=date.today()
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return complaint


def get_complaints(classname: CLASSNAME, db: Session, skip: int = 0, limit: int = 100):
    limit__all = db.query(models.Complaint).filter(models.Complaint.classname == classname.value).offset(skip).limit(
        limit).all()
    return limit__all


def get_complaints_by_phone(phone: str, db: Session, skip: int = 0, limit: int = 100):
    limit__all = db.query(models.Complaint).filter(models.Complaint.phone == phone).offset(skip).limit(
        limit).all()
    return limit__all


def get_complaint(complaint_id: int, db: Session):
    return db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()


def delete_complaint(complaint_id: int, db: Session):
    complaint = db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()
    db.delete(complaint)
    db.commit()
    return complaint


def get_nearby_complaint(db: Session):
    return [
        NearByComplaintResponse(
            id=result.id,
            longitude=result.longitude,
            latitude=result.latitude,
            time=result.time,
            address=result.address,
            file_url=f"{s3_bucket.bucket_url_prefix}pre-images/00000{result.id}"
        )
        for result in db.query(models.DetectImage).limit(10).all()
    ]


def get_nearby_problem(latitude: float, longitude: float, db: Session):
    # return [
    #     NearByComplaintResponse(
    #         id=result.id,
    #         longitude=result.longitude,
    #         latitude=result.latitude,
    #         time=result.time,
    #         address=result.address,
    #         file_url=f"https://d1m84t8yekat2i.cloudfront.net/pre-images/00000{result.id}"
    #     )
    #     for result in db.query(models.DetectImage).limit(10).all()
    # ]

    point = WKTElement(f'POINT({longitude} {latitude})', srid=4326)

    # 반경 5미터 이내의 complaint 데이터를 조회
    nearby_problem = (
        db.query(models.DetectImage)
        .filter(func.ST_DWithin(models.DetectImage.geom, point, 5.0 / 1000))  # 5미터 = 0.005 킬로미터
        .all()
    )

    return nearby_problem


def get_linear_chart(db: Session):
    now = datetime.now()
    # 오늘의 시작과 끝 시간을 계산
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_today = start_of_today + timedelta(days=1)
    result = (
        db.query(
            func.date_trunc('hour', models.Complaint.created_at).label('hour'),
            func.count(models.Complaint.id).label('count')
        )
        .filter(models.Complaint.created_at >= start_of_today, models.Complaint.created_at < end_of_today)
        .group_by('hour')
        .order_by('hour')
        .all()
    )

    formatted_result = [
        {
            "hour": hour.strftime('%H'),  # 'HH' 포맷으로 시간 출력
            "count": count
        }
        for hour, count in result
    ]

    return formatted_result


def get_pie_chart(db, start_date: datetime, end_date: datetime):
    total_count = (
        db.query(func.count(models.Complaint.id))
        .filter(models.Complaint.created_at >= start_date, models.Complaint.created_at < end_date)
        .scalar()
    )

    status_counts = (
        db.query(
            models.Complaint.status.label('status'),
            func.count(models.Complaint.id).label('count')
        )
        .filter(models.Complaint.created_at >= start_date, models.Complaint.created_at < end_date)
        .group_by(models.Complaint.status)
        .order_by(models.Complaint.status)
        .all()
    )

    percentages = [
        {
            "status": status,
            "percentage": (count / total_count) * 100
        }
        for status, count in status_counts
    ]

    pie_chart_data = []
    for status, count in status_counts:
        percentage = (count / total_count * 100) if total_count > 0 else 0
        pie_chart_data.append({
            "status": status,
            "count": count,
            "percentage": math.floor(percentage * 10) / 10
        })

    return pie_chart_data


def get_stick_chart(db: Session, start_date: datetime, end_date: datetime):
    result = (
        db.query(
            func.date(models.Complaint.created_at).label('date'),
            func.count(models.Complaint.id).label('count')
        )
        .filter(models.Complaint.created_at >= start_date, models.Complaint.created_at <= end_date)
        .group_by(func.date(models.Complaint.created_at))
        .order_by(func.date(models.Complaint.created_at))
        .all()
    )

    formatted_result = [
        {
            "day": hour.strftime('%H'),  # 'HH' 포맷으로 시간 출력
            "count": count
        }
        for hour, count in result
    ]

    return formatted_result

def update_complaints(db: Session, id: int, complaint: schemas.OptionalDescription):
    result = get_complaint(id, db)

    result.phone = complaint.phone
    result.description = complaint.description

    db.commit()
    db.refresh(result)
    return result

class NearByComplaintResponse():
    def __init__(self, id, longitude, latitude, time, address, file_url):
        self.id = id
        self.longitude = longitude
        self.latitude: latitude
        self.time = time
        self.address = address
        self.file_url = file_url