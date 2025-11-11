from datetime import datetime, timezone
from typing import Any, Literal, Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from pydantic.config import ConfigDict
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def validate(cls, value: Any, _info) -> ObjectId:
        if isinstance(value, ObjectId):
            return value
        if isinstance(value, str) and ObjectId.is_valid(value):
            return ObjectId(value)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        return core_schema.with_info_after_validator_function(
            cls.validate,
            core_schema.union_schema(
                [core_schema.is_instance_schema(ObjectId), core_schema.str_schema()]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x),
                return_schema=core_schema.str_schema(),
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema_, handler):
        json_schema = handler(core_schema_)
        json_schema.update(type="string")
        return json_schema


GoalType = Literal["weight_loss", "maintenance", "weight_gain"]
ActivityLevel = Literal["sedentary", "light", "moderate", "active", "very_active"]
DietType = Literal["veg", "non_veg", "vegan", "keto", "paleo", "balanced"]
GenderType = Literal["male", "female"]


class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(ge=13, le=100)
    height: float = Field(gt=0)
    weight: float = Field(gt=0)
    goal: GoalType = "maintenance"
    activityLevel: ActivityLevel = "moderate"
    dietType: DietType = "balanced"
    gender: GenderType = "male"


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=13, le=100)
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)
    goal: Optional[GoalType] = None
    activityLevel: Optional[ActivityLevel] = None
    dietType: Optional[DietType] = None
    gender: Optional[GenderType] = None


class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    password: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


class UserPublic(UserBase):
    id: PyObjectId = Field(alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
