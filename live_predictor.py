import time
import pytesseract
import webbrowser
from pathlib import Path
from PIL import ImageGrab, ImageOps, ImageEnhance
import pandas as pd
import json
from datetime import datetime
from ai_engine import load_model, predict_next

webbrowser.open("https://www.bustabit.com")

x, y, width, height = 100, 200, 150, 50
padding = 20

model = load_model()
prediction_data = []

def extract_multiplier():
    screenshot = ImageGrab.grab(bbox=(x - padding, y - padding, x + width + padding, y + height + padding))
    gray = ImageOps.grayscale(screenshot)
    contrast = ImageEnhance.Contrast(gray).enhance(2.0)
    sharp = ImageEnhance.Sharpness(contrast).enhance(2.0)
    text = pytesseract.image_to_string(sharp)
    try:
        return float(text.strip().replace('x', '').replace('X', ''))
    except ValueError:
        return None

def retrain_model(dataframe):
    from xgboost import XGBClassifier
    model = XGBClassifier()
    model.fit(dataframe[["avg_5", "avg_10", "std_10", "low_streak"]], dataframe["target"])
    model.save_model("xgboost_model.json")
    return model

def get_latest_data():
    """Read latest live OCR data for Streamlit dashboard."""
    try:
        with open("live_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None

round_counter = 0
training_log = []

while True:
    multiplier = extract_multiplier()
    if multiplier is not None:
        features = {
            "features": {
                "avg_5": multiplier,
                "avg_10": multiplier,
                "std_10": 0.5,
                "low_streak": 2
            }
        }
        result, confidence = predict_next(features, model)

        with open("live_data.json", "w", encoding="utf-8") as f:
            json.dump(features, f)

        log_entry = [datetime.now(), multiplier, result, confidence]
        pd.DataFrame([log_entry], columns=["time", "multiplier", "result", "confidence"]).to_csv(
            "prediction_log.csv", mode="a", header=not Path("prediction_log.csv").exists(), index=False
        )

        training_log.append({
            "avg_5": multiplier,
            "avg_10": multiplier,
            "std_10": 0.5,
            "low_streak": 2,
            "target": int(multiplier >= 2.0)
        })

        round_counter += 1

        if round_counter >= 10:
            df_train = pd.DataFrame(training_log)
            model = retrain_model(df_train)
            print("Model retrained with last 10 rounds.")
            training_log.clear()
            round_counter = 0

    time.sleep(5)
