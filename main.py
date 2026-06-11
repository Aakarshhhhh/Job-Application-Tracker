from fastapi import FastAPI
from database import Base,engine
from database import get_db
from models import Application, User
from schemas import ApplicationCreate, ApplicationResponse
from schemas import UserCreate, UserResponse, UserLogin
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException
from typing import List
from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

Base.metadata.create_all(bind = engine)
app = FastAPI()

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

@app.get("/")
def get_message():
    return {"Message" : "My First API"}

@app.get("/about")
def about():
    return {"Message": "Job Application Tracker"}


@app.post("/applications",response_model = ApplicationResponse)
def create_application(application:ApplicationCreate,db: Session = Depends(get_db)):
    new_application = Application(
        company_name = application.company_name,
        status = application.status,
        position = application.position,
        application_link = application.application_link,
        notes = application.notes
    )
    print("POST route called")
    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application
    

@app.get("/applications",response_model = List[ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    applications = db.query(Application).all()
    return applications

@app.get("/applications/{id}",response_model = ApplicationResponse)
def get_application(id: int,db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == id).first()
    if application is None:
        raise HTTPException(status_code = 404 ,detail = "Application not Found")
    return application

@app.put("/applications/{id}",response_model = ApplicationResponse)
def update_application(id: int,updated_application: ApplicationCreate, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == id).first()
    if application is None:
        raise HTTPException(status_code = 404, detail = "Application not found")
    application.company_name = updated_application.company_name
    application.status = updated_application.status
    application.position = updated_application.position
    application.application_link = updated_application.application_link
    application.notes = updated_application.notes
    db.commit()
    db.refresh(application)
    return application

@app.delete("/applications/{id}")
def delete_application(id: int,db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == id).first()
    if application is None:
        raise HTTPException(status_code = 404, detail = "Application not found")
    db.delete(application)
    db.commit()
    return {"Message": "Data deleted Successfully"}

@app.post("/users", response_model = UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print(user.password)
    print(len(user.password))
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        email = user.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = 30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def get_current_user(token: str, db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    user_id = payload["user_id"]
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 401, detail = "Unauthorized User")
    return user



@app.post("/login")
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if user is None:
        raise HTTPException(status_code = 401, detail = "Invalid Credentials")
    if not pwd_context.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code = 401, detail = "Invalid Credentials")
    access_token = create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
   