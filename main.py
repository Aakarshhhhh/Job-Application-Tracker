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
    return {"Message" : "My First API"}

@app.get("/about")
def about():
    return {"Message": "Job Application Tracker"}

next_id = 1
applications = []

@app.post("/applications")
def create_application(application:ApplicationCreate):
    global next_id
    
    new_application = {
        "id": next_id,
        "company_name": application.company_name,
            "position": application.position,
            "status": application.status
            }
    applications.append(new_application)
    next_id += 1

    return new_application

@app.get("/applications")
def get_application():
    return {"Applications": applications}

@app.get("/applications/{id}")
def get_application():
    for application in applications:
        if application["id"] == id:
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
