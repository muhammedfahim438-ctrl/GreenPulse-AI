# ══════════════════════════════
# Crop Yield Prediction Route
# Now uses Real AI Model!
# ══════════════════════════════

from flask import Blueprint, request, jsonify
from ai_model import predict_yield

predict_bp = Blueprint('predict', __name__)


@predict_bp.route('/api/predict', methods=['POST'])
def predict():

    data = request.get_json()

    # get all values from request
    crop       = data.get('crop', 'wheat')
    temp       = data.get('temperature', 25)
    rain       = data.get('rainfall', 800)
    humidity   = data.get('humidity', 65)
    area       = data.get('area', 1)
    fertilizer = data.get('fertilizer', 'medium')
    soil       = data.get('soil', 'alluvial')
    season     = data.get('season', 'rabi')

    # get prediction from AI model
    result = predict_yield(
        crop, temp, rain,
        humidity, area, fertilizer,
        soil, season
    )

    # if model not trained yet
    if result is None:
        return jsonify({
            'status':  'error',
            'message': 'AI model not trained yet. Run train_model.py first!'
        }), 500

    return jsonify({
        'status': 'success',
        'crop':   crop,
        'area':   area,
        **result
    })