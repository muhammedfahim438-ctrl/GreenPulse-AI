# ══════════════════════════════
# Crop Yield Prediction Route
# Improved with 15 crops!
# ══════════════════════════════

from flask import Blueprint, request, jsonify
from ai_model import predict_yield

predict_bp = Blueprint('predict', __name__)


@predict_bp.route('/api/predict', methods=['POST'])
def predict():

    data = request.get_json()

    crop       = data.get('crop',        'wheat')
    temp       = data.get('temperature', 25)
    rain       = data.get('rainfall',    800)
    humidity   = data.get('humidity',    65)
    area       = data.get('area',        1)
    fertilizer = data.get('fertilizer', 'medium')
    soil       = data.get('soil',       'alluvial')
    season     = data.get('season',     'rabi')
    ph_level   = data.get('ph_level',   6.5)
    irrigation = data.get('irrigation', 'drip')

    result = predict_yield(
        crop, temp, rain,
        humidity, area, fertilizer,
        soil, season, ph_level, irrigation
    )

    if result is None:
        return jsonify({
            'status':  'error',
            'message': 'AI model not trained yet!'
        }), 500

    return jsonify({
        'status': 'success',
        'crop':   crop,
        'area':   area,
        **result
    })