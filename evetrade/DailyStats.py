from datetime import datetime, timedelta
from sqlalchemy import and_

from Config import Config
from DB import DB, WalletTransaction, MarketOrder
from WebHandler import WebHandler
from ItemStats import Item

class Day(object):
    @classmethod
    def transactions(cls, day):
        query_filter = and_(WalletTransaction.transaction_date >= day, WalletTransaction.transaction_date < day + timedelta(days=1))
        return DB.session().query(WalletTransaction).filter(query_filter).order_by(WalletTransaction.transaction_date).all()

    @classmethod
    def item_stats(cls, day, txns=None):
        items = dict()

        if txns is None:
            txns = cls.transactions(day)

        for txn in txns:
            if txn.type_id not in items:
                items[txn.type_id] = {"num_bought": 0, "total_bought_isk": 0, "num_sold": 0, "total_sold_isk": 0}

            if txn.transaction_type == 1:
                items[txn.type_id]["total_bought_isk"] += txn.price * txn.quantity
                items[txn.type_id]["num_bought"] += txn.quantity
            else:
                items[txn.type_id]["total_sold_isk"] += txn.price * txn.quantity
                items[txn.type_id]["num_sold"] += txn.quantity

        if len(items) == 0:
            return items

        buy_price_query = """
        SELECT transaction_date, type_id, quantity, SUM(quantity) OVER (PARTITION BY type_id ORDER BY transaction_date desc) AS total_qty, price
        FROM wallet_transactions
        WHERE type_id IN ({}) AND transaction_type = 1 AND transaction_date < %s
        ORDER BY type_id, transaction_date desc
        """

        params = items.keys()
        params.append(day + timedelta(days=1))

        for row in DB.execute(buy_price_query.format(",".join(["%s" for i in items])), params):
            if row["total_qty"] - row["quantity"] <= items[row["type_id"]]["num_sold"]:
                num_counted = row["quantity"] - max(row["total_qty"] - items[row["type_id"]]["num_sold"], 0)
                items[row["type_id"]]["total_cost_on_sold"] = items[row["type_id"]].get("total_cost_on_sold", 0) + row["price"] * num_counted
                items[row["type_id"]]["total_cost_on_sold_counted"] = items[row["type_id"]].get("total_cost_on_sold_counted", 0) + num_counted

        for type_id, item in items.items():
            item["info"] = Item.info(type_id)

        return items

    @classmethod
    def stats(cls, datestring):
        day = datetime.strptime(datestring, "%Y-%m-%d")
        txns = cls.transactions(day)
        items = cls.item_stats(day, txns)
        sold_items = [i for i in items.values() if i["num_sold"] > 0 and "total_cost_on_sold" in i]

        bought = [i for i in txns if i.transaction_type == 1]
        sold = [i for i in txns if i.transaction_type == 0]

        stats = {
            "datestring": datestring,
            "txns": txns,
            "items": items,
            "sold_items": sold_items,
            }

        stats["total_bought"] = sum([i.price * i.quantity for i in bought])
        stats["total_sold"] = sum([i.price * i.quantity for i in sold])
        stats["profit_on_sold"] = sum([i["total_sold_isk"] - i["total_cost_on_sold"] for i in sold_items if "total_cost_on_sold" in i])

        return stats


class DailyStatsHandler(WebHandler):
    def get(self, datestring):
        if datestring == "today":
            datestring = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")

        day_stats = Day.stats(datestring)
        #self.write(day_stats.__repr__())
        self.write(self.loader.load("daily_stats.html").generate(day=datestring, stats=day_stats, number_format=self.number_format))
