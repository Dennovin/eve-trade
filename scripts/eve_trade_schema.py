#!/usr/bin/env python
import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from evetrade import Config

Config.parse_args()

engine = sqlalchemy.create_engine(Config.get("db_url"), connect_args=Config.get("db_args"))
connection = engine.connect()
transaction = connection.begin()

schema_dir = Config.resource_filename("schema")

fnum = 0
while True:
    try:
        schema_file = os.path.join(schema_dir, "{}.sql".format(fnum))
        testquery_file = os.path.join(schema_dir, "{}.testquery".format(fnum))
        with open(schema_file, "r") as schema, open(testquery_file, "r") as testquery:
            result = connection.execute(testquery.read()).fetchone()
            if result[0]:
                break
            else:
                connection.execute(schema.read())
                transaction.commit()

        fnum += 1

    except IOError:
        break
    except:
        transaction.rollback()
        raise
