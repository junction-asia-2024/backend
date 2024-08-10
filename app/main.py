from fastapi import Depends, FastAPI, UploadFile, File
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import os
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


@app.on_event("startup")
def startup_event():
    # Path to the SQL file
    sql_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '/app', 'insert.text'))

    # Name of the table to check
    table_name = "complaints"

    # Execute the SQL commands from the file if the table is empty
    execute_sql_file_if_empty(sql_file_path, table_name)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# 민원 등록
@app.post("/api/complaints", response_model=schemas.ComplaintGet)
def create_complaint(complaint: schemas.ComplaintCreate, db: Session = Depends(get_db)):
    return crud.create_complaint(db=db, complaint=complaint)


# 민원 목록 조회
@app.get("/api/complaints", response_model=list[schemas.ComplaintGet])
def get_complaints(classname: CLASSNAME, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_complaints(classname, db, skip=skip, limit=limit)


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
