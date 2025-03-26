
# nexaFit – Nutrition & Lifestyle Support API

A powerful, Dockerized FastAPI backend for calorie burn prediction and personalized meal planning. Built with ML (XGBoost), async HTTP requests, and MongoDB logging, it's the foundation of a smart health platform.

---

##  Features

-  **Calorie Prediction** using custom-trained XGBoost model
-  **Smart Meal Plan Generator** using Spoonacular API
-  Asynchronous HTTP requests with `httpx`
-  Ready for production with Docker
-  CORS support for integration with any frontend
-  MongoDB logging for user-specific history

---

##  Project Structure

```
.
├── main.py                   # FastAPI app entry point
├── models.py                 # Pydantic request/response models
├── ml_predictor.py           # XGBoost prediction logic
├── database.py               # MongoDB interaction
├── calorie_predictor.json    # Trained XGBoost model
├── Dockerfile                # Docker config
├── compose.yaml              # Docker Compose (optional)
├── requirements.txt
└── .env                      # Environment variables (local only)
```

---

##  Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/ezahpizza/nexaFit-backend.git
cd nexaFit-backend
```

### 2. Setup environment

Create a `.env` file:

```env
CALORIE_MODEL_PATH=model/model.xgb
SPOONACULAR_API_KEY=your_spoonacular_api_key
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run locally

```bash
uvicorn main:app --reload
```

---

##  Run with Docker

Build and run using Docker:

```bash
docker build -t nexaFit-api .
docker run -p 8000:8000 --env-file .env nexaF it-api
```

Or use Docker Compose:

```bash
docker compose up --build
```

---

##  API Endpoints

### `POST /predict-calories`

Predict calories burned based on exercise metrics.

#### Request:
```json
{
  "user_id": "user123",
  "gender": 1,
  "age": 25,
  "height": 170,
  "weight": 70,
  "duration": 30,
  "heart_rate": 120,
  "body_temp": 98.6
}
```

#### Response:
```json
{
  "user_id": "user123",
  "input_data": { ... },
  "predicted_calories": 240.5
}
```

---

### `POST /meal-plan?user_id=user123`

Generate a weekly meal plan.

#### Request:
```json
{
  "diet_type": "vegetarian",
  "max_calories": 2000,
  "intolerances": ["gluten", "dairy"]
}
```

#### Response:
```json
{
  "user_id": "user123",
  "request_data": { ... },
  "recipes": [ ... ]
}
```

---

### `GET /user/predictions/{user_id}`  
Fetch past calorie predictions.

### `GET /user/meals/{user_id}`  
Fetch previously generated meal plans.

---

##  Secrets

Add your API key in `.env`:

```env
SPOONACULAR_API_KEY=your_key_here
```

Get a free key from [spoonacular.com](https://spoonacular.com/food-api).

---

##  Dependencies

- `fastapi`
- `uvicorn`
- `xgboost`
- `httpx`
- `pydantic`
- `python-dotenv`
- `pymongo`

---

##  Future Ideas

- Integration with fitness trackers
- User authentication (e.g., Clerk or OAuth)
- Daily meal notifications
- Meal plan ratings & feedback loop

---

##  Author

Built by [Prateek Mohapatra](https://github.com/ezahpizza)  
Part of the larger **nexaFit** platform.

---

##  License

MIT License — free to use, modify, and deploy.
```

---

