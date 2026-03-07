# ══════════════════════════════
# Weather Route
# ══════════════════════════════

from flask import Blueprint, request, jsonify
from services.weather_service import (
    get_current_weather,
    get_forecast,
    check_alerts
)
from services.email_service import send_weather_alert

weather_bp = Blueprint('weather', __name__)


# ── get current weather ──
@weather_bp.route('/api/weather', methods=['GET'])
def get_weather():

    city    = request.args.get('city', 'Chennai')
    weather = get_current_weather(city)

    if not weather:
        return jsonify({
            'status':  'error',
            'message': f'City "{city}" not found'
        }), 404

    alerts   = check_alerts(weather)
    forecast = get_forecast(city)

    return jsonify({
        'status':   'success',
        'weather':  weather,
        'forecast': forecast,
        'alerts':   alerts
    })


# ── search city weather ──
@weather_bp.route('/api/weather/search', methods=['GET'])
def search_weather():

    city = request.args.get('city', '')

    if not city:
        return jsonify({
            'status':  'error',
            'message': 'Please provide city name'
        }), 400

    weather = get_current_weather(city)

    if not weather:
        return jsonify({
            'status':  'error',
            'message': f'City "{city}" not found'
        }), 404

    return jsonify({
        'status':  'success',
        'weather': weather
    })


# ── send weather alert email ──
@weather_bp.route('/api/alert/send', methods=['POST'])
def send_alert():

    data        = request.get_json()
    to_email    = data.get('email')
    farmer_name = data.get('name', 'Farmer')
    alert_type  = data.get('alert_type', 'high_temp')
    details     = data.get('details', {})

    if not to_email:
        return jsonify({
            'status':  'error',
            'message': 'Email address is required'
        }), 400

    success = send_weather_alert(
        to_email,
        farmer_name,
        alert_type,
        details
    )

    if success:
        return jsonify({
            'status':  'success',
            'message': f'Alert email sent to {to_email}'
        })
    else:
        return jsonify({
            'status':  'error',
            'message': 'Failed to send email'
        }), 500