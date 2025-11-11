from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from database import get_database
from models.user_model import UserInDB, UserUpdate
from utils.dependencies import get_current_user

router = APIRouter()


def _get_user_collection() -> AsyncIOMotorCollection:
    return get_database()["users"]


@router.get("/me")
async def get_profile(current_user: UserInDB = Depends(get_current_user)):
    return current_user.model_dump(by_alias=True, exclude={"password"})


@router.put("/update")
async def update_profile(
    payload: UserUpdate,
    current_user: UserInDB = Depends(get_current_user),
):
    users_collection = _get_user_collection()
    update_data = dict(payload.model_dump(exclude_none=True))
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided")

    update_data["updatedAt"] = datetime.now(tz=timezone.utc)
    await users_collection.update_one({"_id": current_user.id}, {"$set": update_data})
    updated = await users_collection.find_one({"_id": current_user.id})
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user = UserInDB(**updated)
    return user.model_dump(by_alias=True, exclude={"password"})
