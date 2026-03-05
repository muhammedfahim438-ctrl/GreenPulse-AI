# ══════════════════════════════
# Weather Monitoring Route
# ══════════════════════════════

from flask import Blueprint, request, jsonify

# create blueprint
weather_bp = Blueprint('weather', __name__)

# ── get weather data endpoint ──
@weather_bp.route('/api/weather', methods=['GET'])
def get_weather():

    # get city from request
    city = request.args.get('city', 'Pune')

    # for now we return sample weather data
    # later we will connect OpenWeatherMap API
    weather_data = {
        'city':        city,
        'temperature': 34,
        'humidity':    68,
        'rainfall':    12,
        'wind_speed':  18,
        'condition':   'Partly Cloudy',
        'icon':        '🌤️',
        'forecast': [
            {
                'day':         'Today',
                'temp':        34,
                'condition':   'Partly Cloudy',
                'icon':        '🌤️',
                'humidity':    68,
                'rainfall':    0
            },
            {
                'day':         'Tomorrow',
                'temp':        31,
                'condition':   'Cloudy',
                'icon':        '⛅',
                'humidity':    72,
                'rainfall':    5
            },
            {
                'day':         'Wednesday',
                'temp':        28,
                'condition':   'Rain',
                'icon':        '🌧️',
                'humidity':    85,
                'rainfall':    25
            },
            {
                'day':         'Thursday',
                'temp':        26,
                'condition':   'Thunderstorm',
                'icon':        '⛈️',
                'humidity':    90,
                'rainfall':    82
            },
            {
                'day':         'Friday',
                'temp':        27,
                'condition':   'Light Rain',
                'icon':        '🌦️',
                'humidity':    80,
                'rainfall':    15
            },
            {
                'day':         'Saturday',
                'temp':        30,
                'condition':   'Partly Cloudy',
                'icon':        '🌤️',
                'humidity':    70,
                'rainfall':    0
            },
            {
                'day':         'Sunday',
                'temp':        33,
                'condition':   'Sunny',
                'icon':        '☀️',
                'humidity':    60,
                'rainfall':    0
            }
        ]
    }

    # check for temperature alert
    alerts = []

    if weather_data['temperature'] > 35:
        alerts.append({
            'type':    'danger',
            'message': 'High temperature alert! Consider extra irrigation.'
        })

    if weather_data['humidity'] > 85:
        alerts.append({
            'type':    'warning',
            'message': 'High humidity! Risk of fungal disease.'
        })

    weather_data['alerts'] = alerts

    return jsonify({
        'status': 'success',
        'data':   weather_data
    })