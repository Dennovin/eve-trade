from datetime import datetime, timedelta
import logging

from WebHandler import WebHandler
from DailyStats import Day
from GeneralStats import GeneralStats

class HomepageHandler(WebHandler):
    def get(self):
        stats = []
        for i in range(6, -1, -1):
            stats.append(Day.stats(self.session, datetime.strftime(datetime.utcnow() - timedelta(days=i), "%Y-%m-%d")))

        order_totals = GeneralStats.current_order_totals()

        self.write(self.loader.load("index.html").generate(stats=stats, order_totals=order_totals, number_format=self.number_format))
        self.finish()
