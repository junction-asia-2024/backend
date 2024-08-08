from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from . import s3_bucket

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, email=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/login", response_model=schemas.User)
def login(login_request: schemas.UserCreate, db: Session = Depends(get_db)):
    result = crud.login(db, login_request)
    if result is False:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@app.post("/users/pictures")
async def upload_picture(file: UploadFile):
    s3_bucket.s3.put_object(
        Body = await file.read(),
        Bucket = f'{s3_bucket.bucket_name}',
        Key = f'{file.filename}',
        ContentType = 'image/jpeg'
    )