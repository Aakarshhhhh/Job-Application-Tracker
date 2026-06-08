from database import Base
from sqlalchemy import  Column, Integer, String, TIMESTAMP, Boolean, text

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key = True, nullable = False)
    company_name = Column(String, nullable = False)
    position = Column(String, nullable = False)
    status = Column(String, nullable = False)
    application_link = Column(String)
    notes = Column(String)
    created_at = Column(TIMESTAMP(timezone = True),server_default = text('now()'))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    hashed_password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True),server_default = text('now()'))
