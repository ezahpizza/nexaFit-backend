import os
import httpx
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from models import CaloriePredictionInput, CaloriePredictionResult, MealPlanRequest, MealPlanResult
from ml_predictor import CaloriePredictor
from database import DatabaseManager

load_dotenv()

app = FastAPI(  title="nexaFit",
                description="A complete nutrition and lifestyle support platform.",
                version="1.0.0",)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML Predictor and Database
ml_predictor = CaloriePredictor(os.getenv('CALORIE_MODEL_PATH'))
db_manager = DatabaseManager()

# -------------------------------------------------------------------
async def generate_meal_plan(diet: str = None, calories: int = None, intolerances: list = None):
    api_key = os.getenv("SPOONACULAR_API_KEY")
    url = "https://api.spoonacular.com/mealplanner/generate"

    params = {
        "apiKey": api_key,
        "timeFrame": "week"
    }

    if diet:
        params["diet"] = diet
    if calories:
        params["targetCalories"] = calories
    if intolerances:
        params["intolerances"] = ",".join(intolerances)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        print(f"Meal plan GET URL: {response.url}")
        response.raise_for_status()
        return response.json()

# -------------------------------------------------------------------
async def fetch_recipe_details(recipe_ids: list):
    api_key = os.getenv("SPOONACULAR_API_KEY")
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(
                f"https://api.spoonacular.com/recipes/{recipe_id}/information",
                params={"apiKey": api_key}
            ) for recipe_id in recipe_ids
        ]
        responses = await asyncio.gather(*tasks)
        return [
            r.json() for r in responses if r.status_code == 200
        ]

# -------------------------------------------------------------------
@app.post("/predict-calories")
async def predict_calories(input_data: CaloriePredictionInput):
    try:
        features = [
            input_data.gender,
            input_data.age,
            input_data.height,
            input_data.weight,
            input_data.duration,
            input_data.heart_rate,
            input_data.body_temp
        ]

        predicted_calories = ml_predictor.predict(features)

        prediction_entry = {
            "user_id": input_data.user_id,
            "input_data": input_data.model_dump(),
            "predicted_calories": predicted_calories
        }

        await db_manager.log_calorie_prediction(prediction_entry)
        return CaloriePredictionResult(**prediction_entry)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------------------------
@app.post("/meal-plan")
async def create_meal_plan(request: MealPlanRequest, user_id: str):
    try:
        # Generate plan
        meal_plan = await generate_meal_plan(
            diet=request.diet_type,
            calories=request.max_calories,
            intolerances=request.intolerances
        )

        if not meal_plan.get("week"):
            raise HTTPException(status_code=404, detail="No meals found. Try relaxing your filters.")

        # Get all recipe IDs
        recipe_ids = [
            meal["id"]
            for day in meal_plan["week"].values()
            for meal in day.get("meals", [])
        ]

        # Fetch all recipe details in parallel
        detailed_recipes = await fetch_recipe_details(recipe_ids)

        # Prepare and log
        meal_plan_entry = {
            "user_id": user_id,
            "request_data": request.model_dump(),
            "recipes": detailed_recipes
        }

        await db_manager.log_meal_plan(meal_plan_entry)
        return MealPlanResult(**meal_plan_entry)

    except httpx.RequestError as e:
        print(f"Spoonacular API Error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Spoonacular API error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------------------------
@app.get("/user/predictions/{user_id}")
async def get_user_predictions(user_id: str):
    return await db_manager.get_user_predictions(user_id)

@app.get("/user/meals/{user_id}")
async def get_user_meal_plans(user_id: str):
    return await db_manager.get_user_meal_plans(user_id)
