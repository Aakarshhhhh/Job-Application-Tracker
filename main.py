from fastapi import FastAPI
from database import Base,engine
from database import get_db
from models import Application, User
from schemas import ApplicationCreate, ApplicationResponse
from schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException
from typing import List
from passlib.context import CryptContext

Base.metadata.create_all(bind = engine)
app = FastAPI()

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")


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
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        email = user.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user