# ══════════════════════════════
# Disease Detection Route
# ══════════════════════════════

from flask import Blueprint, request, jsonify
import random

# create blueprint
disease_bp = Blueprint('disease', __name__)

# ── disease detection endpoint ──
@disease_bp.route('/api/disease', methods=['POST'])
def detect_disease():

    # check if image file was sent
    if 'image' not in request.files:
        return jsonify({
            'status':  'error',
            'message': 'No image file uploaded'
        }), 400

    # get the uploaded image
    image = request.files['image']

    # check if file has a name
    if image.filename == '':
        return jsonify({
            'status':  'error',
            'message': 'No file selected'
        }), 400

    # ── disease results list ──
    # in real app this will use CNN AI model
    # for now we return sample results
    diseases = [
        {
            'disease':    'Leaf Blight',
            'confidence': 91,
            'severity':   'High',
            'type':       'Fungal',
            'treatments': [
                'Apply Mancozeb fungicide immediately',
                'Remove and burn infected leaves',
                'Avoid overhead irrigation',
                'Improve air circulation between plants'
            ]
        },
        {
            'disease':    'Rust Disease',
            'confidence': 87,
            'severity':   'High',
            'type':       'Fungal',
            'treatments': [
                'Apply Propiconazole fungicide',
                'Use rust resistant varieties next season',
                'Early sowing helps avoid rust season',
                'Monitor neighboring crops for spread'
            ]
        },
        {
            'disease':    'Powdery Mildew',
            'confidence': 83,
            'severity':   'Medium',
            'type':       'Fungal',
            'treatments': [
                'Spray Sulphur based fungicide',
                'Neem oil spray is effective organic option',
                'Ensure plants get adequate sunlight',
                'Avoid wetting foliage when watering'
            ]
        },
        {
            'disease':    'Healthy Leaf',
            'confidence': 96,
            'severity':   'None',
            'type':       'None',
            'treatments': [
                'Your plant looks healthy!',
                'Continue regular watering schedule',
                'Keep monitoring weekly for early signs'
            ]
        }
    ]

    # pick random result
    # in real app AI model will analyze image
    result = random.choice(diseases)

    return jsonify({
        'status':     'success',
        'filename':   image.filename,
        'result':     result
    })
