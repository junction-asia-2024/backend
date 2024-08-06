from sqlalchemy.orm import Session

from . import models, schemas
from .utils import Hasher


def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=Hasher.get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login(db: Session, login_request: schemas.UserCreate):
    user = get_user(db, login_request.email)
    if user is None:
        return False
    if Hasher.verify_password(login_request.password, user.password) is False:
        return False
    return user