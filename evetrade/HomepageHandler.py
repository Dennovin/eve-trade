from datetime import datetime, timedelta
import logging

from WebHandler import WebHandler
from DailyStats import DateRange
from GeneralStats import GeneralStats

class HomepageHandler(WebHandler):
    def get(self):
        stats = {
            "days": [],
            "weeks": [],
            "months": [],
            }

        for i in range(6, -1, -1):
            stats["days"].append(DateRange.stats(self.session, datetime.strftime(datetime.utcnow() - timedelta(days=i), "%Y-%m-%d")))

        for i in range(4, -1, -1):
            week_start = datetime.now() - timedelta(days=datetime.now().weekday()) - timedelta(weeks=i)
            week_end = week_start + timedelta(weeks=1)
            stats["weeks"].append(DateRange.stats(self.session, datetime.strftime(week_start, "%Y-%m-%d"), datetime.strftime(week_end, "%Y-%m-%d")))

        order_totals = GeneralStats.current_order_totals()

        self.write(self.loader.load("index.html").generate(stats=stats, order_totals=order_totals, number_format=self.number_format))
        self.finish()
