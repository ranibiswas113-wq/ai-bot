from flask import Flask, render_template, jsonify
from datetime import datetime
import pytz
import json

app = Flask(__name__)

class WebClock:
    def __init__(self):
        self.timezones = [
            'UTC',
            'US/Eastern',
            'US/Central',
            'US/Mountain',
            'US/Pacific',
            'Europe/London',
            'Europe/Paris',
            'Asia/Tokyo',
            'Asia/Hong_Kong',
            'Australia/Sydney'
        ]

    def get_all_times(self):
        """
        Get current time in all timezones as JSON.
        
        Returns:
            List of dicts with timezone and formatted time
        """
        times = []
        for tz_str in self.timezones:
            try:
                tz = pytz.timezone(tz_str)
                time_in_tz = datetime.now(tz)
                times.append({
                    'timezone': tz_str,
                    'time': time_in_tz.strftime('%H:%M:%S'),
                    'date': time_in_tz.strftime('%Y-%m-%d'),
                    'full': time_in_tz.strftime('%Y-%m-%d %H:%M:%S %Z')
                })
            except pytz.exceptions.UnknownTimeZoneError:
                pass
        return times

clock = WebClock()

@app.route('/')
def index():
    """Serve the clock HTML page."""
    return render_template('clock.html')

@app.route('/api/time')
def get_time():
    """API endpoint to get all times."""
    return jsonify(clock.get_all_times())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
