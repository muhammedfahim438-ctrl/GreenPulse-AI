# ══════════════════════════════
# Weather Service
# Connects to OpenWeatherMap API
# ══════════════════════════════

import requests
import os
from dotenv import load_dotenv

# load API key from .env file
load_dotenv()

API_KEY  = os.getenv('WEATHER_API_KEY')
BASE_URL = 'http://api.openweathermap.org/data/2.5'


def get_current_weather(city):
    try:
        url    = f'{BASE_URL}/weather'
        params = {
            'q':     city,
            'appid': API_KEY,
            'units': 'metric'
        }

        response = requests.get(url, params=params)
        data     = response.json()

        if data.get('cod') != 200:
            return None

        weather = {
            'city':        data['name'],
            'country':     data['sys']['country'],
            'temperature': round(data['main']['temp']),
            'feels_like':  round(data['main']['feels_like']),
            'humidity':    data['main']['humidity'],
            'wind_speed':  round(data['wind']['speed'] * 3.6),
            'condition':   data['weather'][0]['description'].title(),
            'pressure':    data['main']['pressure'],
            'visibility':  data.get('visibility', 0) // 1000,
        }

        return weather

    except Exception as e:
        print(f'Weather API error: {e}')
        return None


def get_forecast(city):
    try:
        url    = f'{BASE_URL}/forecast'
        params = {
            'q':     city,
            'appid': API_KEY,
            'units': 'metric',
            'cnt':   7
        }

        response = requests.get(url, params=params)
        data     = response.json()

        if data.get('cod') != '200':
            return []

        forecast = []
        for item in data['list']:
            forecast.append({
                'date':        item['dt_txt'],
                'temperature': round(item['main']['temp']),
                'humidity':    item['main']['humidity'],
                'condition':   item['weather'][0]['description'].title(),
                'rainfall':    item.get('rain', {}).get('3h', 0)
            })

        return forecast

    except Exception as e:
        print(f'Forecast API error: {e}')
        return []


def check_alerts(weather):
    alerts = []

    if weather['temperature'] > 35:
        alerts.append({
            'type':    'danger',
            'message': f"High temperature {weather['temperature']}°C! Consider extra irrigation."
        })

    if weather['humidity'] > 85:
        alerts.append({
            'type':    'warning',
            'message': f"High humidity {weather['humidity']}%! Risk of fungal disease."
        })

    if weather['wind_speed'] > 50:
        alerts.append({
            'type':    'warning',
            'message': f"Strong winds {weather['wind_speed']} km/h! Protect your crops."
        })

    return alerts