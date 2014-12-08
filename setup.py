import os
from setuptools import setup, find_packages

setup(
    name="eve-trade",
    description="EVE Online market trade monitoring tools",
    url="https://github.com/Dennovin/eve-trade",
    version="0.01",
    author="Corey Cossentino",
    author_email="corey@cossentino.com",
    license="MIT",
    packages=find_packages(),
    package_data={
        "evetrade": ["static/*", "templates/*", "schema/*"],
        },
    install_requires=[
        "psycopg2 >= 2.5.4",
        "requests == 2.2.1",
        "sqlalchemy >= 0.9.8",
        "tornado >= 4.0.2",
        ],
    scripts=[
        "scripts/eve_trade_schema.py",
        "scripts/eve_trade_web.py",
        "scripts/update_transactions.py",
        ],
    )
