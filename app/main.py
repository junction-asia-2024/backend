from fastapi import Depends, FastAPI, UploadFile, File
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from . import s3_bucket
from .enums import TYPE

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hc():
    return 'success'


# 민원 등록
@app.post("/api/complaints", response_model=schemas.ComplaintGet)
def create_complaint(complaint: schemas.ComplaintCreate, db: Session = Depends(get_db)):
    return crud.create_complaint(db=db, complaint=complaint)


# 민원 목록 조회
@app.get("/api/complaints", response_model=list[schemas.ComplaintGet])
def get_complaints(type: TYPE, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_complaints(type, db, skip=skip, limit=limit)


# 민원 단건 조회
@app.get("/api/complaints/{complaint_id}", response_model=schemas.ComplaintGet)
def get_complaints(complaint_id: int, db: Session = Depends(get_db)):
    return crud.get_complaint(complaint_id, db)


# 민원 삭제
@app.delete("/api/complaints/{complaint_id}", response_model=schemas.ComplaintGet)
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
