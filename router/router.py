from fastapi import APIRouter
from schema.user_schema import UserSchema
from config.db import conn
from model.users import users

user = APIRouter()

@user.get("/")
def root():
    return {"message": "Hi, I am FastAPI with a Router"}

@user.post("/api/user")
def create_user(data_user: UserSchema):
   new_user = data_user.dict()
   conn.execute(users.insert().values(new_user))
   return "Success"
