
from pymongo.collection import Collection
from app.models import User, UserInDB, UserWithProfile, Profile
from app.utils import hash_password, verify_password
from bson import ObjectId
from fastapi import HTTPException
import logging
from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, collection: Collection, profile_collection: Collection):
        self.collection = collection
        self.profile_collection = profile_collection

    def create_user(self, user: User) -> UserInDB:
        existing_user = self.collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=402, detail="User with same email already exists")
        user_dict = user.dict()
        hashed_password = hash_password(user_dict.pop("password"))
        user_dict["hashed_password"] = hashed_password
        user_dict["linked_ids"] = []
        result = self.collection.insert_one(user_dict)
        return UserInDB(id=str(result.inserted_id), username=user_dict["username"], email=user_dict["email"], hashed_password=hashed_password, linked_ids=user_dict["linked_ids"])

    def authenticate_user(self, email: str, password: str) -> bool:
        user = self.collection.find_one({"email": email})
        if not user:
            return False
        if verify_password(password, user["hashed_password"]):
            return True
        return False

    def link_id(self, user_id: str, id_to_link: str):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise ValueError("User not found")

        if id_to_link not in user.get("linked_ids", []):
            self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"linked_ids": id_to_link}}
            )

    def delete_user(self, user_id: str) -> str:
        user_obj_id = ObjectId(user_id)
        self.collection.delete_one({"_id": user_obj_id})
        return str(user_obj_id)

    def delete_related_data(self, user_obj_id):
        self.collection.database["posts"].delete_many({"user_id": user_obj_id})
        self.collection.database["comments"].delete_many({"user_id": user_obj_id})

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return plain_password == hashed_password


    