
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from pydantic import EmailStr
from app.services import UserService
from app.models import User, UserWithProfile, Profile
from app.config import settings
from bson import ObjectId
import logging

router = APIRouter()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db():
    from pymongo import MongoClient
    client = MongoClient(settings.mongodb_uri)
    return client['assignment_db']

@router.post("/auth/register")
async def register_user(user: User, db: Database = Depends(get_db)):
    user_service = UserService(db["users"], db["profiles"])
    user_in_db = user_service.create_user(user)
    return user_in_db

@router.post("/auth/login")
async def login(email: EmailStr, password: str, db: Database = Depends(get_db)):
    user_service = UserService(db["users"], db["profiles"])
    if not user_service.authenticate_user(email, password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Logged in successfully"}

@router.post("/link_id")
async def link_id(user_id: str, id_to_link: str, db: Database = Depends(get_db)):
    user_service = UserService(db["users"], db["profiles"])
    try:
        user_service.link_id(user_id, id_to_link)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "ID linked successfully"}

@router.delete("/user/{user_id}")
async def delete_user(user_id: str, db: Database = Depends(get_db)):
    user_service = UserService(db["users"], db["profiles"])
    user_obj_id = user_service.delete_user(user_id)
    user_service.delete_related_data(user_obj_id)
    return {"message": f"User {str(user_obj_id)} and all related data deleted successfully"}




