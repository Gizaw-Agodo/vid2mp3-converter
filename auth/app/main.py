from fastapi import FastAPI, Depends
from app.schemas.auth_schema import CreateUserModel, GetUserModel
from app.core.dependecy import get_session, get_auth_service
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.core.security import create_access_token, verify_access_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

app = FastAPI()
app.add_middleware(CORSMiddleware,
                      allow_origins=["*"], 
                    allow_credentials=True,
                        allow_methods=["*"],  
                        allow_headers=["*"], 
                   )

@app.get('/')
def base_route():
    return {"message":"welcome to the app"}

@app.post('/register')
def create_user(
    user_data :CreateUserModel, 
    session : Session  = Depends(get_session),
    auth_service : AuthService = Depends(get_auth_service)
    ):
    new_user = auth_service.create_user(user_data, session)
    return new_user

@app.post("/login")
def login_user(
    user_data:GetUserModel, 
    session : Session = Depends(get_session),
    auth_service : AuthService = Depends(get_auth_service)
    ):
    user = auth_service.login(user_data, session)

    token = create_access_token({"username" : user.username})
    return {"token" : token}

@app.post('/verify')
def verify_token(token :str = Depends(oauth2_scheme)):
    decoded = verify_access_token(token)
    if not decoded:
        raise HTTPException(detail="Invalid tokens", status_code=401)
    return decoded