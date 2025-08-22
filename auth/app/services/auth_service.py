from app.schemas.auth_schema import CreateUserModel, GetUserModel
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_passowrd
from fastapi import HTTPException

class AuthService:
    def create_user(self, user_data :CreateUserModel, session : Session ):
        hashed_password = hash_password(user_data.password)
        db_user = User(
            username=user_data.username,
            password=hashed_password,
           )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    
    def login(self, user_data : GetUserModel, session : Session):

        db_user = session.query(User).filter(User.username == user_data.username).first()

        if not db_user : 
            raise HTTPException(detail="user not found", status_code=401) 
        
        if not verify_passowrd(user_data.password, db_user.password):  # type: ignore
            raise HTTPException(detail="invalid credentials", status_code=401)
        
        return db_user




