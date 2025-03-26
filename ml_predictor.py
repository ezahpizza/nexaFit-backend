import xgboost as xgb
import pandas as pd
import numpy as np
from joblib import load
from sklearn.preprocessing import StandardScaler
from typing import List

class CaloriePredictor:
    def __init__(self, model_path: str):
        self.model = xgb.XGBRegressor()
        self.model.load_model(model_path)  
        self.scaler = load('std_scaler.bin')

    def predict(self, input_data: List[float]) -> float:
        # Convert input to numpy array and scale
        feature_names = ['gender', 'age', 'height', 'weight', 'duration', 'heart_rate', 'body_temp']
        input_df = pd.DataFrame([input_data], columns=feature_names)
        scaled_input = self.scaler.transform(input_df)
        
        # Create DMatrix and predict
        prediction = self.model.predict(scaled_input)
        
        return float(prediction)