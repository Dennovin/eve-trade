import psycopg2
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import sessionmaker

from Config import Config
from EVEAPI import EVEAPI

Base = declarative_base(cls=DeferredReflection)


class DB(object):
    engine = None
    Session = sessionmaker()

    @classmethod
    def get_engine(cls):
        if cls.engine is None:
            cls.engine = sqlalchemy.create_engine(Config.get("db_url"), connect_args=Config.get("db_args"))
            cls.Session.configure(bind=cls.engine)

        return cls.engine

    @classmethod
    def prepare(cls):
        Base.prepare(cls.get_engine())

    @classmethod
    def session(cls):
        return cls.Session()


class APIKey(Base):
    __tablename__ = "api_keys"


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    @classmethod
    def fetch_from_api(cls, key):
        rows = EVEAPI.api_call("char/WalletTransactions", key)
        for row in rows:
            obj = cls()

            obj.transaction_id = row.get("transactionID")
            obj.character_id = key.character_id
            obj.transaction_date = row.get("transactionDateTime")
            obj.quantity = row.get("quantity")
            obj.type_id = row.get("typeID")
            obj.price = row.get("price")
            obj.client_name = row.get("clientName")
            obj.station_id = row.get("stationID")
            obj.transaction_type = (1 if row.get("transactionType") == "buy" else 0)

            yield obj


class MarketOrder(Base):
    __tablename__ = "market_orders"

    @classmethod
    def fetch_from_api(cls, key):
        rows = EVEAPI.api_call("char/MarketOrders", key)
        for row in rows:
            obj = cls()

            obj.order_id = row.get("orderID")
            obj.character_id = key.character_id
            obj.issued_date = row.get("issued")
            obj.type_id = row.get("typeID")
            obj.price = row.get("price")
            obj.order_type = ("buy" if row.get("bid") else "sell")
            obj.station_id = row.get("stationID")
            obj.range = row.get("range")
            obj.vol_entered = row.get("volEntered")
            obj.vol_remaining = row.get("volRemaining")
            obj.order_state = row.get("orderState")

            yield obj

