from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('DATABASE_NAME')]
        
        # Collections
        self.calorie_predictions = self.db.calorie_predictions
        self.meal_plans = self.db.meal_plans

    async def log_calorie_prediction(self, prediction_data):
        return await self.calorie_predictions.insert_one(prediction_data)

    async def log_meal_plan(self, meal_plan_data):
        return await self.meal_plans.insert_one(meal_plan_data)

    async def get_user_predictions(self, user_id):
        predictions = await self.calorie_predictions.find({"user_id": user_id}).to_list(length=100)
        
        for pred in predictions:
            pred["_id"] = str(pred["_id"])

        return predictions


    async def get_user_meal_plans(self, user_id):
        meal_plans = await self.meal_plans.find({"user_id": user_id}).to_list(length=None)
        
        for plan in meal_plans:
            plan['_id'] = str(plan['_id'])
        
        return meal_plans