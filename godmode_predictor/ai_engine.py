import xgboost as xgb
import pandas as pd
import os

FEATURE_NAMES = ["avg_5", "avg_10", "std_10", "low_streak"]

def load_model(path="xgboost_model.json"):
    model = xgb.XGBClassifier()
    if os.path.exists(path):
        model.load_model(path)
    else:
        raise FileNotFoundError("Model file not found. Please train it first.")
    return model

def predict_next(data, model):
    feature_dict = data.get('features', {})
    missing = [f for f in FEATURE_NAMES if f not in feature_dict]
    if missing:
        raise KeyError(f"Missing feature(s) for prediction: {missing}")

    features = pd.DataFrame([feature_dict])[FEATURE_NAMES]
    prob = model.predict_proba(features)[0][1]
    return prob > 0.7, prob * 100
