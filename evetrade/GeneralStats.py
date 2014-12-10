from DB import DB, WalletTransaction, MarketOrder

class GeneralStats(object):
    @classmethod
    def current_order_totals(cls):
        totals_query = """
        SELECT
          sum(case when order_type = 'buy' then 1 else 0 end) AS num_buy,
          sum(case when order_type = 'sell' then 1 else 0 end) AS num_sell,
          sum(case when order_type = 'buy' then price * vol_remaining else 0 end) AS total_buy,
          sum(case when order_type = 'sell' then price * vol_remaining else 0 end) AS total_sell
        FROM market_orders
        WHERE order_state = %s
        """

        row = DB.execute(totals_query, [MarketOrder.STATE_ACTIVE]).fetchone()
        return {
            "num_buy": row[0],
            "num_sell": row[1],
            "total_buy": row[2],
            "total_sell": row[3],
            }
