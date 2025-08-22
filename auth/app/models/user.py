from app.core.database import Base
from sqlalchemy import Column, Integer,String

class User(Base):
    __tablename__ = "user"
    id  = Column(Integer, primary_key=True,index=True )
    username  = Column(String(50), nullable=False)
    password  = Column(String(255), nullable=False)

