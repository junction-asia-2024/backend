import os
import aiohttp
from datetime import datetime, date
from fastapi import Depends, FastAPI, UploadFile, Form, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from . import crud, models, schemas
from .database import SessionLocal, engine
from . import s3_bucket
from .enums import CLASSNAME
from .gpt import gpt_start

from typing_extensions import Annotated

models.Base.metadata.create_all(bind=engine)

# app = FastAPI()
app = FastAPI(docs_url='/api/docs', openapi_url='/api/openapi.json')

origins = [
    "http://localhost:3000",
    "http://minwon.site"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/api/complaints")
def create_complaint(
        file: Annotated[str, Form()],
        location: Annotated[str, Form()],
        latitude: Annotated[str, Form()],
        longitude: Annotated[str, Form()],
        classname: Annotated[str, Form()],
        db: Session = Depends(get_db)
):
    complaint = schemas.ComplaintCreate(
        location=location,
        latitude=latitude,
        longitude=longitude,
        classname=classname,
        image_link=file,
        status="W",
    )

    return crud.create_complaint(db=db, complaint=complaint)


# 민원 목록 조회
@app.get("/api/complaints")
def get_complaints(classname: CLASSNAME, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_complaints(classname, db, skip=skip, limit=limit)


# 민원 목록 조회
@app.get("/api/complaints/phone")
def get_complaints_by_phone(phone: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_complaints_by_phone(phone, db, skip=skip, limit=limit)


@app.get("/api/complaints/detail")
def get_complaints_detail(classname: CLASSNAME, location: str, db: Session = Depends(get_db), skip: int = 0,
                          limit: int = 100):
    return crud.get_complaints_detail(classname, location, db, skip=skip, limit=limit)


# 민원 단건 조회
@app.get("/api/complaints/{complaint_id}")
def get_complaints(complaint_id: int, db: Session = Depends(get_db)):
    return crud.get_complaint(complaint_id, db)


# 민원 삭제
@app.delete("/api/complaints/{complaint_id}")
def get_complaints(complaint_id: int, db: Session = Depends(get_db)):
    return crud.delete_complaint(complaint_id, db)


@app.post("/api/complaints/files")
async def upload_picture(file: UploadFile):
    s3_bucket.s3.put_object(
        Body=await file.read(),
        Bucket=f'{s3_bucket.bucket_name}',
        Key=f'{file.filename}',
        ContentType='image/jpeg'
    )

    return {"image_url": f"{s3_bucket.bucket_url_prefix}{file.filename}"}


@app.post("/api/complaints/add/{complaint_id}")
def update_description(complaint_id: int, data: schemas.OptionalDescription, db: Session = Depends(get_db)):
    return crud.update_complaints(db, complaint_id, data)


"""
    내 주변에 있는 문제들을 불러옵니다.
"""


@app.get("/api/detects")
def get_nearby_problem(latitude: float, longitude: float, db: Session = Depends(get_db)):
    return crud.get_nearby_problem(latitude, longitude, db)


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


@app.get("/api/location")
async def get_location(address: str):
    url = f"http://dapi.kakao.com/v2/local/search/address.json?query={address}"
    headers = {
        "Authorization": f"KakaoAK {os.getenv('KAKAO_REST_API_KEY')}",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Failed to fetch data from Kakao API")

            data = await response.json()  # await 추가
            if not data['documents']:
                raise HTTPException(status_code=404, detail="Address not found")

            location = data['documents'][0]['address']
            lat = location['y']
            lng = location['x']

            return {"lat": lat, "lng": lng}

    return {"lat": None, "lng": None}


@app.get("/api/gpt")
def get_gpt():
    return gpt_start()
    return crud.get_stick_chart(db, start_date=start_date, end_date=end_date)
