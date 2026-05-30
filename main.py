from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

@app.get("/")
def get_message():
    return {"Message" : "My First API"}

@app.get("/about")
def about():
    return {"Message": "Job Application Tracker"}


class ApplicationCreate(BaseModel):
    company_name: str
    position: str
    status: str

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
