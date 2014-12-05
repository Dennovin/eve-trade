#!/usr/bin/env python

import argparse
import logging
import psycopg2.extras

from evetrade import Config, DB, EVEAPI, APIKey, WalletTransaction, MarketOrder

BATCH_SIZE = 1000

Config.parse_args()
DB.prepare()

session = DB.session()

for key in session.query(APIKey):
    for i, txn in enumerate(WalletTransaction.fetch_from_api(key)):
        session.add(txn)
        if i % BATCH_SIZE == BATCH_SIZE - 1:
            session.commit()

    session.commit()

    for i, order in enumerate(MarketOrder.fetch_from_api(key)):
        session.add(order)
        if i % BATCH_SIZE == BATCH_SIZE - 1:
            session.commit()

    session.commit()
