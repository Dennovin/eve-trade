from datetime import datetime, timedelta

from WebHandler import WebHandler
from DailyStats import Day

class HomepageHandler(WebHandler):
    def get(self):
        stats = []
        for i in range(6, -1, -1):
            stats.append(Day.stats(self.session, datetime.strftime(datetime.utcnow() - timedelta(days=i), "%Y-%m-%d")))

        self.write(self.loader.load("index.html").generate(stats=stats, number_format=self.number_format))
        self.finish()
