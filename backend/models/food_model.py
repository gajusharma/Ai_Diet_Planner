from typing import List, Literal

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from models.user_model import DietType, PyObjectId

MealType = Literal["breakfast", "lunch", "dinner", "snacks"]


class FoodBase(BaseModel):
    food: str
    calories: int
    protein: float
    carbs: float
    fat: float
    mealType: List[MealType]
    type: DietType = "balanced"


class FoodInDB(FoodBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
