# ══════════════════════════════
# Disease Detection Route
# Now uses Real AI Model!
# ══════════════════════════════

from flask import Blueprint, request, jsonify
from disease_model import detect_disease

disease_bp = Blueprint('disease', __name__)


@disease_bp.route('/api/disease', methods=['POST'])
def detect():

    # check if image was sent
    if 'image' not in request.files:
        return jsonify({
            'status':  'error',
            'message': 'No image uploaded'
        }), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({
            'status':  'error',
            'message': 'No file selected'
        }), 400

    # detect disease using AI model
    result = detect_disease(image)

    if result is None:
        return jsonify({
            'status':  'error',
            'message': 'Model not trained. Run train_disease_model.py first!'
        }), 500

    return jsonify({
        'status':   'success',
        'filename': image.filename,
        'result':   result
    })