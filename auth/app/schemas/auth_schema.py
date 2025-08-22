from pydantic import BaseModel

class CreateUserModel(BaseModel):
    username : str
    password : str

class GetUserModel(BaseModel):
    username : str
    password : str
