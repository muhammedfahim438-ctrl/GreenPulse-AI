# ══════════════════════════════
# GreenPulse AI — AI Model
# Loads and uses trained model
# for crop yield prediction
# ══════════════════════════════

import joblib
import numpy as np
import os

# path to saved model
MODEL_PATH = 'models/crop_yield_model.pkl'

# crop name to number mapping
CROP_MAP = {
    'wheat':  0,
    'maize':  1,
    'rice':   2,
    'tomato': 3,
    'cotton': 4,
    'potato': 5
}

# fertilizer to number mapping
FERTILIZER_MAP = {
    'none':   0,
    'low':    1,
    'medium': 2,
    'high':   3
}

# soil to number mapping
SOIL_MAP = {
    'black':    0,
    'red':      1,
    'alluvial': 2,
    'sandy':    3,
    'clay':     4
}

# season to number mapping
SEASON_MAP = {
    'kharif': 0,
    'rabi':   1,
    'zaid':   2
}


def load_model():
    # load trained model from file
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def predict_yield(
    crop, temperature, rainfall,
    humidity, area, fertilizer,
    soil, season
):
    try:
        # load model
        model = load_model()

        if model is None:
            return None

        # convert text inputs to numbers
        crop_num       = CROP_MAP.get(crop, 0)
        fertilizer_num = FERTILIZER_MAP.get(fertilizer, 2)
        soil_num       = SOIL_MAP.get(soil, 2)
        season_num     = SEASON_MAP.get(season, 0)

        # create input array for model
        import pandas as pd

        # create input dataframe with feature names
        features = pd.DataFrame([[
            crop_num,
            float(temperature),
            float(rainfall),
            float(humidity),
            float(area),
            fertilizer_num,
            soil_num,
            season_num
        ]], columns=[
            'crop', 'temperature', 'rainfall',
            'humidity', 'area', 'fertilizer',
            'soil', 'season'
        ])

        # get prediction from model
        predicted = model.predict(features)[0]




        # get prediction from model
        predicted = model.predict(features)[0]

        # round to 1 decimal
        predicted = round(float(predicted), 1)

        # calculate total yield
        total = round(predicted * float(area), 1)

        # decide status
        if predicted >= 4.0:
            status = 'Excellent'
        elif predicted >= 3.0:
            status = 'Good'
        elif predicted >= 2.0:
            status = 'Average'
        else:
            status = 'Low'

        return {
            'predicted_yield': predicted,
            'total_yield':     total,
            'yield_status':    status,
            'unit':            'tons per hectare'
        }

    except Exception as e:
        print(f'Prediction error: {e}')
        return None