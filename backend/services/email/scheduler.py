"""
Email Scheduler
Schedules emails for optimal sending times
"""
from datetime import datetime, timedelta
import logging
from typing import List, Optional
import pytz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailScheduler:
    """Schedules emails for optimal delivery times"""

    # Optimal sending hours (9 AM - 5 PM)
    OPTIMAL_HOURS = list(range(9, 18))

    def __init__(self):
        """Initialize scheduler"""
        pass

    def schedule_email(
        self,
        timezone: str = 'UTC',
        preferred_hour: Optional[int] = None
    ) -> datetime:
        """
        Calculate optimal send time for email
        Args:
            timezone: Target timezone (e.g., 'America/New_York')
            preferred_hour: Preferred hour (9-17), or None for next available
        Returns:
            Scheduled datetime
        """
        try:
            tz = pytz.timezone(timezone)
        except:
            tz = pytz.UTC

        now = datetime.now(tz)

        # If preferred hour specified and valid
        if preferred_hour and preferred_hour in self.OPTIMAL_HOURS:
            scheduled = now.replace(hour=preferred_hour, minute=0, second=0, microsecond=0)

            # If time has passed today, schedule for tomorrow
            if scheduled <= now:
                scheduled += timedelta(days=1)

            return scheduled

        # Otherwise, find next optimal time
        current_hour = now.hour

        # If within optimal hours, schedule for current hour
        if current_hour in self.OPTIMAL_HOURS:
            return now + timedelta(minutes=1)  # Send shortly

        # If before 9 AM, schedule for 9 AM today
        if current_hour < 9:
            return now.replace(hour=9, minute=0, second=0, microsecond=0)

        # If after 5 PM, schedule for 9 AM tomorrow
        return (now + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)

    def schedule_batch(
        self,
        batch_size: int,
        interval_minutes: int = 2,
        timezone: str = 'UTC',
        start_time: Optional[datetime] = None
    ) -> List[datetime]:
        """
        Schedule multiple emails with intervals
        Args:
            batch_size: Number of emails to schedule
            interval_minutes: Minutes between each email
            timezone: Target timezone
            start_time: Start time (default: next optimal time)
        Returns:
            List of scheduled datetimes
        """
        if not start_time:
            start_time = self.schedule_email(timezone)

        scheduled_times = []
        current_time = start_time

        for i in range(batch_size):
            scheduled_times.append(current_time)
            current_time += timedelta(minutes=interval_minutes)

            # Skip non-optimal hours
            while current_time.hour not in self.OPTIMAL_HOURS:
                # Move to next day's 9 AM
                current_time = (current_time + timedelta(days=1)).replace(
                    hour=9, minute=0, second=0, microsecond=0
                )

        return scheduled_times

    def get_timezone_for_country(self, country: str) -> str:
        """
        Get common timezone for country
        Args:
            country: Country name
        Returns:
            Timezone string
        """
        timezone_map = {
            'USA': 'America/New_York',
            'UK': 'Europe/London',
            'Canada': 'America/Toronto',
            'Germany': 'Europe/Berlin',
            'Australia': 'Australia/Sydney',
            'Singapore': 'Asia/Singapore',
            'Switzerland': 'Europe/Zurich',
            'Netherlands': 'Europe/Amsterdam',
            'Sweden': 'Europe/Stockholm',
            'China': 'Asia/Shanghai',
            'Hong Kong': 'Asia/Hong_Kong',
            'Japan': 'Asia/Tokyo',
            'France': 'Europe/Paris',
            'Norway': 'Europe/Oslo',
            'New Zealand': 'Pacific/Auckland'
        }

        return timezone_map.get(country, 'UTC')
