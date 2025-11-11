from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorCollection

from database import get_database
from models.user_model import PyObjectId, UserInDB
from utils.jwt_handler import JWTException, decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_collection() -> AsyncIOMotorCollection:
    db = get_database()
    return db["users"]


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    try:
        payload = decode_access_token(token)
    except JWTException as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    users_collection = get_user_collection()
    user_data = await users_collection.find_one({"_id": PyObjectId(user_id)})
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return UserInDB(**user_data)
