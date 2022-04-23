from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get("/")
def hello():
    return {"hello": "world"}


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def signup(user: schemas.Signup, db: Session = Depends(get_db)):
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail=f"user with email {user.email} already exist")
    user.password = utils.hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login', status_code=200)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No account registered")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
