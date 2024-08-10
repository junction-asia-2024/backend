from datetime import datetime, date

from fastapi import Depends, FastAPI, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from . import s3_bucket
from .enums import CLASSNAME

models.Base.metadata.create_all(bind=engine)

# app = FastAPI()
app = FastAPI(docs_url='/api/docs', openapi_url='/api/openapi.json')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api")
def read_root(db: Session = Depends(get_db)):
    file = open('/code/app/insert.txt', 'r')
    query = file.read()
    db.execute(text(query))
    db.commit()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# 민원 등록
@app.post("/api/complaints")
def create_complaint(complaint: schemas.ComplaintCreate, db: Session = Depends(get_db)):
    return crud.create_complaint(db=db, complaint=complaint)


# 민원 목록 조회
@app.get("/api/complaints")
def get_complaints(classname: CLASSNAME, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_complaints(classname, db, skip=skip, limit=limit)


# 민원 목록 조회
@app.get("/api/complaints/phone")
def get_complaints_by_phone(phone: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_complaints_by_phone(phone, db, skip=skip, limit=limit)


# 민원 단건 조회
@app.get("/api/complaints/{complaint_id}")
def get_complaints(complaint_id: int, db: Session = Depends(get_db)):
    return crud.get_complaint(complaint_id, db)


# 민원 삭제
@app.delete("/api/complaints/{complaint_id}")
def get_complaints(complaint_id: int, db: Session = Depends(get_db)):
    return crud.delete_complaint(complaint_id, db)


@app.post("/api/users/pictures")
async def upload_picture(file: UploadFile):
    s3_bucket.s3.put_object(
        Body=await file.read(),
        Bucket=f'{s3_bucket.bucket_name}',
        Key=f'{file.filename}',
        ContentType='image/jpeg'
    )

"""
    내 주변에 있는 문제들을 불러옵니다.
"""
@app.get("/api/detects")
def get_nearby_complaint(db: Session = Depends(get_db)):
    return crud.get_nearby_complaint(db)

@app.get("/api/chart/linear")
def get_linear_chart(db: Session = Depends(get_db), ):
    return crud.get_linear_chart(db)


@app.get("/api/chart/pie")
def get_pie_chart(start_date: datetime, end_date: datetime, db: Session = Depends(get_db), ):
    return crud.get_pie_chart(db, start_date=start_date, end_date=end_date)


@app.get("/api/chart/stick")
def get_stick_chart(start_date: datetime, end_date: datetime, db: Session = Depends(get_db), ):
    return crud.get_stick_chart(db, start_date=start_date, end_date=end_date)


@app.post("/api/users/pictures")
async def upload_picture(file: UploadFile):
    s3_bucket.s3.put_object(
        Body=await file.read(),
        Bucket=f'{s3_bucket.bucket_name}',
        Key=f'{file.filename}',
        ContentType='image/jpeg'
    )