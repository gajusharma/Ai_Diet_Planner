from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from database import get_database
from models.mealplan_model import MealPlanInDB
from models.user_model import PyObjectId, UserInDB
from utils.dependencies import get_current_user
from utils.diet_generator import generate_weekly_plan

router = APIRouter()


def _collections() -> tuple[AsyncIOMotorCollection, AsyncIOMotorCollection]:
    db = get_database()
    return db["mealplans"], db["foods"]


@router.post("/generate")
async def generate_diet_plan(current_user: UserInDB = Depends(get_current_user)):
    mealplans_collection, foods_collection = _collections()
    try:
        week_plan = await generate_weekly_plan(current_user, foods_collection)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    payload = {
        "userId": current_user.id,
        "week": [item.model_dump() for item in week_plan],
    "createdAt": datetime.now(tz=timezone.utc),
    }

    await mealplans_collection.delete_many({"userId": current_user.id})
    result = await mealplans_collection.insert_one(payload)
    stored = await mealplans_collection.find_one({"_id": result.inserted_id})

    plan = MealPlanInDB(**stored).model_dump(by_alias=True)
    return {"success": True, "plan": plan}


@router.get("/user/{user_id}")
async def get_user_plan(user_id: str, current_user: UserInDB = Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    mealplans_collection, _ = _collections()
    plan = await mealplans_collection.find_one({"userId": PyObjectId(user_id)})
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal plan not found")

    return {"success": True, "plan": MealPlanInDB(**plan).model_dump(by_alias=True)}


@router.delete("/user/{user_id}")
async def delete_user_plan(user_id: str, current_user: UserInDB = Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    mealplans_collection, _ = _collections()
    result = await mealplans_collection.delete_many({"userId": PyObjectId(user_id)})

    return {"success": True, "deleted": result.deleted_count}
