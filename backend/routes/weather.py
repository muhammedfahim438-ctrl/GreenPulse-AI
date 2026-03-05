# ══════════════════════════════
# Weather Route
# ══════════════════════════════

from flask import Blueprint, request, jsonify
from services.weather_service import (
    get_current_weather,
    get_forecast,
    check_alerts
)

weather_bp = Blueprint('weather', __name__)

# ── get current weather ──
@weather_bp.route('/api/weather', methods=['GET'])
def get_weather():

    # get city from request
    city = request.args.get('city', 'Pune')

    # get weather from OpenWeatherMap
    weather = get_current_weather(city)

    # if city not found
    if not weather:
        return jsonify({
            'status':  'error',
            'message': f'City "{city}" not found'
        }), 404

    # get alerts
    alerts = check_alerts(weather)

    # get forecast
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
            'message': 'Please provide a city name'
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