from datetime import datetime
import pytz
import time

class DigitalClock:
    def __init__(self, timezones=None):
        """
        Initialize digital clock with multiple timezones.
        
        Args:
            timezones: List of timezone strings (e.g., ['US/Eastern', 'Europe/London'])
        """
        if timezones is None:
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
        else:
            self.timezones = timezones

    def get_time(self, timezone_str):
        """
        Get current time in a specific timezone.
        
        Args:
            timezone_str: Timezone string (e.g., 'US/Eastern')
            
        Returns:
            Formatted time string
        """
        try:
            tz = pytz.timezone(timezone_str)
            time_in_tz = datetime.now(tz)
            return time_in_tz.strftime('%Y-%m-%d %H:%M:%S %Z')
        except pytz.exceptions.UnknownTimeZoneError:
            return f"Unknown timezone: {timezone_str}"

    def display_all_timezones(self):
        """
        Display current time in all configured timezones.
        """
        print("\n" + "="*60)
        print("DIGITAL CLOCK - WORLD TIME")
        print("="*60)
        for tz in self.timezones:
            print(f"{tz:20} : {self.get_time(tz)}")
        print("="*60 + "\n")

    def live_clock(self, interval=1):
        """
        Display live updating clock for all timezones.
        
        Args:
            interval: Update interval in seconds
        """
        try:
            while True:
                self.display_all_timezones()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Clock stopped.")


if __name__ == "__main__":
    # Create clock instance
    clock = DigitalClock()
    
    # Display single snapshot
    print("\nSingle Snapshot:")
    clock.display_all_timezones()
    
    # Uncomment below for live updating clock
    # print("Starting live clock (Press Ctrl+C to stop):")
    # clock.live_clock(interval=1)
