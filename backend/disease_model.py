# ══════════════════════════════
# GreenPulse AI — Disease Model
# Detects crop diseases from
# uploaded leaf images
# ══════════════════════════════

import numpy as np
from PIL import Image
import joblib
import os

# path to saved model
MODEL_PATH = 'models/disease_model.pkl'

# disease labels
DISEASE_LABELS = {
    0: 'Healthy Leaf',
    1: 'Leaf Blight',
    2: 'Rust Disease',
    3: 'Powdery Mildew'
}

# disease details
DISEASE_DETAILS = {
    'Healthy Leaf': {
        'severity':   'None',
        'type':       'None',
        'icon':       '✅',
        'treatments': [
            'Your plant looks healthy!',
            'Continue regular watering schedule.',
            'Keep monitoring weekly for early signs.',
            'Maintain good soil nutrition.'
        ]
    },
    'Leaf Blight': {
        'severity':   'High',
        'type':       'Fungal',
        'icon':       '🍂',
        'treatments': [
            'Apply Mancozeb fungicide immediately.',
            'Remove and burn all infected leaves.',
            'Avoid overhead irrigation.',
            'Improve air circulation between plants.'
        ]
    },
    'Rust Disease': {
        'severity':   'High',
        'type':       'Fungal',
        'icon':       '🟤',
        'treatments': [
            'Apply Propiconazole fungicide.',
            'Use rust resistant varieties next season.',
            'Early sowing helps avoid rust season.',
            'Monitor neighboring crops for spread.'
        ]
    },
    'Powdery Mildew': {
        'severity':   'Medium',
        'type':       'Fungal',
        'icon':       '⬜',
        'treatments': [
            'Spray Sulphur based fungicide.',
            'Neem oil spray is effective organic option.',
            'Ensure plants get adequate sunlight.',
            'Avoid wetting foliage when watering.'
        ]
    }
}


def extract_features(image_file):
    img       = Image.open(image_file)
    img       = img.resize((100, 100))
    img       = img.convert('RGB')
    img_array = np.array(img)

    red_avg   = np.mean(img_array[:, :, 0])
    green_avg = np.mean(img_array[:, :, 1])
    blue_avg  = np.mean(img_array[:, :, 2])

    total = red_avg + green_avg + blue_avg + 1

    brown_ratio = (red_avg * 0.6 + blue_avg * 0.2) / total
    green_ratio = green_avg / total

    dark_pixels = np.sum(
        (img_array[:, :, 0] < 80) &
        (img_array[:, :, 1] < 80) &
        (img_array[:, :, 2] < 80)
    )
    spot_ratio = dark_pixels / (100 * 100)

    return np.array([[
        red_avg,
        green_avg,
        blue_avg,
        brown_ratio,
        green_ratio,
        spot_ratio
    ]])


def detect_disease(image_file):
    try:
        if not os.path.exists(MODEL_PATH):
            return None

        model = joblib.load(MODEL_PATH)

        features    = extract_features(image_file)
        prediction  = model.predict(features)[0]
        probability = model.predict_proba(features)[0]

        disease_name = DISEASE_LABELS[int(prediction)]
        confidence   = round(float(np.max(probability)) * 100, 1)
        details      = DISEASE_DETAILS[disease_name]

        return {
            'disease':    disease_name,
            'confidence': confidence,
            'severity':   details['severity'],
            'type':       details['type'],
            'icon':       details['icon'],
            'treatments': details['treatments']
        }

    except Exception as e:
        print(f'Disease detection error: {e}')
        return None