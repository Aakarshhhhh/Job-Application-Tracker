from typing import Optional
from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    company_name : str
    status : str
    position : str
    application_link : Optional[str] = None
    notes : Optional[str] = None
