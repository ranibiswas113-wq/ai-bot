# Weather Dashboard Setup Guide

## Overview
The Weather Dashboard fetches real-time weather data from the OpenWeatherMap API.

## Getting Started

### 1. Get a Free API Key
1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Go to your API keys page
4. Copy your API key

### 2. Set Up Environment Variable

**Linux/Mac:**
```bash
export WEATHER_API_KEY='your_api_key_here'
```

**Windows (PowerShell):**
```powershell
$env:WEATHER_API_KEY='your_api_key_here'
```

**Windows (Command Prompt):**
```cmd
set WEATHER_API_KEY=your_api_key_here
```

### 3. Run the Application

**CLI Version:**
```bash
python weather_cli.py
```

**Web Version:**
```bash
pip install flask requests
python weather_web.py
```

Then visit http://localhost:5002 in your browser.

## Features

### Current Weather
- Real-time temperature and conditions
- "Feels like" temperature
- Min/Max temperatures
- Humidity and pressure
- Wind speed and direction
- Cloud coverage
- Visibility
- Sunrise/Sunset times

### 5-Day Forecast
- Hourly forecasts
- Temperature trends
- Weather conditions
- Wind speed
- Humidity levels

### Multi-City Support
- Search multiple cities at once
- Compare weather across locations
- Local caching for faster lookups

## API Endpoints (Web Version)

- `GET /` - Dashboard page
- `GET /api/weather/<city>` - Get current weather
- `GET /api/forecast/<city>` - Get 5-day forecast

## Cache
Weather data is cached locally in `weather_cache.json` to reduce API calls.

## Troubleshooting

**"API key not configured"**
- Ensure WEATHER_API_KEY environment variable is set
- Verify the API key is correct

**"City not found"**
- Check the spelling of the city name
- Try using country code (e.g., "London,GB")

**Rate limiting**
- Free tier has 60 calls/minute limit
- Data is cached to reduce API calls

## API Documentation
For more details, visit: https://openweathermap.org/weather-conditions
