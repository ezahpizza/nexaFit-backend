from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from bson import ObjectId
import datetime

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _):  # Add second parameter
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return str(ObjectId(v))

class CaloriePredictionInput(BaseModel):
    user_id: str
    gender: int  # 0 for male, 1 for female
    age: float
    height: float
    weight: float
    duration: float
    heart_rate: float
    body_temp: float

class CaloriePredictionResult(BaseModel):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    input_data: CaloriePredictionInput
    predicted_calories: float
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

class MealPlanRequest(BaseModel):
    diet_type: Optional[str] = None
    max_calories: Optional[int] = None
    intolerances: Optional[List[str]] = None
    meal_type: Optional[str] = None

class MealPlanResult(BaseModel):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    request_data: MealPlanRequest
    recipes: List[dict]
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)