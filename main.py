from fastapi import FastAPI
from pydantic import BaseModel
from database import Base,engine
from models import Application
from database import get_db
from models import Application
from schemas import ApplicationCreate
from sqlalchemy.orm import Session
from fastapi import Depends

Base.metadata.create_all(bind = engine)
app = FastAPI()

@app.get("/")
def get_message():
    return {"Message": "TESTING NEW CODE"}

@app.get("/")
def get_message():
    return {"Message" : "My First API"}

@app.get("/about")
def about():
    return {"Message": "Job Application Tracker"}


@app.post("/applications")
def create_application(application:ApplicationCreate,db: Session = Depends(get_db)):
    print("POST route called")
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
    

@app.get("/applications")
def get_application(db: Session = Depends(get_db)):
    applications = db.query(applications).all()
    return applications

@app.get("/applications/{id}")
def get_application(id: int,db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == id).first()
    if application is None:
        return {"Message": "Application not found"}
    return application

@app.put("/applications/{id}")
def update_application(item_id: int, application: ApplicationCreate):
    for app in applications:
        if app["id"] == item_id:
            app["company_name"] = application.company_name
            app["position"] = application.position
            app["status"] = application.status
            return {"message": "Successfully updated data"}
        
    return {"Message": "Error data not Valid"}

@app.delete("/applications/{id}")
def delete_application(item_id: int):
    for app in applications:
        if app["id"] == item_id:
            applications.remove(app)
            return {"message": "Application removed Successfully"}
        
    return {"Message": "Data not found"}