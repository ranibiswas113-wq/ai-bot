import requests
import json
from datetime import datetime
import os
from pathlib import Path

class WeatherDashboard:
    """
    Weather Dashboard using OpenWeatherMap API.
    Sign up at https://openweathermap.org/api for a free API key.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize Weather Dashboard.
        
        Args:
            api_key: OpenWeatherMap API key (or set WEATHER_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv('WEATHER_API_KEY')
        if not self.api_key:
            print("Warning: WEATHER_API_KEY not set. Get one at https://openweathermap.org/api")
        
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.weather_cache_file = 'weather_cache.json'
        self.cache = self.load_cache()

    def load_cache(self):
        """Load weather cache from file."""
        if os.path.exists(self.weather_cache_file):
            try:
                with open(self.weather_cache_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save_cache(self):
        """Save weather cache to file."""
        with open(self.weather_cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def get_current_weather(self, city, country_code=None):
        """
        Get current weather for a city.
        
        Args:
            city: City name
            country_code: Optional country code (e.g., 'US', 'GB')
            
        Returns:
            Weather data dictionary
        """
        if not self.api_key:
            return {'error': 'API key not configured'}
        
        location = f"{city},{country_code}" if country_code else city
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache the result
            self.cache[city] = {
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
            self.save_cache()
            
            return data
        except requests.exceptions.RequestException as e:
            return {'error': f'Failed to fetch weather: {str(e)}'}

    def get_forecast(self, city, country_code=None, days=5):
        """
        Get weather forecast for a city.
        
        Args:
            city: City name
            country_code: Optional country code
            days: Number of days to forecast (1-5 for free tier)
            
        Returns:
            Forecast data dictionary
        """
        if not self.api_key:
            return {'error': 'API key not configured'}
        
        location = f"{city},{country_code}" if country_code else city
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f'Failed to fetch forecast: {str(e)}'}

    def parse_weather_data(self, data):
        """
        Parse and format weather data for display.
        
        Args:
            data: Raw weather API response
            
        Returns:
            Formatted weather information
        """
        if 'error' in data or 'cod' in data and data['cod'] != '200':
            return None
        
        main = data.get('main', {})
        weather = data.get('weather', [{}])[0]
        wind = data.get('wind', {})
        clouds = data.get('clouds', {})
        
        return {
            'city': data.get('name'),
            'country': data.get('sys', {}).get('country'),
            'temperature': main.get('temp'),
            'feels_like': main.get('feels_like'),
            'temp_min': main.get('temp_min'),
            'temp_max': main.get('temp_max'),
            'pressure': main.get('pressure'),
            'humidity': main.get('humidity'),
            'weather': weather.get('main'),
            'description': weather.get('description'),
            'icon': weather.get('icon'),
            'wind_speed': wind.get('speed'),
            'wind_deg': wind.get('deg'),
            'cloudiness': clouds.get('all'),
            'visibility': data.get('visibility'),
            'sunset': data.get('sys', {}).get('sunset'),
            'sunrise': data.get('sys', {}).get('sunrise')
        }

    def display_weather(self, city, country_code=None):
        """
        Display formatted weather for a city.
        
        Args:
            city: City name
            country_code: Optional country code
        """
        print(f"\nFetching weather for {city}...")
        data = self.get_current_weather(city, country_code)
        weather = self.parse_weather_data(data)
        
        if not weather:
            print(f"Error: City not found or API error")
            return
        
        print("\n" + "="*60)
        print(f"🌍 {weather['city']}, {weather['country']}")
        print("="*60)
        print(f"🌡️  Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)")
        print(f"📊 Min/Max: {weather['temp_min']}°C / {weather['temp_max']}°C")
        print(f"☁️  Weather: {weather['description'].title()}")
        print(f"💨 Wind: {weather['wind_speed']} m/s at {weather['wind_deg']}°")
        print(f"💧 Humidity: {weather['humidity']}%")
        print(f"🔍 Visibility: {weather['visibility']/1000:.1f} km")
        print(f"☁️  Cloudiness: {weather['cloudiness']}%")
        print(f"🔽 Pressure: {weather['pressure']} hPa")
        print("="*60 + "\n")

    def display_forecast(self, city, country_code=None):
        """
        Display weather forecast for a city.
        
        Args:
            city: City name
            country_code: Optional country code
        """
        print(f"\nFetching forecast for {city}...")
        data = self.get_forecast(city, country_code)
        
        if 'error' in data or 'list' not in data:
            print(f"Error: Could not fetch forecast")
            return
        
        print("\n" + "="*60)
        print(f"📅 5-Day Forecast for {city}")
        print("="*60)
        
        forecasts = data.get('list', [])
        current_date = None
        
        for forecast in forecasts:
            dt = datetime.fromtimestamp(forecast['dt'])
            date_str = dt.strftime('%Y-%m-%d')
            
            if date_str != current_date:
                print(f"\n{date_str}:")
                current_date = date_str
            
            time_str = dt.strftime('%H:%M')
            temp = forecast['main']['temp']
            weather = forecast['weather'][0]['main']
            
            print(f"  {time_str} - {temp}°C - {weather}")
        
        print("\n" + "="*60 + "\n")

    def interactive_menu(self):
        """
        Display interactive menu for weather dashboard.
        """
        if not self.api_key:
            print("⚠️  API key not configured!")
            print("Get a free API key at: https://openweathermap.org/api")
            api_key = input("Enter your API key: ").strip()
            if api_key:
                self.api_key = api_key
                os.environ['WEATHER_API_KEY'] = api_key
            else:
                print("Cannot proceed without API key")
                return
        
        while True:
            print("\n🌤️  WEATHER DASHBOARD")
            print("1. Current weather")
            print("2. 5-day forecast")
            print("3. Weather for multiple cities")
            print("4. Exit")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == '1':
                city = input("Enter city name: ").strip()
                if city:
                    self.display_weather(city)
            
            elif choice == '2':
                city = input("Enter city name: ").strip()
                if city:
                    self.display_forecast(city)
            
            elif choice == '3':
                cities = input("Enter cities (comma-separated): ").strip().split(',')
                for city in cities:
                    self.display_weather(city.strip())
            
            elif choice == '4':
                print("Goodbye!")
                break
            
            else:
                print("Invalid option")


if __name__ == "__main__":
    dashboard = WeatherDashboard()
    dashboard.interactive_menu()
