from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)
API_KEY = os.getenv('WEATHER_API_KEY', '')
BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_weather(city):
    """Fetch weather data from OpenWeatherMap API."""
    try:
        url = f"{BASE_URL}/weather"
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def get_forecast(city):
    """Fetch weather forecast from OpenWeatherMap API."""
    try:
        url = f"{BASE_URL}/forecast"
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

@app.route('/')
def index():
    """Serve the weather dashboard."""
    return render_template('weather.html', api_key_set=bool(API_KEY))

@app.route('/api/weather/<city>')
def get_weather_api(city):
    """API endpoint to get current weather."""
    if not API_KEY:
        return jsonify({'error': 'API key not configured'}), 400
    
    data = get_weather(city)
    if not data or 'cod' in data and data['cod'] != '200':
        return jsonify({'error': 'City not found'}), 404
    
    main = data.get('main', {})
    weather = data.get('weather', [{}])[0]
    wind = data.get('wind', {})
    
    return jsonify({
        'city': data.get('name'),
        'country': data.get('sys', {}).get('country'),
        'temperature': main.get('temp'),
        'feels_like': main.get('feels_like'),
        'temp_min': main.get('temp_min'),
        'temp_max': main.get('temp_max'),
        'humidity': main.get('humidity'),
        'pressure': main.get('pressure'),
        'description': weather.get('description'),
        'icon': weather.get('icon'),
        'wind_speed': wind.get('speed'),
        'cloudiness': data.get('clouds', {}).get('all'),
        'visibility': data.get('visibility')
    })

@app.route('/api/forecast/<city>')
def get_forecast_api(city):
    """API endpoint to get weather forecast."""
    if not API_KEY:
        return jsonify({'error': 'API key not configured'}), 400
    
    data = get_forecast(city)
    if not data or 'list' not in data:
        return jsonify({'error': 'Failed to fetch forecast'}), 404
    
    forecasts = []
    for item in data.get('list', []):
        main = item.get('main', {})
        weather = item.get('weather', [{}])[0]
        dt = datetime.fromtimestamp(item['dt'])
        
        forecasts.append({
            'datetime': dt.isoformat(),
            'date': dt.strftime('%Y-%m-%d'),
            'time': dt.strftime('%H:%M'),
            'temperature': main.get('temp'),
            'description': weather.get('description'),
            'icon': weather.get('icon'),
            'humidity': main.get('humidity'),
            'wind_speed': item.get('wind', {}).get('speed')
        })
    
    return jsonify(forecasts)

if __name__ == '__main__':
    if not API_KEY:
        print("⚠️  Warning: WEATHER_API_KEY environment variable not set")
        print("Get a free API key at: https://openweathermap.org/api")
    app.run(debug=True, port=5002)
