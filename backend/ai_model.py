# ══════════════════════════════
# GreenPulse AI — AI Model
# Improved with 15 crops +
# farming tips + soil advice
# ══════════════════════════════

import joblib
import numpy as np
import pandas as pd
import os

MODEL_PATH    = 'models/crop_yield_model.pkl'
FEATURES_PATH = 'models/feature_names.pkl'

# 15 crops mapping
CROP_MAP = {
    'wheat':     0,
    'maize':     1,
    'rice':      2,
    'tomato':    3,
    'cotton':    4,
    'potato':    5,
    'sugarcane': 6,
    'soybean':   7,
    'sunflower': 8,
    'groundnut': 9,
    'onion':     10,
    'banana':    11,
    'mango':     12,
    'chilli':    13,
    'turmeric':  14
}

FERTILIZER_MAP = {
    'none':   0,
    'low':    1,
    'medium': 2,
    'high':   3
}

SOIL_MAP = {
    'black':    0,
    'red':      1,
    'alluvial': 2,
    'sandy':    3,
    'clay':     4
}

SEASON_MAP = {
    'kharif': 0,
    'rabi':   1,
    'zaid':   2
}

IRRIGATION_MAP = {
    'rainfed':  0,
    'sprinkler': 1,
    'drip':     2
}

# farming tips per crop
CROP_TIPS = {
    'wheat': [
        'Sow wheat in November for best yield.',
        'Apply nitrogen fertilizer in 3 splits.',
        'Irrigate at crown root initiation stage.',
        'Watch for rust disease in February.'
    ],
    'rice': [
        'Maintain 2-5 cm water level in field.',
        'Transplant 21 day old seedlings.',
        'Apply zinc sulphate to prevent deficiency.',
        'Drain field 2 weeks before harvest.'
    ],
    'maize': [
        'Plant with 75cm row spacing.',
        'Apply potassium for strong stalks.',
        'Irrigate at silking and tasseling stage.',
        'Harvest when husk turns brown.'
    ],
    'tomato': [
        'Use drip irrigation for best results.',
        'Stake plants to prevent lodging.',
        'Apply calcium to prevent blossom end rot.',
        'Monitor for early blight regularly.'
    ],
    'potato': [
        'Plant in well drained loamy soil.',
        'Hill up soil around plants after 3 weeks.',
        'Maintain consistent moisture levels.',
        'Harvest when leaves turn yellow.'
    ],
    'sugarcane': [
        'Plant in deep well drained soil.',
        'Apply heavy doses of nitrogen.',
        'Trash mulching saves water.',
        'Harvest at 12 months for best sugar.'
    ],
    'cotton': [
        'Plant after last frost date.',
        'Thin plants to 30cm spacing.',
        'Monitor for bollworm regularly.',
        'Reduce irrigation before harvest.'
    ],
    'soybean': [
        'Inoculate seeds with Rhizobium bacteria.',
        'Plant in well drained fertile soil.',
        'Avoid waterlogging at any stage.',
        'Harvest when pods turn brown.'
    ],
    'sunflower': [
        'Plant in full sun location.',
        'Apply boron micronutrient.',
        'Protect from birds at harvest.',
        'Harvest when back of head turns yellow.'
    ],
    'groundnut': [
        'Plant in sandy loam soil.',
        'Apply gypsum at flowering stage.',
        'Do not irrigate near harvest time.',
        'Dry pods thoroughly before storage.'
    ],
    'onion': [
        'Transplant 6 week old seedlings.',
        'Apply sulphur for better pungency.',
        'Stop irrigation 2 weeks before harvest.',
        'Cure bulbs in sun for 2 weeks.'
    ],
    'banana': [
        'Plant in deep well drained soil.',
        'Apply heavy mulch around plants.',
        'Use drip irrigation system.',
        'Remove extra suckers regularly.'
    ],
    'mango': [
        'Prune after harvest for better yield.',
        'Apply potassium before flowering.',
        'Control mango hopper with neem oil.',
        'Harvest at mature green stage.'
    ],
    'chilli': [
        'Transplant at 5-6 leaf stage.',
        'Apply calcium and boron regularly.',
        'Use yellow sticky traps for thrips.',
        'Pick fruits regularly to boost yield.'
    ],
    'turmeric': [
        'Plant in well drained loamy soil.',
        'Mulch heavily with green leaves.',
        'Apply organic manure generously.',
        'Harvest 9 months after planting.'
    ]
}

# soil recommendations
SOIL_ADVICE = {
    'black': [
        'Black soil has excellent water retention.',
        'Add gypsum to improve drainage.',
        'Best for cotton and soybean.',
        'Deep ploughing improves productivity.'
    ],
    'red': [
        'Red soil needs more organic matter.',
        'Add compost to improve fertility.',
        'Best for groundnut and potato.',
        'Frequent light irrigation recommended.'
    ],
    'alluvial': [
        'Alluvial soil is highly fertile.',
        'Best soil for most crops!',
        'Maintain pH between 6.5 and 7.5.',
        'Rotate crops to prevent nutrient depletion.'
    ],
    'sandy': [
        'Sandy soil drains too fast.',
        'Add organic matter to improve retention.',
        'Frequent small irrigations work best.',
        'Best for root vegetables like carrot.'
    ],
    'clay': [
        'Clay soil retains too much water.',
        'Add sand and compost to improve drainage.',
        'Avoid working when wet.',
        'Best for rice cultivation.'
    ]
}


def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def predict_yield(
    crop, temperature, rainfall,
    humidity, area, fertilizer,
    soil, season,
    ph_level=6.5, irrigation='drip'
):
    try:
        model = load_model()
        if model is None:
            return None

        crop_num       = CROP_MAP.get(crop, 0)
        fertilizer_num = FERTILIZER_MAP.get(fertilizer, 2)
        soil_num       = SOIL_MAP.get(soil, 2)
        season_num     = SEASON_MAP.get(season, 0)
        irrigation_num = IRRIGATION_MAP.get(irrigation, 2)

        features = pd.DataFrame([[
            crop_num,
            float(temperature),
            float(rainfall),
            float(humidity),
            float(area),
            fertilizer_num,
            soil_num,
            season_num,
            float(ph_level),
            irrigation_num
        ]], columns=[
            'crop', 'temperature', 'rainfall',
            'humidity', 'area', 'fertilizer',
            'soil', 'season', 'ph_level', 'irrigation'
        ])

        predicted = round(float(model.predict(features)[0]), 2)
        total     = round(predicted * float(area), 2)

        if predicted >= 5.0:
            status = 'Excellent'
        elif predicted >= 3.5:
            status = 'Good'
        elif predicted >= 2.0:
            status = 'Average'
        else:
            status = 'Low'

        # get farming tips
        tips = CROP_TIPS.get(crop, [
            'Monitor crops regularly.',
            'Maintain proper irrigation.',
            'Apply fertilizer as needed.',
            'Watch for pest and disease.'
        ])

        # get soil advice
        soil_tips = SOIL_ADVICE.get(soil, [
            'Test soil regularly.',
            'Add organic matter.',
            'Maintain proper pH.',
            'Rotate crops yearly.'
        ])

        return {
            'predicted_yield': predicted,
            'total_yield':     total,
            'yield_status':    status,
            'unit':            'tons per hectare',
            'farming_tips':    tips,
            'soil_advice':     soil_tips
        }

    except Exception as e:
        print(f'Prediction error: {e}')
        return None