from datetime import datetime, timezone
from typing import Dict, List

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from models.food_model import MealType
from models.user_model import PyObjectId


class MealEntry(BaseModel):
    name: str
    calories: int
    protein: float | None = None
    carbs: float | None = None
    fat: float | None = None


class DailyMeals(BaseModel):
    day: str
    meals: Dict[MealType, List[MealEntry]]
    totalCalories: int
    macros: Dict[str, float]


class MealPlanInDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: PyObjectId
    week: List[DailyMeals]
    createdAt: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
