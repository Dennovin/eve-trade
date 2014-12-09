import requests

from Config import Config
from DB import DB, WalletTransaction, MarketOrder
from WebHandler import WebHandler

class Item(object):
    cached_info = dict()

    @classmethod
    def info(cls, type_id):
        if type_id not in cls.cached_info:
            req = requests.get(Config.get("item_api"), params={"id": type_id})
            req.raise_for_status()
            items = req.json()
            cls.cached_info[type_id] = items[0] if len(items) > 0 else None

        return cls.cached_info[type_id]

    @classmethod
    def transactions_with(cls, session, type_id):
        return session.query(WalletTransaction).filter(WalletTransaction.type_id == type_id).order_by(WalletTransaction.transaction_date).all()

    @classmethod
    def orders_with(cls, session, type_id):
        return session.query(MarketOrder).filter(MarketOrder.type_id == type_id).order_by(MarketOrder.issued_date).all()

    @classmethod
    def stats(cls, session, type_id):
        txns = cls.transactions_with(session, type_id)
        orders = cls.orders_with(session, type_id)
        info = cls.info(type_id)

        bought = [i for i in txns if i.transaction_type == 1]
        sold = [i for i in txns if i.transaction_type == 0]

        open_buy_orders = [i for i in orders if i.order_type == "buy" and i.order_state == MarketOrder.STATE_ACTIVE]
        open_sell_orders = [i for i in orders if i.order_type == "sell" and i.order_state == MarketOrder.STATE_ACTIVE]

        stats = {
            "info": info,
            "txns": txns,
            "orders": orders,
            }

        stats["buy_orders"] = [i for i in orders if i.order_type == "buy"]
        stats["sell_orders"] = [i for i in orders if i.order_type == "sell"]
        stats["total_bought"] = sum([i.quantity for i in bought])
        stats["total_bought_isk"] = sum([i.price * i.quantity for i in bought])
        stats["total_sold"] = sum([i.quantity for i in sold])
        stats["total_sold_isk"] = sum([i.price * i.quantity for i in sold])
        stats["total_for_sale"] = sum([i.vol_remaining for i in open_sell_orders])
        stats["total_for_sale_isk"] = sum([i.vol_remaining * i.price for i in open_sell_orders])
        stats["actual_profit"] = stats["total_sold_isk"] - stats["total_bought_isk"]
        stats["projected_profit_sell_orders"] = stats["actual_profit"] + stats["total_for_sale_isk"]

        if stats["total_bought"] > 0:
            stats["avg_bought_price"] = stats["total_bought_isk"] / stats["total_bought"]

        if stats["total_sold"] > 0:
            stats["avg_sold_price"] = stats["total_sold_isk"] / stats["total_sold"]
            stats["profit_on_sold"] = stats["total_sold"] * (stats["avg_sold_price"] - stats["avg_bought_price"])

        if len(open_sell_orders) > 0:
            stats["avg_sell_order_price"] = stats["total_for_sale_isk"] / stats["total_for_sale"]
            stats["projected_profit_all"] = stats["actual_profit"] + ((stats["total_bought"] - stats["total_sold"]) * stats["avg_sell_order_price"])
        elif stats["total_sold"] > 0:
            stats["projected_profit_all"] = stats["actual_profit"] + ((stats["total_bought"] - stats["total_sold"]) * stats["avg_sold_price"])

        return stats


class ItemStatsHandler(WebHandler):
    def get(self, type_id):
        item_stats = Item.stats(self.session, type_id)

        self.write(self.loader.load("item_stats.html").generate(item=item_stats, number_format=self.number_format))
        self.finish()

