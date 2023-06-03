from fastapi import APIRouter

user = APIRouter()

@user.get("/")
async def root():
    return {"message": "Hi, I am FastAPI with a Router"}
