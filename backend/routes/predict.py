# ══════════════════════════════
# Crop Yield Prediction Route
# ══════════════════════════════

from flask import Blueprint, request, jsonify

# create blueprint
predict_bp = Blueprint('predict', __name__)

# ── crop yield prediction endpoint ──
@predict_bp.route('/api/predict', methods=['POST'])
def predict_yield():

    # get data sent from frontend
    data = request.get_json()

    # read all values from request
    crop       = data.get('crop', 'wheat')
    temp       = float(data.get('temperature', 25))
    rain       = float(data.get('rainfall', 800))
    humidity   = float(data.get('humidity', 65))
    area       = float(data.get('area', 1))
    fertilizer = data.get('fertilizer', 'medium')
    season     = data.get('season', 'rabi')
    soil       = data.get('soil', 'alluvial')

    # ── base yield for each crop (tons per hectare) ──
    base_yield = {
        'wheat':  3.2,
        'maize':  4.0,
        'rice':   2.5,
        'tomato': 3.8,
        'cotton': 1.8,
        'potato': 5.0
    }

    # start with base yield
    yld = base_yield.get(crop, 3.0)

    # ── adjust based on temperature ──
    if temp > 35:
        yld -= 0.5    # too hot
    elif temp < 15:
        yld -= 0.4    # too cold
    elif 20 <= temp <= 30:
        yld += 0.3    # ideal range

    # ── adjust based on rainfall ──
    if 600 <= rain <= 1200:
        yld += 0.3    # ideal rainfall
    elif rain < 300:
        yld -= 0.5    # too dry
    elif rain > 2000:
        yld -= 0.3    # too wet

    # ── adjust based on humidity ──
    if 50 <= humidity <= 80:
        yld += 0.2    # ideal humidity
    elif humidity > 90:
        yld -= 0.3    # too humid

    # ── adjust based on fertilizer ──
    if fertilizer == 'high':
        yld += 0.4
    elif fertilizer == 'medium':
        yld += 0.2
    elif fertilizer == 'none':
        yld -= 0.3

    # ── adjust based on season ──
    if season == 'rabi':
        yld += 0.1

    # ── adjust based on soil ──
    if soil == 'alluvial':
        yld += 0.2
    elif soil == 'sandy':
        yld -= 0.2

    # make sure yield is never below 0.5
    yld = max(0.5, yld)

    # round to 1 decimal
    yld = round(yld, 1)

    # calculate total yield for whole farm
    total = round(yld * area, 1)

    # decide status based on yield
    if yld >= 4.0:
        status = 'Excellent'
    elif yld >= 3.0:
        status = 'Good'
    elif yld >= 2.0:
        status = 'Average'
    else:
        status = 'Low'

    # send result back to frontend
    return jsonify({
        'status':          'success',
        'crop':            crop,
        'predicted_yield': yld,
        'total_yield':     total,
        'area':            area,
        'yield_status':    status,
        'unit':            'tons per hectare'
    })